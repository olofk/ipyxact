#ipyxact example. Parses an IP-XACT XML file called generic_example.xml
#and prints out a C header of the register maps found
import sys
import xml.etree.ElementTree as ET

from ipyxact import Ipxact

def gen_mask(offset, width):
    mask = 0
    for i in range(offset, offset+width):
        mask += 1<<i
    return mask
def print_c_header(memory_maps, offset=0, name=None):
    s = ""
    for m in memory_maps[0].memoryMap:
        if name:
            mname=name.upper()
        else:
            mname = m.name.upper()
        for block in m.addressBlock:
            for reg in sorted(block.register, key=lambda addr: addr.addressOffset):
                s += "#define {}_{} 0x{:08X} \n".format(mname,
                                                        reg.name.upper(),
                                                        offset + block.baseAddress + reg.addressOffset)

                if reg.field:
                    for f in sorted(reg.field, key=lambda x: x.bitOffset):
                        s += "#define {}_{}_{}_MASK 0x{:08X}\n".format(m.name.upper(),
                                                                       reg.name.upper().replace('-','_'),
                                                                       f.name.upper().replace('-','_'),
                                                                       gen_mask(f.bitOffset, f.bitWidth))
                        if f.enumeratedValues:
                            s += "\ntypedef enum {\n"
                            for es in f.enumeratedValues:
                                s += "".join(["  {} = {},\n".format(e.name, e.value) for e in sorted(es.enumeratedValue, key=lambda x: x.value)])
                            s+= "}} {}_t;\n\n".format(f.name.lower())
                s += "\n"
    return s

def write_c_header(f, offset, name):
    tree = ET.parse(f)
    root = tree.getroot()
    ipxact = Ipxact(root)
    return print_c_header(ipxact.memoryMaps, offset, name)

if __name__ == "__main__":
    f = open(sys.argv[1])
    name = None
    offset = 0
    print(write_c_header(f, offset, name))
    f.close()


