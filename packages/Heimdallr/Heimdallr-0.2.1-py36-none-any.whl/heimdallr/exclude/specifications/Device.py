#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from attr import dataclass

from warg.mixins.dict_mixins import IterDictValuesMixin

__author__ = "Christian Heider Nielsen"
__doc__ = ""

__all__ = ['Device']


@dataclass
class Device(IterDictValuesMixin):
  """
  __slots__=['id', 'name', 'free', 'used', 'total', 'processes']
"""

  __slots__ = ['id',
               'name',
               'free',
               'used',
               'total',
               'processes']
  id: Any
  name: Any
  free: Any
  used: Any
  total: Any
  processes: Any

  def __post_init__(self):
    pass
