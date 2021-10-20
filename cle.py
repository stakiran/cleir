# encoding: utf-8

import datetime
import json
import os
import re
import sys

import libclipboard

LINEBREAK = '\r\n'

class Util:
    @staticmethod
    def success():
        sys.exit(0)

    @staticmethod
    def abort(msg):
        print(msg)
        sys.exit(1)

    @staticmethod
    def lines2str(lines):
        return LINEBREAK.join(lines)

    @staticmethod
    def str2lines(s):
        return s.split(LINEBREAK)

    @staticmethod
    def clipboard2lines():
        s = Util.clipboard2str()
        return Util.str2lines(s)

    @staticmethod
    def clipboard2str():
        s = libclipboard.precise_clipget()
        if s=='':
            Util.abort('Clipboard is empty.')
        return s

    @staticmethod
    def lines2clipboard(lines):
        s = Util.lines2str(lines)
        Util.str2clipboard(lines)

    @staticmethod
    def str2clipboard(s):
        libclipboard.Clipboard.set(s)

class Editor:
    def __init__(self, s):
        self._original_str = s

        self._testmode = False

    @property
    def original_string(self):
        return self._original_str

    def use_testmode(self):
        self._testmode = True

    def _is_testmode(self):
        return self._testmode

    def is_satisfied(self):
        raise NotImplementedError

    def is_already_generated(self):
        raise NotImplementedError

    def _generate_newstring(self):
        raise NotImplementedError

    def edit(self):
        s = self._generate_newstring()

        if self._is_testmode():
            return s

        Util.str2clipboard(s)

class BoxDrivePathPersonalization(Editor):
    def __init__(self, s):
        super().__init__(s)

        self.YOUR_PREFIX = '%userprofile%'

    def is_satisfied(self):
        s = self.original_string
        lines = Util.str2lines(s)

        is_multiline = len(lines)>=2
        if is_multiline:
            return False

        path = lines[0]
        path = path.lower()
        contains_box_str = path.find('\\box\\') != -1
        if contains_box_str:
            return True
        return False

    def is_already_generated(self):
        return False

    def _generate_newstring(self):
        path = self.original_string

        # C:\\Users\\XXXX\\Box\\projectXYZ\\folder\\file.ext
        #                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        #                       rest
        driveletter, maybe_users, maybe_username, maybe_box, rest = path.split('\\', 4)

        newpath = os.path.join(self.YOUR_PREFIX, rest)

        return newpath

class AmazonUrlSimplification(Editor):
    def __init__(self, s):
        super().__init__(s)

        self.URL_PREFIX = 'https://www.amazon.co.jp/dp/'

    def is_satisfied(self):
        s = self.original_string
        lines = Util.str2lines(s)

        is_multiline = len(lines)>=2
        if is_multiline:
            return False

        path = lines[0]
        path = path.lower()
        is_prefix_correct = path.startswith(self.URL_PREFIX)
        if is_prefix_correct:
            return True
        return False

    def is_already_generated(self):
        prefix_len = len('https://www.amazon.co.jp/dp/')
        #isbn_or_asin_len_1 = 10
        isbn_or_asin_len_2 = 13

        generated_len_minimum = prefix_len + isbn_or_asin_len_2

        s = self.original_string
        if len(s) <= generated_len_minimum:
            return True
        return False

    def _generate_newstring(self):
        # 取り出すのは isbn or asin
        # 10 or 13 桁の英数字
        # see: https://www.amazon.co.jp/gp/help/customer/display.html?nodeId=201889580

        s = self.original_string

        parts = s.split('/')
        body = ''
        for part in parts:
            if len(part)!=10 and len(part)!=13:
                continue
            if not(part.isalnum()):
                continue
            body = part
            break

        prefix = self.URL_PREFIX
        url = prefix + body
        newstr = url
        return newstr

if __name__=='__main__':
    original_cbstr = Util.clipboard2str()
    s = original_cbstr

    inst = BoxDrivePathPersonalization(s)
    if not inst.is_satisfied():
        print('not safisfied')
        sys.exit(0)
    if inst.is_already_generated():
        print('already generated')
        sys.exit(0)
    inst.edit()
    print('edit!')
