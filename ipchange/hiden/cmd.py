import argparse
import os
import sys
import ipaddress
import ipchange.hiden

sys.tracebacklimit = 0


def hiden_change_ip():
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description='Change IP Addresses of Hiden RGA'
    )

    parser.add_argument(
        'Old IP Address',
        metavar='old_address', type=ipaddress.ip_address,
        help='Old IP Address'
    )

    parser.add_argument(
        'New IP Address',
        metavar='new_address', type=ipaddress.ip_address,
        help='New IP Address'
    )

    args = vars(parser.parse_args())

    ipchange.hiden.hiden_change_ip(str(args['Old IP Address']),
                                   str(args['New IP Address']))

    return 0


