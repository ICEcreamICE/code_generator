#!/usr/local/bin/python3

import argparse, textwrap
from re import T
from ast import parse

# import os
# import sys
# # sys.path.append(os.path.abspath('./'))
# print('path is ===>', sys.path, "==\n", os.path.abspath('./'))

# from flow.cg_class.LineParser import LineParser#, tkinter
from cg_class.LineParser import LineParser#, tkinter
from cg_class.ModuleParser import *

def option_parser():
  options_dict = {}
  #parse argv TODO: make argv to argv_dict next
  parser = argparse.ArgumentParser( prog='GEN', description='CGEN Digital Flow Start',
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    epilog=textwrap.dedent('''
                                      Examples:
                                        RunTest: GEN -proj <ProjName> -test <UVMTestCase> -wave
                                        RunLint: GEN -proj <ProjName> -lint
                                        RunRegr: GEN -proj <ProjName> -regr <VsifName>
                                        RunAms:  GEN -proj <ProjName> -test <UVMTestCase> -wave -ams
                                    ''')
                                  )

  ################-------------------################
  ##PROJ NAME
  # parser.add_argument('-proj', required=True, help='select the project you are working with', metavar='IC#######')
  # ##PROJ_UVM_COMMAND
  # parser.add_argument('-regr', help='run regression', metavar='VsifName')
  # parser.add_argument('-test', help='select test cases to run', metavar='TestName')
  # parser.add_argument('-wave', action='store_true', help='enable waveform recording')
  # parser.add_argument('-post', help='enable post verification',  metavar='SDF File Name')
  # parser.add_argument('-noclean', action='store_true', help='not clean old dir')
  # parser.add_argument('-newrun', action='store_true', help='run verification in a new directory')
  # parser.add_argument('-genfile', action='store_true', help='generate RTL and TB file only')
  # parser.add_argument('-gentemp', help='generate RTL and SV file Template', metavar='FileName')
  # parser.add_argument('-seed', help='provide random seed to be simulated', default='1', metavar='Random|#seed#')
  # parser.add_argument('-args', nargs='+', type=str, help='collect $plusargs for Systemverilog Env.', default='',
  #                     metavar=('\"+args0 +ar...\"')
  #                    )
  # ##PROJ_SYN_COMMAND
  # ##PROJ_PNR_COMMAND
  # ##PROJ_STA_COMMAND
  # ##PROJ_AMS_COMMAND
  # parser.add_argument('-ams', action='store_true', help='enable co-sim with spectre')
  # ##PROJ_LINT_COMMAND
  # parser.add_argument('-lint', action='store_true', help='start lint check')
  # ##PROJ_USE4COMPATIBILITY
  # parser.add_argument('-convreggen', action='store_true', help='Switch Register Generation Method to Old Algorithm')
  # parser.add_argument('-cosim', action='store_true', help='Enable co-simulation with MCU integrated')
  # parser.add_argument('-fpga', action='store_true', help='Support FPGA simulation')
  parser.add_argument('-src', required=True, help='source file here', metavar='N/A')
  parser.add_argument('-dst', required=True, help='dst file here', metavar='N/A')
  


  args = parser.parse_args()
  print (args)
  # options_dict.update({'MAIN_PROJ' : args.proj})
  # options_dict.update({'REGR' : args.regr})
  # options_dict.update({'AMS'  : args.ams})
  # options_dict.update({'LINT' : args.lint})
  # options_dict.update({'TEST' : args.test})
  # options_dict.update({'POST' : args.post})
  # options_dict.update({'WAVE' : args.wave})
  # options_dict.update({'NOCLEAN': args.noclean})
  # options_dict.update({'NEWRUN': args.newrun})
  # options_dict.update({'GENFILE': args.genfile})
  # options_dict.update({'GENTEMP': args.gentemp})
  # options_dict.update({'SEED': args.seed})
  # options_dict.update({'ARGS': args.args})
  # options_dict.update({'CONVENTIONALREGGEN': args.convreggen})
  # options_dict.update({'COSIM': args.cosim})
  # options_dict.update({'FPGA': args.fpga})
  options_dict.update({'SRC': args.src})
  options_dict.update({'DST': args.dst})
  return options_dict

def PlayOverture(staff):
  return staff.Sonata()

def PlayMarch(staff):
  return staff.Render()

def PlayRequiem(staff):
  return staff.Lacrimosa()

def main():
  #Read args
#  top = tkinter.Tk()
#  top.mainloop()
  MainProjArgs = option_parser()
  #Analyze
  # RunList = ['RTL', 'VER', 'AMS', 'HAL', 'RGR', 'PST', 'IPS']
  # for Staff in RunList:
  #   exec('MainProjArgs = PlayOverture(m' + Staff+ '(MainProjArgs))')
  # #Template
  # if MainProjArgs['GENTEMP']:
  #   tempfile = TempFile(MainProjArgs['GENTEMP'])
  #   tempfile.CreateTmp()
  #   exit()
  # #Compose
  # ComposeList = ['RTL', 'VER', 'IPS', 'UVM']
  # if MainProjArgs['LINT']:
  #   ComposeList.extend(['LINT'])
  # if MainProjArgs['POST'] != None:
  #   ComposeList.extend(['PST'])
  # if MainProjArgs['REGR']:
  #   ComposeList.extend(['RGR'])
  # ComposeList.extend(['AUTO'])
  # for Staff in ComposeList:
  #   exec('MainProjArgs = PlayMarch(a' + Staff+ '(MainProjArgs, a' + Staff + '))')
  
  # #Run
  # if not MainProjArgs['GENFILE']:
  #   uvm = cUVM(MainProjArgs, 'cUVM')
  #   if MainProjArgs['TEST']:
  #     Rslt, RunDir = PlayRequiem(uvm)
  #   elif (MainProjArgs['LINT']):
  #     hal = cHAL(MainProjArgs, 'cHAL')
  #     Rslt, RunDir = PlayRequiem(hal)
  #   elif (MainProjArgs['REGR']):
  #     rgr = cRGR(MainProjArgs, 'cHAL')
  #     Rslt, RunDir = PlayRequiem(rgr)
  #   else:
  #     print ('Plase assign a task')
  #     exit(1)
  #   #Check
  #   checker = CHECKER(Rslt, RunDir, MainProjArgs)
  #   checker.CheckRunResult()
  _list=[]
  _src=MainProjArgs['SRC']
  _dst=MainProjArgs['DST']
  _parser=LineParser(_src, _dst, _list)
  _parserRslt=_parser.Parser()
  print("done Parsing!")
  GLOBAL([_dst])

if __name__ == "__main__":
  main()
