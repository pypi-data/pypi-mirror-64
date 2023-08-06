# -*- coding: utf-8 -*-

import collections
import time
from threading import Lock

from pyipx800 import pyipxBase

class Analog(pyipxBase.pyipxBase):
  """Representing an IPX800 Analog."""
  _mutex = Lock()
  _updatets = time.time()

  def __init__(self, ipx, id: int):
    super().__init__(ipx, id)

  def update(self):
    with Analog._mutex:
      if (self._content==None or (time.time() - Analog._updatets >= pyipxBase.pyipxBase.scan_interval)):
        self._content = self._ipx.request({"Get": "A"})
        Analog._updatets = time.time()
    return self._content

  @staticmethod
  def len(ipx):
    return len(ipx.request({"Get": "A"}))

  @property
  def state(self) -> int:
    """Return the current Analog status."""
    self.update()
    return self._content[f"A{self.id}"]

