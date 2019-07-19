#!/usr/bin/python 
# -*- coding: ascii -*-

#---------------------------------------------------------
# My small python exploitation library
#---------------------------------------------------------


import socket
import struct
import bitstring

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


def p8(v):
    return struct.pack('>B',v)

def p16(v):
    return struct.pack('>H', v & 0xffff)

def p32(v):
    return struct.pack('>I', v & 0xffffffff)

def p64(v):
    return struct.pack('>Q', v & 0xffffffffffffffff)

def u8(v):
    return struct.unpack('>B', v)[0]

def u16(v):
    return struct.unpack('>H', v)[0]

def u32(v):
    return struct.unpack('>I', v)[0]

def u64(v):
    return struct.unpack('>Q', v)[0]


def red(str):
  return bcolors.RED + str + bcolors.ENDC

def blue(str):
  return bcolors.BLUE + str + bcolors.ENDC

def green(str):
  return bcolors.GREEN + str + bcolors.ENDC

def yellow(str):
  return bcolors.YELLOW + str + bcolors.ENDC

def bold(str):
  return bcolors.BOLD + str + bcolors.ENDC

def underline(str):
  return bcolors.UNDERLINE + str + bcolors.ENDC

