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



namespace GENAPI_NAMESPACE
{

    //! the type of callback
    typedef enum _ECallbackType
    {
        cbPostInsideLock = 1,   //!> callback is fired on leaving the tree inside the lock-guarded area
        cbPostOutsideLock = 2,  //!> callback is fired on leaving the tree inside the lock-guarded area
    } ECallbackType;


    %{
        namespace GENAPI_NAMESPACE {

        class PyNodeCallback : public CNodeCallback
        {
        public:
            PyNodeCallback( INode *pNode, PyObject *pyfunc, ECallbackType CallbackType):
                CNodeCallback( pNode, CallbackType ),
                m_pyfunc(pyfunc)
            {
                SWIG_PYTHON_THREAD_BEGIN_BLOCK;
                Py_XINCREF(m_pyfunc);         /* Add a reference to new callback */
                SWIG_PYTHON_THREAD_END_BLOCK;
            };

            //! virtual destructor
            virtual ~PyNodeCallback()
            {
                SWIG_PYTHON_THREAD_BEGIN_BLOCK;
                Py_XDECREF(m_pyfunc);          /* Dispose of previous callback */
                SWIG_PYTHON_THREAD_END_BLOCK;
            };

            //! fires the callback if th type is right
            virtual void operator()( ECallbackType CallbackType ) const{
                PyObject *result, *node, *arglist;

                if (CallbackType == m_CallbackType)
                {
                   swig_type_info *outtype = 0;
                   void * outptr = 0;
                   switch (m_pNode->GetPrincipalInterfaceType()){
                                case intfIValue :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__IValue;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::IValue*>(m_pNode);
                                            break;
                                case intfIInteger :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__IInteger;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::IInteger*>(m_pNode);
                                            break;
                                case intfIBoolean :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__IBoolean;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::IBoolean*>(m_pNode);
                                            break;
                                case intfICommand :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__ICommand;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::ICommand*>(m_pNode);
                                            break;
                                case intfIFloat :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__IFloat;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::IFloat*>(m_pNode);
                                            break;
                                case intfIString :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__IString;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::IString*>(m_pNode);
                                            break;
                                case intfIRegister :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__IRegister;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::IRegister*>(m_pNode);
                                            break;
                                case intfICategory :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__ICategory;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::ICategory*>(m_pNode);
                                            break;
                                case intfIEnumeration :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__IEnumeration;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumeration*>(m_pNode);
                                            break;
                                case intfIEnumEntry :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__IEnumEntry;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumEntry*>(m_pNode);
                                            break;
                                case intfIPort :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__IPort;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::IPort*>(m_pNode);
                                            break;
                                case intfIBase :
                                            outtype = SWIGTYPE_p_GENAPI_NAMESPACE__IBase;
                                            outptr  = dynamic_cast<GENAPI_NAMESPACE::IBase*>(m_pNode);
                                            break;
                    };
                    SWIG_PYTHON_THREAD_BEGIN_BLOCK;
                    node = SWIG_NewPointerObj(outptr, outtype, 0 );
                    arglist = Py_BuildValue("(O)", node);

                    result = PyEval_CallObject(m_pyfunc, arglist);
                    Py_DECREF(arglist);

                    if (!result){
                        // this should be fixed. For now I use the already installed exception catcher
                        Swig::DirectorException::raise("error in callback");
                    }
                    Py_XDECREF(result);

                    SWIG_PYTHON_THREAD_END_BLOCK;
                }
                return /*void*/;
            }

            //! destroys the object
            virtual void Destroy(){
                delete this;
            };

            //! returns the node the callback is registered to
            INode* GetNode()
            {
                return m_pNode;
            }
        private:
            PyObject *m_pyfunc;
        };
    };

%}

    %typemap(in) PyObject *PyFunc {
        if (!PyCallable_Check($input)) {
            PyErr_SetString(PyExc_TypeError, "Need a callable object!");
            return NULL;
        }
        $1 = $input;
    }

    // we don't need the baseclass here
    %warnfilter(401) PyNodeCallback;

    class PyNodeCallback: public CNodeCallback
    {
    public:
        PyNodeCallback( INode *pNode, PyObject *PyFunc, ECallbackType CallbackType);

        //! virtual destructor
        virtual ~PyNodeCallback();
        virtual INode* GetNode();
    };

    %pythoncode %{
        def Register(node, callback_fun, callback_type=cbPostInsideLock):
            assert callback_type in ( cbPostOutsideLock, cbPostInsideLock)
            cb = PyNodeCallback(node, callback_fun, callback_type)
            cb.thisown = 0
            return node.RegisterCallback(cb)

    %}

    //! Unregistering callback by handle
    // definition in Node.cpp
    void Deregister (GENAPI_NAMESPACE::CallbackHandleType pCallbackInfo );


}