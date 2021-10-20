# encoding: utf-8

import datetime
import json
import os
import re
import sys

def is_mac():
    import platform
    p = platform.platform()
    if len(p)>=6 and p[:6]=='Darwin':
        return True
    return False

if is_mac():
    import libclipboard_mac as libclipboard
else:
    import libclipboard

class Util:

    @staticmethod
    def success():
        sys.exit(0)

    @staticmethod
    def abort(msg):
        print(msg)
        sys.exit(1)

    @staticmethod
    def file2list(filepath):
        ret = []
        with open(filepath, encoding='utf8', mode='r') as f:
            ret = [line.rstrip('\n') for line in f.readlines()]
        return ret

    @staticmethod
    def list2file(filepath, ls):
        with open(filepath, encoding='utf8', mode='w') as f:
            f.writelines(['{:}\n'.format(line) for line in ls] )

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
        toplevel_function_names = [name for name in callable_names if name[0].islower()]
        return toplevel_function_names

    @staticmethod
    def call_by_funcname_in_global(funcname, *args):
        """ @exception KeyError if funcname not found. """
        try:
            f = globals()[funcname]
        except KeyError:
            raise
        return f(*args)

    @staticmethod
    def today_datetimestr_short_with_dow(days=0):
        todaydt = datetime.datetime.today()
        if days!=0:
            delta = datetime.timedelta(days=days)
            todaydt += delta
        datestr = todaydt.strftime('%y%m%d')

        wd =  todaydt.weekday()
        dow_e = ['Mon',"Tue","Wed","Thu","Fri","Sat","Sun"][wd]

        return '{}({})'.format(datestr, dow_e)

    @staticmethod
    def today_datetimestr_trita_with_dow(days=0):
        todaydt = datetime.datetime.today()
        if days!=0:
            delta = datetime.timedelta(days=days)
            todaydt += delta
        datestr = todaydt.strftime('%Y/%m/%d')

        wd =  todaydt.weekday()
        dow_e = ['Mon',"Tue","Wed","Thu","Fri","Sat","Sun"][wd]

        return '{} {}'.format(datestr, dow_e)

class LineLevel:

    @staticmethod
    def prepend(s, prependee):
        return '{:}{:}'.format(prependee, s)

    @staticmethod
    def prepend_with_indent(s, prependee):
        insertpos = 0
        ls = list(s)
        bound_of_insertpos = len(s)
        while True:
            if insertpos >= bound_of_insertpos:
                insertpos = 0
                break
            if s[insertpos] in [" ", "\t"]:
                insertpos += 1
                continue
            break
        newstr = s[:insertpos] + prependee + s[insertpos:]
        return newstr

def zenkaku2hankaku(s):
    ret = s
    ret = ret.replace('　', '  ')

    before_strs = 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９'
    after_strs  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    for i, char in enumerate(before_strs):
        after_c = after_strs[i]
        before_c = char
        ret = ret.replace(before_c, after_c)

    return ret

def tab2space(s):
    ret = s
    ret = ret.replace('\t', '  ')
    return ret

'''
def remove_lf(s):
    ret = s
    ret = ret.replace('\n', '')
    return ret

def remove_crlf(s):
    ret = s
    ret = ret.replace('\r\n', '')
    return ret
'''

def remove_spaces(s):
    ret = s
    ret = ret.replace(' ', '')
    return ret

def remove_duplicate_lines(s):
    lines = Util.str2lines(s)
    lines_without_dup = list(set(lines))
    newlines = lines_without_dup
    newstr = Util.lines2str(newlines)
    return newstr

def remove_blank_lines(s):
    lines = Util.str2lines(s)
    newlines = []
    for line in lines:
        if len(line.strip()) == 0:
            continue
        newlines.append(line)
    newstr = Util.lines2str(newlines)
    return newstr

def crlf2space(s):
    ret = s
    ret = ret.replace('\r\n', ' ')
    return ret

def escape_tag(s):
    ret = s
    ret = ret.replace('<', '&lt;')
    ret = ret.replace('>', '&gt;')
    return ret

def sort_asc(s):
    lines = Util.str2lines(s)
    newlines = sorted(lines)
    newstr = Util.lines2str(newlines)
    return newstr

def sort_desc(s):
    lines = Util.str2lines(s)
    newlines = sorted(lines)
    newlines.reverse()
    newstr = Util.lines2str(newlines)
    return newstr

def reverse_order(s):
    lines = Util.str2lines(s)
    newlines = []
    for line in lines:
        newlines.insert(0, line)
    newstr = Util.lines2str(newlines)
    return newstr

def from_powerpoint_ppt(s):
    newstr = s.replace('', '\n')
    newstr = newstr.replace('“', '"')
    newstr = newstr.replace('”', '"')
    newstr = newstr.replace('　', '  ')
    return newstr

def mdquote(s):
    lines = Util.str2lines(s)
    MARKDOWN_QUOTE_PREFIX = '> '
    # aaa
    # aaa
    # aaa
    #  |
    #  V
    # > aaa
    # > 
    # > aaa
    # > 
    # > aaa
    newlines = []
    for line in lines:
        newline = '{}{}'.format(MARKDOWN_QUOTE_PREFIX, line)
        blank_between_each_line = MARKDOWN_QUOTE_PREFIX
        newlines.append(newline)
        newlines.append(blank_between_each_line)
    newstr = Util.lines2str(newlines)
    return newstr

def mdlinks(s):
    lines = Util.str2lines(s)
    MARKDOWN_QUOTE_PREFIX = '> '
    # aaa.md
    # bbb.md
    #  |
    #  V
    # - [aaa.md](aaa.md)
    # - [bbb.md](bbb.md)
    newlines = []
    for line in lines:
        newline = '- [{}]({})'.format(line, line)
        newlines.append(newline)
    newstr = Util.lines2str(newlines)
    return newstr

def prependmdlist(s):
    lines = Util.str2lines(s)
    MARKDOWN_LIST_PREFIX = '- '
    newlines = [LineLevel.prepend(line, MARKDOWN_LIST_PREFIX) for line in lines]
    newstr = Util.lines2str(newlines)
    return newstr

def prependmdlist_with_indent(s):
    lines = Util.str2lines(s)
    MARKDOWN_LIST_PREFIX = '- '
    newlines = [LineLevel.prepend_with_indent(line, MARKDOWN_LIST_PREFIX) for line in lines]
    newstr = Util.lines2str(newlines)
    return newstr

def amazon_url_simplify(s):
    # s は単一行 url とする
    # 取り出すのは isbn or asin
    # 10 or 13 桁の英数字
    # see: https://www.amazon.co.jp/gp/help/customer/display.html?nodeId=201889580
    prefix = 'https://www.amazon.co.jp/dp/'
    parts = s.split('/')
    body = ''
    for part in parts:
        if len(part)!=10 and len(part)!=13:
            continue
        if not(part.isalnum()):
            continue
        body = part
        break
    url = prefix + body
    newstr = url
    return newstr

def mask(s):
    masking_char = 'X'
    masked_str = re.sub(r'[a-zA-Z0-9]', 'X', s)
    newstr = masked_str
    return newstr

def pretty_jsonstring(s):
    d = json.loads(s)
    option_jsondump = {
        'ensure_ascii' : False,
        'indent' : 4,
    }
    prettyed_string = json.dumps(d, **option_jsondump)
    newstr = prettyed_string
    return newstr

def minify_jsonstring(s):
    d = json.loads(s)
    option_jsondump = {
        'ensure_ascii' : False,
        'separators' : (',', ':'),
    }
    minified = json.dumps(d, **option_jsondump)
    newstr = minified
    return newstr

def onenote2scb(s):
    lines = Util.str2lines(s)

    L1 = "\t• "
    L2 = "\t\t○ "
    L3 = "\t\t\t§ "
    L4 = "\t\t\t\t□ "
    L5 = "\t\t\t\t\t® "
    L6 = "\t\t\t\t\t\t◊ "
    L7 = "\t\t\t\t\t\t\t} "
    L8 = "\t\t\t\t\t\t\t\t– "

    newlines = []
    for line in lines:
        newline = line
        newline = newline.replace(L1, " "*1)
        newline = newline.replace(L2, " "*2)
        newline = newline.replace(L3, " "*3)
        newline = newline.replace(L4, " "*4)
        newline = newline.replace(L5, " "*5)
        newline = newline.replace(L6, " "*6)
        newline = newline.replace(L7, " "*7)
        newline = newline.replace(L8, " "*8)
        newlines.append(newline)

    newstr = Util.lines2str(newlines)
    return newstr

def remove_scrapbox_link_bracket(s):
    newstr = s
    newstr = newstr.replace('[', '')
    newstr = newstr.replace(']', '')
    return newstr

class Argument:

    @staticmethod
    def parse():
        import argparse

        parser = argparse.ArgumentParser()

        parser.add_argument('-e', '--edit', default=False, action='store_true')

        parser.add_argument('-l', '--list', default=False, action='store_true')

        parser.add_argument('commands', nargs='*')

        parsed_args = parser.parse_args()
        return parsed_args

if is_mac():
    LINEBREAK = '\n'
else:
    LINEBREAK = '\r\n'

MYFULLPATH = os.path.abspath(sys.argv[0])
MYDIR = os.path.dirname(MYFULLPATH)

args = Argument.parse()

if args.edit:
    Util.str2clipboard(MYFULLPATH)
    print('Copied the this script path: {:}'.format(MYFULLPATH))
    Util.success()

funcnames = Util.get_toplevel_function_names_of_me()
if args.list:
    [print(name) for name in funcnames]
    Util.success()

commandnames = args.commands
original_cbstr = Util.clipboard2str()
current_str = original_cbstr
print('All {:} commands.'.format(len(commandnames)))
for commandname in commandnames:
    try:
        current_str = Util.call_by_funcname_in_global(commandname, current_str)
    except KeyError:
        print('[Warning!] Not found "{:}", skipped.'.format(commandname))
        continue
    print('[Success!] Executed "{:}".'.format(commandname))

if len(commandnames)!=0:
    Util.str2clipboard(current_str)
