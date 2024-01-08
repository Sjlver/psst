## What can go wrong?

This document describes scenarios where using `psst` leaks information about the secret. While `psst` is secure if used correctly, there are subtle difficulties and outright attacks.

### Manipulated `psst` worksheet

Users should always use `psst` worksheets that come directly from
https://github.com/Sjlver/psst.

If an attacker can manipulate the worksheet, they can cause shares to leak
information about the secret. Here are two examples of manipulated tables:

```
Original                Share 3 leaks secret    6=1 leaks secret
----------------        ----------------        ----------------
0  ⚀  0  0  0  0        0  ⚀  0  0  0  0        0  ⚀  0  0  0  0
0  ⚁  1  2  3  4        0  ⚁  1  2  3  4        0  ⚁  1  2  3  4
0  ⚂  2  4  1  3        0  ⚂  2  4  0  3        0  ⚂  2  4  1  3
0  ⚃  3  1  4  2        0  ⚃  3  1  4  2        0  ⚃  3  1  4  2
0  ⚄  4  3  2  1        0  ⚄  4  3  0  1        0  ⚄  4  3  2  1
0  ⚅  re-throw          0  ⚅  re-throw          0  ⚅  0  0  0  0
```

The first example shows the first block (for secret digit `0`) of an original
`psst` table. Users can verify that each share could contain any digit with the
same probability, depending on the dice throw. This follows from the fact that
each column contains every digit exactly once.

In the second example, share #3 has been manipulated. It contains the digit `0`
more often than it should. This leaks information about the secret: if an
attacker obtains share #3 and sees a `0`, there is a high probability that it
comes from this block, hence the secret digit is `0` as well.

In the third example, an attacker changed the last line from "re-throw" to a
copy of the first line. This has the same effect as using a loaded dice, where
the digit `1` appears twice as often as other digits. If the attacker obtains
any share and sees a `0`, there is a _2/5_ instead of _1/5_ probability that it
comes from this manipulated block, and thus that the secret digit is `0` as
well.

### Not enough randomness

`psst` is only secure if users use a fair, unpredictable source of randomness.
When the random data is non-ideal, shares will reveal some information about the
secret.

In the ideal case, each digit contains _log₂(5) = 2.32_ bits of randomness:
every secret digits is as likely as any other. Casino dice, thrown correctly,
will be close to this ideal situation.

A non-ideal source of randomness has less entropy. For example, consider a dice
where the digit `1` is four times as likely as the others. `1` comes up with
probability _4/8_, the other digits `2-5` with probability _1/8_ (`6` never
occurs since we re-throw the dice in this case). This dice has an entropy of
_2.00_ bits.

Using this non-ideal dice, each digit leaks _2.32 - 2.00 = 0.32_ bits of
information. Let us consider the example where the secret could be either
`yesyes` or `nonono`:

```
Secret (if yesyes):     42 04 32 42 04 32
Secret (if nonono):     22 23 22 23 22 23
Share #1 (dice throws): 43 00 40 04 01 41
Share #2:               44 01 03 11 03 00
```

Looking at share #1, an alert user could spot that the digit `0` appears
somewhat frequently. This is a result of the loaded dice: Share #1 is `0`
exactly if the dice comes up `1`.

An attacker who obtains share #2 could now "guess" that share #1 is `00 00...`,
which is the most likely value. From this, they can reconstruct parts of the
secret:

```
Share #1 ("guessed"):   00 00 00 00 00 00
Share #2:               44 01 03 11 03 00
Reconstructed secret:   11 04 02 44 02 00
```

The attacker can now compare the reconstructed secret to the two possible
messages:

```
Secret (if yesyes):     42 04 32 42 04 32 (5 digits match)
                           ǁǁ  ǁ ǁ  ǁ
Reconstructed secret:   11 04 02 44 02 00
                               ǁ     ǁ
Secret (if nonono):     22 23 22 23 22 23 (2 digits match)
```

From this, the attacker can guess that the secret was probably `yesyes`.

This issue is quite serious, even in cases where there are more than two
possible messages. For example, a BIP-39 word contains 11 bits of entropy. Users
who follow the `psst` worksheet will use at least 10 digits to encode that word.
Using the loaded dice from the previous example, each digit will leak 0.32 bits
of entropy. Thus, the BIP-39 word only has _11 - 10\*0.32 = 7.8_ bits of entropy
left; it is as if there were only 222 words in the wordlist, rather than 2048.

### Attacker-controlled randomness

Suppose Eve approaches Alice: "Dear Alice, you should use my _SuperDice_ app for
`psst`! It is very convenient, because it can simulate a five-sided dice. You'll
never have to re-throw and will save so much time. By the way, I can also guard
one of the shares for you, if you like. That's how nice I am."

If Alice follows Eve's evil advice, Eve will be able to easily reconstruct the
secret. Eve would program her SuperDice app to emit pseudo-random numbers. These
look to Alice indistinguishable from true randomness, but Eve can reproduce
exactly the same sequence using her knowledge of the pseudo-random seed.

### Side-channel attacks

Suppose Mallory approaches Bob: "Hey Bob, I made an app that makes `psst` so
much easier to use. See, you just enter your secret digit, and it automatically
displays the right block of the conversion table. It's perfectly safe, of
course, because you still use your own casino dice that no attacker could
predict."

This approach is not safe at all, because the app could transmit the secret to
Mallory. Mallory does not even need to see any of the shares.
