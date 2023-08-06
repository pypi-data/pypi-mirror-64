# -*- coding: utf-8 -*-

import collections
import time
from threading import Lock

from pyipx800 import pyipxBase

class VirtualInput(pyipxBase.pyipxBase):
  """Representing an IPX800 VirtualInput."""
  _mutex = Lock()
  _updatets = time.time()

  def __init__(self, ipx, id: int):
    super().__init__(ipx, id)

  def update(self):
    with VirtualInput._mutex:
      if (self._content==None or (time.time() - VirtualInput._updatets >= pyipxBase.pyipxBase.scan_interval)):
        self._content = self._ipx.request({"Get": "VI"})
        VirtualInput._updatets = time.time()
    return self._content

  @staticmethod
  def len(ipx):
    return len(ipx.request({"Get": "VI"}))

  @property
  def state(self) -> bool:
    """Return the current VirtualInput status."""
    self.update()
    return self._content[f"VI{self.id}"] == 1

  def on(self) -> bool:
    """Turn on a VI and return True if it was successful."""
    params = {"SetVI": self.id}
    self._ipx.request(params)
    return True

  def off(self) -> bool:
    """Turn off a VI  and return True if it was successful."""
    params = {"ClearVI": self.id}
    self._ipx.request(params)
    return True

  def toggle(self) -> bool:
    """Toggle a VI and return True if it was successful."""
    params = {"ToggleVI": self.id}
    self._ipx.request(params)
    return True


class VirtualOutput(pyipxBase.pyipxBase):
  """Representing an IPX800 VirtualOutput."""
  _mutex = Lock()
  _updatets = time.time()

  def __init__(self, ipx, id: int):
    super().__init__(ipx, id)

  def update(self):
    with VirtualOutput._mutex:
      if (self._content==None or (time.time() - VirtualOutput._updatets >= pyipxBase.pyipxBase.scan_interval)):
        self._content = self._ipx.request({"Get": "VO"})
        VirtualOutput._updatets = time.time()
    return self._content

  @staticmethod
  def len(ipx):
    return len(ipx.request({"Get": "VO"}))

  @property
  def state(self) -> bool:
    """Return the current VirtualInput status."""
    self.update()
    return self._content[f"VO{self.id}"] == 1

  def on(self) -> bool:
    """Turn on a VO and return True if it was successful."""
    params = {"SetVO": self.id}
    self._ipx.request(params)
    return True

  def off(self) -> bool:
    """Turn off a VO and return True if it was successful."""
    params = {"ClearVO": self.id}
    self._ipx.request(params)
    return True

  def toggle(self) -> bool:
    """Toggle a VO and return True if it was successful."""
    params = {"ToggleVO": self.id}
    self._ipx.request(params)
    return True



class VirtualAnalog(pyipxBase.pyipxBase):
  """Representing an IPX800 VirtualAnalog."""
  _mutex = Lock()
  _updatets = time.time()

  def __init__(self, ipx, id: int):
    super().__init__(ipx, id)

  def update(self):
    with VirtualAnalog._mutex:
      if (self._content==None or (time.time() - VirtualAnalog._updatets >= pyipxBase.pyipxBase.scan_interval)):
        self._content = self._ipx.request({"Get": "VA"})
        VirtualAnalog._updatets = time.time()
    return self._content

  @staticmethod
  def len(ipx):
    return len(ipx.request({"Get": "VA"}))

  @property
  def state(self) -> int:
    """Return the current VirtualAnalog value."""
    self.update()
    return self._content[f"VA{self.id}"] 

  def set(self, value) -> bool:
    """Change VA value and return True if it was successful."""
    params = { "SetVA{:02d}".format(self.id): value}
    self._ipx.request(params)
    return True

