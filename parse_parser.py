#!/usr/bin/python3
import re
f=open("trlo_setup_parser.y").read()
f+=open("trlo_setup_parser_rules.y").read()
f+=open("tridi_setup_parser_rules.y").read()

block=re.compile("[{][^{}]*[}]", re.M|re.DOTALL)

f=block.sub("", f)
f=block.sub("", f)
f=re.sub("';'","SEMICOLON", f)
bnf=re.compile("\n([^\n: ]*):([^;]*);", re.M|re.DOTALL)
rules={}
assignments=[]

assign=re.compile("^(.*) ('='|sig_op_[^ ]*) (.*) SEMICOLON$")

for m in bnf.finditer(f):
    lhs=m.group(1)
    rhs=re.sub("%s:"%lhs, "|", m.group(2))
    rhs=re.sub("\s+", " ", rhs).split('|')
    rhs=list(map(lambda a: re.sub("(^ )|( $)", "", a), rhs))

    rules.setdefault(lhs, [])
    rules[lhs]+=rhs
    for l in rhs:
        m=assign.match(l)
        if m:
            assignments.append((m.group(1), m.group(2), m.group(3)))

queue=list(map(lambda a:(a[0], a[1]), assignments))
lhs2op={}
kwre=re.compile("KW_([^ ]+)")
opparse={"'='":"=", "sig_op_ce":":=", "sig_op_le":"<=", "sig_op_eg":"=>"}
for l in queue: 
    firstword=l[0].split(" ")[0] # "foo index" -> "foo"
    op=opparse[l[1]]
    m=kwre.match(firstword)
    if m:
        if m.group(1) in lhs2op and lhs2op[m.group(1)]!=op:
            print("Different assignments found for %s: %s and %s",
                    m.group(1), lhs2op[m.group(1)], op)
        lhs2op[m.group(1)]=op
    elif firstword in rules:
        for r in rules[firstword]:
            item=r, l[1]
            if item not in queue:
                queue.append(item)
    else:
        print("No rule for %s, ignored."%firstword)
print(lhs2op)
