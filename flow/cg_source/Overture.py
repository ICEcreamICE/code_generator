#!/usr/local/bin/python3
import json, os, re, random, sys, importlib

class OVERTURE():
  def __init__ (self):
    self.Name = 'ROOT'
    self.User = os.environ['USER']
    self.RanColor = str(random.randint(32,36))
    self.LogColor = '\033[1;' + self.RanColor + 'm'
    self.ColorEnd = '\033[0m'
    self.Debug = 0

  def Printer(self, src):
    _Type = type(src)
    if 'array' in _Type:
      for _Element in src:
        print ('Array ', '>' * 44)
        print (src)
        print ('<' * 50)
    elif 'dict' in _Type:
      for _Element in src:
        print ('Dict ', '=' * 45)
        print (src)
        print ('=' * 50)
    else:
      print (_Type, '-' * 50)
      print (src)
      print ('-' * 50)

  def IsHex(self, src):
    try:
      int(src, base=16)
      return True
    except:
      pass
    return False

  def LogPrinter(self, str):
    print (self.LogColor, self.Name, ':\n', str, self.ColorEnd)

  def FailPrinter(self, str):
    print ('\033[1;31m', self.Name, ':\n', str, self.ColorEnd)
    
  def ColorPrinter(self, input, debug=0):
    if debug:
      print()
      print (self.LogColor, self.Name, ':', self.ColorEnd)
    if (type(input) == list):
      for _element in input:
        print (self.LogColor, _element, self.ColorEnd)
    elif (type(input) == dict):
      for _key in input:
        print (self.LogColor, _key, '=>', input[_key], self.ColorEnd)
    else:
      print (self.LogColor, input, self.ColorEnd)

  def ReadJson(self, file):
    with open (file, 'r') as jsonF:
      _Dict = json.load(jsonF)
      jsonF.close()
    return _Dict

  def CheckKeyExistence(self, key='', dict={}):
    if key in dict.keys():
      return True
    else:
      return False

  def CheckKeyValueExistence(self, key='', dict={}):
    if self.CheckKeyExistence(key, dict):
      if dict[key] != None:
        return True
      else:
        return False
    else:
      self.FailPrinter('Key not exist!')
      exit(1)

  def CheckDirExistence(self, regex='', dir=''):
    if regex:
      if dir:
        regex = regex
        dir = dir
      else:
        regex = regex
        dir = os.getcwd()
    else:
      _Str = 'Must provided a matching pattern!'
      self.LogPrinter (_Str)
      exit(1)
    return re.search(regex, dir)

  def CheckDirHasFile(self, input):
    FileType = type(input)
    ErrCount = 0
    if (FileType is list) or (FileType is dict):
      for file in input:
        if (os.listdir(file)):
          pass
        else:
          ErrCount += 1
      if ErrCount > 0:
        return False
      else:
        return True
    else:
      if (os.listdir(input)):
        return True
      else:
        return False

  def Cleaner(self, top):
    for root, dirs, files in os.walk(top, topdown=False):
      for name in files:
        if ('rtl' in root or 'ver' in root or 'analog' in root or self.MainDict['TEST'] in root or 'pst' in root):
          if os.path.islink(os.path.join(root, name)):
            os.unlink(os.path.join(root, name))
          else:
            os.remove(os.path.join(root, name))
      for name in dirs:
        if ('rtl' in root or 'ver' in root or 'analog' in root or self.MainDict['TEST'] in root or 'pst' in root):
          if os.path.islink(os.path.join(root, name)):
            os.unlink(os.path.join(root, name))
          else:
            os.rmdir(os.path.join(root, name))

  def WriteFile(self, fileName, List, type):
    with open (fileName, type) as RunFile:
      for file in List:
        RunFile.write (file + '\n')
      RunFile.close()

  def ReturnVerilogValue(self, QuotH=[], Size=8):
    _SumUp = 0
    if len(QuotH) > 1:
      for _Value in QuotH:
        _Tmp = 0
        if "'h" in _Value:
          return _Value
        else:
          _Tmp = int(_Value, base=16)
        _SumUp = _SumUp + _Tmp
    else:
      _Value = QuotH[0]
      if "'h" in _Value:
        return _Value
      else:
        _SumUp = int(_Value, base=16)
    return (str(Size) + "'h" + str(hex(_SumUp)[2:]))

  def SubstituteFunctionName(self, src):
    _SearchFunctionName = '(`)((\w+)\((\w?)+\))'
    _SubstitueFunctionName = 'Cfg.CF(MINE).\g<2>'
    _SearchFunctionNameResult = re.search(_SearchFunctionName, src)
    if _SearchFunctionNameResult != None:
      _SearchFunctionReplace = re.sub(_SearchFunctionName, _SubstitueFunctionName, src)
      return _SearchFunctionReplace
    else:
      _SearchFunctionReplace = src
      return _SearchFunctionReplace

  def CheckConditions(self, dict, InCond):
    MINE = dict
    SearchBrace = '.?``{(.+)}.?'
    #print (">>>>", len(InCond))
    sys.path.append (dict['CF_DIR'])
    _Cfg = importlib.import_module ('CF')
    _Condition = ''
    _ReturnVal = ''
    if type(InCond) == list:
      if (len(InCond) > 0):
        for Cond in InCond:
          _Result = re.search (SearchBrace, Cond)
          if _Result is not None:
            Cond = self.SubstituteFunctionName(_Result.group(1))
          _Condition = _Condition + ' ' + Cond
        try:
          _ReturnVal = eval(_Condition)
          return (_ReturnVal)
        except:
          print ("%s Wrong condition found, Plese check! --->", self.Name, InCond)
          exit(1)
      else:
        print ("ERROR! Plase check cfg file condition")
        exit(1)
    else:
      _Condition = InCond
      _Result = re.search (SearchBrace, _Condition)
      if _Result:
        _Condition = self.SubstituteFunctionName(_Result.group(1))
      try:
        _ReturnVal = eval(_Condition)
        return (_ReturnVal)
      except:
        print ("Wrong condition found, Plese check! --->", self.Name, InCond)
        exit(1)  