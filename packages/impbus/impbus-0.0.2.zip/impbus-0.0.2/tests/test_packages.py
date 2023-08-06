# -*- coding: UTF-8 -*-

from binascii import a2b_hex as a2b

import pytest

from implib2.imp_crc import MaximCRC
from implib2.imp_packages import Package, PackageError


class TestPackage:

    def setup(self):
        self.pkg = Package()
        self.crc = MaximCRC()

    def test__pack_head(self):
        # e.g. get_long_ack
        pkg = a2b('fd0200bb81002d')
        assert self.pkg.pack(serno=33211, cmd=2) == pkg

    def test__pack_head_AndData(self):
        # e.g. get_erp_image, page1
        pkg = a2b('fd3c03bb810083ff01df')
        data = a2b('ff01')
        assert self.pkg.pack(serno=33211, cmd=60, data=data) == pkg

    def test__pack_head_WithParamNoAndParamAd(self):
        # e.g get_serno
        pkg = a2b('fd0a03bb81009b0100c4')
        data = a2b('0100')
        assert self.pkg.pack(serno=33211, cmd=10, data=data) == pkg

    def test__pack_head_WithParamNoAndParamAdAndParam(self):
        # e.g. set_serno
        pkg = a2b('fd0b07bb8100580100bb810000fb')
        data = a2b('0100bb810000')
        assert self.pkg.pack(serno=33211, cmd=11, data=data) == pkg

    def test__pack_data_ToLong(self):
        data = b'\xff' * 253
        with pytest.raises(PackageError, message="Data block bigger than 252Bytes!"):
            self.pkg.pack(serno=33211, cmd=11, data=data)

    def test__unpack_head(self):
        # e.g. responce to probe_module_long(33211)
        data = {'header': {'state': 0, 'cmd': 11, 'length': 0,
                           'serno': 33211}, 'data': None}
        pkg = a2b('000b00bb8100e6')
        assert self.pkg.unpack(pkg) == data

    def test__unpack_head_AndData(self):
        # e.g. responce to get_serial(33211)
        data = {'header': {'state': 0, 'cmd': 10, 'length': 5,
                           'serno': 33211}, 'data': b'\xbb\x81\x00\x00'}
        pkg = a2b('000a05bb8100aabb810000cc')
        assert self.pkg.unpack(pkg) == data

    def test__unpack_data_ToLong(self):
        data = b'\xff' * 253
        crc = self.crc.calc_crc(data)
        pkg = a2b('fd3cffbb8100e0') + data + crc
        with pytest.raises(PackageError, message="Data block bigger than 252Bytes!"):
            self.pkg.unpack(pkg)

    def test__unpack_data_FaultyCRC(self):
        data = b'\xff' * 252
        pkg = a2b('fd3cffbb8100e0') + data + b'\xff'
        with pytest.raises(PackageError, message="Package with faulty data CRC!"):
            self.pkg.unpack(pkg)

    def test__unpack_head_FaultyCRC(self):
        data = b'\xff' * 252
        crc = self.crc.calc_crc(data)
        pkg = a2b('fd3cffbb8100f0') + data + crc
        with pytest.raises(PackageError, message="Package with faulty header CRC!"):
            self.pkg.unpack(pkg)

    def test__unpack_head_WithProbeErrorState(self):
        data = b'\xff' * 252
        crc = self.crc.calc_crc(data)
        pkg = a2b('853cffbb8100d9') + data + crc
        with pytest.raises(PackageError, message="actual moisture is too small in DAC"):
            self.pkg.unpack(pkg)
