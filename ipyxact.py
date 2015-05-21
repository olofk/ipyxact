"""
The MIT License (MIT)

Copyright (c) 2015 Olof Kindgren <olof.kindgren@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

IPXACT_NS = 'http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.4'
ns = {'spirit' : IPXACT_NS}

class IpxactInt(int):
    def __new__(cls, *args, **kwargs):
        if not args:
            return super(IpxactInt, cls).__new__(cls)
        elif len(args[0]) > 2 and args[0][0:2] == '0x':
            return super(IpxactInt, cls).__new__(cls, args[0][2:], 16)
        else:
            return super(IpxactInt, cls).__new__(cls, args[0])

class IpxactItem(object):
    MEMBERS = {}
    CHILDREN = []
    def __init__(self, root=None):
        for key, value in self.MEMBERS.items():
            setattr(self, key, value)
        for c in self.CHILDREN:
            setattr(self, c, [])

        if root:
            self.parse_tree(root)

    def parse_tree(self, root):
        for _name, _type in self.MEMBERS.items():
            tmp = root.find('./spirit:{}'.format(_name), ns)
            if tmp is not None:
                setattr(self, _name, _type(tmp.text))
            else:
                setattr(self, _name, _type())

        for c in self.CHILDREN:
            for f in root.findall(".//spirit:{}".format(c), ns):
                child = getattr(self, c)
                class_name = c[0].upper() + c[1:]
                t = eval(class_name)(f)
                child.append(t)
    
class Field(IpxactItem):
    MEMBERS = {'name'        : str,
               'description' : str,
               'bitOffset'   : IpxactInt,
               'bitWidth'    : IpxactInt,
               'access'      : str}

class Register(IpxactItem):
    MEMBERS = {'name'          : str,
               'description'   : str,
               'addressOffset' : IpxactInt,
               'width'         : IpxactInt}
    CHILDREN = ['field']

class AddressBlock(IpxactItem):
    MEMBERS = {'name'        : str,
               'description' : str,
               'baseAddress' : IpxactInt,
               'width' : IpxactInt}

    CHILDREN = ['register']

class MemoryMap(IpxactItem):
    MEMBERS = {'name' : str}

    CHILDREN = ['addressBlock']

class MemoryMaps(IpxactItem):
    CHILDREN = ['addressMap']

class Ipxact:
    def __init__(self, root):
        self.memoryMaps = [MemoryMap(m) for m in root.findall('spirit:memoryMap', ns)]

#        self.memoryMaps = 
        
#for mmap in mmaps:
#    memory_map = MemoryMap(mmap)
    
