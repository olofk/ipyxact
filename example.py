#ipyxact example. Parses an IP-XACT XML file called generic_example.xml
#and prints out extended Markdown of the register maps found

import xml.etree.ElementTree as ET

from ipyxact import MemoryMap, Ipxact

def print_memorymaps(memory_maps):
    s = ""
    for m in memory_maps:
        for block in m.addressBlock:
            for reg in block.register:
                s += "\n##0x{:x} {}\n\n".format(reg.addressOffset, reg.name)
                if reg.description:
                    s += "{}\n\n".format(reg.description)

                s += "Bits | Access | Name | Description\n"
                s += "-----|--------|------|------------\n"
                if reg.field:
                    for f in reg.field:
                        if f.bitWidth == 1:
                            bits = f.bitOffset
                        else:
                            bits = "{}:{}".format(f.bitOffset+f.bitWidth-1,f.bitOffset)
                        s += "{}|{}|{}|{}\n".format(bits, f.access, f.name, f.description)

    print(s)



tree = ET.parse('generic_example.xml')
root = tree.getroot()
ipxact = Ipxact(root)

print_memorymaps(ipxact.memoryMaps)

