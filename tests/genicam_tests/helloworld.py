from genicam import CNodeMapRef, GenericException, IsReadable
import sys


def main():
    try:
        XMLFileName = "HelloWorld.xml"

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile(XMLFileName)

        theNode = Camera._GetNode("TheNode")
        print(type(theNode))

        theInt = Camera.GetNode("TheInt")
        print(type(theInt))

        nodes = Camera._GetNodes()
        for n in nodes:
            print(n.ToString())

        theFloat = Camera.GetNode("TheFloat")

        print(theNode.ToString())
        print(theInt.ToString())
        print(theInt.Node.GetPropertyNames())
        print(IsReadable(theNode))

        print(theFloat.GetIntAlias())
        print(theInt.GetFloatAlias())

        print(Camera.DeviceInfo)
        ver, build = Camera.DeviceInfo.GetGenApiVersion()
        print(ver.Major)
        print(ver.Minor)
        print(ver.SubMinor)

        return 0
    except GenericException as e:
        print("Error ", e.GetDescription())

        return -1


if __name__ == "__main__":
    sys.exit(main())
