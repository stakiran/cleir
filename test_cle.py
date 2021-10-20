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

    def test_amazon(self):
        s = 'https://www.amazon.co.jp/dp/B081V4TW2W/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1'
        expect = 'https://www.amazon.co.jp/dp/B081V4TW2W'
        inst = cle.AmazonUrlSimplification(s)
        inst.use_testmode()
        actual = inst.edit()
        self.assertEqual(expect, actual)

        s = 'https://www.amazon.co.jp/%E3%83%AC%E3%83%95%E3%82%A1%E3%83%AC%E3%83%B3%E3%82%B9%E3%81%A8%E5%9B%B3%E6%9B%B8%E9%A4%A8-%E3%81%82%E3%82%8B%E5%9B%B3%E6%9B%B8%E9%A4%A8%E5%8F%B8%E6%9B%B8%E3%81%AE%E6%97%A5%E8%A8%98-%E5%A4%A7%E4%B8%B2-%E5%A4%8F%E8%BA%AB-ebook/dp/B081V4TW2W'
        expect = 'https://www.amazon.co.jp/dp/B081V4TW2W'
        inst = cle.AmazonUrlSimplification(s)
        inst.use_testmode()
        actual = inst.edit()
        self.assertEqual(expect, actual)

if __name__ == '__main__':
    unittest.main()
