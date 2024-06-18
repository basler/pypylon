%rename(VariantContainerType) Pylon::DataProcessing::EVariantContainerType;

#if PYLON_DATAPROCESSING_VERSION_MAJOR >= 2
%include <pylondataprocessing/VariantContainerType.h>;
#else
/*!
 * \namespace Pylon
 * \brief The Pylon namespace
 */
namespace Pylon
{
    /*!
     * \namespace Pylon::DataProcessing
     * \brief The DataProcessing namespace
     */
    namespace DataProcessing
    {
        /*!
         \brief
            Lists the built-in variant container types.
        **/
        enum EVariantContainerType
        {
            VariantContainerType_None           = 0,    //!< A basic data object without any container.
            VariantContainerType_Array          = 1,    //!< An array that may contain basic data objects.
            VariantContainerType_Unsupported    = 2     //!< A container type that is not supported natively by this SDK yet.
        };
    }
}
#endif
