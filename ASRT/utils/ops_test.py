#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2016-2099 Ailemon.net
#
# This file is part of ASRT Speech Recognition Tool.
#
# ASRT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# ASRT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ASRT.  If not, see <https://www.gnu.org/licenses/>.
# ============================================================================

"""
@author: nl8590687
ops.py单元测试
"""

import pytest
from ops import get_edit_distance

class TestGetEditDistance:
    def test_1(self):
        examle_input = ["abc", "abc"]
        examle_output = 0
        result = get_edit_distance(examle_input[0], examle_input[1])
        assert result == examle_output

    def test_2(self):
        examle_input = ["abc", "adc"]
        examle_output = 1
        result = get_edit_distance(examle_input[0], examle_input[1])
        assert result == examle_output

    def test_3(self):
        examle_input = ["abc", "a"]
        examle_output = 2
        result = get_edit_distance(examle_input[0], examle_input[1])
        assert result == examle_output

    def test_4(self):
        examle_input = ["abc", "addce"]
        examle_output = 3
        result = get_edit_distance(examle_input[0], examle_input[1])
        assert result == examle_output
