# psst: Paper-based Secret Sharing Technique

`psst` is a system for storing secrets without a single point of failure. `psst`
helps the user to split a secret into up to four parts. Each part in isolation
reveals nothing about the secret (except its length). Any two parts combined
allow the secret to be restored.

The main goal of `psst` is simplicity. It is a system that can be used with just
pen, paper and a six-sided dice.

`psst` is a restricted case of
[Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing),
operating in GF(5) with a threshold of two. See the
[Design Choices](#design-choices) section below for more information about that
choice.

## How to use `psst`?

1. Download the [`psst` PDF (A4 paper)](docs/psst-worksheet.pdf).
2. Print the PDF.
3. Follow the instructions on the printed PDF.

## Motivation

### Why use `psst`?

- It's fun. You may officially
  [call yourself a geek](https://phdcomics.com/comics/archive.php?comicid=25) if
  you use it.
- You might learn something about finite fields and information theory :)
- That's all there is, really. Please don't use `psst` if you don't find it fun,
  or if you need a secure, tried, certified, compliant, or peer-reviewed system.

### The fundamental trade-off between security and availability

The most common way to store secrets like BIP-39 seed phrases is to make a paper
copy. This provides a basic level of _security_ and _availability_:

- **Security:** Malicious actors who want to steal the secret need to know where
  it is stored, and get physical access to it. Users can improve security by
  hiding the secret, putting it in a bank vault, and similar techniques.
- **Availability:** The secret is backed up. Users can improve availability by
  creating multiple copies. They can make copies highly durable, for example by
  engraving the secret in a metal plate.

Users face various trade-offs between security and availability. For example,
hiding a secret can improve security, but also reduces availability because
recovering the secret becomes more difficult. Similarly, creating multiple
copies improves availability, but reduces security because any of the copies
could be compromised.

`psst` provides a different trade-off:

- **`psst` security:** `psst` improves security, because malicious actors need
  to obtain two of the shares. This can be significantly harder than accessing a
  single secret.

  Note, however, that `psst` still has single points of failure: the full secret
  is present when it is being split and when it is being recovered, so these
  moments remain critical. Also, once the secret is to be used, it probably
  needs to be entered into some electronic device, which could contain malware
  or otherwise be compromised.

- **`psst` availability:** `psst` improves availability, because users can more
  safely create multiple copies of their shares.

  Note, however, that `psst` adds complexity and introduces more opportunities
  for errors. If `psst` is used incorrectly, shares might contain the wrong data
  and the secret might be lost.

Before using `psst`, users should carefully consider their needs and risks with
respect to security and availability. Please evaluate whether `psst` really
provides a better trade-off than the existing solution. Please also read about
[alternatives](#alternatives) below.

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
secret sharing, and use one of the [alternatives](#alternatives).

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
[alternative implementations](#alternatives) of Shamir's Secret Sharing.

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

## Where and how to store shares?

How to store shares is up to you, the user! It is a complex question for which
we provide only minimal guidance here. The main recommendation is to store
shares in different physical locations; otherwise, there is again a single point
of failure, and not much is gained by using `psst`.

An important consideration is whether to give shares to other people, or to
store them in locations that only you have access to. By involving other people,
you can potentially increase the availability of shares. You can give
instructions for what to do with shares in emergencies or when you die.

That said, involving other people also puts trust and responsability on them. It
might put people at risk. In extreme cases, they might get robbed or kidnapped
by people who want to obtain the secret share. Please follow `psst`s principle
to only include people who have fun participating.

## Alternatives

A number of other implementations if Shamir's Secret Sharing exist:

- [SLIP-0039](https://github.com/satoshilabs/slips/blob/master/slip-0039.md)
  is a scheme for hardware wallet seeds, supported by Trezor.
- [SSKR](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-011-sskr.md)
  is a generic crypto-focused scheme.
- [EIP 3450](https://eips.ethereum.org/EIPS/eip-3450) is an unfinished proposal
  focusing on BIP-39 seeds.
- [ssss](http://point-at-infinity.org/ssss/) is a Unix utility.

[SeedXOR](https://seedxor.com/) is a scheme that can be implemented using pen
and paper, like `psst`. The main difference is that it only supports _n_-of-_n_
schemes, for example 2-of-2. If even one share is lost, the secret cannot be
recovered.

For many use cases, it is better to avoid secret sharing altogether. For
example, to securely store cryptocurrency, a multisig scheme has advantages. For
a detailed discussion, refer to
[CasaBlog: Shamir's Secret Sharing Shortcomings](https://blog.keys.casa/shamirs-secret-sharing-security-shortcomings/).

For a good overview of considerations for storing secrets, see
[How to Back Up a Seed Phrase](https://blog.lopp.net/how-to-back-up-a-seed-phrase/).

## Acknowledgements

`psst` was started by [Sjlver](https://github.com/Sjlver) and builds on the
thinking of many others.

If you have fun using `psst`, you can send a tip:

- Bitcoin: `bc1q3hnhtgrse3etk52m626zxrkz0hah8hkag4et38`
- Ethereum: `0xAF16c970cb2329E9c3B8f4E54e1e8580937f8406`
