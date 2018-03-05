from pypylon import genicam  # CNodeMapRef, GenericException, IsReadable


def main():
    try:
        XMLFileName = "HelloWorld.xml"

        Camera = genicam.CNodeMapRef()
        Camera._LoadXMLFromFile(XMLFileName)

        theNode = Camera.GetNode("TheNode")
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
        print(genicam.IsReadable(theNode))

        print(theFloat.GetIntAlias())
        print(theInt.GetFloatAlias())

        print(Camera.DeviceInfo)

        return 0
    except genicam.GenericException as e:
        print("Error ", e.GetDescription())

        return -1


if __name__ == "__main__":
    main()
