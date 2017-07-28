# -*- coding: utf-8 -*-
'''
Copyright (C) 2012-2017  Diego Torres Milano
Created on Jan 5, 2015

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author: Diego Torres Milano
'''

__version__ = '13.4.0'

import os
import platform


def _nd(name):
    '''
    @return: Returns a named decimal regex
    '''
    return '(?P<%s>\d+)' % name


def _nh(name):
    '''
    @return: Returns a named hex regex
    '''
    return '(?P<%s>[0-9a-f]+)' % name


def _ns(name, greedy=False):
    '''
    NOTICE: this is using a non-greedy (or minimal) regex

    @type name: str
    @param name: the name used to tag the expression
    @type greedy: bool
    @param greedy: Whether the regex is greedy or not

    @return: Returns a named string regex (only non-whitespace characters allowed)
    '''
    return '(?P<%s>\S+%s)' % (name, '' if greedy else '?')


def obtainPxPy(m):
    px = int(m.group('px'))
    py = int(m.group('py'))
    return (px, py)


def obtainVxVy(m):
    wvx = int(m.group('vx'))
    wvy = int(m.group('vy'))
    return wvx, wvy


def obtainVwVh(m):
    (wvx, wvy) = obtainVxVy(m)
    wvx1 = int(m.group('vx1'))
    wvy1 = int(m.group('vy1'))
    return (wvx1 - wvx, wvy1 - wvy)


def which(program, isWindows=False):
    import os

    def is_exe(_fpath, _isWindows):
        return os.path.isfile(_fpath) and os.access(_fpath, os.X_OK if not _isWindows else os.F_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program, isWindows):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file, isWindows):
                return exe_file

    return None


def obtainAdbPath():
    adb = 'bin/adb'
    return adb


def profileStart():
    import cProfile
    global profile
    profile = cProfile.Profile()
    profile.enable()


def profileEnd():
    profile.disable()
    import StringIO, pstats
    import sys
    s = StringIO.StringIO()
    ps = pstats.Stats(profile, stream=s).sort_stats('cumulative')
    ps.print_stats()
    print >> sys.stderr, '.' * 60
    print >> sys.stderr, "STATS:\n", s.getvalue()
    print >> sys.stderr, '.' * 60
