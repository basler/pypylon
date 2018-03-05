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

#ifndef GENAPI_PYPORTIMPL_H
#define GENAPI_PYPORTIMPL_H

namespace GENAPI_NAMESPACE
{
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
		CPyPortImpl(): CPortImpl()
        {
        }

        //! Destructor
        virtual ~CPyPortImpl()
        {
        }

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
        virtual void PyRead(int64_t Address, void *pBuffer, int64_t Length) = 0;

        //! Writes a chunk of bytes to the port
        virtual void PyWrite(int64_t Address, const void *pBuffer, int64_t Length) = 0;


        //! Reads a chunk of bytes from the port
	virtual void Read(void *pBuffer, int64_t Address, int64_t Length){
			PyRead(Address, pBuffer,Length);
		}

        //! Writes a chunk of bytes to the port
	virtual void Write(const void *pBuffer, int64_t Address, int64_t Length){
			PyWrite(Address, pBuffer,Length);
		}

    };
}

#endif // ifndef GENAPI_PORTIMPL_H
