import dbus
import dbus.service
import time
import logging

import gatt_base.gatt_lib_exceptions as gatt_except
import gatt_base.gatt_lib_variables as gatt_var


class Characteristic(dbus.service.Object):
    """
    org.bluez.GattCharacteristic1 interface implementation
    """

    def __init__(self, bus, index, uuid, flags, service):
        self.path = service.path + '/char' + str(index)
        self.bus = bus
        self.uuid = uuid
        self.service = service
        self.flags = flags
        self.descriptors = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
            gatt_var.GATT_CHRC_IFACE: {
                'Service': self.service.get_path(),
                'UUID': self.uuid,
                'Flags': self.flags,
                'Descriptors': dbus.Array(
                    self.get_descriptor_paths(),
                    signature='o')
            }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_descriptor(self, descriptor):
        self.descriptors.append(descriptor)

    def get_descriptor_paths(self):
        result = []
        for desc in self.descriptors:
            result.append(desc.get_path())
        return result

    def get_descriptors(self):
        return self.descriptors

    @dbus.service.method(gatt_var.DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != gatt_var.GATT_CHRC_IFACE:
            raise gatt_except.InvalidArgsException()

        return self.get_properties()[gatt_var.GATT_CHRC_IFACE]

    @dbus.service.method(gatt_var.GATT_CHRC_IFACE,
                         in_signature='a{sv}',
                         out_signature='ay')
    def ReadValue(self, options):
        logger = logging.getLogger("rotating.logger")
        logger.debug('[%s] Default ReadValue called, returning error', time.strftime('%d/%m %H:%M:%S'))
        raise gatt_except.NotSupportedException()

    @dbus.service.method(gatt_var.GATT_CHRC_IFACE, in_signature='aya{sv}')
    def WriteValue(self, value, options):
        logger = logging.getLogger("rotating.logger")
        logger.debug('[%s] Default WriteValue called, returning error', time.strftime('%d/%m %H:%M:%S'))
        raise gatt_except.NotSupportedException()

    @dbus.service.method(gatt_var.GATT_CHRC_IFACE)
    def StartNotify(self):
        logger = logging.getLogger("rotating.logger")
        logger.debug('[%s] Default StartNotify called, returning error', time.strftime('%d/%m %H:%M:%S'))
        raise gatt_except.NotSupportedException()

    @dbus.service.method(gatt_var.GATT_CHRC_IFACE)
    def StopNotify(self):
        logger = logging.getLogger("rotating.logger")
        logger.debug('[%s] Default StopNotify called, returning error', time.strftime('%d/%m %H:%M:%S'))
        raise gatt_except.NotSupportedException()

    @dbus.service.signal(gatt_var.DBUS_PROP_IFACE,
                         signature='sa{sv}as')
    def PropertiesChanged(self, interface, changed, invalidated):
        pass
