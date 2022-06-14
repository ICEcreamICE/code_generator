#!/usr/local/bin/python3
from cg_source.Overture import *
import json, os, re, sys, importlib
#from cg_class.globalizer import *

class LineParser (OVERTURE):
  def __init__ (self, src_file, dst_file, dict):
    #print ('init LineParser')
    self.stat = {}
    self.stat['RECORD_LINE_NUM'] = 1
    self.stat['VALID_IF']   = True
    self.stat['VALID_FOR']   = True
    self.stat['IF_CONDITION']    = None
    self.stat['IF_NEST_LEVEL']   = 0
    self.stat['FOR_NEST_LEVEL']   = 0
    self.stat['LOOP']            = 'COMPLETED'
      #'RECORD_LINE_NUM': 1 | 2 | 3 | ...
      #'VALID_FOR_GEN'  : YES | NO
      #'IF_CONDITION'   : IF | ELSIF | ELSE | ENDIF | None
      #'IF_NEST_LEVEL'  : 0 | 1 | 2 | ...
      #'LOOP'           : RUNNING | COMPLETED
    self.src_file = src_file
    self.dst_file = dst_file
    self.dict     = dict
#    self.glbs = Globalizer()

  def if_branch(self, command, eval_content, line):
    _if_line = ''
    _space = ' '
    _TotalSpaceValue = 0
    _ifSpaceValue = 0
    _SpaceValue = 0
    
    _TotalSpaceValue = int(self.stat['IF_NEST_LEVEL'] + self.stat['FOR_NEST_LEVEL'])
    #print (command)
    if int(_TotalSpaceValue) > 0:
      _ifSpaceValue = _TotalSpaceValue
      _SpaceValue = int(_TotalSpaceValue - 2)

#    _SpaceValue = _SpaceValue + int(self.stat['FOR_NEST_LEVEL'])
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

    #line_number += 1
    return _if_line
#    self.stat[line_number].update({'VALID_IF': if_result})

#TODO: Not close FOR-ENDFOR loop will not be notified! comment ``FOR loop has bug (//``FOR)
  def for_loop(self, command, eval_content, line):
    #print (eval_content)
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
    if re.search('"', being_matched):
      _qoute = "'''"
    else:
      _qoute = '"""'
    being_matched = being_matched.strip('\n')
    _string_size = len(being_matched)
    _tmp = re.finditer ("``{([^}]*)}", being_matched)
    _start_stop_list = []
    _sub_line = ''
    _variable_list = []
    _first_iter = True
    _write_string = ''
    #print (_string_size)
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

    #print(len(being_matched))
    #print (being_matched[0:11])
    #print (being_matched[14:25])
    #print (being_matched[28:34])
    #print (being_matched[37:38])
    #print ("END")
    #print (_start_stop_list)
    #print (being_matched)
    for _sstart, _send, _vstart, _vend in _start_stop_list:
      #print (_sstart)
      #print (_send)
      #print (_vstart)
      #print (_vend)
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
      #print(_svariable)
      _write_string = (_write_string
                       + _qoute + _svariable  + _qoute
                       + _plus_string
                       + _variable
                       + _plus_string_left_enbrace)
      #print (_write_string)
      #_sub_line = _sub_line + being_matched[
    #print (_write_string)
    #exit()
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

  def Parser(self):
    MINE = self.dict
    #print ('parsing...')
    #for f in func_list:
    #  TEST_COND = self.f()
    #print (self.TEST_COND())
    parsing_file = self.src_file
    _space = ' '
    line_number  = 0
    SearchCfg      = '.?``CFG\s?{(.+)}(.+)?'
    search_if      = '.?``IF\s?{(.+)}(.+)?'
    search_elsif   = '.?``ELSIF\s?{(.+)}(.+)?'
    search_else    = '.?``ELSE(.+)?'
    search_endif   = '.?``ENDIF(.+)?'
#    search_for     = '``FOR\s?{\s?(.+)\s?}\s?{\s?(.+)\s?}\s?{\s?(.+)\s?}' 
    search_for     = '.?``FOR\s?{\s?(.+)\s?}\s?(.+)?'
#    search_for     = '.?(?<!//)``FOR\s?{\s?(.+)\s?}\s?(.+)?'
    search_endfor  = '.?``ENDFOR(.+)?'
    search_content = '^.+$'
    _InitialFunction =  'bui'+'ltins.X'+'Y' + 'T = ' + str(MINE) + '\n' #+'print("==================", CODEGEN)\n'
    _InitialImport = 'import sys,bu' + 'iltins\n' + _InitialFunction
    _dst_file_content = 'import sys \nsys.path.append ("' + self.dict['CF_DIR']  +'")\nfrom CF import *\n'
    #_dst_file_content = '\"\"\"\n'
    exec (_InitialImport)
    with open (self.src_file, 'r') as parsing_file:
      sys.path.append (self.dict['CF_DIR']) 
      _Cfg = importlib.import_module ('CF')
      file_lines = parsing_file.readlines()
      #while (line_number < len(file_lines)):
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
            #print ('1')
            eval_content = result_if.group(1)
            eval_content = self.SubstituteFunctionName(eval_content)
            _dst_file_content = self.if_branch('IF', eval_content, _dst_file_content)
          elif (result_elsif != None):
            #print ('2')
            eval_content = result_elsif.group(1)
            eval_content = self.SubstituteFunctionName(eval_content)
            _dst_file_content = self.if_branch('ELSIF', eval_content, _dst_file_content)
          elif (result_else != None):
            #print ('3')
            _dst_file_content = self.if_branch('ELSE', 'False', _dst_file_content)
          elif (result_endif != None):
            #print ('4')
            _dst_file_content = self.if_branch('ENDIF', 'False', _dst_file_content)
          elif (result_for != None):
            #print ('5')
            eval_content = result_for.group(1)
            eval_content = self.SubstituteFunctionName(eval_content)
            _dst_file_content = self.for_loop('FOR', eval_content, _dst_file_content)
          elif (result_endfor != None):
            #print ('6')
            _dst_file_content = self.for_loop('ENDFOR', 'False', _dst_file_content)
          else:
            if re.search ('``', line) != None:
              #TODO: causion this line may has \n as blow condition
              #print ('line: ', line)
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
            # print (_dst_file_content)
            line_number += 1
#    _dst_file_content = _dst_file_content + '\n' +'\"\"\"'
    parsing_file.close()
    #print (self.dst_file)
    with open (self.dst_file, 'w') as output_content:
#      for lines in _dst_file_content:
#        print (lines + '\n')
#        output_content.write (lines)
      #_test = """print ('// *                                            HangZhou XinYun Photoelectric Technology Co. , Ltd\\n')"""
#      _dst_file_content = """output_content.write ("i2c_slv #(.I2C_SLV_ADR_0(7'b111_0000), .I2C_SLV_ADR_1(7'b111_0100)) inst_i2c_slv (\\n")"""
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
