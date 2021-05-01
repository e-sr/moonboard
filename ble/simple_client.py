from gi.repository import GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop


def handle_notification(s):
    print('New Problem: '+s)


if __name__ == '__main__':

    dbml = DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    proxy = bus.get_object('com.moonboard','/com/moonboard')

    proxy.connect_to_signal('new_problem', handle_notification)
    loop = GLib.MainLoop()

    dbus.set_default_main_loop(dbml)

    # Run the loop
    try:
        loop.run()
    except KeyboardInterrupt:
        print("keyboard interrupt received")
    except Exception as e:
        print("Unexpected exception occurred: '{}'".format(str(e)))
    finally:
        loop.quit()