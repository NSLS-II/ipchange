import socket
import re


def socket_get(s, cmd, reply=True):
    _cmd = cmd + "\r\n"
    bcmd = _cmd.encode('ascii')
    s.sendall(bcmd)
    if reply:
        data = s.recv(1024)
        return data.decode('ascii').rstrip()
    else:
        return None


def hiden_change_ip(old_addr, new_addr):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((old_addr, 5025))

        hid = socket_get(s, "pget ID").strip()
        print("ID      = {}".format(hid))
        if hid is None or hid == "":
            print("WARN... ID is empty!?  Often happens if the softioc is still running, ensure it's stopped")
        elif hid == '1':
            print("WARN... ID is '1'!?  Should be like 'HAL RC RGA 101 #14768'")
            print('        If new IP does not take, maybe power cycle the device and try again?')

        hip = socket_get(s, "pget IP-address").strip()
        print("IP Addr = {}".format(hip))
        # note returned IP is ',' (comma) separated, NOT '.' (period) separated!
        if not re.match(r'^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(,(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}$', hip):
            print("WARN... IP is '{}'!?  Is the softioc running?  Ensure it's stopped.".format(hip))
            print('        If new IP does not take, maybe power cycle the device and try again?')

        if new_addr is not None:
            _addr = [int(a) for a in new_addr.split(".")]
            cmd = "pset assigned-IP {:03} {:03} {:03} {:03}".format(*_addr)
            print("Set     = {}".format(cmd))
            socket_get(s, cmd)
            print("Set     = save")
            socket_get(s, "save")
            print("Set     = boot mon")
            socket_get(s, "boot mon", False)

