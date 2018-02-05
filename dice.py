#!/usr/bin/env python
# die roller program. 
# python dice.py "3x2d12+6"
# v1.5 - added the "nx" syntax
# v2.0 - allow for advantage and disadvantage, maybe with H/L?

# python combat.py "3x(1d20H+7v13>(2d6H+6))"
#                   3x the following:
#                   1d20H+7: roll two d20s, add 7 to each, 
#                           return the higher value
#                   v13>: if preceeding is greater than 13, continue, 
#                         if not, skip
#                   (..): groups the thing to do
#                   2d6H: roll 2d6 twice, return the higher value

# python combat.py "d20-1Lv10>(1d4-1)"
#                   d20-1L: roll two d20s, subtract 1 from each, 
#                           return the lower value

import sys, random, re

dice=random.SystemRandom()

def rolldice(input):
    if input[0] == 'd':
        temp = '1'+input
    else:
        temp = input
    if temp[-1] == 'H':
        mode = 1
        temp = temp[:-1]
    elif temp[-1] == 'L':
        mode = 2
        temp = temp[:-1]
    else:
        mode = 0
    if [temp] != temp.split('+'):
        num = int(temp.split('+')[0].split('d')[0])
        die = int(temp.split('+')[0].split('d')[1])
        try: 
            modif = int(temp.split('+')[1])
        except ValueError:
            modif = 0
    elif [temp] != temp.split('-'):
        num = int(temp.split('-')[0].split('d')[0])
        die = int(temp.split('-')[0].split('d')[1])
        try: 
            modif = -1*int(temp.split('-')[1])
        except ValueError:
            modif = 0
    else:
        num = int(temp.split('d')[0])
        die = int(temp.split('d')[1])
        modif = 0
    roll = 0
    roll2 = 0
    for i in range(num):
        roll += dice.randrange(die) + 1
        roll2 += dice.randrange(die) + 1
    roll += modif
    roll2 += modif
    if mode == 0:
        return roll
    elif mode == 1:
        if roll > roll2:
            return roll
        else:
            return roll2
    else:
        if roll > roll2:
            return roll2
        else:
            return roll

# input format: 1d4+6
full = []
rex = re.compile("^\d*x.*$")
input = ""
if(len(sys.argv) < 2):
    print("ERROR: not enough arguments. Format: python dice.py \"1x1d4+2\"")
    exit()

for i in sys.argv[1].split(' '):
    if rex.match(i):
        i = ' '.join([i.split('x')[1]] * int(i.split('x')[0]))
        #print(i)
        input += i + " "
    else:
        input += i + " "

rex = re.compile("^d?\d*d\d*[+-]?\d*[HL]?$")
for i in input.split(' '):
    if rex.match(i):
        #print(i)
        full.append(str(rolldice(i)))
    else:
        #print(i)
        full.append(i)

print(' '.join(full))
