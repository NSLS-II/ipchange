import requests
import hashlib


class MoxaHTTP_2_2:
    def __init__(self, addr):
        """Initialize class for Moxa HTTP 2.2 Communication

        addr : str 
            Address of moxa to communicate with
        """
        self._addr = addr
        self._cookies = None
        self._base_url = 'http://{}'.format(addr)

    def login(self, username='admin', password=''):
        """ Login to MOXA Web Interface"""

        if password != '':
            password = hashlib.md5(bytes(password, 'ascii')).hexdigest()

        data = {
            'Username': 'admin',
            'Password': password,
            'MD5Password': '',
            'FakeChallenge': 5555,
            'Submit.x' : 0,
            'Submit.y' : 0
        }

        r = requests.post(self._base_url, data=data)

        if r.status_code != 200:
            raise RuntimeError('HTTP Login failed.')

        # Check by asking for main page again

        r = requests.get(self._base_url, cookies=self._cookies)

        if r.status_code != 200:
            raise RuntimeError('HTTP Login failed verification.')

    def set_ipaddr(self, ipaddr, netmask, gateway):
        """Set the IP Address of the MOXA and restart

        ipaddr : str 
            New IP Address
        netmask: str
            New NETMASK 
        gateway: str
            New Gateway
        """

        set_url = ("/Set.htm?IPConfig=0&IPaddr={}&Netmask={}&"
                "Gateway={}&DNS1=&DNS2=&WINSDisable=0&WINSServer="
                "&IP6Config=0&IPv6DNS1=&IPv6DNS2=&CONN_PRIORITY=0&"
                "LAN1Speed=0&Submit=Submit&setfunc=Basic+Network")
        set_url = set_url.format(ipaddr, netmask, gateway)

        r = requests.get(self._base_url + set_url, cookies=self._cookies)
        if r.status_code != 200:
            raise RuntimeError('Failed to set IP Address, invalid response.')

        r = requests.get(self._base_url + '/SaveRestart.htm', cookies=self._cookies) 
        if r.status_code != 200:
            raise RuntimeError('Failed to restart MOXA, invalid response.')


if __name__ == "__main__":
    m = MoxaHTTP_2_2('10.65.2.2')
    m.login('admin', '')
    m.set_ipaddr('10.65.2.3', '255.255.255.0', '')
