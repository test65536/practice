import struct


def bytes2float(bytes):
    embody = bytearray()
    for tempi in range(0, 4):
        embody.append(bytes[tempi])
    return struct.unpack("!f", embody)[0]


array = 0x3e, 0xf5, 0xc2, 0x8f
f = bytes2float(array)
print('%.2f' % f)
