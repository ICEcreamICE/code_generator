#!/usr/local/bin/python3
from cg_source.Overture import *
import json, os, re, sys, importlib
#from cg_class.globalizer import *

class LineParser (OVERTURE):
  def __init__ (self, src_file, dst_file, dict):
    self.stat = {}
    self.stat['RECORD_LINE_NUM'] = 1
    self.stat['VALID_IF']   = True
    self.stat['VALID_FOR']   = True
    self.stat['IF_CONDITION']    = None
    self.stat['IF_NEST_LEVEL']   = 0
    self.stat['FOR_NEST_LEVEL']   = 0
    self.stat['LOOP']            = 'COMPLETED'
    self.src_file = src_file
    self.dst_file = dst_file
    self.dict     = dict

  def if_branch(self, command, eval_content, line):
    _if_line = ''
    _space = ' '
    _TotalSpaceValue = 0
    _ifSpaceValue = 0
    _SpaceValue = 0
    
    _TotalSpaceValue = int(self.stat['IF_NEST_LEVEL'] + self.stat['FOR_NEST_LEVEL'])
    if int(_TotalSpaceValue) > 0:
      _ifSpaceValue = _TotalSpaceValue
      _SpaceValue = int(_TotalSpaceValue - 2)

    if command == 'IF':
      _eval_content = '' + eval_content + ':'
      _if_line = line + _space* _ifSpaceValue + 'if ' + _eval_content + '\n'
    elif command == 'ELSIF':
      _eval_content = '' + eval_content + ':'
      _if_line = line + _space* _SpaceValue + 'elif ' + _eval_content + '\n'
    elif command == 'ELSE':
      _if_line = line + _space* _SpaceValue + 'else:' + '\n'
    elif command == 'ENDIF':
      _if_line = line + '\n'
    #self.stat['VALID_IF'] = if_result
    #self.stat['IF_CONDITION'] = command
    if  (command == 'IF'):
      self.stat['IF_NEST_LEVEL'] = self.stat['IF_NEST_LEVEL'] + 2 #TODO add ID to suggest different command, IF/FOR
    elif (command == 'ENDIF'):
      self.stat['IF_NEST_LEVEL'] = self.stat['IF_NEST_LEVEL'] - 2
    return _if_line

#TODO: Not close FOR-ENDFOR loop will not be notified! comment ``FOR loop has bug (//``FOR)
  def for_loop(self, command, eval_content, line):
    _tmp_search = re.search ("\s?(\w+)\s?in\s?(.+)\s?", eval_content)
    _space = ' '
    _for_line = ''
    _SpaceValue = int(self.stat['FOR_NEST_LEVEL']) + int(self.stat['IF_NEST_LEVEL'])

    if (command == 'FOR'):
      if _tmp_search:
        if (_tmp_search[0] == None):
          print ("ERROR cannot found start loop value")
          exit()
        else:
          _for_line = line + _space*_SpaceValue + 'for ' + eval_content + ':\n'
      else:
        print ("Unsuported ``FOR condition! --> ", eval_content)
        exit(1)
    else:
      _for_line =  line + '\n'

    if  (command == 'FOR'):
      self.stat['FOR_NEST_LEVEL'] = self.stat['FOR_NEST_LEVEL'] + 2 #TODO add ID to suggest different command, IF/FOR
    elif (command == 'ENDFOR'):
      self.stat['FOR_NEST_LEVEL'] = self.stat['FOR_NEST_LEVEL'] - 2
    return _for_line

  def sub_func(self, being_matched):
    _qoute = self.QuoteStyleSelection(being_matched)
    being_matched = being_matched.strip('\n')
    _string_size = len(being_matched)
    _tmp = re.finditer ("``{([^}]*)}", being_matched)
    _start_stop_list = []
    _sub_line = ''
    _variable_list = []
    _first_iter = True
    _write_string = ''
    _tmp = list(_tmp) #_tmp type changed from iter to list CAUTION TODO: Fix it later
    if _tmp:
      for _value in list(_tmp):
        if _first_iter == True:
          #initial start location 0 (ZERO)
          _value_list = [0]
          _first_iter = False
#===========================================
        if 0:
          print ("=========")
          print (_value)
          print (_value.start(1))
          print (_value.end(1))
          print (_value.group(1))
          print ("=========")
#===========================================
        #Location befor ancher ``{
        _value_list.append(_value.start(1) - 3)
        #Location of the last of ancher
        _value_list.append(_value.start(1))
        #Location of the last character of variable
        _value_list.append(_value.end(1))
        #Location 
        _start_stop_list.append(_value_list)
        _value_list = []
  #new loop round start point after }
        _value_list.append(_value.end(1) + 1)
        if (_value.end(1) == _string_size):
          _loop_completed = True
        else:
          _loop_completed = False
    else:
      print ("Unsuported ``{} condition! --> ", being_matched)
      exit(1)

    if _loop_completed == False:
      _value_list.append(_string_size)
      _value_list.append('')
      _value_list.append('')
      _start_stop_list.append(_value_list)

    for _sstart, _send, _vstart, _vend in _start_stop_list:
      _svariable = 'being_matched' + '[' +  str(_sstart) + ':' + str(_send) + ']'
      if (_vstart != ''):
        _variable = 'being_matched[' +  str(_vstart) + ':' + str(_vend) + ']'
        _variable = eval(_variable)
        _variable = self.SubstituteFunctionName(_variable)
        _plus_string = ' + str('
        _plus_string_left_enbrace = ') +'
      else:
        _variable = ''
        _plus_string = ''
        _plus_string_left_enbrace = ''
      _svariable = eval(_svariable)
      _write_string = (_write_string
                       + _qoute + _svariable  + _qoute
                       + _plus_string
                       + _variable
                       + _plus_string_left_enbrace)
    return _write_string

  def variable_sub(self, command, eval_content, line):
    _sub_group = re.sub ('``(\w+)\s', self.sub_func, line)

  def substituter(self, line):
    _part1 = ''
    _part2 = ''
    _part3 = ''
    if re.search ("(.+)``(\w+)(.+)") != None:
      _part1 = '' 
    else:
      print ('Error from substituter')
      exit(1)

  def ParsePythonCommand(self, line):
    _writeString = ''
    _qoute = self.QuoteStyleSelection(line)
    _searchTriApostrophe = '\s?```(.+)'
    _searchTriApoString = '\s?````p((\s?)+)(.+)'
    _result = re.search(_searchTriApostrophe, line)
    _resultString = re.search(_searchTriApoString, line)
    # _writeString = " ".join([_qoute, _result.group(1), _qoute])
    if _resultString:
      _writeString = _resultString.group(1) + 'output_content.write(' + _resultString.group(3) + ")"
    else:
      _writeString = _result.group(1)
    return _writeString

  def Parser(self):
    MINE = self.dict
    parsing_file = self.src_file
    _space = ' '
    line_number  = 0
    SearchCfg      = '.?``CFG\s?{(.+)}(.+)?'
    search_if      = '.?``IF\s?{(.+)}(.+)?'
    search_elsif   = '.?``ELSIF\s?{(.+)}(.+)?'
    search_else    = '.?``ELSE(.+)?'
    search_endif   = '.?``ENDIF(.+)?'
    search_for     = '.?``FOR\s?{\s?(.+)\s?}\s?(.+)?'
    search_endfor  = '.?``ENDFOR(.+)?'
    search_content = '```'
    _dst_file_content = ''
    #exec (_InitialImport)
    with open (self.src_file, 'r') as parsing_file:
      sys.path.append("./RTL_CODE") 
      _Cfg = importlib.import_module ('CONF')
      file_lines = parsing_file.readlines()
      for line in file_lines:
        ResultCfg    = re.search(SearchCfg,    line)
        result_if    = re.search(search_if,    line)
        result_elsif = re.search(search_elsif, line)
        result_else  = re.search(search_else,  line)
        result_endif = re.search(search_endif, line)
        result_if    = re.search(search_if,    line)
        result_for   = re.search(search_for,   line)
        result_endfor = re.search(search_endfor, line)
        result_content = re.search(search_content, line)
        if re.search ('``CFG', line) != None:
          if (ResultCfg != None):
            try:
              _Resulteval = self.SubstituteFunctionName(ResultCfg.group(1))
              _Resulteval = eval(_Resulteval)
            except:
              print ("Wrong CFG syntax found, Please check! --->", ResultCfg.group(1))
              exit(1)
            if not _Resulteval:
              return 'None', False
            continue
          else:
            print ("Wrong CFG linefound, Please check! --->", line)
            exit(1)
        elif re.search ('//(.*)``', line) != None:
          continue
        else:
          if (result_if != None):
            eval_content = result_if.group(1)
            eval_content = self.SubstituteFunctionName(eval_content)
            _dst_file_content = self.if_branch('IF', eval_content, _dst_file_content)
          elif (result_elsif != None):
            eval_content = result_elsif.group(1)
            eval_content = self.SubstituteFunctionName(eval_content)
            _dst_file_content = self.if_branch('ELSIF', eval_content, _dst_file_content)
          elif (result_else != None):
            _dst_file_content = self.if_branch('ELSE', 'False', _dst_file_content)
          elif (result_endif != None):
            _dst_file_content = self.if_branch('ENDIF', 'False', _dst_file_content)
          elif (result_for != None):
            eval_content = result_for.group(1)
            eval_content = self.SubstituteFunctionName(eval_content)
            _dst_file_content = self.for_loop('FOR', eval_content, _dst_file_content)
          elif (result_endfor != None):
            _dst_file_content = self.for_loop('ENDFOR', 'False', _dst_file_content)
          elif (result_content != None):
            line = self.ParsePythonCommand(line)
            _dst_file_content = (_dst_file_content
                                 + _space * (int(self.stat['IF_NEST_LEVEL']) + int(self.stat['FOR_NEST_LEVEL']))
                                 + line
                                 + "\n"
                                 )
          else:
            if re.search ('``', line) != None:
              #TODO: causion this line may has \n as blow condition
              line = self.sub_func(line)
              _dst_file_content = (_dst_file_content
                                   + _space * (int(self.stat['IF_NEST_LEVEL']) + int(self.stat['FOR_NEST_LEVEL']))
                                   + "output_content.write ("
                                   + line
                                   + " + \"\\n\")\n"
                                   )
            else:
              _dst_file_content = (_dst_file_content
                                   + _space * (int(self.stat['IF_NEST_LEVEL']) + int(self.stat['FOR_NEST_LEVEL']))
                                   + "output_content.write (r\"\"\"" 
                                   + line.rstrip() 
                                   + " \"\"\"" 
                                   + "+\"\"\"\\n\"\"\")\n"
                                   )
            line_number += 1
    parsing_file.close()
    #print (self.dst_file)
    with open (self.dst_file, 'w') as output_content:
      #print (_dst_file_content)
      if self.stat['FOR_NEST_LEVEL'] != 0:
        print ("Unmatched ``FOR-``ENDFOR pair, please check!")
        exit(1)
      if self.stat['IF_NEST_LEVEL'] != 0:
        print ("Unmatched ``IF-``ELSEIF-``ELSE-``ENDIF pair, please check!")
        exit(1)
      #try:
      exec (compile(_dst_file_content, "my", mode='exec'))
      #except:
      #  print ("Failed to generate file, Please check your command;\nFile Name is -->", self.dst_file)
      #  exit(1)
      #output_content.write (_dst_file_content)
    return self.dst_file, True
