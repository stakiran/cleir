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

        s = 'https://www.amazon.co.jp/%E3%82%AA%E3%83%BC%E3%83%AB%EF%BC%95%E5%BC%8F%E3%80%8C%E6%9A%97%E8%A8%98%E6%B3%95%E3%80%8D%E3%80%9C%E7%90%86%E7%A7%91%E7%A4%BE%E4%BC%9A%E3%81%8C%E8%8B%A6%E6%89%8B%E3%81%AA%E4%B8%AD%E5%AD%A6%E7%94%9F%E3%81%A7%E3%82%82%EF%BC%91%E3%83%9A%E3%83%BC%E3%82%B8%E3%82%92%EF%BC%93%E5%88%86%E3%81%A7%E7%9E%AC%E9%96%93%E6%9A%97%E8%A8%98%EF%BC%81%E3%80%9C%EF%BC%9C%EF%BC%91%EF%BC%95%EF%BC%90%E7%82%B9%E3%82%A2%E3%83%83%E3%83%97%E3%82%92%E7%8B%99%E3%81%86%E5%8B%89%E5%BC%B7%E6%B3%95%EF%BC%9E-%E4%BD%90%E3%80%85%E6%9C%A8%E5%8B%87%E6%B0%97-ebook/dp/B01FE7KR7E/'
        expect = 'https://www.amazon.co.jp/dp/B01FE7KR7E'
        inst = cle.AmazonUrlSimplification(s)
        inst.use_testmode()
        actual = inst.edit()
        self.assertEqual(expect, actual)

    def test_chain(self):
        use_testmode = True

        s = 'not target string'
        expect = None
        actual = cle.editor_chain(s, use_testmode)
        self.assertEqual(expect, actual)

        s = 'C:\\Users\\XXXX\\Box\\projectXYZ\\01.管理\\WBS.xlsx'
        expect = '%userprofile%\\projectXYZ\\01.管理\\WBS.xlsx'
        actual = cle.editor_chain(s, use_testmode)
        self.assertEqual(expect, actual)

        s = 'https://www.amazon.co.jp/%E3%83%AC%E3%83%95%E3%82%A1%E3%83%AC%E3%83%B3%E3%82%B9%E3%81%A8%E5%9B%B3%E6%9B%B8%E9%A4%A8-%E3%81%82%E3%82%8B%E5%9B%B3%E6%9B%B8%E9%A4%A8%E5%8F%B8%E6%9B%B8%E3%81%AE%E6%97%A5%E8%A8%98-%E5%A4%A7%E4%B8%B2-%E5%A4%8F%E8%BA%AB-ebook/dp/B081V4TW2W'
        expect = 'https://www.amazon.co.jp/dp/B081V4TW2W'
        actual = cle.editor_chain(s, use_testmode)
        self.assertEqual(expect, actual)

if __name__ == '__main__':
    unittest.main()
