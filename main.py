#!/usr/local/bin/python2

import sys, getopt, code

from assembler.parser import Parser

def print_help_and_exit():
   print ('main.py -i <inputfile> -o <outputfile>')
   sys.exit(2)

def main(argv):

   # Set inputfile and ouptut file to <input filename> and <input file name or default>
   inputfile = ''
   outputfile = "output.mntdw"
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print_help_and_exit()
   for opt, arg in opts:
      if opt == '-h':
         print_help_and_exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   # If inputfile is still "" then throw an error.
   if inputfile == "":
      print("No input file specified.")
      print_help_and_exit()

   parser = Parser(inputfile)
   parser.assemble()
   parser.saveFile(outputfile)
   # print(parser.mntdw_lines)
   # code.interact(local=locals())



if __name__ == "__main__":
   main(sys.argv[1:])
