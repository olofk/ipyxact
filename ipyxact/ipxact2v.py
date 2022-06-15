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
        self.top_view_name = view_name

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

    def get_component_instantiation(self, component, view_name):
        view = self.get_view(component, view_name)
        comp_inst_ref = view.componentInstantiationRef

        for componentInstantiation in component.model.instantiations.componentInstantiation:
            if componentInstantiation.name == comp_inst_ref:
                return componentInstantiation
        raise KeyError("FIXME: Couldn't find componentInstantiation "+comp_inst_ref)

    def get_design(self, view):
        for designInstantiation in self.top_component.model.instantiations.designInstantiation:
            if designInstantiation.name == view.designInstantiationRef:
                return self.find(designInstantiation.designRef)
        raise KeyError("FIXME: Couldn't find designRef")

    def get_external_ports(self):
        return self.get_ports(self.top_component)

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
            design     = self.get_design(view)
            design_cfg = self.get_design_cfg(view)
            for componentInstance in design.componentInstances.componentInstance:
                instance_name = componentInstance.instanceName
                component = self.find(componentInstance.componentRef)

                #Fixme: Check instance_view_name
                for viewConfiguration in design_cfg.viewConfiguration:
                    if viewConfiguration.instanceName == instance_name:
                        instance_view_name = viewConfiguration.view.viewRef

                self.instances[instance_name] = self.add_instance(component, instance_view_name, instance_name)

        return self.instances

    def get_view(self, component, view_name):
        for view in component.model.views.view:
            if view.name == view_name:
                return view
        raise KeyError("FIXME: Couldn't find view "+view_name)

    def add_instance(self, component, instance_view_name, instance_name):

        instantiation = self.get_component_instantiation(component, instance_view_name)
        module_name = instantiation.moduleName
        ports = []
        for name, comp_port in self.get_ports(component).items():
            port = Port(comp_port.name)
            port.direction = comp_port.dir
            port.width = comp_port.width
            port._type = comp_port._type
            ports.append(port)

        instance = Instance(module_name, instance_name, [], ports)
        return instance

    def get_component_ref_from_instance_name(self, design, instance_name):
        for componentInstance in design.componentInstances.componentInstance:
            if componentInstance.instanceName == instance_name:
                return componentInstance
        raise KeyError(f"Could not find instance {instance_name!r} in design '{design.vendor}:{design.library}:{design.name}:{design.version}'")

    def get_top_bus_interface(self, bus_name):
        return self.get_bus_interface(self.top_component, bus_name)

    def get_instance_bus_interface(self, design, instance_name, bus_name):
        component_instance = self.get_component_ref_from_instance_name(design, instance_name)
        component_ref = component_instance.componentRef
        component = self.find(component_ref)
        return self.get_bus_interface(component, bus_name)

    def get_bus_interface(self, component, bus_name):
        for busInterface in component.BusInterfaces.BusInterface:
            if busInterface.name == bus_name:
                return busInterface
        raise KeyError("No bus today " + bus_name)

    def get_abstraction_type(self, busInterface, view_name):
        for abstractionType in busInterface.AbstractionTypes.abstractionType:
            if not abstractionType.viewRef or view_name in [x.valueOf_ for x in abstractionType.viewRef]:
                return abstractionType
        raise KeyError("Fail")

    def find_wire_width_in_abs_def(self, abs_def, wire_name, bus_mode):
        for port in abs_def.ports.port:
            if port.logicalName == wire_name:
                mode_info = getattr(port.wire, bus_mode)
                if mode_info.width:
                    return mode_info.width.parse_uint()
                else:
                    return 0
        raise Exception("No bus mode for " + wire_name)

    def add_interconnection(self, design, interconnection):
        ic_name = interconnection.name

        logical_ports = {}

        def _add_logical_ports(instance_name, busInterface, logical_ports):
            if hasattr(busInterface, "master"):
                bus_mode = 'onMaster'
            elif hasattr(busInterface, "slave"):
                bus_mode = 'onSlave'
            else:
                raise Exception("bus mode not handled")
            abstractionType = self.get_abstraction_type(busInterface, "rtl") #FIXME: How??
            abs_def = self.find(abstractionType.abstractionRef)
            for portMap in abstractionType.portMaps.portMap:
                log_port = portMap.logicalPort
                log_name = log_port.name
                if not log_name in logical_ports:
                    #Sanity check that logical port width is equal on all (both?) sides?
                    left  = -1
                    right = 0
                    port_width = 0
                    if hasattr(log_port, 'Range') and log_port.Range:
                        left  = log_port.Range.left.parse_uint()
                        right = log_port.Range.right.parse_uint()
                    port_width = left+1-right
                    wire_width = self.find_wire_width_in_abs_def(abs_def, log_name, bus_mode)
                    logical_ports[log_name] = {'endpoints' : [],
                                               'wire_width' : wire_width,
                                               'port_width' : port_width}
                logical_ports[log_name]['endpoints'].append((instance_name, portMap.physicalPort.name))

        for activeInterface in interconnection.activeInterface:
            instance_name = activeInterface.componentRef
            bus_name      = activeInterface.busRef
            busInterface = self.get_instance_bus_interface(design, instance_name, bus_name)
            _add_logical_ports(instance_name, busInterface, logical_ports)

        for hierInterface in interconnection.hierInterface:
            instance_name = None #No support for fancy hierarchies. Assume current toplevel
            bus_name      = hierInterface.busRef
            busInterface  = self.get_top_bus_interface(bus_name)
            _add_logical_ports(instance_name, busInterface, logical_ports)

        for k, log_port in logical_ports.items():
            port_width = log_port['port_width']
            wire_width = log_port['wire_width']
            endpoints = log_port['endpoints']
            if len(endpoints) > 1:
                wire = Wire(ic_name+'_'+k)
                wire.width = wire_width
                wire.endpoints = []
                for endpoint in log_port['endpoints']:
                    if endpoint[0]:
                        inst = self.instances[endpoint[0]]
                        for port in inst.ports:
                            if endpoint[1] == port.name:
                                wire.endpoints.append(port)
                    else:
                        wire.endpoints.append(self.module_ports[endpoint[1]])
                self.wires.append(wire)

    def add_adhoc_connection(self, adHocConnection):
        wire = Wire(adHocConnection.name)
        wire.endpoints = []

        for pr in adHocConnection.portReferences.internalPortReference:
            for port in self.instances[pr.componentRef].ports:
                if pr.portRef == port.name:
                    wire.endpoints.append(port)

        for pr in adHocConnection.portReferences.externalPortReference:
            wire.endpoints.append(self.module_ports[pr.portRef])
        self.wires.append(wire)

    def infer_width_from_ports(self, wire):
        for endpoint in wire.endpoints:
            width = endpoint.width

            if wire.width and width != wire.width:
                raise Exception(f"Width mismatch for {wire.name}. Wire width is {wire.width}. Port {endpoint.name}.{endpoint[1]} width is {width}")
            wire.width  = width

    def infer_type_from_ports(self, wire):
        for endpoint in wire.endpoints:
            _type = endpoint._type

            if wire._type and _type != wire._type:
                raise Exception(f"_Type mismatch for {wire.name}. Wire _type is {wire._type}. Port {endpoint[0]}.{endpoint[1]} _type is {_type}")
            wire._type  = _type

    def connect(self):
        view_name = self.top_view_name
        component = self.top_component

        view = self.get_view(self.top_component, view_name)

        design  = self.get_design(view)

        self.module_ports = self.get_external_ports() #FIXME: 1-bit vectors
        self.instances = self.get_instances(view)

        if design.adHocConnections:
            for adHocConnection in design.adHocConnections.adHocConnection:
                self.add_adhoc_connection(adHocConnection)

        if design.interconnections:
            for interconnection in design.interconnections.interconnection:
                self.add_interconnection(design, interconnection)

        def merge_wires(wires):
            alpha_wire = wires[0]
            for beta_wire in wires[1:]:
                while beta_wire.endpoints:
                    endpoint = beta_wire.endpoints.pop()
                    for i in range(len(self.ports[endpoint].wires)):
                        if self.ports[endpoint].wires[i] == beta_wire:
                            self.ports[endpoint].wires[i] = alpha_wire
                    if not endpoint in alpha_wire.endpoints:
                        alpha_wire.endpoints.append(endpoint)
            return alpha_wire

        #If a port is connected to multiple wires, merge these wires
        for port in self.ports:
            wires = self.ports[port].wires
            if len(wires)>1:
                self.ports[port].wires = [merge_wires(wires)]

        #Remove all wires that are now unconnected
        self.wires[:] = [wire for wire in self.wires if len(wire.endpoints)>1]

        #Fix wire names connected to external ports
        for w in self.wires:
            for e in w.endpoints:
                if type(e) == ModulePort:
                    w.external = True
                    w.name = e.name

        #Negotiate wire widths and types
        for w in self.wires:
            if not w.width:
                self.infer_width_from_ports(w)
            if not w._type:
                self.infer_type_from_ports(w)
            min_width = 1000000# FIXME
            for endpoint in w.endpoints:
                min_width = min(min_width, endpoint.width)
            if min_width == 1000000:
                raise Exception("No way this is happening")
            if min_width:
                w.width = min_width

        #Connect instance ports to wires
        for w in self.wires:
            for ep in w.endpoints:
                ep.value = w.name

    def write(self, view_name, module_name, output_file):
        vw = VerilogWriter(module_name) #FIXME
        vw.header = "//design2v did this\n"
        for module_port in self.module_ports.values():
            vw.add(module_port)
        for wire in self.wires:
            if not hasattr(wire, 'external'):
                vw.add(wire)
        for instance in self.instances.values():
            vw.add(instance)
        for _import in self.imports:
            vw.header += f'import {_import};\n'
        vw.write(output_file)

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

    i.write(view_name, module_name, args.output_file)

if __name__ == '__main__':
    main()
