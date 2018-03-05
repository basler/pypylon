//-----------------------------------------------------------------------------
//  (c) 2012 by Basler Vision Technologies
//  Section: Vision Components
//  Project: GenApi
//  Author:  Thies Moeller
//  $Header$
//
//  License: This file is published under the license of the EMVA GenICam  Standard Group.
//  A text file describing the legal terms is included in  your installation as 'GenICam_license.pdf'.
//  If for some reason you are missing  this file please contact the EMVA or visit the website
//  (http://www.genicam.org) for a full copy.
//
//  THIS SOFTWARE IS PROVIDED BY THE EMVA GENICAM STANDARD GROUP "AS IS"
//  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE EMVA GENICAM STANDARD  GROUP
//  OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,  SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT  LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,  DATA, OR PROFITS;
//  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY  THEORY OF LIABILITY,
//  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT  (INCLUDING NEGLIGENCE OR OTHERWISE)
//  ARISING IN ANY WAY OUT OF THE USE  OF THIS SOFTWARE, EVEN IF ADVISED OF THE
//  POSSIBILITY OF SUCH DAMAGE.
//-----------------------------------------------------------------------------


%{
#include "PyPortImpl.h"
%}

%nodefaultdtor GENAPI_NAMESPACE::CPortImpl;
%nodefaultctor GENAPI_NAMESPACE::CPortImpl;

%warnfilter(403) GENAPI_NAMESPACE::CPortImpl;

%nodefaultdtor GENAPI_NAMESPACE::CPyPortImpl;
%feature("director") GENAPI_NAMESPACE::CPyPortImpl; 

namespace GENAPI_NAMESPACE
{

    //*************************************************************
    // CPortImpl class
    //*************************************************************

    %ignore CPortImpl;
    /**
    \brief Standard implementation for a port
    //! \ingroup GenApi_PublicUtilities
    */
    class CPortImpl : public IPortConstruct, public IPortReplay
    {
    public:
        //! Constructor
        CPortImpl();
        
        //! Destructor
        virtual ~CPortImpl();

        /*---------------------------------------------------------------*/
        // IPortConstruct implementation (without IPort & IBase)
        /*---------------------------------------------------------------*/

        //! Sets pointer the real port implementation; this function may called only once
        //virtual void SetPortImpl(IPort* pPort);

        //! Determines if the port adapter must perform an endianess swap
        virtual EYesNo GetSwapEndianess();


        //---------------------------------------------------------------
        // IPortReplay implementation
        //---------------------------------------------------------------

        //! sends the commands to the camera.
        /*! the default implementation just walks the list and issues each command
        using the WriteRegister method. Depending on the capabilities of
        the transport layer the implementation can however use a special command
        which sends all register write commands as one package.
        */
        virtual void Replay( IPortWriteList *pPortRecorder, bool Invalidate = true );

        // Invalidate the node
        void InvalidateNode();


    };

    %rename(Read) CPyPortImpl::PyRead;
    %rename(Write) CPyPortImpl::PyWrite;
    %rename(CPortImpl) CPyPortImpl;
    
	
    //*************************************************************
    // CPortImpl class
    //*************************************************************

    /**
    \brief Standard implementation for a port
    //! \ingroup GenApi_PublicUtilities
    */
    class CPyPortImpl : public CPortImpl
    {
    public:
        //! Constructor
        CPyPortImpl();

        //! Destructor
        virtual ~CPyPortImpl();

        /*---------------------------------------------------------------*/
        // IBase ==> You need to override this method
        /*---------------------------------------------------------------*/

        //! Get the access mode of the node
        /*! Driver closed => NI, Driver open => RW, analysing a struct, RO */
        virtual EAccessMode GetAccessMode() const = 0;

        /*---------------------------------------------------------------*/
        // IPort ==> You need to override these methods
        /*---------------------------------------------------------------*/

        //! Reads a chunk of bytes from the port
        //virtual void Read(void *pBuffer, int64_t Address, int64_t Length);

        //! Writes a chunk of bytes to the port
        //virtual void Write(const void *pBuffer, int64_t Address, int64_t Length);

        //! Reads a chunk of bytes from the port
        virtual void PyRead(int64_t Address, void *pBuffer, int64_t Length) = 0;

        //! Writes a chunk of bytes to the port
        virtual void PyWrite(int64_t Address, const void *pBuffer, int64_t Length) = 0;

        // Invalidate the node
        void InvalidateNode();

    };
}
    

