import argparse
import os
import sys
import ipaddress
import ipchange.moxa

sys.tracebacklimit = 0


def moxa_base_argparser(description):
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description=description
    )

    parser.add_argument(
        'MOXA address/hostname',
        metavar='host', type=str,
        help='Address or Hostname of the MOXA to change'
    )

    parser.add_argument(
        '-u', '--username', dest='username', action='store',
        help='Username of the MOXA to connect to',
        default=None
    )

    parser.add_argument(
        '-p', '--password', dest='password', action='store',
        help='Password of the MOXA to connect to',
        default=None
    )

    parser.add_argument(
        '-c', '--cookie-file', dest='cookie_file', action='store',
        help='File to store cookie for session information',
        default=None
    )

    return parser


def moxa_change_ip():
    parser = moxa_base_argparser('Change IP Addresses of MOXA Terminal Server')

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

    args = vars(parser.parse_args())

    moxa = ipchange.moxa.MoxaHTTP_2_2(
        args['MOXA address/hostname'],
        cookie_file=args['cookie_file']
    )

    moxa.login(
        username=args['username'],
        password=args['password']
    )

    moxa.set_ipaddr(
        str(args['New IP Address']),
        str(args['New Netmask']),
        str(args['New Gateway'])
    )

    return 0


def moxa_download():

    parser = moxa_base_argparser('Download Moxa Configuration')

    parser.add_argument(
        '-o', '--output-file', dest='filename', action='store',
        help='Name of file to dump config to',
        default=None
    )

    args = vars(parser.parse_args())

    moxa = ipchange.moxa.MoxaHTTP_2_2(
        args['MOXA address/hostname'],
        cookie_file=args['cookie_file']
    )

    moxa.login(
        username=args['username'],
        password=args['password']
    )

    config = moxa.download_config()

    if args['filename'] is None:
        print(config, file=sys.stdout)
    else:
        with open(args['filename'], 'w') as f:
            f.write(config)

    moxa.logout()

    return 0


def moxa_change_passwd():

    parser = moxa_base_argparser('Download Moxa Configuration')

    parser.add_argument(
        'New Password',
        metavar='passwd', type=str,
        help='New Password'
    )

    args = vars(parser.parse_args())

    moxa = ipchange.moxa.MoxaHTTP_2_2(
        args['MOXA address/hostname'],
        cookie_file=args['cookie_file']
    )

    moxa.login(
        username=args['username'],
        password=args['password']
    )

    moxa.change_passwd(args['New Password'])
