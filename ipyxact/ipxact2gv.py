# Copyright 2019-2022 Olof Kindgren <olof.kindgren@gmail.com>
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import lxml
import os

logging.basicConfig(level=logging.WARNING)

import ipyxact.ipxact2014 as ipxact
from ipyxact.verilogwriter import Instance, ModulePort, Port, VerilogWriter, Wire

class IPXactLibrary(object):
    instances = {}

    ports  = {}
    wires = []
    library = {}
    def __init__(self):
        self.module_ports = {}
        self.imports = []

    def set_top_component(self, vlnv):
        self.top_component = self.library[tuple(vlnv.split(':'))]

    def set_top_view(self, view_name):
        self.view = self.get_view(self.top_component, view_name)
        self.design  = self.get_design(self.top_component, self.view)

    def add_file(self, f):
        try:
            obj = ipxact.parse(f, True)
            vlnv = None
            vlnv = (obj.vendor, obj.library, obj.name, obj.version)
            if isinstance(obj, ipxact.Component):
                self.library[vlnv] = obj
                logging.debug("Adding component from " + f)
            elif isinstance(obj, ipxact.design):
                self.library[vlnv] = obj
                logging.debug("Adding design from " + f)
            elif isinstance(obj, ipxact.designConfiguration):
                self.library[vlnv] = obj
                logging.debug("Adding designConfig from " + f)
            elif isinstance(obj, ipxact.busDefinition):
                self.library[vlnv] = obj
                logging.debug("Adding busDefinition from " + f)
            elif isinstance(obj, ipxact.abstractionDefinition):
                self.library[vlnv] = obj
                logging.debug("Adding abstractionDefinition from " + f)
            else:
                logging.debug("Not adding {}. Unhandled type {}".format(f, obj.__class__.__name__))

        except lxml.etree.XMLSyntaxError as e:
            logging.warning("Failed to parse {} : {}".format(f, e.msg))

    def find(self, x):
        vlnv = (x.vendor, x.library, x.name, x.version)
        try:
            return self.library[vlnv]
        except KeyError:
            raise Exception(f"Could not find '{':'.join(vlnv)}' in library")

    def get_design(self, component, view):
        designInstantiation = self.get_list_entry_by_ref(component.model.instantiations.designInstantiation,
                                                 "name", view.designInstantiationRef)

        return self.find(designInstantiation.designRef)

    def get_ports(self, component):
        module_ports = {}
        for port in component.model.ports.port:
            name = port.name
            left = 0
            right = 0

            if port.wire.Vectors:
                if len(port.wire.Vectors.Vector) > 1:
                    raise NotImplementedError("No clue how to handle multiple vectors")
                left  = port.wire.Vectors.Vector[0].left.parse_uint()
                right = port.wire.Vectors.Vector[0].right.parse_uint()
            _dir = {'in' : 'input', 'out' : 'output', 'inout' : 'inout' , 'phantom': None}[port.wire.direction]
            if _dir:
                if port.wire.wireTypeDefs:
                    #NOTE: No idea how multiple typedefs are supposed to work. Just pick the first one
                    wire_type = port.wire.wireTypeDefs.wireTypeDef[0].typeDefinition[0].valueOf_ + "::"
                    wire_type += port.wire.wireTypeDefs.wireTypeDef[0].typeName.valueOf_
                    if not wire_type in self.imports:
                        self.imports.append(wire_type)
                else:
                    wire_type = None
                    width = left+1-right

                module_ports[name] = ModulePort(name,
                                                dir=_dir,
                                                width=width,
                                                low=right,
                                                asc=(right>left),
                                                _type=wire_type)
        return module_ports

    def get_design_cfg(self, view):
        design_cfg_name = view.designConfigurationInstantiationRef
        for designConfigurationInstantiation in self.top_component.model.instantiations.designConfigurationInstantiation:
            if designConfigurationInstantiation.name == design_cfg_name:
                return self.find(designConfigurationInstantiation.designConfigurationRef)

        raise KeyError("FIXME design_cfg")


    def get_instances(self, view):
        if not self.instances:
            design     = self.get_design(self.top_component, view)
            design_cfg = self.get_design_cfg(view)
            for componentInstance in design.componentInstances.componentInstance:
                instance_name = componentInstance.instanceName
                component = self.find(componentInstance.componentRef)

                #Fixme: Check instance_view_name
                instance_view_name = self.get_list_entry_by_ref(design_cfg.viewConfiguration, "instanceName", instance_name)

                self.instances[instance_name] = self.add_instance(component, instance_view_name, instance_name)

        return self.instances

    #Iterates over list l searching for a tag with value val and return that entry
    def get_list_entry_by_ref(self, l, tag, val):
        for x in l:
            if getattr(x, tag) == val:
                return x
        raise KeyError(f"FIXME: Couldn't find {tag} {val}")

    def get_view(self, component, view_name):
        return self.get_list_entry_by_ref(component.model.views.view, "name", view_name)

    #Map ports to buses
    def get_ports_and_buses(self, component):
        bus_ports = []
        buses = []
        ports = []
        if component.BusInterfaces:
            for busInterface in component.BusInterfaces.BusInterface:
                bus_name = busInterface.name
                lib_ref = busInterface.busType
                bus_type = f"{lib_ref.vendor}:{lib_ref.library}:{lib_ref.name}:{lib_ref.version}"
                buses.append((bus_name, bus_type))
                for abstractionType in busInterface.AbstractionTypes.abstractionType:
                    for portMap in abstractionType.portMaps.portMap:
                        bus_ports.append(portMap.physicalPort.name)
                    #How does multiple abstraction types work?

        for name, comp_port in self.get_ports(component).items():
            if not comp_port.name in bus_ports:
                ports.append((comp_port.name, comp_port.dir))
            #port._type = comp_port._type
        return (buses, bus_ports, ports)

    def add_instance(self, component, instance_view_name, instance_name):

        #instantiation = self.get_component_instantiation(component, instance_view_name)
        #module_name = instantiation.moduleName
        module_name = "fixme"

        (buses, bus_ports, ports) = self.get_ports_and_buses(component)
        instance = {"type" : module_name,
                    "name" : instance_name,
                    "buses" : buses,
                    "bus_ports" : bus_ports,
                    "ports" : ports}

        return instance

    def connect(self):
        f = open("out.gv", "w")
        f.write("digraph G {\n")
        f.write("graph [rankdir = LR];\n")
        f.write("node[shape=record, style=filled];\n")

        #(buses, bus_ports, ports)
        self.module_ports = self.get_ports_and_buses(self.top_component)
        for bus in self.module_ports[0]:
            f.write(f"{bus[0]}[shape=diamond];\n")

        for port in self.module_ports[2]:
            f.write(f"{port[0]}[shape=cds];\n")
        self.instances = self.get_instances(self.view)

        for name, v in self.instances.items():
            f.write(f'{v["name"]}[label="')
            f.write("| ".join([f"<{x[0]}> {x[0]}" for x in v["ports"]+v["buses"]]))
            f.write('"];\n')

        if self.design.adHocConnections:
            for adHocConnection in self.design.adHocConnections.adHocConnection:
                name = adHocConnection.name
                source = ""
                targets = []
                for pr in adHocConnection.portReferences.internalPortReference:
                    for port in self.instances[pr.componentRef]["ports"]:
                        if pr.portRef == port[0]:
                            if port[1] == "input":
                                targets.append(pr.componentRef+":"+pr.portRef)
                            elif port[1] == "output":
                                if source:
                                    print("Already got source")
                                    exit(1)
                                source = pr.componentRef+":"+pr.portRef
                            else:
                                print("Unknown direction " + port[1])
                                exit(1)

                            #wire.endpoints.append(port)

                for pr in adHocConnection.portReferences.externalPortReference:
                    for ext_port in self.module_ports[2]:
                        if ext_port[0] == pr.portRef:
                            direction = ext_port[1]
                    #ep = self.instances.module_ports[pr.portRef]
                    if direction == "output":
                        targets.append(pr.portRef+":w")
                    elif direction == "input":
                        if source:
                            print("Already got source")
                            exit(1)
                        source = pr.portRef+":e"
                    else:
                        print("Unknown direction " + direction)
                        exit(1)
                for t in targets:
                    f.write(f"{source} -> {t};\n")


        if self.design.interconnections:
            for interconnection in self.design.interconnections.interconnection:
                #FIXME: Only handle point-to-point buses for now
                #FIXME: Do something sensible with directions or mark masters and slaves
                point1 = ""
                point2 = ""
                name = interconnection.name
                for activeInterface in interconnection.activeInterface:
                    if point2:
                        print("Can't handle interconnections with >2 endpoints yet")
                        exit(1)
                    if point1:
                        point2 = activeInterface.componentRef+":"+activeInterface.busRef
                    else:
                        point1 = activeInterface.componentRef+":"+activeInterface.busRef
        
                for hierInterface in interconnection.hierInterface:
                    #FIXME: All external bus connections will end up on the left side for now
                    if point2:
                        print("Can't handle interconnections with >2 endpoints yet")
                        exit(1)
                    if point1:
                        point2 = hierInterface.busRef #+":e"
                    else:
                        point1 = hierInterface.busRef #+":e"
                    f.write(f"{point1} -> {point2};\n")
                

        f.write("}\n")
        f.close()


def parse_args():
    parser = argparse.ArgumentParser(
            description='Generate structural verilog from an IP-XACT file')
    parser.add_argument('vlnv', help='VLNV of toplevel')
    parser.add_argument('view', help='View of toplevel')
    parser.add_argument('-d', action='append', help='Directory containing IP-XACT files to be loaded')
    parser.add_argument('-m', dest='module_name', help='Output module name')
    parser.add_argument('-o', dest='output_file', help='Write output to file')
    parser.add_argument('files', nargs='*', help='IP-XACT files to load')
    return parser.parse_args();

def main():
    args = parse_args()

    i = IPXactLibrary()
    for _dir in args.d or []:
        for f in os.listdir(_dir):
            if f.endswith('.xml'):
                i.add_file(os.path.join(_dir, f))
    for f in args.files:
        i.add_file(f)
    i.set_top_component(args.vlnv)
    view_name = args.view
    i.set_top_view(view_name)
    i.connect()

    module_name = args.module_name or i.top_component.name

if __name__ == '__main__':
    main()
