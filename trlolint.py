#!/usr/bin/python3
import sys, re, argparse
from trlo_kw import *
#sectionre=re.compile("SECTION\s*[(]\s*([^)]*)\s*[)]\s*[{]([^}]*)[}]",
#                     re.M|re.DOTALL)

parser = argparse.ArgumentParser(description="Tries to parse a trlo file.")
#parser.add_argument("-h", "--help", action="store_true", help="Displays this help text and exits.")
parser.add_argument("-i", "--in-place", action="store_true", help="writes changes to input file. Take care!")
parser.add_argument("-a", "--assignment", action="store_true", help="try to fix assignment operators.")
parser.add_argument("filename", help="trlo-file to operate on")


assignre=re.compile("\s*(//)?\s*([^:=<]*?)\s*(=|:=|<=|=>)\s*([^;]*);")

args=parser.parse_args()

lines=open(args.filename).read().split('\n')

insection=False

aliases={}
output=""
for l in lines:
    #print(l, insection)
    m=assignre.match(l)
    if args.assignment and m:
        lhs=m.group(2)
        oldop=m.group(3)
        rhs=m.group(4)
        op=oldop
        if not insection:
            op=":="
            if not m.group(1):
                aliases[lhs]=rhs
        else:
            lhs_kw=lhs.split(" ")[0]
            if lhs_kw in aliases:
                lhs_kw=aliases[lhs_kw].split(" ")[0]
            lhs_kw=lhs_kw.split("(")[0].split('[')[0].split(" ")[0]
            if lhs_kw in lhs2op:
                op=lhs2op[lhs_kw]
            elif not m.group(1): # not commented out
                print("No db entry for keyword \"%s\""%lhs_kw)
        l=l[0:m.start(3)] + op + l[m.end(3):]
    if l.find("{")!=-1:
        insection=True
    if l.find("}")!=-1:
        insection=False
    output+=l+"\n"
if args.in_place:
    f=open(args.filename, "w").write(output)

