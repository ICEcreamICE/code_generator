from opcode import hascompare
from operator import mod
from telnetlib import Telnet
from cg_source.Overture import *
import re, sys

class LINE(OVERTURE):
  def __init__(self, line):
    self.line = line
    self.lineNum = 0
    self.linesplits = re.split("( )+", self.line)
    self.name = None #name, ohters(None)
    self.type = None #port, instance, reg/wire, others
    self.arrayCnt = 0
    self.width = []
    self.array = False
    self.direction = None #input/output
    self.autoInstancName=''
    self.autoInstanceSkipPort=''
    self.PortDeclaration = [
      'input', 'output', 'inout'
    ]
    self.SignalDeclaration = [
      'reg', 'wire'
    ]
    self.VerilogCMD = [
      'always', 'assign', 'case', 'endcase'
    ]
    self.keywords = [
      'always', 'assign', 'case', 'endcase', 'begin', 'end',
      'if', 'else'
    ]
    self.WidthAncher = '(\[.+:.+\])+'
    self.NameAncher = '([a-zA-Z0-9`_$]+)'
    self.LineAncher = '[,;]'
    self.InstanceAncher = '(\w+)'
    self.InstancePort = '\.(\w+)\s?\(.*\)\s?,'
    self.UpdateInfo(line)

  def HasKeyword(self, element, lst):
    for e in lst:
      if element == e:
        return True
      else:
        return False

  def HasComment(self, element):
    _result = re.search(r"//.+", element)
    if _result != None:
      return True
    else:
      return False
  
  def HasBracket(self, element):
    _result = re.search(self.WidthAncher, element)
    if _result != None:
      return True
    else:
      return False

  def UpdateInstanceSkipPort(self):
    pass

  def UpdateArray(self):
    self.arrayCnt = self.arrayCnt + 1
    if self.arrayCnt > 1:
      self.array = True

  def UpdateType(self, lst):
    if lst[0] in self.Signal:
      self.type = lst[0]
      lst = lst.pop(0)
      return lst
    else:
      print ("cannot find any type in port")
      exit(1)

  def UpdateWidth(self, lst):
      _result = re.search(self.WidthAncher, lst[0])
      if _result != None:
        self.width.append(lst)
        lst.pop(0)
        self.UpdateArray()
        return lst
      else:
        if self.arrayCnt < 1:
          self.width.append(0)
          self.UpdateArray()
        else:
          print ("wrong type in line", lst[0])
          exit(1)
        return lst

  def UpdateName(self, lst):
    _result = re.search(self.NameAncher, lst[0])
    if _result != None:
     self.name = _result.group(1)
     lst = lst.pop(0)
     return lst
    else:
      print ("name cannot found, abort!")
      exit(1)

  def UpdateDirection(self, lst):
    self.direction = lst[0]
    lst = lst.pop(0)
    return lst

  def UpdateMisc(self, lst):
    _isComment = False
    while len(lst) != 0:
      if not _isComment:
        if self.HasComment(lst):
          _isComment = True
          self.comment = ' '.jion(self.comment, lst[0])
          lst.pop(0)
          break
        else:
          lst = self.UpdateWidth(lst)
      else:
        self.comment = ' '.jion(self.comment, lst[0])
        lst.pop(0)

  def FindPorts(self):
    _isPort = False
    _list = self.linesplits
    if self.HasKeyword(_list[0], self.PortDeclaration):
      _list = self.UpdateDirection(_list[0])
      _isPort = True
      _list = self.UpdateType(_list)
      _list = self.UpdateWidth(_list)
      _list = self.UpdateName(_list)
      self.UpdateMisc(_list)
      return _isPort
    else:
      return _isPort
  
  def FindDeclaration(self):
    _isSignal = False
    _list = self.linesplits
    if self.HasKeyword(_list[0], self.SignalDeclaration):
      _isSignal = True
      _list = self.UpdateType(_list)
      _list = self.UpdateWidth(_list)
      _list = self.UpdateName(_list)
      self.UpdateMisc(_list)
      return _isSignal
    else:
      return _isSignal

  def FindInstance(self):
    _isInstance = False
    _list = self.linesplits
    for e in _list:
      if self.HasKeyword(e, self.keywords):
        return _isInstance
      else:
        continue
    return _isInstance

  def UpdateInfo(self):
    if self.FindPorts():
      return "port"
    elif self.FindDeclaration():
      return "signal"
    elif self.FindInstance():
      return "instance"
    else:
      return None


class MODULE(OVERTURE):
  def __init__(self):
    super().__init__()
    self.Name = "ModuleParser"
    self.LineNumber = 0
    self.PortDeclaration = {
      'input'  : True,
      'output' : True,
      'inout'  : True
    }
    self.LineType = {
      'direction' : 'input',
      'type'      : 'wire',
      'width'     : '31:0',
      'name'      : 'bus_signal0'
    }
    self.LineContents = {
      'line0': self.LineType
    }
    self.ModuleTree = {
      'ModuleName1' : {
        self.LineContents
      }
    }
    self.input = {}
    self.output = {}
    self.instance = {}

# input Type [MSB:LSB] SignalName --?[ArrayLeft:ArrayRight]--;
  def FindContents(self, lines):
    _lineDict={}
    _lineNumber=0
    for line in lines:
      exec('_lineDict', r'={line', _lineNumber, r':', LINE.UpdateInfo(line), r'}')
      _lineNumber+=1
    return _lineDict

class TOP():
  def __init__(self):
    self.Modules={}

  def ModuleDeclaration(self, lines, moduleName):
    _dictModule={}
    exec('_dictModule', r'={', moduleName, ':', MODULE.FindContents(lines), r'}')
    return _dictModule

class GLOBAL():
  def __init__(self):
    self.filelist=[]
    self.lineCache=[]
    self.moduleSearch=r'\s?module\s?(\w+)\s?(?'
    self.modules={}

  def FindModule(self, f):
    _moduleName=''
    for l in f:
      self.lineCache.append(l.strip('\n'))
      if 'endmodule' in l:
        self.modules=self.FileAnalyzer(_moduleName)
        self.lineCache=[]
        _moduleName=''
      elif re.search(self.moduleSearch, l):
        _result=re.search(self.moduleSearch, l)
        _moduleName=_result.group(1)
      else:
        continue

  def FileAnalyzer(self, moduleName):
    exec(str(moduleName), '=', TOP.ModuleDeclaration(self.lineCache))
    exec('self.modules.update', '(', str(moduleName), ')')

  def FileReader(self, lst):
    for f in lst:
      _file = open(f)
      self.FindModule(_file)
