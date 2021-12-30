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
    access: str
    usage: str
  CHILDREN:
    - register
    - registerFile
access:
  MEMBERS:
    portAccessType: str
    accessHandles: str
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
    - parameters
componentInstantiation:
  MEMBERS:
    name: str
    moduleName: str
constraintSet:
  ATTRIBS:
    constraintSetId: str
  MEMBERS:
    timingConstraint: IpxactFloat
  CHILD:
    - vector
    - driveConstraint
    - loadConstraint
    - timingConstraint
constraintSets:
  CHILDREN:
    - constraintSet
driver:
  MEMBERS:
    defaultValue: str
    clockDriver: str
    singleShotDriver: str
drivers:
  CHILDREN:
    - driver
enumeratedValue:
  MEMBERS:
    name: str
    description: str
    displayName: str
    value: str
enumeratedValues:
  CHILDREN:
    - enumeratedValue
reset:
  MEMBERS:
    value: IpxactInt
    mask: IpxactInt
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
instantiations:
  CHILDREN:
    - componentInstantiation
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
    addressUnitBits: IpxactInt
  CHILDREN:
    - addressBlock
memoryMaps:
  CHILDREN:
    - memoryMap
model:
  CHILD:
    - views
    - ports
    - instantiations
parameters:
  CHILDREN:
    - parameter
parameter:
  ATTRIBS:
    parameterId: str
  MEMBERS:
    name: str
    value: str
    displayName: str
physicalPort:
  MEMBERS:
    name: str
  CHILD:
    - vector
port:
  MEMBERS:
    name: str
    description: str
  CHILD:
    - wire
    - access
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
    dim: IpxactInt
    access: str
    addressOffset: IpxactInt
    size: IpxactInt
    volatile: IpxactBool
    isPresent: str
  CHILDREN:
    - field
  CHILD:
    - alternateRegisters
    - reset
registerFile:
  MEMBERS:
    name: str
    description: str
    dim: IpxactInt
    addressOffset: IpxactInt
    range: IpxactInt
  CHILDREN:
    - register
timingConstraint:
  ATTRIBS:
    clockEdge: str
    clockName: str
    delayType: str
vectors:
  CHILDREN:
    - vector
vector:
  MEMBERS:
    left:  IpxactInt
    right: IpxactInt
view:
  MEMBERS:
    name: str
    envIdentifier: str
    componentInstantiationRef: str
views:
  CHILDREN:
    - view
wire:
  MEMBERS:
    direction: str
    allLogicalDirectionsAllowed: IpxactBool
  CHILD:
    - constraintSets
    - vectors
    - drivers
"""
