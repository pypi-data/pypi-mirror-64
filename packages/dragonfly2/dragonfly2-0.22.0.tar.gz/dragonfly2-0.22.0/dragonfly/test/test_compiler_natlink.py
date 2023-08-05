﻿#
# This file is part of Dragonfly.
# (c) Copyright 2007, 2008 by Christo Butcher
# Licensed under the LGPL.
#
#   Dragonfly is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Dragonfly is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with Dragonfly.  If not, see
#   <http://www.gnu.org/licenses/>.
#
import codecs
import unittest

from six import PY2

from dragonfly import CompoundRule, Choice, Grammar


class TestCompilerNatlink(unittest.TestCase):

    def test_natlink_compiler(self):
        from dragonfly.engines.backend_natlink.compiler import NatlinkCompiler
        extras = [
            Choice("food", {
                "(an | a juicy) apple": "good",
                "a [greasy] hamburger": "bad"
            })
        ]
        rule = CompoundRule('ExampleCustomRule', "I want to eat <food>",
                            extras)
        grammar = Grammar(name="mygrammar")
        grammar.add_rule(rule)

        c = NatlinkCompiler()
        (compiled_grammar, rule_names) = c.compile_grammar(grammar)

        assert rule_names == (None, "ExampleCustomRule")
        if PY2:
            assert compiled_grammar.encode("hex") == "0000000000000000040000001c0000001c000000010000004578616d706c65437573746f6d52756c650000000500000000000000060000000000000002000000900000000c0000000100000049000000100000000200000077616e74000000000c00000003000000746f00000c00000004000000656174000c000000050000006100000010000000060000006772656173790000140000000700000068616d6275726765720000000c00000008000000616e000010000000090000006a75696379000000100000000a0000006170706c6500000003000000e0000000e00000000100000001000000010000000100000001000000030000000100000003000000020000000300000003000000030000000400000002000000010000000100000002000000010000000100000003000000050000000100000004000000030000000600000002000000040000000300000007000000020000000100000001000000010000000100000002000000030000000800000001000000010000000300000005000000030000000900000002000000010000000200000002000000030000000a000000020000000100000002000000020000000200000001000000"
        else:
            assert codecs.encode(compiled_grammar, "hex_codec") == b"0000000000000000040000001c0000001c000000010000004578616d706c65437573746f6d52756c650000000500000000000000060000000000000002000000900000000c0000000100000049000000100000000200000077616e74000000000c00000003000000746f00000c00000004000000656174000c00000005000000616e00000c000000060000006100000010000000070000006a7569637900000010000000080000006170706c6500000010000000090000006772656173790000140000000a00000068616d62757267657200000003000000e0000000e00000000100000001000000010000000100000001000000030000000100000003000000020000000300000003000000030000000400000002000000010000000100000002000000010000000100000001000000020000000300000005000000010000000100000003000000060000000300000007000000020000000100000002000000020000000300000008000000020000000100000001000000010000000300000006000000010000000400000003000000090000000200000004000000030000000a000000020000000100000002000000020000000200000001000000"

if __name__ == '__main__':
    unittest.main()
