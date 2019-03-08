import struct


def bytes2float(bytes):
    embody=bytearray()
    for tempi in range(0,4):
        embody.append(bytes[tempi])
    return struct.unpack("!f",embody)[0]


def float2bytes(float_num):
    embody=struct.pack("f",float_num)
    return [embody[3],embody[2],embody[1],embody[0]]


if __name__ == "__main__":
    float_num_origin = 0.48
    bytes = float2bytes(float_num_origin)
    float_num = bytes2float([0x3e,0xf5,0xc2,0x8f])
    print(bytes)
    print(float_num)