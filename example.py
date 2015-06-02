#ipyxact example. Parses an IP-XACT XML file called generic_example.xml
#and prints out extended Markdown of the register maps found
import sys

import xml.etree.ElementTree as ET

from ipyxact import MemoryMap, Ipxact

def print_memorymaps(memory_maps):
    s = """Fancy title
===========

Register Map
------------
"""
    for m in memory_maps:
        for block in m.addressBlock:
            for reg in sorted(block.register, key=lambda addr: addr.addressOffset):
                s += "\n##0x{:x} {}\n\n".format(reg.addressOffset, reg.name)
                if reg.description:
                    s += "{}\n\n".format(reg.description)

                s += "Bits | Access | Name | Description\n"
                s += "-----|--------|------|------------\n"
                if reg.field:
                    for f in sorted(reg.field, key=lambda x: x.bitOffset):
                        description = f.description
                        if f.enumeratedValues:
                            for es in f.enumeratedValues:
                                description += "".join(["<br>{} = {}".format(e.value, e.name) for e in es.enumeratedValue])

                        if f.bitWidth == 1:
                            bits = f.bitOffset
                        else:
                            bits = "{}:{}".format(f.bitOffset+f.bitWidth-1,f.bitOffset)
                        s += "{}|{}|{}|{}\n".format(bits, f.access, f.name, description)
                else:
                    s += "{}|{}|{}|{}\n".format("{}:{}".format(reg.size-1, 0), reg.access, reg.name, "-")

    print(s)


f = open(sys.argv[1])
tree = ET.parse(f)
root = tree.getroot()
ipxact = Ipxact(root)

print_memorymaps(ipxact.memoryMaps)

