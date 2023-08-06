#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from attr import dataclass

from warg.mixins.dict_mixins import IterDictValuesMixin

__author__ = "Christian Heider Nielsen"
__doc__ = ""

__all__ = ['Process']


@dataclass
class Process(IterDictValuesMixin):
  """
  __slots__=['used_gpu_mem',
               'device_idx',
               'name',
               'username',
               'memory_percent',
               'cpu_percent',
               'cmdline',
               'device_name',
               'create_time',
               'status',
               'pid']
"""

  __slots__ = ['used_gpu_mem',
               'device_idx',
               'name',
               'username',
               'memory_percent',
               'cpu_percent',
               'cmdline',
               'device_name',
               'create_time',
               'status',
               'pid']
  used_gpu_mem: Any
  device_idx: Any
  name: Any
  username: Any
  memory_percent: Any
  cpu_percent: Any
  cmdline: Any
  device_name: Any
  create_time: Any
  status: Any
  pid: Any

  def __post_init__(self):
    pass
