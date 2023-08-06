# -*- coding: utf-8 -*-

import collections
import time
from threading import Lock

from pyipx800 import pyipxBase

class Counter(pyipxBase.pyipxBase):
  """Representing an IPX800 Counter."""
  _mutex = Lock()
  _updatets = time.time()

  def __init__(self, ipx, id: int):
    super().__init__(ipx, id)

  def update(self):
    with Counter._mutex:
      if (self._content==None or (time.time() - Counter._updatets >= pyipxBase.pyipxBase.scan_interval)):
        self._content = self._ipx.request({"Get": "C"})
        Counter._updatets = time.time()
      return self._content

  @staticmethod
  def len(ipx):
    return len(ipx.request({"Get": "C"}))

  @property
  def state(self) -> int:
    """Return the current Counter status."""
    self.update()
    return self._content[f"C{self.id}"]


