"""Analyze letter frequencies in the bip-39 English wordlist."""

import collections

with open('src/bip39-wordlist-en.txt') as f:
    words = [w.strip() for w in f]

freqs = collections.defaultdict(lambda: [0]*10)

for w in words:
    for i, l in enumerate(w):
        freqs[l][i] += 1

for l, f in sorted(freqs.items(), key=lambda x: sum(x[1])):
    f_formatted = [f"{x:3d}" for x in f]
    print(f"{l}: {sum(f):4d} = {' '.join(f_formatted)}")

# q:   21 =   8   5   4   3   1   0   0   0   0   0
# j:   29 =  20   0   7   2   0   0   0   0   0   0
# z:   31 =   4   1  12  10   3   1   0   0   0   0
# x:   42 =   0  25  13   0   3   1   0   0   0   0
# k:  130 =  20   8  12  49  35   4   2   0   0   0
# v:  150 =  46  11  43  31   9   9   1   0   0   0
# w:  161 =  69  26  19  25   7  11   3   1   0   0
# f:  205 = 106   8  33  33  16   7   2   0   0   0
# y:  210 =   6  18  28  30  43  36  39  10   0   0
# b:  240 = 117  17  51  38  11   5   1   0   0   0
# g:  272 =  76   7  60  63  34  19  12   1   0   0
# h:  285 =  64  78  18  43  60  19   3   0   0   0
# m:  324 = 105  28  76  59  27  16  12   1   0   0
# p:  337 = 132  43  65  66  23   5   3   0   0   0
# d:  381 = 112  16  64  87  48  41  11   2   0   0
# u:  432 =  35 163  92  81  44  16   1   0   0   0
# c:  515 = 186  37  92  87  53  41  16   3   0   0
# l:  620 =  76 117 116 114 112  55  24   6   0   0
# s:  641 = 250  21 135 105  53  45  29   3   0   0
# n:  649 =  41 101 161 120  90  88  41   7   0   0
# i:  730 =  55 222 154 147 107  39   5   1   0   0
# o:  738 =  55 276 149 100  94  45  17   2   0   0
# t:  763 = 121  44 134 173 122 102  58   9   0   0
# r:  879 = 108 191 183 108 120 116  41  12   0   0
# a:  918 = 136 306 200 129  93  45   8   1   0   0
# e: 1365 = 100 279 127 242 295 182 111  29   0   0
#
# We choose to merge j and x. They are among the rarest letters. Moreover, for
# all positions except the third letter, they can be disambiguated with an easy
# rule:
#
# - A letter in first position must be j
# - A letter in second position must be x
# - A letter in fourth position must be j
# - A letter in fifth or sixth position must be x
#
# In third position, it's an x in about 66% of the cases.
