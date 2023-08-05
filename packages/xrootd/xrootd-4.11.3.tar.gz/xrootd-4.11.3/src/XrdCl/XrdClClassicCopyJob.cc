//------------------------------------------------------------------------------
// Copyright (c) 2011-2014 by European Organization for Nuclear Research (CERN)
// Author: Lukasz Janyst <ljanyst@cern.ch>
//------------------------------------------------------------------------------
// This file is part of the XRootD software suite.
//
// XRootD is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// XRootD is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with XRootD.  If not, see <http://www.gnu.org/licenses/>.
//
// In applying this licence, CERN does not waive the privileges and immunities
// granted to it by virtue of its status as an Intergovernmental Organization
// or submit itself to any jurisdiction.
//------------------------------------------------------------------------------

#include "XrdCl/XrdClClassicCopyJob.hh"
#include "XrdCl/XrdClConstants.hh"
#include "XrdCl/XrdClLog.hh"
#include "XrdCl/XrdClDefaultEnv.hh"
#include "XrdCl/XrdClFile.hh"
#include "XrdCl/XrdClMonitor.hh"
#include "XrdCl/XrdClUtils.hh"
#include "XrdCl/XrdClCheckSumManager.hh"
#include "XrdCks/XrdCksCalc.hh"
#include "XrdCl/XrdClUglyHacks.hh"
#include "XrdCl/XrdClRedirectorRegistry.hh"
#include "XrdCl/XrdClZipArchiveReader.hh"
#include "XrdCl/XrdClPostMaster.hh"
#include "XrdCl/XrdClJobManager.hh"

#include <memory>
#include <mutex>
#include <queue>
#include <algorithm>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include "XrdClXCpCtx.hh"

namespace
{
  //----------------------------------------------------------------------------
  //! Check sum helper for stdio
  //----------------------------------------------------------------------------
  class CheckSumHelper
  {
    public:
      //------------------------------------------------------------------------
      //! Constructor
      //------------------------------------------------------------------------
      CheckSumHelper( const std::string &name,
                      const std::string &ckSumType ):
        pName( name ),
        pCkSumType( ckSumType ),
        pCksCalcObj( 0 )
      {};

      //------------------------------------------------------------------------
      //! Destructor
      //------------------------------------------------------------------------
      virtual ~CheckSumHelper()
      {
        delete pCksCalcObj;
      }

      //------------------------------------------------------------------------
      //! Initialize
      //------------------------------------------------------------------------
      XrdCl::XRootDStatus Initialize()
      {
        using namespace XrdCl;
        if( pCkSumType.empty() )
          return XRootDStatus();

        Log             *log    = DefaultEnv::GetLog();
        CheckSumManager *cksMan = DefaultEnv::GetCheckSumManager();

        if( !cksMan )
        {
          log->Error( UtilityMsg, "Unable to get the checksum manager" );
          return XRootDStatus( stError, errInternal );
        }

        pCksCalcObj = cksMan->GetCalculator( pCkSumType );
        if( !pCksCalcObj )
        {
          log->Error( UtilityMsg, "Unable to get a calculator for %s",
                      pCkSumType.c_str() );
          return XRootDStatus( stError, errCheckSumError );
        }

        return XRootDStatus();
      }

      //------------------------------------------------------------------------
      // Update the checksum
      //------------------------------------------------------------------------
      void Update( const void *buffer, uint32_t size )
      {
        if( pCksCalcObj )
          pCksCalcObj->Update( (const char *)buffer, size );
      }

      //------------------------------------------------------------------------
      // Get checksum
      //------------------------------------------------------------------------
      XrdCl::XRootDStatus GetCheckSum( std::string &checkSum,
                                       std::string &checkSumType )
      {
        using namespace XrdCl;
        Log *log = DefaultEnv::GetLog();

        //----------------------------------------------------------------------
        // Sanity check
        //----------------------------------------------------------------------
        if( !pCksCalcObj )
        {
          log->Error( UtilityMsg, "Calculator for %s was not initialized",
                      pCkSumType.c_str() );
          return XRootDStatus( stError, errCheckSumError );
        }

        int          calcSize = 0;
        std::string  calcType = pCksCalcObj->Type( calcSize );

        if( calcType != checkSumType )
        {
          log->Error( UtilityMsg, "Calculated checksum: %s, requested "
                      "checksum: %s", pCkSumType.c_str(),
                      checkSumType.c_str() );
          return XRootDStatus( stError, errCheckSumError );
        }

        //----------------------------------------------------------------------
        // Response
        //----------------------------------------------------------------------
        XrdCksData ckSum;
        ckSum.Set( checkSumType.c_str() );
        ckSum.Set( (void*)pCksCalcObj->Final(), calcSize );
        char *cksBuffer = new char[265];
        ckSum.Get( cksBuffer, 256 );
        checkSum  = checkSumType + ":";
        checkSum += Utils::NormalizeChecksum( checkSumType, cksBuffer );
        delete [] cksBuffer;

        log->Dump( UtilityMsg, "Checksum for %s is: %s", pName.c_str(),
                   checkSum.c_str() );
        return XrdCl::XRootDStatus();
      }

    private:
      std::string  pName;
      std::string  pCkSumType;
      XrdCksCalc  *pCksCalcObj;
  };

  //----------------------------------------------------------------------------
  //! Abstract chunk source
  //----------------------------------------------------------------------------
  class Source
  {
    public:
      //------------------------------------------------------------------------
      // Destructor
      //------------------------------------------------------------------------
      Source( const std::string &checkSumType = "" ) : pCkSumHelper( 0 )
      {
        if( !checkSumType.empty() )
          pCkSumHelper = new CheckSumHelper( "source", checkSumType );
      };

      virtual ~Source()
      {
        delete pCkSumHelper;
      }

      //------------------------------------------------------------------------
      //! Initialize the source
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Initialize() = 0;

      //------------------------------------------------------------------------
      //! Get size
      //------------------------------------------------------------------------
      virtual int64_t GetSize() = 0;

      //------------------------------------------------------------------------
      //! Get a data chunk from the source
      //!
      //! @param  ci     chunk information
      //! @return        status of the operation
      //!                suContinue - there are some chunks left
      //!                suDone     - no chunks left
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetChunk( XrdCl::ChunkInfo &ci ) = 0;

      //------------------------------------------------------------------------
      //! Get check sum
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetCheckSum( std::string &checkSum,
                                               std::string &checkSumType ) = 0;

    protected:

      CheckSumHelper    *pCkSumHelper;
  };

  //----------------------------------------------------------------------------
  //! Abstract chunk destination
  //----------------------------------------------------------------------------
  class Destination
  {
    public:
      //------------------------------------------------------------------------
      //! Constructor
      //------------------------------------------------------------------------
      Destination( const std::string &checkSumType = "" ):
        pPosc( false ), pForce( false ), pCoerce( false ), pMakeDir( false ),
        pCkSumHelper( 0 )
      {
        if( !checkSumType.empty() )
          pCkSumHelper = new CheckSumHelper( "destination", checkSumType );
      }

      //------------------------------------------------------------------------
      //! Destructor
      //------------------------------------------------------------------------
      virtual ~Destination()
      {
        delete pCkSumHelper;
      }

      //------------------------------------------------------------------------
      //! Initialize the destination
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Initialize() = 0;

      //------------------------------------------------------------------------
      //! Finalize the destination
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Finalize() = 0;

      //------------------------------------------------------------------------
      //! Put a data chunk at a destination
      //!
      //! @param  ci     chunk information
      //! @return status of the operation
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus PutChunk( XrdCl::ChunkInfo &ci ) = 0;

      //------------------------------------------------------------------------
      //! Flush chunks that might have been queues
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Flush() = 0;

      //------------------------------------------------------------------------
      //! Get check sum
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetCheckSum( std::string &checkSum,
                                               std::string &checkSumType ) = 0;

      //------------------------------------------------------------------------
      //! Set POSC
      //------------------------------------------------------------------------
      void SetPOSC( bool posc )
      {
        pPosc = posc;
      }

      //------------------------------------------------------------------------
      //! Set force
      //------------------------------------------------------------------------
      void SetForce( bool force )
      {
        pForce = force;
      }

      //------------------------------------------------------------------------
      //! Set coerce
      //------------------------------------------------------------------------
      void SetCoerce( bool coerce )
      {
        pCoerce = coerce;
      }

      //------------------------------------------------------------------------
      //! Set makedir
      //------------------------------------------------------------------------
      void SetMakeDir( bool makedir )
      {
        pMakeDir = makedir;
      }

    protected:
      bool pPosc;
      bool pForce;
      bool pCoerce;
      bool pMakeDir;

      CheckSumHelper    *pCkSumHelper;
  };

  //----------------------------------------------------------------------------
  //! StdIn source
  //----------------------------------------------------------------------------
  class StdInSource: public Source
  {
    public:
      //------------------------------------------------------------------------
      //! Constructor
      //------------------------------------------------------------------------
      StdInSource( const std::string &ckSumType, uint32_t chunkSize ):
        Source( ckSumType ),
        pCurrentOffset(0),
        pChunkSize( chunkSize )
      {

      }

      //------------------------------------------------------------------------
      //! Destructor
      //------------------------------------------------------------------------
      virtual ~StdInSource()
      {

      }

      //------------------------------------------------------------------------
      //! Initialize the source
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Initialize()
      {
        if( pCkSumHelper )
          return pCkSumHelper->Initialize();
        return XrdCl::XRootDStatus();
      }

      //------------------------------------------------------------------------
      //! Get size
      //------------------------------------------------------------------------
      virtual int64_t GetSize()
      {
        return -1;
      }

      //------------------------------------------------------------------------
      //! Get a data chunk from the source
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetChunk( XrdCl::ChunkInfo &ci )
      {
        using namespace XrdCl;
        Log *log = DefaultEnv::GetLog();

        uint32_t toRead = pChunkSize;
        char *buffer = new char[toRead];

        int64_t  bytesRead = 0;
        uint32_t offset    = 0;
        while( toRead )
        {
          int64_t bRead = read( 0, buffer+offset, toRead );
          if( bRead == -1 )
          {
            log->Debug( UtilityMsg, "Unable to read from stdin: %s",
                        strerror( errno ) );
            delete [] buffer;
            return XRootDStatus( stError, errOSError, errno );
          }

          if( bRead == 0 )
            break;

          bytesRead += bRead;
          offset    += bRead;
          toRead    -= bRead;
        }

        if( bytesRead == 0 )
        {
          delete [] buffer;
          return XRootDStatus( stOK, suDone );
        }

        if( pCkSumHelper )
          pCkSumHelper->Update( buffer, bytesRead );

        ci.offset = pCurrentOffset;
        ci.length = bytesRead;
        ci.buffer = buffer;
        pCurrentOffset += bytesRead;
        return XRootDStatus( stOK, suContinue );
      }

      //------------------------------------------------------------------------
      //! Get check sum
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetCheckSum( std::string &checkSum,
                                               std::string &checkSumType )
      {
        using namespace XrdCl;
        if( pCkSumHelper )
          return pCkSumHelper->GetCheckSum( checkSum, checkSumType );
        return XRootDStatus( stError, errCheckSumError );
      }

    private:
      StdInSource(const StdInSource &other);
      StdInSource &operator = (const StdInSource &other);

      uint64_t        pCurrentOffset;
      uint32_t        pChunkSize;
  };

  //----------------------------------------------------------------------------
  //! XRootDSource
  //----------------------------------------------------------------------------
  class XRootDSource: public Source
  {
    public:
      //------------------------------------------------------------------------
      //! Constructor
      //------------------------------------------------------------------------
      XRootDSource( const XrdCl::URL *url,
                    uint32_t          chunkSize,
                    uint8_t           parallelChunks,
                    const std::string &ckSumType ):
        Source( ckSumType ),
        pUrl( url ), pFile( new XrdCl::File() ), pSize( -1 ),
        pCurrentOffset( 0 ), pChunkSize( chunkSize ),
        pParallel( parallelChunks ),
        pNbConn( 0 )
      {
        int val = XrdCl::DefaultSubStreamsPerChannel;
        XrdCl::DefaultEnv::GetEnv()->GetInt( "SubStreamsPerChannel", val );
        pMaxNbConn = val - 1; // account for the control stream
      }

      //------------------------------------------------------------------------
      //! Destructor
      //------------------------------------------------------------------------
      virtual ~XRootDSource()
      {
        CleanUpChunks();
        if( pFile->IsOpen() )
          XrdCl::XRootDStatus status = pFile->Close();
        delete pFile;
      }

      //------------------------------------------------------------------------
      //! Initialize the source
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Initialize()
      {
        using namespace XrdCl;
        Log *log = DefaultEnv::GetLog();
        log->Debug( UtilityMsg, "Opening %s for reading",
                                pUrl->GetURL().c_str() );

        std::string value;
        DefaultEnv::GetEnv()->GetString( "ReadRecovery", value );
        pFile->SetProperty( "ReadRecovery", value );

        XRootDStatus st = pFile->Open( pUrl->GetURL(), OpenFlags::Read );
        if( !st.IsOK() )
          return st;

        StatInfo *statInfo;
        st = pFile->Stat( false, statInfo );
        if( !st.IsOK() )
          return st;

        pSize = statInfo->GetSize();
        delete statInfo;

        if( pUrl->IsLocalFile() && !pUrl->IsMetalink() && pCkSumHelper )
          return pCkSumHelper->Initialize();

        if( !pUrl->IsLocalFile() )
          pFile->GetProperty( "DataServer", pDataServer );

        SetOnConnectHandler( pFile );

        return XRootDStatus();
      }

      //------------------------------------------------------------------------
      //! Get size
      //------------------------------------------------------------------------
      virtual int64_t GetSize()
      {
        return pSize;
      }

      //------------------------------------------------------------------------
      //! Get a data chunk from the source
      //!
      //! @param  ci     chunk information
      //! @return        status of the operation
      //!                suContinue - there are some chunks left
      //!                suDone     - no chunks left
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetChunk( XrdCl::ChunkInfo &ci )
      {
        return GetChunkImpl( pFile, ci );
      }

      //------------------------------------------------------------------------
      // Clean up the chunks that are flying
      //------------------------------------------------------------------------
      void CleanUpChunks()
      {
        while( !pChunks.empty() )
        {
          ChunkHandler *ch = pChunks.front();
          pChunks.pop();
          ch->sem->Wait();
          delete [] (char *)ch->chunk.buffer;
          delete ch;
        }
      }

      //------------------------------------------------------------------------
      // Get check sum
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetCheckSum( std::string &checkSum,
                                               std::string &checkSumType )
      {
        if( pUrl->IsMetalink() )
        {
          XrdCl::RedirectorRegistry &registry   = XrdCl::RedirectorRegistry::Instance();
          XrdCl::VirtualRedirector  *redirector = registry.Get( *pUrl );
          checkSum = redirector->GetCheckSum( checkSumType );
          if( !checkSum.empty() ) return XrdCl::XRootDStatus();
        }

        if( pUrl->IsLocalFile() )
        {
          if( pCkSumHelper )
            return pCkSumHelper->GetCheckSum( checkSum, checkSumType );
          else
            return XrdCl::XRootDStatus( XrdCl::stError, XrdCl::errCheckSumError );
        }

        std::string dataServer; pFile->GetProperty( "DataServer", dataServer );
        std::string lastUrl;    pFile->GetProperty( "LastURL",    lastUrl );
        return XrdCl::Utils::GetRemoteCheckSum( checkSum, checkSumType,
                                                dataServer, XrdCl::URL( lastUrl ).GetPath() );
      }

    private:
      XRootDSource(const XRootDSource &other);
      XRootDSource &operator = (const XRootDSource &other);

    protected:

      //------------------------------------------------------------------------
      // Fill the queue with in-the-fly read requests
      //------------------------------------------------------------------------
      template<typename READER>
      inline void FillQueue( READER *reader )
      {
        //----------------------------------------------------------------------
        // Get the number of connected streams
        //----------------------------------------------------------------------
        uint16_t parallel = pParallel;
        if( pNbConn < pMaxNbConn )
        {
          pNbConn = XrdCl::DefaultEnv::GetPostMaster()->
                                                 NbConnectedStrm( pDataServer );
        }
        if( pNbConn ) parallel *= pNbConn;

        while( pChunks.size() < parallel && pCurrentOffset < pSize )
        {
          uint64_t chunkSize = pChunkSize;
          if( pCurrentOffset + chunkSize > (uint64_t)pSize )
            chunkSize = pSize - pCurrentOffset;

          char *buffer = new char[chunkSize];
          ChunkHandler *ch = new ChunkHandler;
          ch->chunk.offset = pCurrentOffset;
          ch->chunk.length = chunkSize;
          ch->chunk.buffer = buffer;
          ch->status = reader->Read( pCurrentOffset, chunkSize, buffer, ch );
          pChunks.push( ch );
          pCurrentOffset += chunkSize;
          if( !ch->status.IsOK() )
          {
            ch->sem->Post();
            break;
          }
        }
      }

      //------------------------------------------------------------------------
      // Set the on-connect handler for data streams
      //------------------------------------------------------------------------
      template<typename READER>
      void SetOnConnectHandler( READER *reader )
      {
        //----------------------------------------------------------------------------
        // On-connect callback job, a lambda would be more elegant, but we still have
        // to support SLC6
        //----------------------------------------------------------------------------
        struct OnConnJob : public XrdCl::Job
        {
            OnConnJob( XRootDSource *self, READER *reader ) : self( self ), reader( reader )
            {
            }

            void Run( void* )
            {
              std::unique_lock<std::mutex> lck( self->pMtx );
              // add new chunks to the queue
              if( self->pNbConn < self->pMaxNbConn )
                self->FillQueue( reader );
            }

          private:
            XRootDSource *self;
            READER       *reader;

        };

        OnConnJob *callback = new OnConnJob( this, reader );
        XrdCl::DefaultEnv::GetPostMaster()->SetOnConnectHandler( pDataServer, callback );
      }

      //------------------------------------------------------------------------
      //! Get a data chunk from the source
      //!
      //! @param  reader  :  reader to read data from
      //! @param  ci      :  chunk information
      //! @return         :  status of the operation
      //!                    suContinue - there are some chunks left
      //!                    suDone     - no chunks left
      //------------------------------------------------------------------------
      template<typename READER>
      XrdCl::XRootDStatus GetChunkImpl( READER *reader, XrdCl::ChunkInfo &ci )
      {
        //----------------------------------------------------------------------
        // Sanity check
        //----------------------------------------------------------------------
        using namespace XrdCl;
        Log *log = DefaultEnv::GetLog();

        if( !reader->IsOpen() )
          return XRootDStatus( stError, errUninitialized );

        //- ---------------------------------------------------------------------
        // Fill the queue
        //----------------------------------------------------------------------
        std::unique_lock<std::mutex> lck( pMtx );
        FillQueue( reader );

        //----------------------------------------------------------------------
        // Pick up a chunk from the front and wait for status
        //----------------------------------------------------------------------
        if( pChunks.empty() )
          return XRootDStatus( stOK, suDone );

        XRDCL_SMART_PTR_T<ChunkHandler> ch( pChunks.front() );
        pChunks.pop();
        lck.unlock();

        ch->sem->Wait();

        if( !ch->status.IsOK() )
        {
          log->Debug( UtilityMsg, "Unable read %d bytes at %ld from %s: %s",
                      ch->chunk.length, ch->chunk.offset,
                      pUrl->GetURL().c_str(), ch->status.ToStr().c_str() );
          delete [] (char *)ch->chunk.buffer;
          CleanUpChunks();
          return ch->status;
        }

        ci = ch->chunk;
        // if it is a local file update the checksum
        if( pUrl->IsLocalFile() && !pUrl->IsMetalink() && pCkSumHelper )
          pCkSumHelper->Update( ci.buffer, ci.length );

        return XRootDStatus( stOK, suContinue );
      }

      //------------------------------------------------------------------------
      // Asynchronous chunk handler
      //------------------------------------------------------------------------
      class ChunkHandler: public XrdCl::ResponseHandler
      {
        public:
          ChunkHandler(): sem( new XrdCl::Semaphore(0) ) {}
          virtual ~ChunkHandler() { delete sem; }
          virtual void HandleResponse( XrdCl::XRootDStatus *statusval,
                                       XrdCl::AnyObject    *response )
          {
            this->status = *statusval;
            delete statusval;
            if( response )
            {
              XrdCl::ChunkInfo *resp = 0;
              response->Get( resp );
              if( resp )
                chunk = *resp;
              delete response;
            }
            sem->Post();
          }

        XrdCl::Semaphore    *sem;
        XrdCl::ChunkInfo     chunk;
        XrdCl::XRootDStatus  status;
      };

      const XrdCl::URL           *pUrl;
      XrdCl::File                *pFile;
      int64_t                     pSize;
      int64_t                     pCurrentOffset;
      uint32_t                    pChunkSize;
      uint16_t                    pParallel;
      std::queue<ChunkHandler *>  pChunks;
      std::string                 pDataServer;
      std::mutex                  pMtx;
      uint16_t                    pNbConn;
      uint16_t                    pMaxNbConn;
  };

  //----------------------------------------------------------------------------
  //! XRootDSourceZip
  //----------------------------------------------------------------------------
  class XRootDSourceZip: public XRootDSource
  {
    public:
      //------------------------------------------------------------------------
      //! Constructor
      //------------------------------------------------------------------------
      XRootDSourceZip( const std::string &filename, const XrdCl::URL *archive,
                       uint32_t          chunkSize,
                       uint8_t           parallelChunks,
                       const std::string &ckSumType ):
                      XRootDSource( archive, chunkSize, parallelChunks, ckSumType ),
                      pFilename( filename ),
                      pZipArchive( new XrdCl::ZipArchiveReader( *pFile ) )
      {
      }

      //------------------------------------------------------------------------
      //! Destructor
      //------------------------------------------------------------------------
      ~XRootDSourceZip()
      {
        XrdCl::XRootDStatus status = pZipArchive->Close();
        delete pZipArchive;
      }

      //------------------------------------------------------------------------
      //! Initialize the source
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Initialize()
      {
        using namespace XrdCl;
        Log *log = DefaultEnv::GetLog();
        log->Debug( UtilityMsg, "Opening %s for reading",
                                pUrl->GetURL().c_str() );

        std::string value;
        DefaultEnv::GetEnv()->GetString( "ReadRecovery", value );
        pFile->SetProperty( "ReadRecovery", value );

        XRootDStatus st = pZipArchive->Open( pUrl->GetURL() );
        if( !st.IsOK() )
          return st;

        st = pZipArchive->Bind( pFilename );
        if( !st.IsOK() )
          return st;

        uint64_t size = 0;
        st = pZipArchive->GetSize( pFilename, size );
        if( st.IsOK() )
          pSize = size;
        else
          return st;

        if( pUrl->IsLocalFile() && !pUrl->IsMetalink() && pCkSumHelper )
          return pCkSumHelper->Initialize();

        SetOnConnectHandler( pFile );

        return XrdCl::XRootDStatus();
      }

      //------------------------------------------------------------------------
      //! Get a data chunk from the source
      //!
      //! @param  buffer buffer for the data
      //! @param  ci     chunk information
      //! @return        status of the operation
      //!                suContinue - there are some chunks left
      //!                suDone     - no chunks left
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetChunk( XrdCl::ChunkInfo &ci )
      {
        return GetChunkImpl( pZipArchive, ci );
      }

      //------------------------------------------------------------------------
      // Get check sum
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetCheckSum( std::string &checkSum,
                                               std::string &checkSumType )
      {
        // The ZIP archive by default contains a ZCRC32 checksum
        if( checkSumType == "zcrc32" )
          return pZipArchive->ZCRC32( checkSum );

        // if it is a local file we can calculate the checksum ourself
        if( pUrl->IsLocalFile() && !pUrl->IsMetalink() && pCkSumHelper )
          return pCkSumHelper->GetCheckSum( checkSum, checkSumType );

        // if it is a remote file other types of checksum are not supported
        return XrdCl::XRootDStatus( XrdCl::stError, XrdCl::errNotSupported );
      }

    private:

      XRootDSourceZip(const XRootDSource &other);
      XRootDSourceZip &operator = (const XRootDSource &other);

      const std::string         pFilename;
      XrdCl::ZipArchiveReader  *pZipArchive;
  };

  //----------------------------------------------------------------------------
  //! XRootDSourceDynamic
  //----------------------------------------------------------------------------
  class XRootDSourceDynamic: public Source
  {
    public:
      //------------------------------------------------------------------------
      //! Constructor
      //------------------------------------------------------------------------
      XRootDSourceDynamic( const XrdCl::URL *url,
                           uint32_t          chunkSize,
                           const std::string &ckSumType ):
        Source( ckSumType ),
        pUrl( url ), pFile( new XrdCl::File() ), pCurrentOffset( 0 ),
        pChunkSize( chunkSize ), pDone( false )
      {
      }

      //------------------------------------------------------------------------
      //! Destructor
      //------------------------------------------------------------------------
      virtual ~XRootDSourceDynamic()
      {
        XrdCl::XRootDStatus status = pFile->Close();
        delete pFile;
      }

      //------------------------------------------------------------------------
      //! Initialize the source
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Initialize()
      {
        using namespace XrdCl;
        Log *log = DefaultEnv::GetLog();
        log->Debug( UtilityMsg, "Opening %s for reading",
                                pUrl->GetURL().c_str() );

        std::string value;
        DefaultEnv::GetEnv()->GetString( "ReadRecovery", value );
        pFile->SetProperty( "ReadRecovery", value );

        XRootDStatus st = pFile->Open( pUrl->GetURL(), OpenFlags::Read );
        if( !st.IsOK() )
          return st;

        if( pUrl->IsLocalFile() && !pUrl->IsMetalink() && pCkSumHelper )
          return pCkSumHelper->Initialize();

        return XRootDStatus();
      }

      //------------------------------------------------------------------------
      //! Get size
      //------------------------------------------------------------------------
      virtual int64_t GetSize()
      {
        return -1;
      }

      //------------------------------------------------------------------------
      //! Get a data chunk from the source
      //!
      //! @param  buffer buffer for the data
      //! @param  ci     chunk information
      //! @return        status of the operation
      //!                suContinue - there are some chunks left
      //!                suDone     - no chunks left
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetChunk( XrdCl::ChunkInfo &ci )
      {
        //----------------------------------------------------------------------
        // Sanity check
        //----------------------------------------------------------------------
        using namespace XrdCl;

        if( !pFile->IsOpen() )
          return XRootDStatus( stError, errUninitialized );

        if( pDone )
          return XRootDStatus( stOK, suDone );

        //----------------------------------------------------------------------
        // Fill the queue
        //----------------------------------------------------------------------
        char     *buffer = new char[pChunkSize];
        uint32_t  bytesRead = 0;

        XRootDStatus st = pFile->Read( pCurrentOffset, pChunkSize, buffer,
                                       bytesRead );

        if( !st.IsOK() )
        {
          delete [] buffer;
          return st;
        }

        if( !bytesRead )
        {
          delete [] buffer;
          return XRootDStatus( stOK, suDone );
        }

        if( bytesRead < pChunkSize )
          pDone = true;

        // if it is a local file update the checksum
        if( pUrl->IsLocalFile() && !pUrl->IsMetalink() && pCkSumHelper )
          pCkSumHelper->Update( buffer, bytesRead );

        ci.offset = pCurrentOffset;
        ci.length = bytesRead;
        ci.buffer = buffer;

        pCurrentOffset += bytesRead;

        return XRootDStatus( stOK, suContinue );
      }

      //------------------------------------------------------------------------
      // Get check sum
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetCheckSum( std::string &checkSum,
                                               std::string &checkSumType )
      {
        if( pUrl->IsMetalink() )
        {
          XrdCl::RedirectorRegistry &registry   = XrdCl::RedirectorRegistry::Instance();
          XrdCl::VirtualRedirector  *redirector = registry.Get( *pUrl );
          checkSum = redirector->GetCheckSum( checkSumType );
          if( !checkSum.empty() ) return XrdCl::XRootDStatus();
        }

        if( pUrl->IsLocalFile() )
        {
          if( pCkSumHelper )
            return pCkSumHelper->GetCheckSum( checkSum, checkSumType );
          else
            return XrdCl::XRootDStatus( XrdCl::stError, XrdCl::errCheckSumError );
        }

        std::string dataServer; pFile->GetProperty( "DataServer", dataServer );
        std::string lastUrl;    pFile->GetProperty( "LastURL",    lastUrl );
        return XrdCl::Utils::GetRemoteCheckSum( checkSum, checkSumType, dataServer,
                                                XrdCl::URL( lastUrl ).GetPath() );
      }

    private:
      XRootDSourceDynamic(const XRootDSourceDynamic &other);
      XRootDSourceDynamic &operator = (const XRootDSourceDynamic &other);
      const XrdCl::URL           *pUrl;
      XrdCl::File                *pFile;
      int64_t                     pCurrentOffset;
      uint32_t                    pChunkSize;
      bool                        pDone;
  };

  //----------------------------------------------------------------------------
  //! XRootDSourceDynamic
  //----------------------------------------------------------------------------
  class XRootDSourceXCp: public Source
  {
    public:
      //------------------------------------------------------------------------
      //! Constructor
      //------------------------------------------------------------------------
      XRootDSourceXCp( const XrdCl::URL* url, uint32_t chunkSize, uint16_t parallelChunks, int32_t nbSrc, uint64_t blockSize ):
        pXCpCtx( 0 ), pUrl( url ), pChunkSize( chunkSize ), pParallelChunks( parallelChunks ), pNbSrc( nbSrc ), pBlockSize( blockSize )
      {
      }

      ~XRootDSourceXCp()
      {
        if( pXCpCtx )
          pXCpCtx->Delete();
      }

      //------------------------------------------------------------------------
      //! Initialize the source
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Initialize()
      {
        XrdCl::Log *log = XrdCl::DefaultEnv::GetLog();
        int64_t fileSize = -1;

        if( pUrl->IsMetalink() )
        {
          XrdCl::RedirectorRegistry &registry = XrdCl::RedirectorRegistry::Instance();
          XrdCl::VirtualRedirector *redirector = registry.Get( *pUrl );
          fileSize = redirector->GetSize();
          pReplicas = redirector->GetReplicas();
        }
        else
        {
          XrdCl::LocationInfo *li = 0;
          XrdCl::FileSystem fs( *pUrl );
          XrdCl::XRootDStatus st = fs.DeepLocate( pUrl->GetPath(), XrdCl::OpenFlags::Compress | XrdCl::OpenFlags::PrefName, li );
          if( !st.IsOK() ) return st;

          XrdCl::LocationInfo::Iterator itr;
          for( itr = li->Begin(); itr != li->End(); ++itr)
          {
            std::string url = "root://" + itr->GetAddress() + "/" + pUrl->GetPath();
            pReplicas.push_back( url );
          }

          delete li;
        }

        std::stringstream ss;
        ss << "XCp sources: ";

        std::vector<std::string>::iterator itr;
        for( itr = pReplicas.begin() ; itr != pReplicas.end() ; ++itr )
        {
          ss << *itr << ", ";
        }
        log->Debug( XrdCl::UtilityMsg, ss.str().c_str() );

        pXCpCtx = new XrdCl::XCpCtx( pReplicas, pBlockSize, pNbSrc, pChunkSize, pParallelChunks, fileSize );

        return pXCpCtx->Initialize();
      }

      //------------------------------------------------------------------------
      //! Get size
      //------------------------------------------------------------------------
      virtual int64_t GetSize()
      {
        return pXCpCtx->GetSize();
      }

      //------------------------------------------------------------------------
      //! Get a data chunk from the source
      //!
      //! @param  buffer buffer for the data
      //! @param  ci     chunk information
      //! @return        status of the operation
      //!                suContinue - there are some chunks left
      //!                suDone     - no chunks left
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetChunk( XrdCl::ChunkInfo &ci )
      {
        XrdCl::XRootDStatus st;
        do
        {
          st = pXCpCtx->GetChunk( ci );
        }
        while( st.IsOK() && st.code == XrdCl::suRetry );
        return st;
      }

      //------------------------------------------------------------------------
      // Get check sum
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetCheckSum( std::string &checkSum,
                                               std::string &checkSumType )
      {
        if( pUrl->IsMetalink() )
        {
          XrdCl::RedirectorRegistry &registry   = XrdCl::RedirectorRegistry::Instance();
          XrdCl::VirtualRedirector  *redirector = registry.Get( *pUrl );
          checkSum = redirector->GetCheckSum( checkSumType );
          if( !checkSum.empty() ) return XrdCl::XRootDStatus();
        }

        std::vector<std::string>::iterator itr;
        for( itr = pReplicas.begin() ; itr != pReplicas.end() ; ++itr )
        {
          XrdCl::URL url( *itr );
          XrdCl::XRootDStatus st = XrdCl::Utils::GetRemoteCheckSum( checkSum,
                              checkSumType, url.GetHostId(), url.GetPath() );
          if( st.IsOK() ) return st;
        }

        return XrdCl::XRootDStatus( XrdCl::stError, XrdCl::errNoMoreReplicas );
      }

    private:


      XrdCl::XCpCtx            *pXCpCtx;
      const XrdCl::URL         *pUrl;
      std::vector<std::string>  pReplicas;
      uint32_t                  pChunkSize;
      uint16_t                  pParallelChunks;
      int32_t                   pNbSrc;
      uint64_t                  pBlockSize;
  };

  //----------------------------------------------------------------------------
  //! SrdOut destination
  //----------------------------------------------------------------------------
  class StdOutDestination: public Destination
  {
    public:
      //------------------------------------------------------------------------
      //! Constructor
      //------------------------------------------------------------------------
      StdOutDestination( const std::string &ckSumType ):
        Destination( ckSumType ), pCurrentOffset(0)
      {
      }

      //------------------------------------------------------------------------
      //! Destructor
      //------------------------------------------------------------------------
      virtual ~StdOutDestination()
      {
      }

      //------------------------------------------------------------------------
      //! Initialize the destination
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Initialize()
      {
        if( pCkSumHelper )
          return pCkSumHelper->Initialize();
        return XrdCl::XRootDStatus();
      }

      //------------------------------------------------------------------------
      //! Finalize the destination
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Finalize()
      {
        return XrdCl::XRootDStatus();
      }

      //------------------------------------------------------------------------
      //! Put a data chunk at a destination
      //!
      //! @param  ci     chunk information
      //! @return status of the operation
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus PutChunk( XrdCl::ChunkInfo &ci )
      {
        using namespace XrdCl;
        Log *log = DefaultEnv::GetLog();

        if( pCurrentOffset != ci.offset )
        {
          log->Error( UtilityMsg, "Got out-of-bounds chunk, expected offset:"
                      " %ld, got %ld", pCurrentOffset, ci.offset );
          return XRootDStatus( stError, errInternal );
        }

        int64_t   wr     = 0;
        uint32_t  length = ci.length;
        char     *cursor = (char*)ci.buffer;
        do
        {
          wr = write( 1, cursor, length );
          if( wr == -1 )
          {
            log->Debug( UtilityMsg, "Unable to write to stdout: %s",
                        strerror( errno ) );
            delete [] (char*)ci.buffer; ci.buffer = 0;
            return XRootDStatus( stError, errOSError, errno );
          }
          pCurrentOffset += wr;
          cursor         += wr;
          length         -= wr;
        }
        while( length );

        if( pCkSumHelper )
          pCkSumHelper->Update( ci.buffer, ci.length );
        delete [] (char*)ci.buffer; ci.buffer = 0;
        return XRootDStatus();
      }

      //------------------------------------------------------------------------
      //! Flush chunks that might have been queues
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Flush()
      {
        return XrdCl::XRootDStatus();
      }

      //------------------------------------------------------------------------
      //! Get check sum
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetCheckSum( std::string &checkSum,
                                               std::string &checkSumType )
      {
        if( pCkSumHelper )
          return pCkSumHelper->GetCheckSum( checkSum, checkSumType );
        return XrdCl::XRootDStatus( XrdCl::stError, XrdCl::errCheckSumError );
      }

    private:
      StdOutDestination(const StdOutDestination &other);
      StdOutDestination &operator = (const StdOutDestination &other);
      uint64_t       pCurrentOffset;
  };

  //----------------------------------------------------------------------------
  //! XRootD destination
  //----------------------------------------------------------------------------
  class XRootDDestination: public Destination
  {
    public:
      //------------------------------------------------------------------------
      //! Constructor
      //------------------------------------------------------------------------
      XRootDDestination( const XrdCl::URL *url, uint8_t parallelChunks,
                         const std::string &ckSumType ):
        Destination( ckSumType ),
        pUrl( url ), pFile( new XrdCl::File( XrdCl::File::DisableVirtRedirect ) ), pParallel( parallelChunks )
      {
      }

      //------------------------------------------------------------------------
      //! Destructor
      //------------------------------------------------------------------------
      virtual ~XRootDDestination()
      {
        CleanUpChunks();
        delete pFile;
      }

      //------------------------------------------------------------------------
      //! Initialize the destination
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Initialize()
      {
        using namespace XrdCl;
        Log *log = DefaultEnv::GetLog();
        log->Debug( UtilityMsg, "Opening %s for writing",
                                pUrl->GetURL().c_str() );

        std::string value;
        DefaultEnv::GetEnv()->GetString( "WriteRecovery", value );
        pFile->SetProperty( "WriteRecovery", value );

        OpenFlags::Flags flags = OpenFlags::Update;
        if( pForce )
          flags |= OpenFlags::Delete;
        else
          flags |= OpenFlags::New;

        if( pPosc )
          flags |= OpenFlags::POSC;

        if( pCoerce )
          flags |= OpenFlags::Force;

        if( pMakeDir)
          flags |= OpenFlags::MakePath;

        Access::Mode mode = Access::UR|Access::UW|Access::GR|Access::OR;

        XrdCl::XRootDStatus st = pFile->Open( pUrl->GetURL(), flags, mode );
        if( !st.IsOK() )
          return st;

        if( pUrl->IsLocalFile() && pCkSumHelper )
          return pCkSumHelper->Initialize();

        return XRootDStatus();
      }

      //------------------------------------------------------------------------
      //! Finalize the destination
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Finalize()
      {
        return pFile->Close();
      }

      //------------------------------------------------------------------------
      //! Put a data chunk at a destination
      //!
      //! @param  ci     chunk information
      //! @return status of the operation
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus PutChunk( XrdCl::ChunkInfo &ci )
      {
        using namespace XrdCl;
        if( !pFile->IsOpen() )
          return XRootDStatus( stError, errUninitialized );

        //----------------------------------------------------------------------
        // If there is still place for this chunk to be sent send it
        //----------------------------------------------------------------------
        if( pChunks.size() < pParallel )
          return QueueChunk( ci );

        //----------------------------------------------------------------------
        // We wait for a chunk to be sent so that we have space for the current
        // one
        //----------------------------------------------------------------------
        XRDCL_SMART_PTR_T<ChunkHandler> ch( pChunks.front() );
        pChunks.pop();
        ch->sem->Wait();
        delete [] (char*)ch->chunk.buffer;
        if( !ch->status.IsOK() )
        {
          Log *log = DefaultEnv::GetLog();
          log->Debug( UtilityMsg, "Unable write %d bytes at %ld from %s: %s",
                      ch->chunk.length, ch->chunk.offset,
                      pUrl->GetURL().c_str(), ch->status.ToStr().c_str() );
          CleanUpChunks();
          return ch->status;
        }

        return QueueChunk( ci );
      }

      //------------------------------------------------------------------------
      //! Clean up the chunks that are flying
      //------------------------------------------------------------------------
      void CleanUpChunks()
      {
        while( !pChunks.empty() )
        {
          ChunkHandler *ch = pChunks.front();
          pChunks.pop();
          ch->sem->Wait();
          delete [] (char *)ch->chunk.buffer;
          delete ch;
        }
      }

      //------------------------------------------------------------------------
      //! Queue a chunk
      //------------------------------------------------------------------------
      XrdCl::XRootDStatus QueueChunk( XrdCl::ChunkInfo &ci )
      {
        // we are writing chunks in order so we can calc the checksum
        // in case of local files
        if( pUrl->IsLocalFile() && pCkSumHelper )
          pCkSumHelper->Update( ci.buffer, ci.length );

        ChunkHandler *ch = new ChunkHandler(ci);
        XrdCl::XRootDStatus st;
        st = pFile->Write( ci.offset, ci.length, ci.buffer, ch );
        if( !st.IsOK() )
        {
          CleanUpChunks();
          delete [] (char*)ci.buffer;
          ci.buffer = 0;
          delete ch;
          return st;
        }
        pChunks.push( ch );
        return XrdCl::XRootDStatus();
      }

      //------------------------------------------------------------------------
      //! Flush chunks that might have been queues
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus Flush()
      {
        XrdCl::XRootDStatus st;
        while( !pChunks.empty() )
        {
          ChunkHandler *ch = pChunks.front();
          pChunks.pop();
          ch->sem->Wait();
          if( !ch->status.IsOK() )
            st = ch->status;
          delete [] (char *)ch->chunk.buffer;
          delete ch;
        }
        return st;
      }

      //------------------------------------------------------------------------
      //! Get check sum
      //------------------------------------------------------------------------
      virtual XrdCl::XRootDStatus GetCheckSum( std::string &checkSum,
                                               std::string &checkSumType )
      {
        if( pUrl->IsLocalFile() )
        {
          if( pCkSumHelper )
            return pCkSumHelper->GetCheckSum( checkSum, checkSumType );
          else
            return XrdCl::XRootDStatus( XrdCl::stError, XrdCl::errCheckSumError );
        }

        std::string dataServer; pFile->GetProperty( "DataServer", dataServer );
        return XrdCl::Utils::GetRemoteCheckSum( checkSum, checkSumType,
                                                dataServer, pUrl->GetPath() );
      }

    private:
      XRootDDestination(const XRootDDestination &other);
      XRootDDestination &operator = (const XRootDDestination &other);

      //------------------------------------------------------------------------
      // Asynchronous chunk handler
      //------------------------------------------------------------------------
      class ChunkHandler: public XrdCl::ResponseHandler
      {
        public:
          ChunkHandler( XrdCl::ChunkInfo ci ):
            sem( new XrdCl::Semaphore(0) ),
            chunk(ci) {}
          virtual ~ChunkHandler() { delete sem; }
          virtual void HandleResponse( XrdCl::XRootDStatus *statusval,
                                       XrdCl::AnyObject    */*response*/ )
          {
            this->status = *statusval;
            delete statusval;
            sem->Post();
          }

          XrdCl::Semaphore       *sem;
          XrdCl::ChunkInfo        chunk;
          XrdCl::XRootDStatus     status;
      };

      const XrdCl::URL           *pUrl;
      XrdCl::File                *pFile;
      uint8_t                     pParallel;
      std::queue<ChunkHandler *>  pChunks;
  };

  static XrdCl::XRootDStatus& UpdateErrMsg( XrdCl::XRootDStatus &status, const std::string &str )
  {
    std::string msg = status.GetErrorMessage();
    msg += " (" + str + ")";
    status.SetErrorMessage( msg );
    return status;
  }
}

namespace XrdCl
{
  //----------------------------------------------------------------------------
  // Constructor
  //----------------------------------------------------------------------------
  ClassicCopyJob::ClassicCopyJob( uint16_t      jobId,
                                  PropertyList *jobProperties,
                                  PropertyList *jobResults ):
    CopyJob( jobId, jobProperties, jobResults )
  {
    Log *log = DefaultEnv::GetLog();
    log->Debug( UtilityMsg, "Creating a classic copy job, from %s to %s",
                GetSource().GetURL().c_str(), GetTarget().GetURL().c_str() );
  }

  //----------------------------------------------------------------------------
  // Run the copy job
  //----------------------------------------------------------------------------
  XRootDStatus ClassicCopyJob::Run( CopyProgressHandler *progress )
  {
    Log *log = DefaultEnv::GetLog();

    std::string checkSumMode;
    std::string checkSumType;
    std::string checkSumPreset;
    std::string zipSource;
    uint16_t    parallelChunks;
    uint32_t    chunkSize;
    uint64_t    blockSize;
    bool        posc, force, coerce, makeDir, dynamicSource, zip, xcp;
    int32_t     nbXcpSources;

    pProperties->Get( "checkSumMode",    checkSumMode );
    pProperties->Get( "checkSumType",    checkSumType );
    pProperties->Get( "checkSumPreset",  checkSumPreset );
    pProperties->Get( "parallelChunks",  parallelChunks );
    pProperties->Get( "chunkSize",       chunkSize );
    pProperties->Get( "posc",            posc );
    pProperties->Get( "force",           force );
    pProperties->Get( "coerce",          coerce );
    pProperties->Get( "makeDir",         makeDir );
    pProperties->Get( "dynamicSource",   dynamicSource );
    pProperties->Get( "zipArchive",      zip );
    pProperties->Get( "xcp",             xcp );
    pProperties->Get( "xcpBlockSize",    blockSize );

    if( zip )
      pProperties->Get( "zipSource",     zipSource );

    if( xcp )
      pProperties->Get( "nbXcpSources",     nbXcpSources );

    //--------------------------------------------------------------------------
    // Initialize the source and the destination
    //--------------------------------------------------------------------------
    XRDCL_SMART_PTR_T<Source> src;
    if( xcp )
      src.reset( new XRootDSourceXCp( &GetSource(), chunkSize, parallelChunks, nbXcpSources, blockSize ) );
    else if( zip ) // TODO make zip work for xcp
      src.reset( new XRootDSourceZip( zipSource, &GetSource(), chunkSize, parallelChunks, checkSumType ) );
    else if( GetSource().GetProtocol() == "stdio" )
      src.reset( new StdInSource( checkSumType, chunkSize ) );
    else
    {
      if( dynamicSource )
        src.reset( new XRootDSourceDynamic( &GetSource(), chunkSize, checkSumType ) );
      else
        src.reset( new XRootDSource( &GetSource(), chunkSize, parallelChunks, checkSumType ) );
    }

    XRootDStatus st = src->Initialize();
    if( !st.IsOK() ) return UpdateErrMsg( st, "source" );
    uint64_t size = src->GetSize() >= 0 ? src->GetSize() : 0;

    XRDCL_SMART_PTR_T<Destination> dest;
    URL newDestUrl( GetTarget() );

    if( GetTarget().GetProtocol() == "stdio" )
      dest.reset( new StdOutDestination( checkSumType ) );
    //--------------------------------------------------------------------------
    // For xrootd destination build the oss.asize hint
    //--------------------------------------------------------------------------
    else
    {
      if( src->GetSize() >= 0 )
      {
        URL::ParamsMap params = newDestUrl.GetParams();
        std::ostringstream o; o << src->GetSize();
        params["oss.asize"] = o.str();
        newDestUrl.SetParams( params );
 //     makeDir = true; // Backward compatability for xroot destinations!!!
      }
      dest.reset( new XRootDDestination( &newDestUrl, parallelChunks, checkSumType ) );
    }

    dest->SetForce( force );
    dest->SetPOSC(  posc );
    dest->SetCoerce( coerce );
    dest->SetMakeDir( makeDir );
    st = dest->Initialize();
    if( !st.IsOK() ) return UpdateErrMsg( st, "destination" );

    //--------------------------------------------------------------------------
    // Copy the chunks
    //--------------------------------------------------------------------------
    ChunkInfo chunkInfo;
    uint64_t  processed = 0;
    while( 1 )
    {
      st = src->GetChunk( chunkInfo );
      if( !st.IsOK() )
        return UpdateErrMsg( st, "source" );

      if( st.IsOK() && st.code == suDone )
        break;

      st = dest->PutChunk( chunkInfo );
      if( !st.IsOK() )
        return UpdateErrMsg( st, "destination" );

      processed += chunkInfo.length;
      if( progress )
      {
        progress->JobProgress( pJobId, processed, size );
        if( progress->ShouldCancel( pJobId ) )
          return XRootDStatus( stError, errOperationInterrupted, kXR_Cancelled, "The copy-job has been cancelled!" );
      }
    }

    st = dest->Flush();
    if( !st.IsOK() )
      return UpdateErrMsg( st, "destination" );

    //--------------------------------------------------------------------------
    // The size of the source is known and not enough data has been transfered
    // to the destination
    //--------------------------------------------------------------------------
    if( src->GetSize() >= 0 && size != processed )
    {
      log->Error( UtilityMsg, "The declared source size is %ld bytes, but "
                  "received %ld bytes.", size, processed );
      return XRootDStatus( stError, errDataError );
    }
    pResults->Set( "size", processed );

    //--------------------------------------------------------------------------
    // Finalize the destination
    //--------------------------------------------------------------------------
    st = dest->Finalize();
    if( !st.IsOK() )
      return UpdateErrMsg( st, "destination" );

    //--------------------------------------------------------------------------
    // Verify the checksums if needed
    //--------------------------------------------------------------------------
    if( checkSumMode != "none" )
    {
      log->Debug( UtilityMsg, "Attempting checksum calculation, mode: %s.",
                  checkSumMode.c_str() );
      std::string sourceCheckSum;
      std::string targetCheckSum;

      //------------------------------------------------------------------------
      // Get the check sum at source
      //------------------------------------------------------------------------
      timeval oStart, oEnd;
      XRootDStatus st;

      if( checkSumMode == "end2end" || checkSumMode == "source" ||
          !checkSumPreset.empty() )
      {
        gettimeofday( &oStart, 0 );
        if( !checkSumPreset.empty() )
        {
          sourceCheckSum  = checkSumType + ":";
          sourceCheckSum += Utils::NormalizeChecksum( checkSumType,
                                                      checkSumPreset );
        }
        else
        {
          st = src->GetCheckSum( sourceCheckSum, checkSumType );
        }
        gettimeofday( &oEnd, 0 );

        if( !st.IsOK() )
          return UpdateErrMsg( st, "source" );

        pResults->Set( "sourceCheckSum", sourceCheckSum );
      }

      //------------------------------------------------------------------------
      // Get the check sum at destination
      //------------------------------------------------------------------------
      timeval tStart, tEnd;

      if( checkSumMode == "end2end" || checkSumMode == "target" )
      {
        gettimeofday( &tStart, 0 );
        st = dest->GetCheckSum( targetCheckSum, checkSumType );
        if( !st.IsOK() )
          return UpdateErrMsg( st, "destination" );
        gettimeofday( &tEnd, 0 );
        pResults->Set( "targetCheckSum", targetCheckSum );
      }

      //------------------------------------------------------------------------
      // Compare and inform monitoring
      //------------------------------------------------------------------------
      if( !sourceCheckSum.empty() && !targetCheckSum.empty() )
      {
        bool match = false;
        if( sourceCheckSum == targetCheckSum )
          match = true;

        Monitor *mon = DefaultEnv::GetMonitor();
        if( mon )
        {
          Monitor::CheckSumInfo i;
          i.transfer.origin = &GetSource();
          i.transfer.target = &GetTarget();
          i.cksum           = sourceCheckSum;
          i.oTime           = Utils::GetElapsedMicroSecs( oStart, oEnd );
          i.tTime           = Utils::GetElapsedMicroSecs( tStart, tEnd );
          i.isOK            = match;
          mon->Event( Monitor::EvCheckSum, &i );
        }

        if( !match )
          return XRootDStatus( stError, errCheckSumError, 0 );
      }
    }
    return XRootDStatus();
  }
}
