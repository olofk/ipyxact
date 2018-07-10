description = """
---
abstractionType:
  ATTRIBS:
    vendor:  str
    library: str
    name:    str
    version: str
addressBlock:
  MEMBERS:
    name: str
    displayName: str
    description: str
    baseAddress: IpxactInt
    range: IpxactInt
    width: IpxactInt
    usage: str
  CHILDREN:
    - register
alternateRegister:
  MEMBERS:
    name: str
    description: str
    access: str
    addressOffset: IpxactInt
    size: IpxactInt
    volatile: IpxactBool
  CHILDREN:
    - field
alternateRegisters:
  CHILDREN:
    - alternateRegister
busInterface:
  MEMBERS:
    name:           str
    master:         str
    mirroredMaster: str
    slave:          str
  CHILD:
    - abstractionType
    - busType
    - portMaps
busInterfaces:
  CHILDREN:
    - busInterface
busType:
  ATTRIBS:
    vendor:  str
    library: str
    name:    str
    version: str
component:
  MEMBERS:
    description: str
    vendor:  str
    library: str
    name:    str
    version: str
  CHILD:
    - busInterfaces
    - fileSets
    - memoryMaps
    - model
enumeratedValue:
  MEMBERS:
    name: str
    description: str
    value: IpxactInt
enumeratedValues:
  CHILDREN:
    - enumeratedValue
reset:
  MEMBERS:
    value: IpxactInt
resets:
  CHILD:
    - reset
field:
  MEMBERS:
    name: str
    description: str
    bitOffset: IpxactInt
    bitWidth: IpxactInt
    modifiedWriteValue: str
    readAction: str
    testable: str
    volatile: IpxactBool
    access: str
  CHILD:
    - resets
  CHILDREN:
    - enumeratedValues
file:
  MEMBERS:
    name: str
    fileType: str
    isIncludeFile: IpxactBool
    logicalName: str
fileSet:
  MEMBERS:
    name: str
  CHILDREN:
    - file
fileSets:
  CHILDREN:
    - fileSet
logicalPort:
  MEMBERS:
    name: str
  CHILD:
    - vector
memoryMap:
  MEMBERS:
    name: str
    displayName: str
    description: str
  CHILDREN:
    - addressBlock
memoryMaps:
  CHILDREN:
    - memoryMap
model:
  CHILD:
    - ports
physicalPort:
  MEMBERS:
    name: str
  CHILD:
    - vector
port:
  MEMBERS:
    name: str
  CHILD:
    - wire
ports:
  CHILDREN:
    - port
portMap:
  CHILD:
    - logicalPort
    - physicalPort
portMaps:
  CHILDREN:
    - portMap
register:
  MEMBERS:
    name: str
    description: str
    access: str
    addressOffset: IpxactInt
    size: IpxactInt
    volatile: IpxactBool
  CHILDREN:
    - field
  CHILD:
    - alternateRegisters
    - reset
vector:
  MEMBERS:
    left:  IpxactInt
    right: IpxactInt
wire:
  MEMBERS:
    direction: str
  CHILD:
    - vector
"""
