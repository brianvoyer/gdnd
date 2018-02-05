#!/usr/bin/env python
# advgen.py
# generate D&D 5e encounter blocks based on dificulty and party level
# by Diana Voyer and David Estes-Smargiassi, 2017
#
# this just generates encounter blocks, not actual encounters. So it
# just generates a list of appropriate CRs for the given difficulties
# and party levels
#
# Usage:
# python advgen.py XP CharLev1 ... CharLevN
# where difficultyLevel is one of "easy", "medium", "hard", or "deadly"
# CharLev's are the character levels separated by spaces
#
# Example usage:
# python advgen.py 40000 9 9 9 9 9
# to generate encounters for a party of 5 level 9 characters that give
# around 40000 XP total

import random, sys, itertools
from fractions import Fraction

#define proportions of encounters
runs = 1000
easymod = 0.00
medimod = 0.15
hardmod = 0.85
deadmod = 0.1

def buildencounter(ratingmin, ratingmax):
    build = []
    total = 0
    nummonst = 0
    while 1:
        monst = random.SystemRandom().choice(challenge)
        #check if the monster is too weak 
        if monst[1] < minxp:
            pass
        else:
            if encMult(nummonst + 1)*(total + monst[1]) >= ratingmax and encMult(nummonst)*total >= ratingmin:
                break
            elif encMult(nummonst + 1)*(total + monst[1]) >= ratingmax:
                pass
            else:
                nummonst += 1
                build += [monst]
                total += monst[1]
    #print sorted(build), encMult(nummonst)*total, total
    return [[int(encMult(nummonst)*total), sorted(build), total]]

def grouplist(lst):
    nlst = {}
    for i in range(len(lst)):
        if lst[i][0] in nlst:
            nlst[lst[i][0]] += 1
        else:
            nlst[lst[i][0]] = 1
    op = []
    for k, v in nlst.iteritems():
        op += [(k,v)]
    return op

# from the DMG (5e)
def encMult(nummonst):
    if nummonst == 0:
        return 1
    elif nummonst == 1:
        return 1
    elif nummonst == 2:
        return 1.5
    elif nummonst > 2 and nummonst <= 6:
        return 2
    elif nummonst > 6 and nummonst <= 10:
        return 2.5
    elif nummonst > 10 and nummonst <= 14:
        return 3
    elif nummonst > 14 and nummonst <= 30:
        return 4
    else:
        return 1000000

challenge = [[0, 10], [0.125, 25], [0.25, 50], [0.5, 100], [1, 200],
	     [2, 450], [3, 700], [4, 1100], [5, 1800], [6, 2300],
	     [7, 2900], [8, 3900], [9, 5000], [10, 5900], [11, 7200],
	     [12, 8400], [13, 10000], [14, 11500], [15, 13000],
	     [16, 15000], [17, 18000], [18, 20000], [19, 22000],
	     [20, 25000], [21, 33000], [22, 41000], [23, 50000],
	     [24, 62000], [25, 75000], [26, 90000], [27, 105000],
	     [28, 120000], [29, 135000], [30, 155000]]

xpthreshs = [[25, 50, 75, 100],
             [50, 100, 150, 200],
             [75, 150, 225, 400],
             [125, 250, 375, 500],
             [250, 500, 750, 1100],
             [300, 600, 900, 1400],
             [350, 750, 1100, 1700],
             [450, 900, 1400, 2100],
             [550, 1100, 1600, 2400],
             [600, 1200, 1900, 2800],
             [800, 1600, 2400, 3600],
             [1000, 2000, 3000, 4500],
             [1100, 2200, 3400, 5100],
             [1250, 2500, 3800, 5700],
             [1400, 2800, 4300, 6400],
             [1600, 3200, 4800, 7200],
             [2000, 3900, 5900, 8800],
             [2100, 4200, 6300, 9500],
             [2400, 4900, 7300, 10900],
             [2800, 5700, 8500, 12700]]

try:
    rating = sys.argv[1]
except:
    print "needs an argument, use \"help\" for help"
    exit()

if rating == "help":
    print "advgen.py"
    print "generate D&D 5e encounter blocks based on XP desired and party level"
    print "by Diana Voyer and David Estes-Smargiassi, 2017"
    print ""
    print "this just generates encounter blocks, not actual encounters. So it"
    print "just generates a list of appropriate CRs for the given difficulties"
    print "and party levels"
    print ""
    print "Usage:"
    print "python advgen.py ApproxXP CharLev1 ... CharLevN"
    print "where difficultyLevel is one of \"easy\", \"medium\", \"hard\", or \"deadly\""
    print "CharLev's are the character levels separated by spaces"
    print ""
    print "Example usage:"
    print "python advgen.py 40000 9 9 9 9 9"
    print "to generate encounters for a party of 5 level 9 characters that give"
    print "around 40000 XP total"
    exit()

try:
    targetXP = int(rating)
except:
    print "Invalid target XP, use \"help\" for help"
    exit()

if len(sys.argv) < 3:
    print "needs a encounter difficulty and character levels"
    print "use \"help\" for help"
    exit()

charlevels = []

for i in range(len(sys.argv)-2):
    charlevels += [int(sys.argv[i+2])]

easythresh = 0
medithresh = 0
hardthresh = 0
deadthresh = 0

for i in charlevels:
    easythresh += xpthreshs[i-1][0]
    medithresh += xpthreshs[i-1][1]
    hardthresh += xpthreshs[i-1][2]
    deadthresh += xpthreshs[i-1][3]

#print "Easy Encounter XP threshold:   {}\nMedium Encounter XP threshold: {}\nHard Encounter XP threshold:   {}\nDeadly Encounter XP threshold: {}".format(easythresh, medithresh, hardthresh, deadthresh)

minxp = 0.04 * easythresh
# if 20 of them isn't even an "easy" encounter, get rid of them
maxxp = 2 * deadthresh
# twice the deadly threshold is probably a good max

enclist = []

# generate easy encounters
for i in range(int(runs * easymod)):
    enclist += buildencounter(easythresh, medithresh)
# generate med encounters
for i in range(int(runs * medimod)):
    enclist += buildencounter(medithresh, hardthresh)
# generate hard encounters
for i in range(int(runs * hardmod)):
    enclist += buildencounter(hardthresh, deadthresh)
# generate deadly encounters
for i in range(int(runs * deadmod)):
    enclist += buildencounter(deadthresh, maxxp)

ratingmin = int(targetXP * 0.95)
ratingmax = int(targetXP * 1.05)

build = []
total = 0
while 1:
    enc = random.SystemRandom().choice(enclist)
    if total + enc[2] >= ratingmax and total > ratingmin:
        break
    elif total + enc[2] >= ratingmax:
        pass
    else:
        build += [enc]
        total += enc[2]
    #print sorted(build), encMult(nummonst)*total, total
#print [[sorted(build), total]]

#enclist.sort()
#sortedenc = list(enclist for enclist,_ in itertools.groupby(enclist))

for i in sorted(build):
    adjxp = i[0]
    enclist = grouplist(i[1])
    enclist.sort()
    xp = i[2]
    CRlist = ""
    for j in enclist:
        CRlist += "{} CR{} + ".format(j[1], str(Fraction(j[0])))
    CRlist = CRlist[:-3]
    if adjxp == xp:
        print "{} ({} XP)".format(CRlist, xp)
    else:
        print "{} ({} XP, {} Adjusted)".format(CRlist, xp, adjxp)

print "Total XP: {}".format(total)
