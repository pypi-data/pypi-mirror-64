# -*- coding: utf-8 -*-

import collections
import time
from threading import Lock

from pyipx800 import pyipxBase

class Relay(pyipxBase.pyipxBase):
  """Representing IPX800 Relay."""
  _mutex = Lock()
  _updatets = time.time()

  def __init__(self, ipx, id: int):
    super().__init__(ipx, id)

  def update(self):
    with Relay._mutex:
      if (self._content==None or (time.time() - Relay._updatets >= pyipxBase.pyipxBase.scan_interval)):
        self._content = self._ipx.request({"Get": "R"})
        Relay._updatets = time.time()
    return self._content

  @staticmethod
  def len(ipx):
    return len(ipx.request({"Get": "R"}))

  @property
  def state(self) -> bool:
    """Return the current Relay status."""
    self.update()
    return self._content[f"R{self.id}"] == 1

  def on(self) -> bool:
    """Turn on an Relay and return True if it was successful."""
    params = {"SetR": self.id}
    self._ipx.request(params)
    return True

  def off(self) -> bool:
    """Turn off an Relay and return True if it was successful."""
    params = {"ClearR": self.id}
    self._ipx.request(params)
    return True

  def toggle(self) -> bool:
    """Toggle an Relay and return True if it was successful."""
    params = {"ToggleR": self.id}
    self._ipx.request(params)
    return True

