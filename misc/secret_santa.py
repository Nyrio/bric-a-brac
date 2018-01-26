##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC BY                                                           #
#                                                                            #
##############################################################################

# This code is useful to generate the matchings for a Secret Santa (where
# everybody has to give a gift to somebody else). Ask an external person to
# run the script, or modify it to send e-mails to the participants.

# The code generates a perfect loop (cf proof below).

import random

def strict_shuffle(l):
    lp = l[:]
    for i in reversed(range(1, len(lp))):
        j = random.randint(0, i-1)
        lp[i], lp[j] = lp[j], lp[i]
    return lp

people = ["person1", "person2", "person3", "etc"] # enter the names here
offers = strict_shuffle(people)

for i in range(len(people)):
    print("%s offers a gift to %s" % (people[i], offers[i]))



# PROOF

# Let's assume that the algorithm generates strictly more than 1 cycle.
# Then one of the cycles, C, has a smallest value v distinct from 0.
# When the value i in the for loop was equal to v, the value j was
# taken strictly smaller than v, let's say v'. Then one of the factors of
# the cycle C is vv', given that it is impossible to have the inverse factor
# in this algorithm.
# Then v' is part of the same cycle than v. This is impossible because we
# defined v as the smallest value in the cycle.
# Therefore it is impossible that the algorithm generates more than 1 cycle,
# which comes from the fact that the smallest value of a cycle can only be 0.

# Therefore the algorithm generates a single loop.

# More about permutations: https://en.wikipedia.org/wiki/Permutation