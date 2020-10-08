import argparse
import os
import sys
import ipaddress
import ipchange.moxa


def axis_changeip():

    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description='Change IP Addresses of AXIS Webcam'
    )

    parser.add_argument(
        'AXIS Webcam address/hostname',
        metavar='host', type=str,
        help='Address or Hostname of the AXIS Webcam to change'
    )

    parser.add_argument(
        'New IP Address',
        metavar='address', type=ipaddress.ip_address,
        help='New IP Address'
    )

    parser.add_argument(
        'New Netmask',
        metavar='netmask', type=ipaddress.ip_address,
        help='New Netmask'
    )

    parser.add_argument(
        'New Gateway',
        metavar='gateway', type=ipaddress.ip_address,
        help='New Gateway'
    )

    parser.add_argument(
        '-u', '--username', dest='username', action='store',
        help='Username of the AXIS Webcam to connect to'
    )

    parser.add_argument(
        '-p', '--password', dest='password', action='store',
        help='Password of the AXIS Webcam to connect to'
    )

    args = vars(parser.parse_args())

    # Now run the set routine

    axis = ipchange.axis.AxisWebcam(
        args['AXIS Webcam address/hostname']
    )

    axis.set_ipaddr(
        str(args['New IP Address']),
        str(args['New Netmask']),
        str(args['New Gateway'])
    )

    return 0