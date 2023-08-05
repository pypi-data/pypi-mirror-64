# Copyright 2019 Andrzej Cichocki

# This file is part of Lurlene.
#
# Lurlene is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Lurlene is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Lurlene.  If not, see <http://www.gnu.org/licenses/>.

from . import V, E
from .lc import Event
import unittest

class TestEvent(unittest.TestCase):

    def test_offkwarg(self):
        namespace = object()
        calls = []
        class MyNote:
            def on(self, frame, hmm):
                calls.append(['on', frame, hmm[0], hmm[frame]])
            def off(self, frame, onframes, hmm):
                calls.append(['off', frame, hmm[0], hmm[frame], onframes])
        self.new = MyNote
        self.onparams = ['frame', 'hmm']
        self.offparams = ['frame', 'onframes', 'hmm']
        e = Event(35, None, self, namespace)
        f = Event(40, 5, self, namespace)
        speed = 10
        kwargs = {(namespace, 'hmm'): V('20/80 100')}
        e(350, speed, {}, kwargs)
        e(360, speed, {}, kwargs)
        e(390, speed, {}, kwargs)
        f(400, speed, {}, kwargs)
        f(410, speed, {}, kwargs)
        self.assertEqual([
            ['on', 0, 55, 55],
            ['on', 10, 55, 56],
            ['on', 40, 55, 59],
            ['off', 50, 55, 60, 50],
            ['off', 60, 55, 61, 50],
        ], calls)

class TestSlice(unittest.TestCase):

    def test_initial(self):
        for end in 5, -96:
            v = V('0/100 100')[:end]
            self.assertEqual(5, v.len)
            self.assertEqual(.5, v[.5])
            self.assertEqual(4.5, v[4.5])
            self.assertEqual(.5, v[5.5])

    def test_terminal(self):
        for start in 95,:
            v = V('0/100 100')[start:]
            self.assertEqual(6, v.len)
            self.assertEqual(95.5, v[.5])
            self.assertEqual(99.5, v[4.5])
            self.assertEqual(100, v[5.5])
            self.assertEqual(95.5, v[6.5])

    def test_embiggen(self):
        v = V('5/4 9')[-1:11]
        self.assertEqual(12, v.len)
        self.assertEqual(9, v[.5])
        self.assertEqual(5.5, v[1.5])
        self.assertEqual(8.5, v[4.5])
        self.assertEqual(9, v[5.5])
        self.assertEqual(9, v[10.5])
        self.assertEqual(5.5, v[11.5])
        self.assertEqual(9, v[12.5])
        self.assertEqual(5.5, v[13.5])
        self.assertEqual(6.5, v[14.5])

    def test_patternkwargs(self):
        vals = []
        class Note:
            def on(self, val, frame):
                vals.append(val[frame])
        p = E(Note, '10x', val = V('/9 9'))[-6:]
        p.apply(1, .5, {})
        p.apply(1, 4.5, {})
        p.apply(1, 5.5, {})
        self.assertEqual([4.5, 8.5, 9], vals)
