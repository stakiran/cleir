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

    @property
    def original_string(self):
        return self._original_str

    def is_satisfied(self):
        raise NotImplementedError

    def is_already_generated(self):
        raise NotImplementedError

    def _generate_newstring(self):
        raise NotImplementedError

    def edit(self):
        s = self._generate_newstring()
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
