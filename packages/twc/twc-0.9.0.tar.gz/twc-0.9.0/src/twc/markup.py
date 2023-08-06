# Copyright (C) 2019 Michał Góral.
#
# This file is part of TWC
#
# TWC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TWC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TWC. If not, see <http://www.gnu.org/licenses/>.

'''Custom markup processor.'''

import re
import attr


_SEPS = re.compile(r'(,|\+)')
_FMT = re.compile(r'(\w[\w.]*(?::.*:)?)')


@attr.s
class Parser:
    '''Parser of task format markup'''
    _substs = attr.ib()
    _markup = attr.ib(factory=list)
    _nextsep = attr.ib(None)

    @property
    def markup(self):
        return self._markup

    def parse(self, text):
        if not text:
            return

        tokens = _SEPS.split(text)
        for token in tokens:
            if token == ',':
                self._nextsep = ' '
            elif token == '+':
                self._nextsep = None
            else:
                self._process_entry(token)

    def _add(self, text, style=''):
        if not text:
            return

        if style:
            style = 'class:{}'.format(style)

        if self._nextsep and self._markup:
            self._markup.append(('', self._nextsep))

        self._markup.append((style, text))

    def _process_entry(self, text):
        match = _FMT.search(text)
        if not match:
            return

        name = match.group(1)

        key, _, opts = match.group(1).partition(':')
        style, _, spec = opts.rstrip(':').partition(':')

        if not spec:
            name = '{{{}}}'.format(key)
        else:
            name = '{{{}:{}}}'.format(key, spec)

        try:
            formatted = name.format_map(self._substs)
        except KeyError:
            return

        if formatted:
            mstart, mend = match.span(1)
            processed = '{}{}{}'.format(text[:mstart], formatted, text[mend:])
            self._add(processed, style)


def format_map(text, substitutions):
    parser = Parser(substitutions)
    parser.parse(text)
    return parser.markup


def format_(text, **kw):
    return format_map(text, kw)
