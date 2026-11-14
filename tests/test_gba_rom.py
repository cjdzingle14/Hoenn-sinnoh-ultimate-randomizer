import unittest

from tools.validate_gba_rom import GBA_LOGO, validate_gba_rom


def make_valid_header():
    data = bytearray(0xC0)
    data[0x04:0xA0] = GBA_LOGO
    data[0xB2] = 0x96
    data[0xBD] = (-(sum(data[0xA0:0xBD]) + 0x19)) & 0xFF
    return bytes(data)


class GbaRomValidationTests(unittest.TestCase):
    def test_accepts_valid_minimum_gba_header(self):
        self.assertEqual(validate_gba_rom(make_valid_header()), [])

    def test_rejects_wrong_nintendo_logo(self):
        data = bytearray(make_valid_header())
        data[0x04] ^= 0xFF
        self.assertTrue(any("Nintendo GBA logo" in e for e in validate_gba_rom(data)))

    def test_rejects_wrong_fixed_byte(self):
        data = bytearray(make_valid_header())
        data[0xB2] = 0
        self.assertTrue(any("fixed header byte" in e for e in validate_gba_rom(data)))

    def test_rejects_bad_header_checksum(self):
        data = bytearray(make_valid_header())
        data[0xBD] ^= 1
        self.assertTrue(any("checksum mismatch" in e for e in validate_gba_rom(data)))

    def test_rejects_truncated_rom(self):
        self.assertTrue(validate_gba_rom(b"\x00" * 100))


if __name__ == "__main__":
    unittest.main()
