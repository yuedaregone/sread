#coding:utf-8
import struct
import ctypes

class BinaryBuffError(RuntimeError):
    def __init__(self, arg):
        self.args = arg

class BinaryBuff:
    def __init__(self, size):
        self._write_offset = 0
        self._read_offset = 0
        self._buff = ctypes.create_string_buffer(size)
        self._ushort_offset = struct.calcsize('H')
        self._int_offset = struct.calcsize('i')
        self._float_offset = struct.calcsize('f')

    def get_buff(self):
        return self._buff

    def get_write_offset(self):
        return self._write_offset

    def get_read_offset(self):
        return self._read_offset

    def reset_write(self):
        self._write_offset = 0

    def reset_read(self):
        self._read_offset = 0

    def write_unsign_short(self, value):
        struct.pack_into('H', self._buff, self._write_offset, value)
        self._write_offset += self._ushort_offset

    def write_int(self, value):
        if not isinstance(value, int):
            value = int(value)
        struct.pack_into('i', self._buff, self._write_offset, value)
        self._write_offset += self._int_offset

    def write_insert_int(self, index, value):
        if not isinstance(value, int):
            value = int(value)
        struct.pack_into('i', self._buff, index, value)

    def write_float(self, value):
        if not isinstance(value, float):
            value = float(value)
        struct.pack_into('f', self._buff, self._write_offset, value)
        self._write_offset += self._float_offset

    def write_string_nolen(self, value):
        if not isinstance(value, bytes):
            if isinstance(value, str):
                value = value.encode('utf-8')
        value_len = len(value)
        value_fmt = str(value_len) + 's'
        struct.pack_into(value_fmt, self._buff, self._write_offset, value)
        self._write_offset += struct.calcsize(value_fmt)

    def write_string(self, value):
        if not isinstance(value, bytes):
            if isinstance(value, str):
                value = value.encode('utf-8')
        value_len = len(value)
        self.write_int(value_len)
        value_fmt = str(value_len) + 's'
        struct.pack_into(value_fmt, self._buff, self._write_offset, value)
        self._write_offset += struct.calcsize(value_fmt)

    def write_int_array(self, value):
        if not isinstance(value, list):
            raise BinaryBuffError("bad type:%s" % str(value))
        value_len = len(value)
        self.write_unsign_short(value_len)
        for v in value:
            self.write_int(v)

    def write_float_array(self, value):
        if not isinstance(value, list):
            raise BinaryBuffError("bad type:%s" % str(value))
        value_len = len(value)
        self.write_unsign_short(value_len)
        for v in value:
            self.write_float(v)

    def write_string_array(self, value):
        if not isinstance(value, list):
            raise BinaryBuffError("bad type:%s" % str(value))
        value_len = len(value)
        self.write_unsign_short(value_len)
        for v in value:
            self.write_string(v)

    def read_unsign_short(self):
        ret, = struct.unpack_from('H', self._buff, self._read_offset)
        self._read_offset += self._ushort_offset
        return ret

    def read_int(self):
        ret, = struct.unpack_from('i', self._buff, self._read_offset)
        self._read_offset += self._int_offset
        return ret

    def read_float(self):
        ret, = struct.unpack_from('f', self._buff, self._read_offset)
        self._read_offset += self._float_offset
        return ret

    def read_string_nolen(self, size):
        value_fmt = str(size) + 's'
        ret, = struct.unpack_from(value_fmt, self._buff, self._read_offset)
        self._read_offset += struct.calcsize(value_fmt)
        return ret

    def read_string(self):
        strlen = self.read_int()
        value_fmt = str(strlen) + 's'
        ret, = struct.unpack_from(value_fmt, self._buff, self._read_offset)
        ret = ret.decode()
        self._read_offset += struct.calcsize(value_fmt)
        return ret

    def read_int_array(self):
        arraylen = self.read_unsign_short()
        retarray = []
        for i in range(0, arraylen):
            retarray.append(self.read_int())
        return retarray

    def read_float_array(self):
        arraylen = self.read_unsign_short()
        retarray = []
        for i in range(0, arraylen):
            retarray.append(self.read_float())
        return retarray

    def read_string_array(self):
        arraylen = self.read_unsign_short()
        retarray = []
        for i in range(0, arraylen):
            retarray.append(self.read_string())
        return retarray

    def write_to_file(self, file_name):
        f = open(file_name, "wb")
        f.write(self._buff[0:self._write_offset])
        f.close()

def test():
    buffer = BinaryBuff(1000)
    buffer.write_int(100)
    buffer.write_float(5.6)
    buffer.write_unsign_short(2)
    buffer.write_string(b"asdsaf")
    buffer.write_int_array([1, 5, 9, 4])
    buffer.write_float_array([2.1, 3.1, 4.1])
    buffer.write_string_array([b"test1", b"last", b"cao"])
    print(buffer.read_int())
    print(buffer.read_float())
    print(buffer.read_unsign_short())
    print(buffer.read_string())
    print(buffer.read_int_array())
    print(buffer.read_float_array())
    print(buffer.read_string_array())

if __name__ == '__main__':
    test()
