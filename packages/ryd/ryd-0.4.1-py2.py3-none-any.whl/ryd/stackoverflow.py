# coding: utf-8

"""
Stackoverflow essentially uses the markdown format:
https://daringfireball.net/projects/markdown/syntax

This means there are no special characters to introduce indented code blocks (i.e like .rst
has ::).

Code is indented by four spaces.

"""


from __future__ import print_function, absolute_import, division, unicode_literals

import sys
from .ryd import (Convertor, IncRaw, Inc, Nim, NimPre, Python, PythonPre, Code,
                  Stdout, StdoutRaw, Comment)
from ruamel.yaml.scalarstring import PreservedScalarString
from ruamel.std.pathlib import Path


class StdOut:
    def __init__(self):
        self.parent = Path('')

    def __enter__(self):
        return sys.stdout

    def __exit__(self, typ, val, trace):
        pass

    def open(self, *args, **kw):
        return self


stdout = StdOut()


class StackOverflowConvertor(Convertor):
    def __init__(self, ryd, yaml, md, path):
        super(StackOverflowConvertor, self).__init__(ryd)
        self._yaml = yaml
        for v in self._tag_obj.values():
            yaml.register_class(v)
        self._md = md
        self._path = path
        if self._ryd._args.stdout or self._md.get('outpath') is None:
            self._out_path = stdout
        else:
            self._out_path = self._path.with_suffix('.md')
        self.updated = True
        ####
        self.data = []
        self.nim_pre = ""
        self.python_pre = ""
        self.last_output = ""

    def __call__(self, s):
        """
        s is the data from a single load from load_all
        returns True if correctly parsed
        """
        self.data.append(s)
        return True

    def write(self):
        with self._out_path.open('w') as fp:
            self.dump(fp, base_dir=self._out_path.parent)

    def dump(self, fp=sys.stdout, base_dir=None):
        last_ended_in_double_newline = False
        last_code = False
        for d in self.data:
            # print(type(d))
            if isinstance(d, IncRaw):
                if last_code:
                    last_code = False
                    fp.write('\n')
                for line in d.strip().splitlines():
                    if not line:
                        continue
                    if base_dir is not None and line[0] != '/':
                        p = base_dir / line
                    else:
                        p = Path(line)
                    print(p.read_text(), file=fp, end="")
            elif isinstance(d, Inc):
                if last_code:
                    last_code = False
                    print('', file=fp)
                for line in d.strip().splitlines():
                    if not line:
                        continue
                    if base_dir is not None and line[0] != '/':
                        p = base_dir / line
                    else:
                        p = Path(line)
                    for line in p.open():
                        if line.strip():
                            print('    ', line, sep="", end="", file=fp)
                        else:
                            print("", line, sep="", end="", file=fp)
            elif isinstance(d, (Nim, Python, Code)):
                if d:
                    if not last_ended_in_double_newline:
                        print('\n', file=fp)
                    for line in d.strip().splitlines():
                        if line.strip():
                            print('    ', line, sep="", file=fp)
                        else:
                            print('', line, sep="", file=fp)
                    last_code = True
                if isinstance(d, Nim):
                    self.last_output = self.check_nim_output(self.nim_pre + d)
                    if self._ryd._args.verbose > 1:
                        print('=========== output =========')
                        print(self.last_output, end="")
                        print('============================')
                    if self.last_output is None:
                        sys.exit(1)
                if isinstance(d, Python):
                    self.last_output = self.check_output(self.python_pre + d)
                    if self._ryd._args.verbose > 1:
                        print('=========== output =========')
                        print(self.last_output, end="")
                        print('============================')
                    if self.last_output is None:
                        sys.exit(1)
            elif isinstance(d, NimPre):
                self.nim_pre = d
            elif isinstance(d, PythonPre):
                self.python_pre = d
            elif isinstance(d, Comment):
                pass
            else:
                drs = d.rstrip()
                last_ended_in_double_newline = True
                d = type(d)(drs + '\n\n')
                if last_code:
                    last_code = False
                    fp.write('\n')
                print(d, file=fp, end="")
                if isinstance(d, (Stdout, StdoutRaw)):
                    prefix = "" if isinstance(d, StdoutRaw) else '    '
                    for line in self.last_output.rstrip().splitlines():
                        print('{}{}'.format(prefix, line), file=fp)
                    last_code = True
                elif type(d) != PreservedScalarString:
                    print('found unknown document type:', d.yaml_tag)
                    sys.exit(1)
                # print(file=fp)
