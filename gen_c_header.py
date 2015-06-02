#ipyxact example. Parses an IP-XACT XML file called generic_example.xml
#and prints out a C header of the register maps found
import sys
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
            for reg in sorted(block.register, key=lambda addr: addr.addressOffset):
                s += "#define {} 0x{:08X} \n".format(reg.name.upper(),
                                                   block.baseAddress + reg.addressOffset)

                if reg.field:
                    for f in sorted(reg.field, key=lambda x: x.bitOffset):
                        s += "#define {}_{}_MASK 0x{:08X}\n".format(reg.name.upper().replace('-','_'),
                                                                  f.name.upper().replace('-','_'),
                                                                  gen_mask(f.bitOffset, f.bitWidth))
                s += "\n"
    print(s)


f = open(sys.argv[1])
tree = ET.parse(f)
root = tree.getroot()
ipxact = Ipxact(root)

print_c_header(ipxact.memoryMaps)

