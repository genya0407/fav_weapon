#coding:utf-8

import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == 'win32' : base = 'Win32GUI'

exe = Executable(script = 'widgets.py',base = base)

setup(name = 'widgets', version = '0.1', description = 'faver', executables = [exe])
