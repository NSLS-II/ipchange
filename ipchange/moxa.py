import requests
import hashlib
import lxml.html


ascii = ('01234567890123456789012345678901 '
         '!"#$%&\'()*+,-./0123456789:;<=>?@'
         'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`'
         'abcdefghijklmnopqrstuvwxyz{|}~')


def xor_passwd(str1, str2, fill=False):
    md = hashlib.md5(bytes(str1, 'ascii')).digest()
    pw_tbl = [ascii.rindex(c) for c in str2]
    result_tbl = [a ^ b for a, b in zip(md, pw_tbl)]

    if fill:
        new_result = list(md)
    else:
        new_result = [None] * len(str2)

    for i in range(len(result_tbl)):
        new_result[i] = result_tbl[i]

    return ''.join('{:02x}'.format(a) for a in new_result)


def get_fake_challenge(htmlstr):
    htmltree = lxml.html.fromstring(htmlstr)

    for el in htmltree.xpath('//input'):
        name = el.attrib['name']
        if name == 'FakeChallenge':
            return el.attrib['value']

    return None


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

        r = requests.get(self._base_url)
        if r.status_code != 200:
            raise RuntimeError('HTTP Login failed.')

        fcr = get_fake_challenge(r.text)

        if fcr is None:
            raise RuntimeError("Error getting FakeChallengeResponse")

        xorpw = xor_passwd(fcr, password)

        data = {
            'Username': username,
            'Password': '',
            'MD5Password': xorpw,
            'FakeChallenge': fcr,
            'Submit.x': 0,
            'Submit.y': 0
        }

        r = requests.post(self._base_url, data=data)
        if r.status_code != 200:
            raise RuntimeError('HTTP Login failed.')

        self._cookies = r.cookies

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

        r = requests.get(
            self._base_url + '/SaveRestart.htm',
            cookies=self._cookies
        )
        if r.status_code != 200:
            raise RuntimeError('Failed to restart MOXA, invalid response.')


if __name__ == "__main__":
    m = MoxaHTTP_2_2('xf06bm-tsrv6')
    m.login('admin', 'test')
    # m.set_ipaddr('10.65.2.3', '255.255.255.0', '')
