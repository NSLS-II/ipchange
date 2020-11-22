import socket


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
        print("ID      = {}".format(socket_get(s, "pget ID")))
        print("IP Addr = {}".format(socket_get(s, "pget IP-address")))

        if new_addr is not None:
            _addr = [int(a) for a in new_addr.split(".")]
            cmd = "pset assigned-IP {:03} {:03} {:03} {:03}".format(*_addr)
            print("Set     = {}".format(cmd))
            socket_get(s, cmd)
            print("Set     = save")
            socket_get(s, "save")
            print("Set     = boot mon")
            socket_get(s, "boot mon", False)

