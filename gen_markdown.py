#ipyxact example. Parses an IP-XACT XML file called generic_example.xml
#and prints out extended Markdown of the register maps found
import sys

from ipyxact.ipyxact import Component

def print_memorymaps(memory_maps, offset=0, title=None):
    s = """{}
===========

Register Map
------------
"""
    if title:
        s = s.format(title)
    else:
        s = s.format("Register map")
    for m in memory_maps.memoryMap:
        for block in m.addressBlock:
            for reg in sorted(block.register, key=lambda addr: addr.addressOffset):
                s += "\n## 0x{:x} {}\n\n".format(offset+block.baseAddress+reg.addressOffset, reg.name)
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

    return s

def write_markdown(f, offset, name):
    component = Component()
    component.load(f)
    return print_memorymaps(component.memoryMaps, offset, name)

if __name__ == "__main__":
    f = open(sys.argv[1])
    title = None
    offset = 0
    print(write_markdown(f, offset, title))
    f.close()

