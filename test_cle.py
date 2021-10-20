# coding: utf-8

import datetime

import unittest

import cle

class TestHelper(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_box(self):
        s = 'C:\\Users\\XXXX\\Box\\projectXYZ\\01.管理\\WBS.xlsx'

        inst = cle.BoxDrivePathPersonalization(s)
        inst.use_testmode()
        actual = inst.edit()

        expect = '%userprofile%\\projectXYZ\\01.管理\\WBS.xlsx'
        self.assertEqual(expect, actual)

if __name__ == '__main__':
    unittest.main()
