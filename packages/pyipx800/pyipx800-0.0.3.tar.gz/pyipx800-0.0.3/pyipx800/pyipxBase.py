import time

class pyipxBase:
  scan_interval = 5.0

  @staticmethod
  def setscaninterval(interval):
    pyipxBase.scan_interval = interval
  
  def __init__(self, ipx, id: int):
    self._ipx = ipx
    self.id = id
    self.name = None
    self._content = None

