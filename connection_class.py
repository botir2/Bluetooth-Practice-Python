#!/usr/bin/python
# encoding=utf8

import sys
import time
import pexpect
import subprocess

class BtAutoPair:
    """Class to auto pair and trust with bluetooth."""

    def __init__(self, mac_address):
        out = subprocess.check_output("/usr/sbin/rfkill unblock bluetooth", shell = True)
        self.child = subprocess.call("/usr/local/bin/auto-agent " + mac_address, shell = True)