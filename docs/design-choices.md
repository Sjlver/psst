## Design choices

When designing `psst`, we wanted to create an implementation of Shamir's Secret
Sharing Scheme that is as simple, easy to use, and easy to understand as
possible. This ensures that recovery is possible, even though the world might
have changed since the shares were created. It makes the system applicable to
many use-cases. It avoids vendor lock-in and proprietary solutions.

We quickly realized that any full implementation of Shamir's Secret Sharing is
too complex for these goals. Implementations face a number of subtle choices:
how to encode shares, how to choose sizes and thresholds, which finite field to
use, etc. Most alternative implementations add encryption, checksums,
verifiability for shares and secrets, and other features. While these can
improve security and usability, they also increase the system's complexity.

In the rest of this section, we explain the considerations that went into the
design of `psst`.

### Why use the GF(5) finite field?

The mathematics of Shamir's Secret Sharing need a finite field to work in.
Essentially, that is a set of elements with operations for addition,
subtraction, multiplication, and division.

The field needs to be large enough for the desired number of shares: a field of
size _n_ allows a maximum of _n - 1_ shares. On the other hand, the field should
be as small as possible, because this simplifies the implementation: one can
explicitly write down all the _n²_ possible combinations of share values.

Size five worked perfectly for the authors because they find that four shares
are enough, and the 25 combinations fit easily on a single page of paper. There
are additional advantages:

- Combinations of two digits map quite naturally to the latin alphabet.
- It is easy to choose a random digit using a dice.

**If dice are so cool, why not use GF(6)?** Unfortunately, there is no GF(6).
All finite fields have a size that is a power of a prime number. There are
fields of size 2, 3, 4, 5, 7, 8, 9, ..., but not 6.

**How about schemes based on XOR?** XOR is a relatively simple operation that
can be performed without a computer. XOR-based secret sharing schemes are
equivalent to Shamir's Secret Sharing in GF(2). They have a few shortcomings
compared to `psst`:

- XOR-based schemes can only support _n_-of-_n_ schemes, for example 2-of-2. If
  any of the shares is lost, the secret cannot be recovered.
- There are subtle design questions, such as how to encode letters and numbers.
- It is not obvious how to obtain randomness.

### Why focus on 2-of-4 secret sharing?

We want a threshold of two because of our primary goal: to eliminate a single
point of failure.

It is in principle possible to use `psst` in a 3-of-4 setting. There would be
125 possible combinations, namely all polygons _ax² + bx + c_ over GF(5), and
users would need two dice throws to choose a polygon for each secret digit.
However, we advise against that. If users cannot tolerate the compromise of one
share, they would be better advised to use a multisig scheme or similar
technique.

Similarly, if user need more than four shares, it seems wiser to not rely on
secret sharing, and use one of the [alternatives](../README.md#alternatives).

### Encoding text (a-z)

Our choice of GF(5) allows for a compact representation of the latin alphabet
(a-z) with two digits per letter, except that there are only 25 two-digit
combinations for 26 letters. We chose to solve this by merging the two letters
`j` and `x`; they are both assigned to the combination `44`.

We made this choice after analyzing letter frequencies and usage in the
[BIP-39 English wordlist](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt).
Both `j` and `x` are among the rarest letters. Replacing one with the other
never causes confusion between two words, even if we only consider the first
four letters of each word.

Moreover, `j` and `x` tend to occupy different positions, so that they can be
disambiguated using the following rules:

- A `44` in first position must be `j` (e.g., "?uice" is "juice")
- A `44` in second position must be `x` (e.g., "e?act" is "exact")
- A `44` in fourth position must be `j`
- A `44` in fifth or sixth position must be `x`

In third position, the combination `44` is `x` in 13 of 20 cases.

We also recommend to pad short words with `q`. It is the rarest letter and is
always followed by `u` in actual usage. This means that one or more `q` at the
end of the word are unambiguously padding.

### Checksums and verification

`psst` deliberately does not have a built-in checksum or other means to verify
that a secret was recovered correctly, unlike most
[alternative implementations](../README.md#alternatives) of Shamir's Secret
Sharing.

This follows from `psst`s goal of maximum simplicity. Even simple checksums are
tedious to compute by hand. Moreover, the secrets often have some built-in
redundancy. For example, a BIP-39 seed phrase must contain valid words from the
wordlist and has a built-in checksum.

Users can often manually add redundancy to the secret. For example, a simple
secret such as a PIN number can be repeated three times. In this spirit, the
`psst` worksheet recommends using more than the minimum four first letters for
BIP-39 words. The probability that a single-letter change would cause a word to
change into another valid word decreases rapidly as more letters are used:

- With 4 letters, the probability of word change is 5.12%
- With 5 letters: the probability of word change is 0.74%
- With 6 letters, the probability of word change is 0.49%

---

Up: [README](../README.md) | Next: [What Can Go Wrong?](what-can-go-wrong.md)
