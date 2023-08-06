# -*- coding: utf-8 *-*

import collections
import warnings
import requests
import re
import datetime
import time
import warnings

from datetime import timedelta
from requests_xml import XMLSession
from socket import timeout
from threading import Lock

from pyipx800.pyipxInput import Input
from pyipx800.pyipxRelay import Relay
from pyipx800.pyipxAnalog import Analog
from pyipx800.pyipxCounter import Counter
from pyipx800.pyipxVirtuals import VirtualInput, VirtualOutput, VirtualAnalog
from pyipx800.pyipxBase import pyipxBase

class ApiError(Exception):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class pyipx800:
  """Class representing the IPX800 and its API."""

  def __init__(self, host, port, api_key="apikey"):
    self.mutex = Lock()
    self._base_url = f"http://{host}:{port}"
    self._api_key = api_key
    self._api_url = f"{self._base_url}/api/xdevices.json"
    self._names_xml_url = f"{self._base_url}/global.xml"
    self._status_xml_url = f"{self._base_url}/user/status.xml"
    self.trace = True
    self.inputs = None
    self.relays = None
    self.analogs = None
    self.counters = None
    self.virt_inputs = None
    self.virt_outputs = None
    self.virt_analogs = None
    
  def request(self, params):
    with self.mutex:
      params_fix = {"key": self._api_key}
      params_fix.update(params)
      try:
        r = requests.get(self._api_url, params=params_fix, timeout=2)
      except timeout as ex:
        warnings.warn("Unable to connect to IPX: %s", str(ex))
        raise ApiError('Connect timeout')
      if (self.trace):
        print("Request ", r.url)
      r.raise_for_status()
      content = r.json()
      result = content.pop("status", None)
      product = content.pop("product", None)
      if product != "IPX800_V4":
        warnings.warn(f"Your device '{product}' might not be compatible")
      if result == "Success":
        if (self.trace):
          print("Content:", content)
        return content
      else:
        if (self.trace):
          print("status:", result)   
        raise ApiError('Not successfull')

  def retrieve_names(self):
    ''' Requests custom names configured in IPX800 UI '''
    session = XMLSession()
    res = session.get(self._names_xml_url)

    if res.status_code == 200:
      for r in self.relays:
        idx = int(r.id)
        _name = res.xml.xpath('//response/output%d' % idx, first=True).text
        self.relays[idx-1].name = _name
      for r in self.inputs:
        idx = int(r.id)
        _name = res.xml.xpath('//response/input%d' % idx, first=True).text
        self.inputs[idx-1].name = _name
      for r in self.analogs:
        idx = int(r.id)
        _name = res.xml.xpath('//response/analog%d' % idx, first=True).text
        self.analogs[idx-1].name = _name
      for r in self.virt_analogs:
        idx = int(r.id)
        _name = res.xml.xpath('//response/analogVirt%d' % idx, first=True).text
        self.virt_analogs[idx-1].name = _name
      for r in self.counters:
        idx = int(r.id)
        _name = res.xml.xpath('//response/compt%d' % idx, first=True).text
        self.counters[idx-1].name = _name
      for r in self.virt_inputs:
        idx = int(r.id)
        _name = res.xml.xpath('//response/inputVirt%d' % idx, first=True).text
        self.virt_inputs[idx-1].name = _name
      for r in self.virt_outputs:
        idx = int(r.id)
        _name = res.xml.xpath('//response/outputVirt%d' % idx, first=True).text
        self.virt_outputs[idx-1].name = _name
    else:
      print("No response when asking for names")

  def configure(self):
    ''' Inputs '''
    self.inputs = []
    for r in range(Input.len(self)):
      self.inputs.append(Input(self,r+1))

    ''' Relays '''
    self.relays = []
    for r in range(Relay.len(self)):
      self.relays.append(Relay(self,r+1))

    ''' Analogs '''
    self.analogs = []
    for r in range(Analog.len(self)):
      self.analogs.append(Analog(self,r+1))

    ''' Counters '''
    self.counters = []
    for r in range(Counter.len(self)):
      self.counters.append(Counter(self,r+1))

    ''' Virtuals '''
    self.virt_inputs = []
    for r in range(VirtualInput.len(self)):
      self.virt_inputs.append(VirtualInput(self,r+1))
      
    self.virt_outputs = []
    for r in range(VirtualOutput.len(self)):
      self.virt_outputs.append(VirtualOutput(self,r+1))
      
    self.virt_analogs = []
    for r in range(VirtualAnalog.len(self)):
      self.virt_analogs.append(VirtualAnalog(self,r+1))

    self.retrieve_names()

