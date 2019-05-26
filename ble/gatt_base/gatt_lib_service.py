import dbus
import dbus.service

import gatt_base.gatt_lib_exceptions as gatt_except
import gatt_base.gatt_lib_variables as gatt_var

class Service(dbus.service.Object):
    """
    org.bluez.GattService1 interface implementation
    """
    def __init__(self, bus, path, index, uuid, primary):
        self.path = path +'/service'+ str(index)
        self.bus = bus
        self.uuid = uuid
        self.primary = primary
        self.characteristics = []
        dbus.service.Object.__init__(self, self.bus, self.path)

    def get_properties(self):
        return {
            gatt_var.GATT_SERVICE_IFACE: {
                'UUID': self.uuid,
                'Primary': self.primary,
                'Characteristics': dbus.Array(
                    self.get_characteristic_paths(),
                    signature='o')
            }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_characteristic(self, characteristic):
        self.characteristics.append(characteristic)

    def get_characteristic_paths(self):
        result = []
        for chrc in self.characteristics:
            result.append(chrc.get_path())
        return result

    def get_characteristics(self):
        return self.characteristics

    @dbus.service.method(gatt_var.DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != gatt_var.GATT_SERVICE_IFACE:
            raise gatt_except.InvalidArgsException()

        return self.get_properties()[gatt_var.GATT_SERVICE_IFACE]
