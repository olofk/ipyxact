import sys
import ipyxact.ipyxact as ipyxact

class Signal(object):
    def __init__(self, name, width=0, low=0, asc=False):
        self.name = name
        self.width=width
        self.low = low
        self.asc = asc

class Vector(ipyxact.Vector):
    def __init__(self, width=0, low=0, asc=False):
        if asc:
            self.left  = low
            self.right = low+width-1
        else:
            self.left  = low+width-1
            self.right = low
        
class Port(ipyxact.Port):
    def __init__(self, name, direction, width=0, low=0, asc=False):
        self.name = name
        self.wire = ipyxact.Wire()
        self.wire.direction = direction
        if width > 0:
            self.wire.vector = Vector(width, low, asc)

class WBBusInterface(ipyxact.BusInterface):
    def __init__(self, name, mode):
        super(WBBusInterface, self).__init__()
        self.name = name

        if mode == 'master':
            self.master = ''
            self.mdir = 'o'
            self.sdir = 'i'
        else:
            self.slave = ''
            self.mdir = 'i'
            self.sdir = 'o'

        abstractionType = ipyxact.AbstractionType()
        abstractionType.vendor  = "org.opencores"
        abstractionType.library = "wishbone"
        abstractionType.name    = "wishbone.absDef"
        abstractionType.version = "b3"
        self.abstractionType = abstractionType

        busType = ipyxact.BusType()
        busType.vendor  = "org.opencores"
        busType.library = "wishbone"
        busType.name    = "wishbone"
        busType.version = "b3"
        self.busType = busType

        self.portMaps = ipyxact.PortMaps()
    def connect(self, prefix):
        for p in WB_MASTER_PORTS:
            portMap = ipyxact.PortMap()

            physicalPort = ipyxact.PhysicalPort()
            physicalPort.name = "{}_{}_i".format(prefix, p.name)
            if p.width > 0:
                physicalPort.vector = Vector(p.width)
            portMap.physicalPort = physicalPort

            logicalPort = ipyxact.LogicalPort()
            logicalPort.name = "{}_o".format(p.name)
            if p.width > 0:
                logicalPort.vector = Vector(p.width)
            portMap.logicalPort = logicalPort

            busif.portMaps.portMap.append(portMap)

        for p in WB_SLAVE_PORTS:
            portMap = ipyxact.PortMap()

            physicalPort = ipyxact.PhysicalPort()
            physicalPort.name = "{}_{}_o".format(prefix, p.name)
            if p.width > 0:
                physicalPort.vector = Vector(p.width)
            portMap.physicalPort = physicalPort

            logicalPort = ipyxact.LogicalPort()
            logicalPort.name = "{}_i".format(p.name)
            if p.width > 0:
                logicalPort.vector = Vector(p.width)
            portMap.logicalPort = logicalPort

            busif.portMaps.portMap.append(portMap)

WB_MASTER_PORTS = [Signal('adr', 32),
                   Signal('dat', 32),
                   Signal('sel',  4),
                   Signal('we'),
                   Signal('cyc'),
                   Signal('stb'),
                   Signal('cti',  3),
                   Signal('bte',  2)]

WB_SLAVE_PORTS  = [Signal('dat', 32),
                   Signal('ack'),
                   Signal('err'),
                   Signal('rty')]


component = ipyxact.Component()
component.version = '1.5'

component.vendor  = 'opencores'
component.library = 'ip'
component.name    = 'autointercon'
component.version = '0'

component.model = ipyxact.Model()

ports = ipyxact.Ports()

clk = Port('wb_clk_i', 'in')
rst = Port('wb_rst_i', 'in')

ports.port.append(clk)
ports.port.append(rst)

for p in WB_MASTER_PORTS:
    mp = Port('wbs_ram_{}_i'.format(p.name), 'in', p.width)
    ports.port.append(mp)

for p in WB_SLAVE_PORTS:
    mp = Port('wbs_ram_{}_o'.format(p.name), 'out', p.width)
    ports.port.append(mp)

component.model.ports = ports

component.busInterfaces = ipyxact.BusInterfaces()
busif = WBBusInterface("wb", "mirroredMaster")
busif.connect("wbs_ram")

component.busInterfaces.busInterface.append(busif)
component.write(sys.argv[1])
