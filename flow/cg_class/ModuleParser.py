from lzma import MODE_FAST
from opcode import hascompare
from operator import mod
from telnetlib import Telnet
from turtle import end_fill
from unicodedata import name
from cg_source.Overture import *
import re, sys

class LEXPARSER(OVERTURE):
  def __init__(self, verilogFile):
    self.inputFile=open(verilogFile, "r+")
    self.symbols={'[':']', '(': ')', '.':'('}
    self.ends={',', ';'}
    self.ignoreKeywords={'wire', 'reg'}
    self.keywords={'input', 'output', 'inout'}
    self.module='module'
    self.endmodule='endmodule'
    self.modules=self.GetModules()

  def GetOneCharacter(self):
    _character = self.inputFile.read(1)
    return _character
  
  def GetNextString(self, c):
    _character = c
    _text = str()
    while _character.isalnum() or _character == '_':
      _text += _character
      _character = self.GetOneCharacter()
    else:
      while not (_character.isalnum() or _character == '_'):
        _character = self.GetOneCharacter()
      else:
        while _character.isalnum() or _character == '_':
          _text += _character
          _character = self.GetOneCharacter()
    return _text, _character

  def GetWidth(self, c):
    _character = c
    _width = str()
    _location = self.inputFile.tell()
    while _character != '[':
      _character = self.GetOneCharacter()
      if _character in self.ends:
        self.inputFile.seek(_location)
        _character = self.GetOneCharacter()
        return '1', _character
    else:
      _width += _character
      while _character != ']':
        if _character == '\n':
          continue
        else:
          _character = self.GetOneCharacter()
          _width += _character
      else:
        if len(_character) == 0:
          print ('Cannot find right braket')
          exit(1)
        else:
          return _width, _character

  def GetExistSignals(self, c):
    _character = c
    _instSignal = list()
    while _character != ';':
      if _character == '.':
        _instSignal.append(self.GetNextString(_character))
      else:
        _character = self.GetOneCharacter()
    else:
      return _instSignal, _character

  def GetNextParen(self, c):
    _character = c
    _text = str()
    _start = int()
    _hasManualSignal=False
    while _character != '(':
      if _character == '#':
        while _character != ')':
          _character = self.GetOneCharacter()
      else:
        _character = self.GetOneCharacter()
    else:
      while _character != ';':
        if _character == ',':
          _start = self.inputFile.tell()
          _hasManualSignal = True
          _character = self.GetOneCharacter()
        elif not _hasManualSignal:
          if _character == ')':
            _start = self.inputFile.tell() - 1
            _character = self.GetOneCharacter()
          else:
            _character = self.GetOneCharacter()
        else:
          _character = self.GetOneCharacter()
      else:
        return _start, _character

  def GetModules(self):
    _character= self.GetOneCharacter()
    _text = str()
    _name = str()
    _start = int()
    _end = int()
    _cmd = str()
    _dict = dict()

    _module = dict()
    _modules = dict()

    _input = dict()
    _inputs = list()
    _output = dict()
    _outputs = list()
    _inout = dict()
    _inouts = list()

    _autoinst = dict()
    _autoinsts = list()

    _hasModuleName = False

    while len(_character) != 0:
      _character = self.GetOneCharacter()
      _text += _character
      if _character.isspace() or not (_character.isalnum() or _character == '_'):
        _text = str()
      elif not _hasModuleName:
        if _text == self.module:
          _start = self.inputFile.tell()
          _character = self.GetOneCharacter()
          _name, _character  = self.GetNextString(_character)
          _cmd = 'temp' + '={\'start\' : ' + str(_start) + '}'
          exec(_cmd, globals(), _dict)
          _module.update(_dict['temp'])
          _hasModuleName = True
        else:
          continue
      elif _text == self.endmodule:
        _end = self.inputFile.tell()
        _character = self.GetOneCharacter()
        _cmd = 'temp' + '={\'end\' : ' + str(_end) + '}'
        exec(_cmd, globals(), _dict)
        _module.update(_dict['temp'])
        _module['inputs'] = _inputs
        _module['outputs'] = _outputs
        _module['inouts'] = _inouts
        _module['autoinsts'] = _autoinsts
        _modules[_name] = _module
        #reset to default
        _hasModuleName = False
        _input = dict()
        _inputs = list()
        _output = dict()
        _outputs = list()
        _inout = dict()
        _inouts = list()
        _autoinst = dict()
        _autoinsts = list()
        _module = dict()
      elif _text in self.keywords:
        if _text == 'input':
          _input['width'], _character = self.GetWidth(_character)
          _input['name'], _character  = self.GetNextString(_character)
          while _input['name'] in self.ignoreKeywords:
            _input['name'], _character  = self.GetNextString(_character)
          _inputs.append(dict(_input))
        elif _text == 'output':
          _output['width'], _character = self.GetWidth(_character)
          _output['name'], _character = self.GetNextString(_character)
          while _output['name'] in self.ignoreKeywords:
            _output['name'], _character  = self.GetNextString(_character)
          _outputs.append(dict(_output))
        elif _text == 'inout':
          _inout['width'], _character = self.GetWidth(_character)
          _inout['name'], _character = self.GetNextString(_character)
          while _inout['name'] in self.ignoreKeywords:
            _inout['name'], _character  = self.GetNextString(_character)
          _inouts.append(dict(_inout))
        else:
          print ('wrong condition of keywords')
          exit(1)
      elif _text == 'AUTOINST':
        _character = self.GetOneCharacter()
        _autoinst['name'], _character = self.GetNextString(_character)
        _autoinst['start'], _character = self.GetNextParen(_character)
        _autoinst['pass'], _character = self.GetExistSignals(_character)
        _autoinsts.append(_autoinst)
      elif _text == self.module:
        print ('two module found without endmodule, syntax error')
        exit(1)
      else:
        continue
    else:
      if _name == None:
        print ('cannot found module in this file')
        exit(1)
      else:
        return _modules

  def TailDetermine(self, entireLength, currtentNum):
    _tail = str()
    _entireLengthNum = entireLength - 1
    if _entireLengthNum != currtentNum:
      _tail = '),\n'
    else:
      _tail = ')\n'
    return _tail

  def WidthTrim(self, width):
    _w = width
    if not ':' in _w:
      _w=''
    return _w


  def AutoGenerate(self):
    _start = int()
    _restStart = int()
    _contentsBeforeStart = str()
    _contentsRest = str()
    _portName = str()
    _instName = str()
    _line = str()
    _lines = '\n'
    _newFile = str()
    _totalPortsNum = int()
    _currentInstPortsNum = 0
    for _module in self.modules:
      if 'autoinsts' in self.modules[_module]:
        for _inst in self.modules[_module]['autoinsts']:
          _start = _inst['start']
          self.inputFile.seek(0)
          _contentsBeforeStart = self.inputFile.read(_start)
          self.inputFile.seek(_start)
          _contentsRest = self.inputFile.read()
          _auto = _inst['name']
          _totalPortsNum = (len(self.modules[_auto]['inputs']) 
                          + len(self.modules[_auto]['outputs']) 
                          + len(self.modules[_auto]['inouts'])
                          )
          for _input in self.modules[_auto]['inputs']:
            _portName = '.' + _input['name'] + ' '
            _instName = ('(' + _input['name']
                             + self.WidthTrim(_input['width'])
                             + self.TailDetermine(_totalPortsNum, _currentInstPortsNum)
                        )
            _line = _portName + _instName
            _lines = _lines + _line
            _currentInstPortsNum += 1
          for _output in self.modules[_auto]['outputs']:
            _portName = '.' + _output['name'] + ' '
            _instName = ('(' + _output['name'] 
                             + self.WidthTrim(_output['width'])
                             + self.TailDetermine(_totalPortsNum, _currentInstPortsNum)
                        )
            _line = _portName + _instName
            _lines = _lines + _line
            _currentInstPortsNum += 1
          for _inout in self.modules[_auto]['inouts']:
            _portName = '.' + _inout['name'] + ' '
            _instName = ('(' + _inout['name'] 
                             + self.WidthTrim(_inout['width']) 
                             + self.TailDetermine(_totalPortsNum, _currentInstPortsNum)
                        )
            _line = _portName + _instName
            _lines = _lines + _line
            _currentInstPortsNum += 1
        _newFile = _contentsBeforeStart + _lines + _contentsRest
    self.inputFile.seek(0)
    self.inputFile.truncate()
    self.inputFile.write(_newFile)
        #   self.inputFile.writelines(self.modules[_module]['autoinsts']['name'],'\n')
    self.inputFile.close()