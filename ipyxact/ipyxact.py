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

import xml.etree.ElementTree as ET

class IpxactInt(int):
    def __new__(cls, *args, **kwargs):
        if not args:
            return super(IpxactInt, cls).__new__(cls)
        elif len(args[0]) > 2 and args[0][0:2] == '0x':
            return super(IpxactInt, cls).__new__(cls, args[0][2:], 16)
        elif "'" in args[0]:
            sep = args[0].find("'")
            if args[0][sep+1] == "h":
                base = 16
            else:
                raise Exception
            return super(IpxactInt, cls).__new__(cls, args[0][sep+2:], base)
        else:
            return super(IpxactInt, cls).__new__(cls, args[0])

class IpxactBool(object):
    def __new__(cls, *args, **kwargs):
        if not args:
            return False
        elif args[0] == 'true':
            return True
        elif args[0] == 'false':
            return False
        else:
            raise Exception

class IpxactItem(object):
    ATTRIBS = {}
    MEMBERS = {}
    CHILDREN = []
    CHILD = []
    def __init__(self):
        for key, value in self.ATTRIBS.items():
            setattr(self, key, value)
        for key, value in self.MEMBERS.items():
            setattr(self, key, value)
        for c in self.CHILDREN:
            setattr(self, c, [])
        for c in self.CHILD:
            setattr(self, c, None)

    def parse_tree(self, root, ns):
        if self.ATTRIBS:
            for _name, _type in self.ATTRIBS.items():
                _tagname = '{' + ns[1] + '}' + _name
                if _tagname in root.attrib:
                    setattr(self, _name, _type(root.attrib[_tagname]))
        for _name, _type in self.MEMBERS.items():
            tmp = root.find('./{}:{}'.format(ns[0], _name), {ns[0] : ns[1]})
            if tmp is not None and tmp.text is not None:
                setattr(self, _name, _type(tmp.text))
            else:
                setattr(self, _name, _type())

        for c in self.CHILDREN:
            for f in root.findall(".//{}:{}".format(ns[0], c), {ns[0] : ns[1]}):
                child = getattr(self, c)
                class_name = c[0].upper() + c[1:]
                t = eval(class_name)()
                t.parse_tree(f, ns)
                child.append(t)
        for c in self.CHILD:
            f = root.find(".//{}:{}".format(ns[0], c), {ns[0] : ns[1]})
            if f is not None:
                class_name = c[0].upper() + c[1:]
                t = eval(class_name)()
                t.parse_tree(f, ns)
                setattr(self, c, t)

    def write(self, root, S):

        for a in self.ATTRIBS:
            root.attrib[S+a] = getattr(self, a)

        for m in self.MEMBERS:
            tmp = getattr(self, m)
            if tmp is not None:
                ET.SubElement(root, S+m).text = str(tmp)

        for c in self.CHILDREN:
            for child_obj in getattr(self, c):
                subel = ET.SubElement(root, S+c)
                child_obj.write(subel, S)
        for c in self.CHILD:
            tmp = getattr(self, c)
            if tmp is not None:
                subel = ET.SubElement(root, S+c)
                tmp.write(subel, S)

class EnumeratedValue(IpxactItem):
    MEMBERS = {'name' : str,
               'value' : IpxactInt}

class EnumeratedValues(IpxactItem):
    CHILDREN = ['enumeratedValue']
    
class Field(IpxactItem):
    MEMBERS = {'name'        : str,
               'description' : str,
               'bitOffset'   : IpxactInt,
               'bitWidth'    : IpxactInt,
               'volatile'    : IpxactBool,
               'access'      : str}
    CHILDREN = ['enumeratedValues']

class Register(IpxactItem):
    MEMBERS = {'name'          : str,
               'description'   : str,
               'access'        : str, #FIXME enum
               'addressOffset' : IpxactInt,
               'size'          : IpxactInt,
               'volatile'      : IpxactBool,
               'width'         : IpxactInt}
    CHILDREN = ['field']

class AddressBlock(IpxactItem):
    MEMBERS = {'name'        : str,
               'description' : str,
               'baseAddress' : IpxactInt,
               'range' : IpxactInt,
               'width' : IpxactInt}

    CHILDREN = ['register']

class MemoryMap(IpxactItem):
    MEMBERS = {'name' : str}

    CHILDREN = ['addressBlock']

class MemoryMaps(IpxactItem):
    CHILDREN = ['memoryMap']

class File(IpxactItem):
    MEMBERS = {'name'          : str,
               'fileType'      : str,
               'isIncludeFile' : IpxactBool}

class FileSet(IpxactItem):
    MEMBERS = {'name' : str}

    CHILDREN = ['file']

class FileSets(IpxactItem):
    CHILDREN = ['fileSet']

class Vector(IpxactItem):
    MEMBERS = {'left'  : IpxactInt,
               'right' : IpxactInt}

class PhysicalPort(IpxactItem):
    MEMBERS = {'name' : str}

    CHILD = ['vector']

class LogicalPort(IpxactItem):
    MEMBERS = {'name' : str}

    CHILD = ['vector']

class PortMap(IpxactItem):
    CHILD = ['logicalPort', 'physicalPort']

class PortMaps(IpxactItem):
    CHILDREN = ['portMap']

class BusType(IpxactItem):
    ATTRIBS = {'vendor'  : str,
               'library' : str,
               'name'    : str,
               'version' : str}

class AbstractionType(IpxactItem):
    ATTRIBS = {'vendor'  : str,
               'library' : str,
               'name'    : str,
               'version' : str}

class BusInterface(IpxactItem):
    MEMBERS = {'name'               : str,
               'master'             : str,
               'mirroredMaster'     : str,
    }

    CHILD = ['abstractionType',
             'busType',
             'portMaps']

    MODELIST = ['master', 'mirroredMaster']

    def parse_tree(self, root, ns):
        super(BusInterface, self).parse_tree(root, ns)
        #Set the mode found in the XML
        for _name in self.MODELIST:
            tmp = root.find('./{}:{}'.format(ns[0], _name), {ns[0] : ns[1]})
            if tmp is not None:
                self.set_mode(_name)

    def set_mode(self, mode):
        #Mark all modes as invalid
        for _name in self.MODELIST:
            setattr(self, _name, None)
        #Set the mode
        setattr(self, mode, "")

class BusInterfaces(IpxactItem):
    CHILDREN = ['busInterface']

class Wire(IpxactItem):
    MEMBERS = {'direction' : str}
    CHILD = ['vector']

class Port(IpxactItem):
    MEMBERS = {'name' : str}
    CHILD = ['wire']
               
class Ports(IpxactItem):
    CHILDREN = ['port']

class Model(IpxactItem):
    CHILD = ['ports']

class Component(IpxactItem):
    MEMBERS = {'vendor'  : str,
               'library' : str,
               'name'    : str,
               'version' : str,
               }
    CHILDREN = ['fileSets', 'memoryMaps']
    CHILD = ['busInterfaces',
             'model',
    ]

class Ipxact:
    nsmap = {'1.4' : ('spirit' , 'http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.4'),
             '1.5' : ('spirit' , 'http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.5')}

    ROOT_TAG = 'component'

    def __init__(self):
        self.component = Component()
        self.version = '1.5'
        
    def load(self, f):
        tree = ET.parse(f)
        root = tree.getroot()
        
        #Warning: Horrible hack to find out which IP-Xact version that is used
        for key, value in root.attrib.items():
            if key == '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation':
                nstags = value.split()
                for version, _val in self.nsmap.items():
                    if _val[1] in nstags:
                        self.version = version

        S = '{%s}' % self.nsmap[self.version][1]
        if not (root.tag == S+self.ROOT_TAG):
            raise Exception

        self.component.parse_tree(root, self.nsmap[self.version])

    def write(self, f):
        ET.register_namespace(self.nsmap[self.version][0], self.nsmap[self.version][1])
        S = '{%s}' % self.nsmap[self.version][1]
        root = ET.Element(S+'component')
        self.component.write(root, S)

        et = ET.ElementTree(root)
        et.write(f, xml_declaration=True, encoding='unicode')
        
