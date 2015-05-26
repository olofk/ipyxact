#ipyxact example. Parses an IP-XACT XML file called generic_example.xml
#and prints out a C header of the register maps found

import xml.etree.ElementTree as ET

from ipyxact import MemoryMap, Ipxact

def gen_mask(offset, width):
    mask = 0
    for i in range(offset, offset+width):
        mask += 1<<i
    return mask
def print_c_header(memory_maps):
    s = ""
    for m in memory_maps:
        for block in m.addressBlock:
            for reg in block.register:
                s += "#define {} 0x{:08X} \n".format(reg.name.upper(),
                                                   block.baseAddress + reg.addressOffset)

                if reg.field:
                    for f in reg.field:
                        s += "#define {}_{}_MASK 0x{:08X}\n".format(reg.name.upper(),
                                                                  f.name.upper(),
                                                                  gen_mask(f.bitOffset, f.bitWidth))
                s += "\n"
    print(s)



tree = ET.parse('generic_example.xml')
root = tree.getroot()
ipxact = Ipxact(root)

print_c_header(ipxact.memoryMaps)

