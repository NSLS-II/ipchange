import ipaddress
import requests
import time
from requests.auth import HTTPDigestAuth


class AxisWebcam:
    def __init__(self, ipaddr, username=None, password=None):
        """Initialize AxisWebcam Object

        ipaddr : str
            IP Address of AXIS Webcam
        username : str
            Username of Axis Webcam
        password : str
            Password of Axis Webcam
        """

        if username is None:
            username = 'root'
        if password is None:
            password = 'pass'

        self._base_url = 'http://{}'.format(ipaddr)
        self._auth = HTTPDigestAuth(username, password)

    def set_ipaddr(self, ipaddr, netmask, gateway):
        """Set the IP Address of the Axis Webcam

        ipaddr : str
            New IP Address
        netmask: str
            New NETMASK
        gateway: str
            New Gateway
        """

        # Use the ipaddress module to determine broadcast adddress
        _iface = ipaddress.ip_interface('{}/{}'.format(ipaddr, netmask))
        broadcast = _iface.network.broadcast_address

        # First lets get the settings page to check auth etc

        r = requests.get(
            self._base_url + '/admin/tcpip.shtml?basic=yes&id=94',
            auth=self._auth
        )
        if r.status_code != 200:
            raise RuntimeError('Unable to connect to Axis Camera')

        data = {
            'root_Network_ZeroConf_Enabled': 'yes',
            'root_Network_Broadcast': str(broadcast),
            'root_Network_Enabled': 'yes',
            'root_Network_IPv6_Enabled': 'no',
            'Network_Enabled': 'on',
            'root_Network_BootProto': 'none',
            'root_Network_IPAddress': str(ipaddr),
            'root_Network_SubnetMask': str(netmask),
            'root_Network_DefaultRouter': str(gateway),
            'root_Network_ARPPingIPAddress_Enabled': 'yes',
            'Network_ARPPingIPAddress_Enabled': 'on',
            'root_RemoteService_Enabled': 'oneclick',
            'RemoteService_Enabled': 'no',
            'RemoteService_Enabled_value': 'oneclick',
            'root_RemoteService_ProxyServer': '',
            'root_RemoteService_ProxyPort': '3128',
            'root_RemoteService_ProxyLogin': '',
            'root_RemoteService_ProxyPassword': '',
            'RemoteService_ProxyAuth_value': 'basic',
            'root_RemoteService_ProxyAuth': 'basic',
            'return_page': '/admin/tcpip.shtml?basic=yes&id=92',
            'action': 'modify',
            'replyfirst': 'no'
        }

        headers = {
            'Referer': self._base_url + '/admin/tcpip.shtml?basic=yes&id=111',
            'Origin': self._base_url,
            'Upgrade-Insecure-Requests': '1'
        }

        r = requests.post(
            self._base_url + "/sm/sm.srv",
            auth=self._auth,
            data=data,
            headers=headers,
            allow_redirects=False
        )

        if r.status_code != 303:
            raise RuntimeError('Request to change IP failed. Bad responce.')

        return

    def change_passwd(self, username, password):
        """Change Password on AXIS Camera

        username : str
            Username to change
        password : str
            New password for username
        """

        r = requests.get(
            self._base_url + '/admin/users.shtml?basic=yes&id=131',
            auth=self._auth,
            allow_redirects=False
        )

        if r.status_code != 200:
            raise RuntimeError('Unable to connect to Axis Camera')

        params = {
            'action': 'update',
            'user': username,
            'pwd': password,
            'timestamp': int(time.time())
        }

        r = requests.get(
            self._base_url + '/axis-cgi/admin/pwdgrp.cgi',
            auth=self._auth,
            params=params,
            allow_redirects=False
        )

        if r.status_code != 200:
            raise RuntimeError('Unable to connect to Axis Camera')
