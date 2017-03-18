#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import glob
import os
import subprocess
import codecs
import difflib

from colorama import init, Fore

init()

# http://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases
class TestTexteEditsParser(unittest.TestCase):
    longMessage = True

def pretty_diff_output(lines):
    out = ''

    for line in lines:
        if line[0] == '-':
            out += Fore.RED + line
        elif line[0] == '+':
            out += Fore.GREEN + line
        else:
            out += Fore.RESET + line
        out = out + '\n'

    return out

def get_compare_outputs_fn(description, input_filename, output_filename):
    def test(self):
        process = subprocess.Popen(
            '../bin/duralex ' + input_filename,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        out, err = process.communicate()
        out = out.decode('utf-8')

        output_data = codecs.open(output_filename, 'r', 'utf-8').read()
        output_data = output_data.replace("\r\n", "\n")

        diff = difflib.unified_diff(output_data.splitlines(), out.splitlines())
        diff_lines = list(diff)
        self.assertEqual(len(diff_lines), 0, description + '\n' + pretty_diff_output(diff_lines))
    return test

if __name__ == '__main__':
    inputs = glob.glob('input/*.json')

    for input_filename in inputs:
        description = os.path.splitext(os.path.basename(input_filename))[0]
        output_filename = './output/' + os.path.basename(input_filename)
        if os.path.isfile(output_filename):
            test_func = get_compare_outputs_fn(description, input_filename, output_filename)
            setattr(TestTexteEditsParser, 'test_{0}'.format(description), test_func)

    unittest.main()
