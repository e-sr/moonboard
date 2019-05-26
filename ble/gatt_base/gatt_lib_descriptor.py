import dbus
import dbus.service
import time
import logging

import gatt_base.gatt_lib_exceptions as gatt_except
import gatt_base.gatt_lib_variables as gatt_var


class Descriptor(dbus.service.Object):
    """
    org.bluez.GattDescriptor1 interface implementation
    """

    def __init__(self, bus, index, uuid, flags, characteristic):
        self.path = characteristic.path + '/desc' + str(index)
        self.bus = bus
        self.uuid = uuid
        self.flags = flags
        self.chrc = characteristic
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
            gatt_var.GATT_DESC_IFACE: {
                'Characteristic': self.chrc.get_path(),
                'UUID': self.uuid,
                'Flags': self.flags,
            }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method(gatt_var.DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != gatt_var.GATT_DESC_IFACE:
            raise gatt_except.InvalidArgsException()

        return self.get_properties()[gatt_var.GATT_DESC_IFACE]

    @dbus.service.method(gatt_var.GATT_DESC_IFACE,
                         in_signature='a{sv}',
                         out_signature='ay')
    def ReadValue(self, options):
        logger = logging.getLogger("rotating.logger")
        logger.debug('[%s] Default ReadValue called, returning error', time.strftime('%d/%m %H:%M:%S'))
        raise gatt_except.NotSupportedException()

    @dbus.service.method(gatt_var.GATT_DESC_IFACE, in_signature='aya{sv}')
    def WriteValue(self, value, options):
        logger = logging.getLogger("rotating.logger")
        logger.debug('[%s] Default WriteValue called, returning error', time.strftime('%d/%m %H:%M:%S'))
        raise gatt_except.NotSupportedException()
