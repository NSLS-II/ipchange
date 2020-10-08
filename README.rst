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



License
-------

This software is licensed under a *3-clause BSD license*.

See LICENSE_ for details.


.. _LICENSE : LICENSE
