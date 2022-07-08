from lzma import MODE_FAST
from opcode import hascompare
from operator import mod
from telnetlib import Telnet
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
      _character = self.GetOneCharacter()
      if _character == '.':
        _instSignal.append(self.GetNextString(_character))
      else:
        continue
    else:
      return _instSignal, _character



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
        _module['output'] = _outputs
        _module['inout'] = _inout
        _module['autoinsts'] = _autoinsts
        _modules[_name] = _module
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
        _autoinst['mame'], _character = self.GetNextString(_character)
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


  # def GetModuleProperties(self):
  #   _character = self.GetOneCharacter()
  #   _text = _character
  #   _moduleName=str
  #   _moduleStartPoint=int
  #   while len(_character) != 0:
  #     _text = _character
  #     while not _character.isspace():
  #       _character = self.GetOneCharacter()
  #       _text += _character
  #     else:
  #       if _text in self.keywords:
  #         self.
  #     _character = self.GetOneCharacter()



  # def GetFollowingSymbol(self, start, expect):
  #   _text = start
  #   _character = self.GetOneCharacter()
  #   while _character != expect:
  #     if _character in self.ends:
  #       print ('find end of Command before', start, expect, 'pairs')
  #       exit(1)
  #     elif _character == '\n':
  #       continue
  #     _test += _character
  #   return _text
  
  # def GetToken(self, c):
  #   _text = c
  #   if _text in self.keywords:



  # def Searching(self):
  #   _character=self.GetOneCharacter()
  #   _text = ''
  #   while len(_character) != 0:
  #     if _character.isspace:
  #       _text = ''
  #     elif _character.isalnum or _character == '_':
  #       _text += _character
  #       self.GetToken(_text)
      


 
    # err_line = the_line
    # err_col  = the_col
 
    # if len(_character) == 0:
    #   return tk_EOI, err_line, err_col
    # elif _character == '[':
    #   self.GetFollowingSymbol('[', self.symbols['['])
    # elif _character == '/':     return div_or_cmt(err_line, err_col)
    # elif _character == '\'':    return char_lit(err_line, err_col)
    # elif _character == '<':     return follow('=', tk_Leq, tk_Lss,    err_line, err_col)
    # elif _character == '>':     return follow('=', tk_Geq, tk_Gtr,    err_line, err_col)
    # elif _character == '=':     return follow('=', tk_Eq,  tk_Assign, err_line, err_col)
    # elif _character == '!':     return follow('=', tk_Neq, tk_Not,    err_line, err_col)
    # elif _character == '&':     return follow('&', tk_And, tk_EOI,    err_line, err_col)
    # elif _character == '|':     return follow('|', tk_Or,  tk_EOI,    err_line, err_col)
    # elif _character == '"':     return string_lit(_character, err_line, err_col)
    # elif _character in self.symbols:
    #   _end = self.symbols[_character]
    #   self.GetOneCharacter()
    #   return sym, err_line, err_col
    # else: return ident_or_int(err_line, err_col)

class LINE(OVERTURE):
  def __init__(self, line, number):
    self.line = line.rstrip()
    self.lineNum = number
    self.linesplits = re.split(" ", self.line.strip(',|;'))
    self.name = None #name, ohters(None)
    self.type = None #port, instance, reg/wire, others
    self.arrayCnt = 0
    self.width = []
    self.array = False
    self.direction = None #input/output
    self.instanceName = None
    self.instancePort = None
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
    self.InstancePortAncher = '\.(\w+)'
    self.commentAncher = '\/\/'
    self.attribute = self.UpdateInfo()
  
  def IsBlankLine(self, line):
    _result=re.search('^[ ]*$', line)
    if _result != None:
      return True
    else:
      return False

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

  def UpdateInstance(self, lst):
    if re.search(self.LineAncher, self.line):
      return False
    else:
      if re.search(self.InstanceAncher, lst[0]):
        self.instanceName=lst[0]
        return True
      elif re.search(self.InstancePortAncher, lst[0]):
        self.instancePort=lst[0]
        return True
      else:
        print ('wrong verilog syntax, please check!', '--->', lst[0], 'in', self.line, 'line num: ', self.lineNum)
        exit(0)

  def UpdateArray(self):
    self.arrayCnt = self.arrayCnt + 1
    if self.arrayCnt > 1:
      self.array = True

  def UpdateType(self, lst):
    if (lst[0]) in self.SignalDeclaration:
      self.type = lst.pop(0)
      # self.direction = lst.pop(0)
      return lst
    else:
      print ("cannot find any type in port")
      exit(1)

  def UpdateWidth(self, lst):
      _result = re.search(self.WidthAncher, lst[0])
      print ('array cnt id is', id(self.arrayCnt))
      if _result != None:
        self.width.append(lst.pop(0))
        self.UpdateArray()
        return lst
      else:
        if self.arrayCnt < 1:
          self.width.append(0)
          self.UpdateArray()
        elif self.arrayCnt == 1:
          pass
        else:
          print ("wrong type in line", lst[0])
          exit(1)
        return lst

  def UpdateName(self, lst):
    _result = re.search(self.NameAncher, lst[0])
    if _result != None:
     self.name = _result.group(1)
     lst.pop(0)
     return lst
    else:
      print ("name cannot found, abort!")
      exit(1)

  def UpdateDirection(self, lst):
    # self.direction = lst[0]
    self.direction = lst.pop(0)
    # lst = lst.pop(0)
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

  def FindBlank(self):
    return self.IsBlankLine(self.line)

  def FindComment(self):
    _isComment = False
    _list = self.linesplits
    if len(_list) == 0:
      return _isComment
    elif re.search(self.commentAncher, _list[0]):
      _isComment = True
      return _isComment
    else:
      return _isComment

  def FindPorts(self):
    _isPort = False
    _list = self.linesplits
    if self.HasKeyword(_list[0], self.PortDeclaration):
      _list = self.UpdateDirection(_list)
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
        self.UpdateInstance(_list)
    return _isInstance

  def UpdateInfo(self):
    if self.FindBlank():
      return r"blank"
    elif self.FindComment():
      return r"comment"
    elif self.FindPorts():
      return r"port"
    elif self.FindDeclaration():
      return r"signal"
    elif self.FindInstance():
      return r"instance"
    else:
      return None


class MODULE(OVERTURE):
  def __init__(self):
    # super().__init__()
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
      'ModuleName1' : [
        self.LineContents
      ]
    }
    self.input = {}
    self.output = {}
    self.instance = {}
    self.line=''

# input Type [MSB:LSB] SignalName --?[ArrayLeft:ArrayRight]--;
  def FindContents(self, lines):
    _lineDict={}
    _lineNumber=0
    for line in lines:
      print (_lineNumber, line)
      _key = 'line' + str(_lineNumber)
      _execContents= ''.join(['temp', '=', 'LINE(line, _lineNumber)'])
      # print(id(_line))
      # _execContents=''.join(['_lineDict', '={\'line', str(_lineNumber), '\':', LINE(line, _lineNumber), '}'])
      print ('a')
      exec(_execContents, globals(), locals())
      print ('b', '\n', locals())

      _lineDict[_key] = locals()['temp']
      # _execContents=''.join(['_lineDict', '={\'_line', str(_lineNumber), '\':', '_line.UpdateInfo()', '}'])
      # exec('_lineDict', r'={line', _lineNumber, r':', line.UpdateInfo(), r'}')
      # print ('a')
      # exec(_execContents)
      # print ('b', '\n')
      _lineNumber+=1
    return _lineDict

class TOP():
  def __init__(self):
    self.modules={}
    self.module=MODULE()

  def ModuleDeclaration(self, lines): #, moduleName):
    _dictModule={}
    # exec('_dictModule', r'={', moduleName, ':', MODULE.FindContents(lines), r'}')
    _dictModule = self.module.FindContents(lines)
    return _dictModule

class GLOBAL():
  def __init__(self, fileList):
    self.top=TOP()
    self.fileList=fileList
    self.lineCache=[]
    self.moduleSearch=r'\s?module\s(\w+)\s?\(?'
    self.modules={}
    self.FileReader(fileList)

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
    _execContents=''.join([str(moduleName), '=', 'self.top.ModuleDeclaration(self.lineCache)'])
    exec(_execContents)
    exec('self.modules.update', '(', str(moduleName), ')')

  def FileReader(self, lst):
    for f in lst:
      _file = open(f)
      self.FindModule(_file)
