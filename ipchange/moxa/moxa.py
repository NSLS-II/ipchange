import hashlib
import lxml.html
import os
import pickle
import requests
import sys


_ascii = ('01234567890123456789012345678901 '
          '!"#$%&\'()*+,-./0123456789:;<=>?@'
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`'
          'abcdefghijklmnopqrstuvwxyz{|}~')


class MoxaHTTP_2_2:
    def __init__(self, addr, verbose=True, cookie_file=None):
        """Initialize class for Moxa HTTP 2.2 Communication

        addr : str
            Address of moxa to communicate with
        """
        self._addr = addr
        self._cookies = None
        self._base_url = 'http://{}'.format(addr)
        self._verbose = verbose
        self._passwd = 'admin'
        self._username = ''

        if cookie_file is None:
            home = os.path.expanduser('~')
            self._cookie_file = os.path.join(home, '.moxa')
        else:
            self._cookie_file = cookie_file

    def _print(self, *args, **kwargs):
        if self._verbose:
            print(*args, file=sys.stderr, **kwargs)

    def save_cookiejar(self):
        """Save Cookie Jar to home folder for reuse"""
        with open(self._cookie_file, 'wb') as f:
            pickle.dump(self._cookies, f)

        self._print(
            "Saved session cookies to {}"
            .format(self._cookie_file)
        )

    def load_cookiejar(self):
        """Load Cookie Jar from home folder"""
        try:
            with open(self._cookie_file, 'rb') as f:
                self._cookies = pickle.load(f)
        except FileNotFoundError:
            self._cookies = None

        if self._cookies is not None:
            self._print(
                "Loaded session cookies from '{}'"
                .format(self._cookie_file)
            )

    def login(self, username, password):
        """ Login to MOXA Web Interface"""

        if username is None:
            username = 'admin'
        if password is None:
            password = ''

        self._passwd = password
        self._username = username

        if self._cookies is None:
            # Load cookies if possible
            self.load_cookiejar()

        r = requests.get(self._base_url, cookies=self._cookies)
        if r.status_code != 200:
            raise RuntimeError('HTTP Login failed.')

        # Did we get a main page? If so we are logged in

        if self._is_main_page(r.text):
            self._print("Already logged in (valid session cookie)")
            return

        if self._is_logged_in(r.text):
            raise RuntimeError(('MOXA Does not permit login, '
                                'session is already open'))

        fcr = self._get_fake_challenge(r.text)

        if fcr is None:
            raise RuntimeError("Error getting FakeChallengeResponse")

        self._print(
            "Logging into MOXA. Username : {} FakeChallenge : {}"
            .format(username, fcr)
        )

        xorpw = self._xor_passwd(fcr, password)

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

        # If we got no cookies set, we failed login
        if len(r.cookies) == 0:
            raise RuntimeError(
                'Failed to login to Moxa.... check username and password'
            )

        for cookie in r.cookies:
            self._print(cookie)

        self._cookies = r.cookies

        self._print("Logged in as {}.".format(username))

        # Check by asking for main page again

        r = requests.get(self._base_url, cookies=self._cookies)

        if r.status_code != 200:
            raise RuntimeError('HTTP Login failed verification.')

        print("Main page requested OK.", file=sys.stderr)

        self.save_cookiejar()

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

        self._print("MOXA Network Settings set to:")
        self._print("    IP      : {}".format(ipaddr))
        self._print("    NETMASK : {}".format(netmask))
        self._print("    GATEWAY : {}".format(gateway))

        self._save_restart()

    def _save_restart(self):
        r = requests.get(
            self._base_url + '/SaveRestart.htm',
            cookies=self._cookies
        )

        if r.status_code != 200:
            raise RuntimeError('Failed to restart MOXA, invalid response.')

        self._print("Sent SaveRestart to Moxa .... rebooting ....")

    def download_config(self):
        """Download the config of the MOXA and return text"""
        r = requests.get(
            self._base_url + '/Config.txt',
            cookies=self._cookies
        )
        if r.status_code != 200:
            raise RuntimeError('Failed to restart MOXA, invalid response.')

        # Check if text file

        if r.headers['Content-Type'] != 'text/plain':
            raise RuntimeError('MOXA Failed to respond with config data')

        self._print("Downloaded config from Moxa")

        return r.text

    def change_passwd(self, new_passwd):
        """Change the password in the MOXA"""

        old_hash = hashlib.md5(bytes(self._passwd, 'ascii')).hexdigest()

        data = {
            'old_passwd': '',
            'passwd': '',
            'conf_passwd': '',
            'pwd': old_hash,
            'newpwd': self._xor_passwd(self._passwd, new_passwd, True),
            'Submit': 'Submit'
        }

        self._print('Setting password to "{}"'.format(new_passwd))
        self._print('Old MD5 = {}'.format(data['pwd']))
        self._print('New MD5 = {}'.format(data['newpwd']))

        r = requests.post(
            self._base_url + '/ChPassword.htm',
            data=data,
            cookies=self._cookies
        )

        if r.status_code != 200:
            raise RuntimeError('Failed to change password on MOXA')

        self._save_restart()

    def logout(self):

        r = requests.get(
            self._base_url + '/LogoutAct.htm',
            cookies=self._cookies,
            allow_redirects=False
        )

        # If we logged out, we get a redirect

        if r.status_code != 307:
            raise RuntimeError('Failed to logout of Moxa.')

        self._print("Logged out of Moxa")

    def _get_fake_challenge(self, htmlstr):
        htmltree = lxml.html.fromstring(htmlstr)

        for el in htmltree.xpath('//input[@name="FakeChallenge"]'):
            return el.attrib['value']

        return None

    def _is_main_page(self, htmlstr):
        htmltree = lxml.html.fromstring(htmlstr)

        if htmltree.xpath('//frame[@name="main"][@src="main.htm"]'):
            return True

        return False

    def _is_logged_in(self, htmlstr):
        htmltree = lxml.html.fromstring(htmlstr)

        for el in htmltree.xpath('//h4'):
            if el.text == 'Already login.':
                return True

        return False

    def _xor_passwd(self, str1, str2, fill=False):
        md = hashlib.md5(bytes(str1, 'ascii')).digest()
        pw_tbl = [_ascii.rindex(c) for c in str2]
        result_tbl = [a ^ b for a, b in zip(md, pw_tbl)]

        if fill:
            new_result = list(md)
        else:
            new_result = [None] * len(str2)

        for i in range(len(result_tbl)):
            new_result[i] = result_tbl[i]

        _hex = ''.join('{:02x}'.format(a) for a in new_result)
        return _hex
