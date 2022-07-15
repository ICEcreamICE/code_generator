from lzma import MODE_FAST
from opcode import hascompare
from operator import mod
from ssl import VerifyFlags
from telnetlib import Telnet
from tempfile import tempdir
from turtle import end_fill
from unicodedata import name
from cg_source.Overture import *
import re, sys

class LEXPARSER(OVERTURE):
  def __init__(self, verilogFile):
    self.inputFile=open(verilogFile, "rb+")
    self.currentFile=verilogFile
    self.symbols={'[':']', '(': ')', '.':'('}
    self.ends={',', ';'}
    self.ignoreKeywords={'wire', 'reg'}
    self.keywords={'input', 'output', 'inout'}
    self.module='module'
    self.endmodule='endmodule'
    self.modules=self.GetModules()

  def TrimCR(self):
    fb = self.inputFile.read()
    new = fb.replace(b'\r\n', b'\n')
    self.inputFile.seek(0)
    self.inputFile.truncate()
    self.inputFile.write(new)
    self.inputFile=open(self.currentFile, "r+")

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

  def GetExistSignals(self, start):
    self.inputFile.seek(start)
    _character = self.GetOneCharacter()
    _instSignal = list()
    _instSignal.append(self.GetNextString(_character))
    _character = self.GetOneCharacter()
    return _instSignal, _character

  def GetNextParen(self, c):
    _character = c
    _start = int()
    _pass = list()
    _hasManualSignal=False
    while _character != '(':
      if _character == '#':
        while _character != ')':
          _character = self.GetOneCharacter()
      else:
        _character = self.GetOneCharacter()
    else:
      while _character != ';':
        if _character == '.':
          _hasManualSignal = True
          _pass.append(self.GetNextString(_character)[0])
          _character = self.GetNextString(_character)[1]
          _character = self.GetOneCharacter()
          _start = self.inputFile.tell()
        elif not _hasManualSignal:
          if _character == ')':
            _start = self.inputFile.tell() - 1
            _character = self.GetOneCharacter()
          else:
            _character = self.GetOneCharacter()
        else:
          _character = self.GetOneCharacter()
      else:
        return _start, _pass, _character

  def GetKeyWordsProperty(self, name, character):
    _c = character
    _cmd =str()
    _dict = dict()
    temp = dict()
    if name in self.keywords:
      _cmd = ''.join([r't=', f'self.GetWidth("{_c}")'])
      exec(_cmd, globals(), locals())
      temp['width'] = locals()['t'][0]
      _c = locals()['t'][1]
      _cmd = ''.join([r't=', f'self.GetNextString("{_c}")'])
      exec(_cmd, globals(), locals())
      temp['name'] = locals()['t'][0]
      _c = locals()['t'][1]
      while temp['name'] in self.ignoreKeywords:
        exec(_cmd, globals(), locals())
        temp['name'] = locals()['t'][0]
        _c = locals()['t'][1]
      _dict = temp
    return _dict, _c

  def GetModules(self):
    self.TrimCR()
    _character= self.GetOneCharacter()
    _text = str()
    _name = str()
    _start = int()
    _end = int()
    _cmd = str()
    _dict = dict()
    _module = dict()
    _modules = dict()
    _inputs = list()
    _outputs = list()
    _inouts = list()
    _autoinst = dict()
    _autoinsts = list()
    _return = tuple()
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
        _inputs = list()
        _outputs = list()
        _inouts = list()
        _autoinst = dict()
        _autoinsts = list()
        _module = dict()
      elif _text in self.keywords:
        _return = self.GetKeyWordsProperty(_text, _character)
        _cmd = ''.join(['_', _text, 's', '.append(_return[0])'])
        exec(_cmd, globals(), locals())
        _character = _return[1]
      elif _text == 'AUTOINST':
        _character = self.GetOneCharacter()
        _autoinst['name'], _character = self.GetNextString(_character)
        _autoinst['start'], _autoinst['pass'], _character = self.GetNextParen(_character)
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

  def GenInstPortDeclr(self, module, auto, name, total, current):
    _c = current
    _line = str()
    _lines = str()
    _pass = list()
    if len(self.modules[module]['autoinsts']) > 0:
      for _inst in self.modules[module]['autoinsts']:
        _pass = _inst['pass']

    for port in self.modules[auto][name]:
      if port['name'] in _pass:
        _c += 1
        continue
      else:
        _portName = '.' + port['name'] + ' '
        _instName = ('(' + port['name']
                         + self.WidthTrim(port['width'])
                         + self.TailDetermine(total, _c)
                    )
        _line = _portName + _instName
        _lines = _lines + _line
        _c += 1
    return _lines, _c

  def AutoGenerate(self):
    _start = int()
    _contentsBeforeStart = str()
    _contentsRest = str()
    _inputLines = str()
    _outputLines = str()
    _inputLines = str()
    _lines = '\n'
    _newFile = str()
    _totalPortsNum = int()
    _currentInstPortsNum = 0
    for _module in self.modules:
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
        _inputLines, _currentInstPortsNum = self.GenInstPortDeclr(_module, _auto, 'inputs', _totalPortsNum, _currentInstPortsNum)
        _outputLines, _currentInstPortsNum = self.GenInstPortDeclr(_module, _auto, 'outputs', _totalPortsNum, _currentInstPortsNum)
        _inoutLines, _currentInstPortsNum = self.GenInstPortDeclr(_module, _auto, 'inouts', _totalPortsNum, _currentInstPortsNum)

        _lines = _lines + _inputLines + _outputLines + _inoutLines
      _newFile = _contentsBeforeStart + _lines + _contentsRest
    self.inputFile.seek(0)
    self.inputFile.truncate()
    self.inputFile.write(_newFile)
    self.inputFile.close()