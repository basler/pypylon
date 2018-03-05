%ignore IDevFileStreamBase;
%ignore ODevFileStreamBase;
%ignore GENAPI_NAMESPACE::IFileProtocolAdapter;
%ignore IFileProtocolAdapter;
%ignore IDevFileStreamBuf;
%ignore ODevFileStreamBuf;
%ignore ODevFileStream;
%ignore IDevFileStream;
%{

#include <GenApi/Filestream.h>

%}

#define _MSC_VER
#define GENICAM_NO_AUTO_IMPLIB

%extend GENAPI_NAMESPACE::FileProtocolAdapter{
    bool openFile(const char * pFileName, const char* mode){
        bool ret = false;
        if ( mode != 0 &&  mode[0] == 'r'){
            ret = $self->openFile(pFileName, std::ios_base::in);
        }
        else if ( mode != 0 &&  mode[0] == 'w'){
            ret = $self->openFile(pFileName, std::ios_base::out);
        }
        return ret;
    }
}
%extend GENAPI_NAMESPACE::FileProtocolAdapter{
    std::streamsize read(char *pBuffer, int64_t Length, int64_t offs, const char * pFileName){
        return $self->read(pBuffer, offs, INTEGRAL_CAST<std::streamsize>(Length), pFileName);
    }
}
%extend GENAPI_NAMESPACE::FileProtocolAdapter{
    int64_t getBufSize(const char * pFileName, const char* mode){
        int64_t buf_size = -1;
        if ( mode != 0 &&  mode[0] == 'r'){
                buf_size = $self->getBufSize(pFileName, std::ios_base::in);
        }
        else if ( mode != 0 &&  mode[0] == 'w'){
                buf_size = $self->getBufSize(pFileName, std::ios_base::out);
        }
        return buf_size;
    }
}



%include <GenApi/Filestream.h>;
#undef _MSC_VER
#undef GENICAM_NO_AUTO_IMPLIB
%rename("%s") "";

%pythoncode {
    class FileAccess(object):
        def __init__(self, read_bufsize = 4096):
            if read_bufsize == 0:
                raise IOError("invalid read_bufsize")

            self.isopen   = False
            self.filename = ""
            self.mode     = ""
            self.fpa      = FileProtocolAdapter()
            self.fpa_bufsize  = 0
            self.fpos     = 0
            self.read_bufsize = read_bufsize

        def open(self, nodemap, filename, openmode):
            self.fpa.attach(nodemap)
            self.filename = filename
            self.fpa.openFile(filename,openmode)
            self.fpa_bufsize = self.fpa.getBufSize(filename, openmode)
            self.fpos = 0
            self.isopen = True

        def close(self):
            self.isopen = False
            self.fpa.closeFile(self.filename)

        def _read(self, size):
            assert(self.isopen)
            buf = ""
            for ofs in xrange(0, size, self.fpa_bufsize):
                read_len, data  = self.fpa.read(self.fpa_bufsize, self.fpos + ofs, self.filename)
                if read_len <= 0:
                    break
                else:
                    buf += data[:min(size-ofs,read_len)]

            self.fpos += len(buf)
            return buf

        def read(self, size = -1):
            assert(self.isopen)
            if size < 0:
                buf = ""
                while True:
                    data  = self._read(self.read_bufsize)
                    buf += data
                    if len(data) < self.read_bufsize:
                        return buf

            else:
                data  = self._read(size)
                return data


        def write(self,data):
            assert(self.isopen)
            ret = self.fpa.write(data, self.fpos, self.filename)
            self.fpos += len(data)
            return ret
}

