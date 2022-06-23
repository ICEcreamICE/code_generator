from cg_source.Overture import *
import re, sys

class ModuleParser(OVERTURE):
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

  def FindContents(self, key, regex, line):
    _lineLST = re.split('( )+', line)
    _re = ''.join('(', regex, ')')
    _group = _re.search(line)
    
    return 
