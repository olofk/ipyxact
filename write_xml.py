import sys
import xml.etree.ElementTree as ET

from ipyxact.ipyxact import Ipxact

if __name__ == "__main__":
    f = open(sys.argv[1])

    tree = ET.parse(f)
    root = tree.getroot()
    ipxact = Ipxact(root)

    f.close()

    ipxact.write('new.xml')
