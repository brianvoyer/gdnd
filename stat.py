#!/usr/bin/env python
# Generates random stats for characters that obey the rule that
# the stats shall be generated in order, but they shall be rerolled
# until at least two stats are at least 15.
import random
import time
import math
rng=random.SystemRandom(int(str(time.time() % 1)[2:]))
while 1:
    temp=[sum(sorted([rng.randint(1, 6) for i in range(4)])[1:]) for i in range(6)]
    if sorted(temp)[-2] > 14:
        #if sorted(temp)[0] < 10:
        break

#print(temp)
mods = []
for i in range(len(temp)):
    mod = int(math.floor((temp[i] - 10)*0.5))
    if mod > -1:
        mods.append(str(temp[i]) + ' (+' + str(mod) + ")")
    else:
        mods.append(str(temp[i]) + '  (' + str(mod) + ")")

#print(mods)
print("STR: {}\nDEX: {}\nCON: {}\nINT: {}\nWIS: {}\nCHA: {}".format(mods[0], mods[1], mods[2], mods[3], mods[4], mods[5]))
