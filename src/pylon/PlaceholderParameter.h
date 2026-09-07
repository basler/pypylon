/*!
\file
\brief Contains the class CPlaceholderParameter, a permanently-invalid sentinel
       parameter that represents a named parameter path that is not available
       in the current device or node map.
*/

#ifndef INCLUDED_BASLER_PYLON_CPLACEHOLDERPARAMETER_H
#define INCLUDED_BASLER_PYLON_CPLACEHOLDERPARAMETER_H

#pragma once

#include <pylon/PylonBase.h>
#include <pylon/Parameter.h>
#include <pylon/Platform.h>
#include <Base/GCException.h>

#ifdef _MSC_VER
#   pragma pack(push, PYLON_PACKING)
#endif /* _MSC_VER */

#if defined(PYLON_WIN_BUILD)
#   pragma warning( push )
#   pragma warning( disable : 4275 )
#   pragma warning( disable : 4250 )
#elif defined(PYLON_UNIX_BUILD)
#   if defined(__clang__)
#       pragma clang diagnostic push
#       pragma clang diagnostic ignored "-Woverloaded-virtual"
#   else
#       pragma GCC diagnostic push
#       pragma GCC diagnostic ignored "-Woverloaded-virtual"
#   endif
#endif

namespace Pylon
{
    /*!
    \brief CPlaceholderParameter is a permanently-invalid sentinel parameter.

    It represents a named parameter path that is not (yet) available in the
    current device or node map.  The parameter is always invalid; every Attach()
    call throws a NOT_IMPLEMENTED_EXCEPTION.  A path string is stored so that
    error messages can tell the caller which parameter was requested.

    The Python layer adds type-safe SetValue / GetValue overloads (for all
    value types used by the standard Pylon parameter classes) as well as every
    Try* / *OrDefault method from those classes.  All such methods return
    \c false / the supplied default, or throw a LogicalErrorException, as
    documented on each overload.
    */
    class CPlaceholderParameter : public CParameter
    {
    public:
        // ------------------------------------------------------------------
        // Construction
        // ------------------------------------------------------------------

        /*!
        \brief Creates a CPlaceholderParameter with an empty path.
        \error
            Does not throw C++ exceptions.
        */
        CPlaceholderParameter()
        {
        }

        /*!
        \brief Creates a CPlaceholderParameter for the given parameter path.
        \param[in] pPath  The parameter path as a null-terminated string.
        \error
            Does not throw C++ exceptions.
        */
        explicit CPlaceholderParameter( const char* pPath )
            : m_path( pPath ? pPath : "" )
        {
        }

        /*!
        \brief Copy constructor.
        \error
            Does not throw C++ exceptions.
        */
        CPlaceholderParameter( const CPlaceholderParameter& rhs )
            : CParameter()
            , m_path( rhs.m_path )
        {
        }

        /*!
        \brief Destructor.
        \error
            Does not throw C++ exceptions.
        */
        virtual ~CPlaceholderParameter()
        {
        }

        // ------------------------------------------------------------------
        // Path accessor
        // ------------------------------------------------------------------

        /*!
        \brief Returns the parameter path supplied at construction.
        \error
            Does not throw C++ exceptions.
        */
        GENICAM_NAMESPACE::gcstring GetPath() const
        {
            return m_path;
        }

        // ------------------------------------------------------------------
        // Assignment
        // ------------------------------------------------------------------

        CPlaceholderParameter& operator=( const CPlaceholderParameter& rhs )
        {
            if ( &rhs != this )
            {
                m_path = rhs.m_path;
            }
            return *this;
        }

        // ------------------------------------------------------------------
        // IsValid — always false
        // ------------------------------------------------------------------

        bool IsValid() const override
        {
            return false;
        }

        // ------------------------------------------------------------------
        // Attach — always throws NOT_IMPLEMENTED
        // ------------------------------------------------------------------

        bool Attach( GenApi::INodeMap* /*pNodeMap*/, const char* /*pName*/ ) override
        {
            throw LOGICAL_ERROR_EXCEPTION(
                "CPlaceholderParameter '%s' cannot be attached. "
                "The parameter is not available for this device.",
                m_path.c_str() );
        }

        bool Attach( GenApi::INodeMap& /*nodeMap*/, const char* /*pName*/ ) override
        {
            throw LOGICAL_ERROR_EXCEPTION(
                "CPlaceholderParameter '%s' cannot be attached. "
                "The parameter is not available for this device.",
                m_path.c_str() );
        }

        bool Attach( GenApi::INode* /*pNode*/ ) override
        {
            throw LOGICAL_ERROR_EXCEPTION(
                "CPlaceholderParameter '%s' cannot be attached. "
                "The parameter is not available for this device.",
                m_path.c_str() );
        }

        bool Attach( GenApi::IValue* /*pValue*/ ) override
        {
            throw LOGICAL_ERROR_EXCEPTION(
                "CPlaceholderParameter '%s' cannot be attached. "
                "The parameter is not available for this device.",
                m_path.c_str() );
        }

    private:
        String_t m_path;
    };

} // namespace Pylon

#if defined(PYLON_WIN_BUILD)
#   pragma warning( pop )
#elif defined(PYLON_UNIX_BUILD)
#   if defined(__clang__)
#       pragma clang diagnostic pop
#   else
#       pragma GCC diagnostic pop
#   endif
#endif

#ifdef _MSC_VER
#   pragma pack(pop)
#endif /* _MSC_VER */

#endif /* INCLUDED_BASLER_PYLON_CPLACEHOLDERPARAMETER_H */

