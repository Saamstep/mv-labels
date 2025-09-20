#!/usr/bin/env python3
# coding: utf-8
"""ping.py - PyATEMMax demo script.
   Part of the PyATEMMax library."""

import argparse
import time
import PyATEMMax

print(f"[{time.ctime()}] PyATEMMax demo script: ping")

DEFAULT_INTERVAL = 1.0
SWITCHER_IP = "192.168.1.83"


switcher = PyATEMMax.ATEMMax()

switcher.connect(SWITCHER_IP)

sources = PyATEMMax.ATEMVideoSources

print(f"{getattr(sources, 'input1')}")

if(switcher.waitForConnection(infinite=False, timeout=5)):
    print(f"[{time.ctime()}] Switcher connected")
    name = "Bob"
    switcher.setInputLongName(sources.input2, f"C2 - {name}")    

    switcher.disconnect()
    exit(0)
else:
      print(f"[{time.ctime()}] Switcher not connected")
      exit(1)