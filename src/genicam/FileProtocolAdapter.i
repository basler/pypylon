%{

#include <GenApi/Filestream.h>

%}

namespace GENAPI_NAMESPACE
{

    /*!
    * @brief
    * Adapter between the std::iostreambuf and the SFNC Features representing the device filesystem
    *
    * The adapter assumes, that the features provide stdio fileaccess
    * compatible semantic
    *
    */
    class FileProtocolAdapter {
    public:
        /*!
        * @brief
        * Constructor
        *
        */
        FileProtocolAdapter();


        /*!
        * @brief
        * attach file protocol adapter to nodemap
        *
        * @param pInterface
        * NodeMap of the device to which the FileProtocolAdapter is attached
        *
        * @return true if attach was successful, false if not
        *
        */
        bool attach(GENAPI_NAMESPACE::INodeMap * pInterface );


        /*!
        * @brief
        * open a file on the device
        *
        * @param pFileName
        * filename of the file to open. The filename must exist in the Enumeration FileSelector
        *
        * @param mode
        * mode to open the file. "r" or "w"
        *
        * @returns
        * true on success, false on error
        *
        */
        %extend {
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

        /*!
        * @brief
        * close a file on the device
        *
        * @param pFileName
        * filename of the file to open. The filename must exist in the Enumeration FileSelector
        *
        * @returns
        * true on success, false on error
        */
        bool closeFile(const char * pFileName);


        /*!
        * @brief
        * writes data into a file.
        *
        * @param buf
        * source buffer
        *
        * @param offs
        * offset into the device file
        *
        * @param len
        * count of bytes to write
        *
        * @param pFileName
        * filename of the file to write into The filename must exist in the Enumeration FileSelector
        *
        * @returns
        * count of bytes written
        *
        */
        %extend {
            std::streamsize write(const char *pBuffer, int64_t Length, int64_t offs, const char * pFileName){
                return $self->write(pBuffer, offs, Length, pFileName);
            }
        }


        /*!
        * @brief
        * read data from the device into a buffer
        *
        * @param buf
        * target buffer
        *
        * @param offs
        * offset in the device file to read from
        *
        * @param len
        * count of bytes to read
        *
        * @param pFileName
        * filename of the file to write into The filename must exist in the Enumeration FileSelector
        *
        * @returns
        * count of bytes successfully read
        *
        */
        %extend {
            std::streamsize read(char *pBuffer, int64_t Length, int64_t offs, const char * pFileName){
                return $self->read(pBuffer, offs, INTEGRAL_CAST<std::streamsize>(Length), pFileName);
            }
        }


        /*!
        * @brief
        * fetch max FileAccessBuffer length for a file
        *
        * @param pFileName
        * filename of the file to open. The filename must exist in the Enumeration FileSelector
        *
        * @param mode
        * mode to open the file. "r" or "w"
        *
        * @returns
        * max length of FileAccessBuffer in the given mode on the given file
        *
        */
        %extend {
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

        //int64_t getBufSize(const char * pFileName, std::ios_base::openmode mode);


        /*!
        * @brief
        * Delete the content of the file.
        *
        * @param pFileName
        * filename of the file to open. The filename must exist in the Enumeration FileSelector
        *
        * @returns
        * true on success, false on error
        */
        bool deleteFile(const char * pFileName);

    };


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
                read_len, data  = self.fpa.read(size, self.fpos, self.filename)
                data = data[:read_len]
                self.fpos += read_len
                return data

            def read(self, size = -1):
                assert(self.isopen)
                if size < 0:
                    buf = b""
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

};

