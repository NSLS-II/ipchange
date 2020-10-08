========
ipchange
========

Introduction
------------

IP Change Scripts for NSLS-II Devices.

This collection of utilities provides command line utilities and python modules for changing the ipaddress's and passwords for:

* Moxa Terminal Servers
* AXIS Webcams

Axis Webcam Usage
-----------------

To change the ipaddress of the axis camera execute:

.. code-block:: shell

    axis_change_ip -u root -u pass axis_cam.nsls2.bnl.local 10.0.0.2 255.255.255.0 10.0.0.1

where `axis_cam.nsls2.bnl.local` is the hostname (or IP) of the camera to change,
`10.0.0.2` is the new ipaddress, `255.255.255.0` is the new netmask and `10.0.0.1` is
the new gateway.

To change the password for a given user:

.. code-block:: shell

    axis_change_passwd -u root -u pass root really_secret

where `root` is the username to change the password of and `really_secret` is
the new password.

MOXA Terminal Server Usage
--------------------------

To change the IP address of the MOXA Terminal Server execute:

.. code-block:: shell

    moxa_change_ip -u root -u pass xf31id1-tsrv1.nsls2.bnl.local 10.0.0.2 255.255.255.0 10.0.0.1

where `xf31id1-tsrv1.nsls2.bnl.local` is the hostname (or IP) of the terminal server to change,
`10.0.0.2` is the new ipaddress, `255.255.255.0` is the new netmask and `10.0.0.1` is
the new gateway.

To download the moxa config execute:

.. code-block:: shell

    moxa_download -u root -u pass xf31id1-tsrv1.nsls2.bnl.local

where `xf31id1-tsrv1.nsls2.bnl.local` is the hostname (or IP) of the terminal server.
If exected as above, the config will be output to `stdout`. Supplying the `-o` option
on the command line will dowload to a file.

Notes
-----

Note: These packages have largely been formed by reverse engineering the HTTP traffic
from the web based admin consoles rather than a published API. Therefore they may be a
little brittle. YMMV

License
-------

This software is licensed under a *3-clause BSD license*.

See LICENSE_ for details.


.. _LICENSE : LICENSE
