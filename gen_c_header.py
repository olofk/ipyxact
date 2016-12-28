#ipyxact example. Parses an IP-XACT XML file called generic_example.xml
#and prints out a C header of the register maps found
import sys

from ipyxact.ipyxact import Component

def gen_mask(offset, width):
    mask = 0
    for i in range(offset, offset+width):
        mask += 1<<i
    return mask
def print_c_header(memory_maps, offset=0, name=None):
    s = ""
    for m in memory_maps.memoryMap:
        if name:
            mname=name.upper()
        else:
            mname = m.name.upper()
        multiblock = len(m.addressBlock) > 1

        for block in m.addressBlock:
            if multiblock:
                bname = mname + '_' + block.name.upper()
            else:
                bname = mname
            for reg in sorted(block.register, key=lambda addr: addr.addressOffset):
                s += "#define {}_{} 0x{:08X} \n".format(bname,
                                                        reg.name.upper(),
                                                        offset + block.baseAddress + reg.addressOffset)

                if reg.field:
                    for f in sorted(reg.field, key=lambda x: x.bitOffset):
                        s += "#define {}_{}_{}_MASK 0x{:08X}\n".format(bname,
                                                                       reg.name.upper().replace('-','_'),
                                                                       f.name.upper().replace('-','_'),
                                                                       gen_mask(f.bitOffset, f.bitWidth))
                        if f.enumeratedValues:
                            s += "\ntypedef enum {\n"
                            for es in f.enumeratedValues:
                                s += "".join(["    {}_{} = {},\n".format(f.name.lower(), e.name, e.value<<f.bitOffset) for e in sorted(es.enumeratedValue, key=lambda x: x.value)])
                            s+= "}} {}_t;\n\n".format(f.name.lower())
                s += "\n"
    return s

def write_c_header(f, offset, name):
    component = Component()
    component.load(f)
    if component.memoryMaps:
        return print_c_header(component.memoryMaps, offset, name)
    else:
        return "No memory maps found"

if __name__ == "__main__":
    f = open(sys.argv[1])
    name = None
    offset = 0
    print(write_c_header(f, offset, name))
    f.close()


