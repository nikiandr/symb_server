import unittest
from catp import CATP


class TestCATP(unittest.TestCase):
    def test_derivative_encode(self):
        CATPObj = CATP()
        self.assertEqual(b'\x00\x00\x00x**2|x\r\n\r\n',
                         CATPObj.encode({
                             'mode': 'derivative',
                             'function': 'x**2',
                             'order': ['x']  # 'order': ['x', 'x']
                         })
                         )

    def test_part_derivative_encode(self):
        CATPObj = CATP()
        self.assertEqual(b'\x00\x00\x00x**2+y**2+z**2|x|x|y|z\r\n\r\n',
                         CATPObj.encode({
                             'mode': 'derivative',
                             'function': 'x**2 + y**2 + z**2',
                             # d^4 f / d^2 x dy dz
                             'order': ['x', 'x', 'y', 'z']
                         })
                         )

    def test_indef_integral_encode(self):
        CATPObj = CATP()
        self.assertEqual(b'\x00\x02\x00x**2|x\r\n\r\n',
                         CATPObj.encode({
                             'mode': 'indef_integral',
                             'variables': ['x'],
                             'function': 'x**2'
                         })
                         )

    def test_def_integral_encode(self):
        CATPObj = CATP()
        self.assertEqual(b'\x00\x01\x00x**2|x|0 1\r\n\r\n',
                         CATPObj.encode({
                             'mode': 'def_integral',
                             'variables': ['x'],
                             'function': 'x**2',
                             'interval': ('0', '1')
                         })
                         )

    def test_simplify_encode(self):
        CATPObj = CATP()
        self.assertEqual(b'\x00\x03\x00sin(x)**2+cos(x)**2+sin(y)**2+cos(y)**2\r\n\r\n',
                         CATPObj.encode({
                             'mode': 'simplify',
                             'expression': 'sin(x)**2 + cos(x)**2 + sin(y)**2 + cos(y)**2'
                         })
                         )

if __name__ == "__main__":
    unittest.main()
