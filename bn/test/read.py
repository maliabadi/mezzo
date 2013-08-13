from os import getcwd
from struct import unpack

INTEGER = 0
STRING = 1
ARRAY = 2
BOOLEAN = 3


def testtypes():
    with open('types.bin' % getcwd(), 'rb') as file:
        while True:
            b = file.read(8)
            if b == '':
                break
            data = unpack('hhhh', b)
    assert data == (0, 1, 2, 3)


def test_alter_int():
    myvalue = 0
    with open('%s/alterint.bin' % getcwd(), 'rb') as file:
        while True:
            bin_type = file.read(2)
            read_type = unpack('h', bin_type)[0]
            if read_type == INTEGER:
                bin_sign = file.read(1)[0]
                read_sign = unpack('?', bin_sign)[0]
                while True:
                    bin_value = file.read(4)
                    read_value = unpack('i', bin_value)[0]
                    if read_value == 0:
                        break
                    if read_sign:
                        myvalue += read_value
                    else:
                        myvalue -= read_value
            break
    assert myvalue == 3
