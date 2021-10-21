# encoding: utf-8

import os
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

    @staticmethod
    def get_toplevel_function_names_of_me():
        global_objs = globals()
        callable_names = [key for key in globals() if callable(global_objs[key])]
        toplevel_function_names = [name for name in callable_names if name[0].isupper()]
        return toplevel_function_names

    @staticmethod
    def new_with_classname_in_global(classname, *args):
        """ @exception KeyError if funcname not found. """
        try:
            c = globals()[classname]
        except KeyError:
            raise
        return c(*args)

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
        self.URL_PREFIX_FOR_VALIDATION = 'https://www.amazon.co.jp/'

    def is_satisfied(self):
        s = self.original_string
        lines = Util.str2lines(s)

        is_multiline = len(lines)>=2
        if is_multiline:
            return False

        path = lines[0]
        path = path.lower()
        is_prefix_correct = path.startswith(self.URL_PREFIX_FOR_VALIDATION)
        if is_prefix_correct:
            return True
        return False

    def is_already_generated(self):
        prefix_len = len(self.URL_PREFIX)
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

class TtpToHttp(Editor):
    def __init__(self, s):
        super().__init__(s)

        self.PREFIX = 'ttp://'
        self.PREFIX_ALREADY = 'http://'

    def is_satisfied(self):
        s = self.original_string
        lines = Util.str2lines(s)

        is_multiline = len(lines)>=2
        if is_multiline:
            return False

        path = lines[0]
        path = path.lower()
        is_prefix_correct = path.startswith(self.PREFIX)
        if is_prefix_correct:
            return True
        return False

    def is_already_generated(self):
        path = self.original_string
        return path.startswith(self.PREFIX_ALREADY)

    def _generate_newstring(self):
        s = self.original_string
        ttp_url = s
        newstr =  'h{}'.format(ttp_url)
        return newstr

def editor_chain(original_string, use_testmode=False):
    classnames = Util.get_toplevel_function_names_of_me()
    removers = ['Util', 'Editor']
    for remover in removers:
        classnames.remove(remover)

    for classname in classnames:
        inst = Util.new_with_classname_in_global(classname, original_string)

        if not inst.is_satisfied():
            continue
        if inst.is_already_generated():
            continue

        if use_testmode:
            inst.use_testmode()
        response = inst.edit()
        if use_testmode:
            return response
        break

if __name__=='__main__':
    original_cbstr = Util.clipboard2str()
    s = original_cbstr

    use_testmode = False
    editor_chain(s, use_testmode)
