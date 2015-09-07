import sys
import xml.etree.ElementTree as ET

from ipyxact.ipyxact import Ipxact

def get_businterfaces(busInterfaces):
    ifs = []
    for busInterface in busInterfaces.busInterface:
        print('='*20)
        print('name    : ' + busInterface.name)
        _vendor  = busInterface.busType.vendor
        _library = busInterface.busType.library
        _name    = busInterface.busType.name
        _version = busInterface.busType.version
        print(busInterface.busType.name)
        print('busType         : {}/{}/{}/{}'.format(_vendor,
                                                     _library,
                                                     _name,
                                                     _version))
        print('abstractionType : {}/{}/{}/{}'.format(_vendor,
                                                     _library,
                                                     _name,
                                                     _version))
        for portMap in busInterface.portMaps.portMap:
            print("{}[{}:{}] => {}[{}:{}]".format(portMap.logicalPort.name,
                                           portMap.logicalPort.vector.left,
                                           portMap.logicalPort.vector.right,
                                           portMap.physicalPort.name,
                                           portMap.physicalPort.vector.left,
                                           portMap.physicalPort.vector.right))
    return ifs
    
if __name__ == "__main__":
    f = open(sys.argv[1])

    tree = ET.parse(f)
    root = tree.getroot()
    ipxact = Ipxact(root)

    print(dir(ipxact))
    #exit(1)
    ifs = get_businterfaces(ipxact.busInterfaces)

    print(ifs)
    f.close()
