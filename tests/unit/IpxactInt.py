import unittest
import io
import tempfile
import xml.etree.ElementTree as ET
from ipyxact.ipyxact import Component, IpxactInt

class IpxactIntTests(unittest.TestCase):
    """
    From IEEE 1685-2014 B.2.14 SCR 14.9:
        A value specified as an unsignedBitVectorExpression shall be resolved to an unsigned
        bit vector as specified by the SystemVerilog specification, where the vector size is
        determined by an external value (e.g., fieldsize for reset-value).
    
    From IEEE 1800-2012 5.7:
        integral_number ::= decimal_number | octal_number | binary_number | hex_number
        decimal_number ::= unsigned_number
            | [ size ] decimal_base unsigned_number
            | [ size ] decimal_base x_digit { _ }
            | [ size ] decimal_base z_digit { _ }
        binary_number ::= [ size ] binary_base binary_value
        octal_number  ::= [ size ] octal_base  octal_value
        hex_number    ::= [ size ] hex_base    hex_value
        size ::= non_zero_unsigned_number
        non_zero_unsigned_number ::= non_zero_decimal_digit { _ | decimal_digit}
        unsigned_number          ::= decimal_digit          { _ | decimal_digit }
        binary_value ::= binary_digit { _ | binary_digit }
        octal_value  ::= octal_digit  { _ | octal_digit }
        hex_value    ::= hex_digit    { _ | hex_digit }
        decimal_base ::= '[s|S]d | '[s|S]D
        binary_base  ::= '[s|S]b | '[s|S]B
        octal_base   ::= '[s|S]o | '[s|S]O
        hex_base     ::= '[s|S]h | '[s|S]H
        non_zero_decimal_digit ::=     1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
        decimal_digit          ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
        binary_digit ::= x_digit | z_digit | 0 | 1
        octal_digit  ::= x_digit | z_digit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7
        hex_digit    ::= x_digit | z_digit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
                         | a | b | c | d | e | f | A | B | C | D | E | F
        x_digit      ::= x | X
        z_digit      ::= z | Z | ?
    """
    
    def testDecimal_num(self):
        self.assertEqual(IpxactInt("100"), 100)
    def testDecimal_underscore(self):
        self.assertEqual(IpxactInt("1_0_0"), 100)
    def testDecimal_unsized(self):
        self.assertEqual(IpxactInt("'d100"), 100)
    def testDecimal_unsized_caps(self):
        self.assertEqual(IpxactInt("'D100"), 100)
    def testDecimal_sized(self):
        self.assertEqual(IpxactInt("8'd100"), 100)
    def testDecimal_sized_caps(self):
        self.assertEqual(IpxactInt("8'D100"), 100)
        
    def testDecimalExceptions_singed(self):
        # don't handle signed expressions
        self.assertRaises(Exception, IpxactInt, "8'sd100")
        self.assertRaises(Exception, IpxactInt, "8'sD100")
        self.assertRaises(Exception, IpxactInt, "8'Sd100")
        self.assertRaises(Exception, IpxactInt, "8'SD100")
    def testDecimalExceptions_unknown(self):
        # don't handle X and Z expressions
        self.assertRaises(Exception, IpxactInt, "8'd10x")
        self.assertRaises(Exception, IpxactInt, "8'd10X")
        self.assertRaises(Exception, IpxactInt, "8'd10z")
        self.assertRaises(Exception, IpxactInt, "8'd10Z")
        self.assertRaises(Exception, IpxactInt, "8'd10?")

    def testHex_nonstandard_0x(self):
        self.assertEqual(IpxactInt("0xF"), 15)
    def testHex_unsized(self):
        self.assertEqual(IpxactInt("'hF"), 15)
        self.assertEqual(IpxactInt("'hf"), 15)
    def testHex_unsized_caps(self):
        self.assertEqual(IpxactInt("'HF"), 15)
        self.assertEqual(IpxactInt("'Hf"), 15)
    def testHex_sized(self):
        self.assertEqual(IpxactInt("4'hF"), 15)
        self.assertEqual(IpxactInt("4'hf"), 15)
    def testHex_sized_caps(self):
        self.assertEqual(IpxactInt("4'HF"), 15)
        self.assertEqual(IpxactInt("4'Hf"), 15)
    def testHex_underscore(self):
        self.assertEqual(IpxactInt("8'h0_F"), 15)
        self.assertEqual(IpxactInt("8'h0_f"), 15)
    def testHex_underscore_caps(self):
        self.assertEqual(IpxactInt("8'h0_F"), 15)
        self.assertEqual(IpxactInt("8'h0_f"), 15)

    def testHexExceptions_signed(self):
        # don't handle signed expressions
        self.assertRaises(Exception, IpxactInt, "4'shF")
        self.assertRaises(Exception, IpxactInt, "4'sHF")
        self.assertRaises(Exception, IpxactInt, "4'ShF")
        self.assertRaises(Exception, IpxactInt, "4'SHF")
    def testHexExceptions_unknown(self):
        # don't handle X and Z expressions
        self.assertRaises(Exception, IpxactInt, "8'hxF")
        self.assertRaises(Exception, IpxactInt, "8'hXF")
        self.assertRaises(Exception, IpxactInt, "8'hzF")
        self.assertRaises(Exception, IpxactInt, "8'hZF")
        self.assertRaises(Exception, IpxactInt, "8'h?F")

    def testBinary_unsized(self):
        self.assertEqual(IpxactInt("'b1100"), 12)
    def testBinary_unsized_caps(self):
        self.assertEqual(IpxactInt("'B1100"), 12)
    def testBinary_sized(self):
        self.assertEqual(IpxactInt("4'b1100"), 12)
    def testBinary_sized_caps(self):
        self.assertEqual(IpxactInt("4'B1100"), 12)
    def testBinary_underscore(self):
        self.assertEqual(IpxactInt("8'b0000_1100"), 12)
    def testBinary_underscore_caps(self):
        self.assertEqual(IpxactInt("8'B0000_1100"), 12)

    def testBinaryExceptions_signed(self):
        # don't handle signed expressions
        self.assertRaises(Exception, IpxactInt, "4'sb1100")
        self.assertRaises(Exception, IpxactInt, "4'sB1100")
        self.assertRaises(Exception, IpxactInt, "4'Sb1100")
        self.assertRaises(Exception, IpxactInt, "4'SB1100")
    def testBinaryExceptions_unknown(self):
        # don't handle X and Z expressions
        self.assertRaises(Exception, IpxactInt, "4'b110x")
        self.assertRaises(Exception, IpxactInt, "4'b110X")
        self.assertRaises(Exception, IpxactInt, "4'b110z")
        self.assertRaises(Exception, IpxactInt, "4'b110Z")
        self.assertRaises(Exception, IpxactInt, "4'b110?")

    def testOctal_unsized(self):
        self.assertEqual(IpxactInt("'o77"), 63)
    def testOctal_unsized_caps(self):
        self.assertEqual(IpxactInt("'O77"), 63)
    def testOctal_sized(self):
        self.assertEqual(IpxactInt("6'o77"), 63)
    def testOctal_sized_caps(self):
        self.assertEqual(IpxactInt("6'O77"), 63)
    def testOctal_underscore(self):
        self.assertEqual(IpxactInt("6'o7_7"), 63)
    def testOctal_underscore_caps(self):
        self.assertEqual(IpxactInt("6'O7_7"), 63)

    def testOctalExceptions_signed(self):
        # don't handle signed expressions
        self.assertRaises(Exception, IpxactInt, "6'so77")
        self.assertRaises(Exception, IpxactInt, "6'sO77")
        self.assertRaises(Exception, IpxactInt, "6'So77")
        self.assertRaises(Exception, IpxactInt, "6'SO77")
    def testOctalExceptions_unknown(self):
        # don't handle X and Z expressions
        self.assertRaises(Exception, IpxactInt, "6'sox7")
        self.assertRaises(Exception, IpxactInt, "6'soX7")
        self.assertRaises(Exception, IpxactInt, "6'soz7")
        self.assertRaises(Exception, IpxactInt, "6'soZ7")
        self.assertRaises(Exception, IpxactInt, "6'so?7")

class ResetMaskTests(unittest.TestCase):
    def check_reset_masks(self, version):
        namespace = Component.nsmap[version][1]
        for mask, expected in [('0x0', 0), ("8'hA5", 0xA5), (None, None)]:
            reset_xml = '<reset><value>0xff</value>{}</reset>'.format(
                '' if mask is None else '<mask>{}</mask>'.format(mask))
            if version == '2014':
                reset_xml = ('<field><name>f</name><bitOffset>0</bitOffset>'
                             '<bitWidth>8</bitWidth><resets>{}</resets>'
                             '</field>').format(reset_xml)
            xml = ('<component xmlns="{namespace}">'
                   '<vendor>v</vendor><library>l</library><name>c</name>'
                   '<version>1</version><memoryMaps><memoryMap><name>m</name>'
                   '<addressBlock><name>a</name><baseAddress>0</baseAddress>'
                   '<range>1</range><width>8</width><register><name>r</name>'
                   '<addressOffset>0</addressOffset><size>8</size>'
                   '{reset}</register></addressBlock>'
                   '<addressUnitBits>8</addressUnitBits></memoryMap>'
                   '</memoryMaps></component>').format(
                       namespace=namespace, reset=reset_xml)
            component = Component()
            component.load(io.BytesIO(xml.encode('utf-8')))
            self.check_parsed_reset(component, version, expected)

            with tempfile.TemporaryFile(mode='w+') as output:
                component.write(output)
                output.seek(0)
                root = ET.parse(output).getroot()
                masks = root.findall('.//{{{}}}mask'.format(namespace))
                self.assertEqual(len(masks), 0 if mask is None else 1)
                if masks:
                    self.assertEqual(int(masks[0].text), expected)
                output.seek(0)
                reloaded = Component()
                reloaded.load(output)
                self.check_parsed_reset(reloaded, version, expected)

    def check_parsed_reset(self, component, version, expected):
        register = component.memoryMaps.memoryMap[0].addressBlock[0].register[0]
        reset = (register.field[0].resets.reset if version == '2014'
                 else register.reset)
        self.assertEqual(reset.value, 0xff)
        self.assertEqual(reset.mask, expected)
        self.assertEqual(register.dim, 0)

    def test_register_reset_2009(self):
        self.check_reset_masks('2009')

    def test_field_reset_2014(self):
        self.check_reset_masks('2014')

def main():
    unittest.main(verbosity=2, )

if __name__ == '__main__':
    main()
