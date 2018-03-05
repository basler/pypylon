namespace GENICAM_NAMESPACE
{
    //! version

    %rename(Version) Version_t;
    struct Version_t
    {
        uint16_t Major;        //!> a is incompatible with b if a != b
        uint16_t Minor;        //!> a is incompatible b a > b
        uint16_t SubMinor;     //!> a is aways compatible with b
    };
};


