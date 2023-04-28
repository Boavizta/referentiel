import os
from pathlib import Path
import yaml
from boaviztapi import data_dir
from boaviztapi.model.component import *
from boaviztapi.model.device.userTerminal import *
from boaviztapi.model.impact import IMPACT_CRITERIAS

config_file = os.path.join(data_dir, 'factors.yml')
impact_factors = yaml.safe_load(Path(config_file).read_text())

Components = [ComponentAssembly, ComponentCase,  ComponentCPU, ComponentHDD, ComponentMotherboard, ComponentPowerSupply, ComponentRAM, ComponentSSD]
EndUserDevice = [DeviceDesktop, DeviceLaptop, DeviceSmartphone, DeviceTablet, DeviceTelevision, DeviceMonitor, DeviceBox, DeviceBox, DeviceUsbStick,DeviceExternalSSD, DeviceExternalHDD]

def impact_criteria():
    s = ""
    for i in IMPACT_CRITERIAS:
        s += f"\n{i.name}:\n  unit: {i.unit} \n  description: {i.description}\n  method: {i.method}"
    return s

def electricity():
    elec = impact_factors["electricity"]
    return yaml.dump(elec)

def end_user_device():
    for d in EndUserDevice:
        s = ""
        id = d()
        s+=f"name: {d.NAME}\ntype: device\nunit: 1\n\n"+"\nimpact_factor:\n  elec : electricity.yml\n  embedded:\n  "+yaml.dump(impact_factors[d.NAME])
        s+=f"\nconstants:\n  default_power: \n    value: {id.usage.hours_electrical_consumption.value}\n    unit: W"
        if impact_factors[d.NAME].get("pro"):
            s+="\n\nattributes:\n  duration:\n    unit: hours\n  average_power:\n     unit: W\n\nmethods:\n  elec:\n    1 : average_power*duration\n    2 : default_consumption*duration\n  embedded :\n    pro: impact_factors.embedded.pro\n    perso : impact_factors.embedded.perso\n  usage : elec*impact_factor.elec"
        else:
            s+="\n\nattributes:\n  duration:\n    unit: hours\n  average_power:\n    unit: W\n\nmethods:\n  elec:\n    1 : average_power*duration\n    2 : default_consumption*duration\n  embedded :\n    impact_factors.embedded.perso\n  usage : elec*impact_factor.elec"
        f = open(f"{d.NAME.lower()}.yml", "w")
        f.write(s)
        f.close()