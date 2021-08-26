#!/usr/bin/env python3
import lexer
import sys
 
n = len(sys.argv)

if(n<2):
    print("You must specify the path of file\n ./csl.py demo.csl")
    exit()
if(n>2):
    print("Too many arguments")
    exit()

fn = sys.argv[1]

if len(fn)<5 or not fn[-4:]==".csl":
    print("Extension of the file must be .csl")

try:
    with open(fn,"r") as file:
        text = file.read()
        if text.strip() == "": exit()
        result, error = lexer.run('fn',text)

        if error: print(error.as_string())

except Exception as e:
    print("Invalid file name")
    exit()
