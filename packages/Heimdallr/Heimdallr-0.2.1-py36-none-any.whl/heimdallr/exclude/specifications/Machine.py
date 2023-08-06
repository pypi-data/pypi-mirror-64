#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from attr import dataclass

from warg.mixins.dict_mixins import IterDictValuesMixin

__author__ = "Christian Heider Nielsen"
__doc__ = ""

__all__ = ['Machine']


@dataclass
class Machine(IterDictValuesMixin):
  """
  __slots__=["name", "device"]
"""

  __slots__ = ["name", "device"]
  name: Any
  device: Any

  def __post_init__(self):
    pass
