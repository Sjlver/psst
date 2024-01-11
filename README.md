# psst: Paper-based Secret Sharing Technique

`psst` is a system for storing secrets without a single point of failure. `psst`
helps the user to split a secret into up to four parts. Each part in isolation
reveals nothing about the secret (except its length). Any two parts combined
allow the secret to be restored.

The main goal of `psst` is simplicity. It is a system that can be used with just
pen, paper and a six-sided dice. `psst` is great for people who want to deeply
understand what they do and verify every step, and for anyone who has fun with
information theory and cryptography.

`psst` is a restricted case of
[Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing),
operating in GF(5) with a threshold of two. See the
[Design Choices](docs/design-choices.md) document for more information about that
choice.

## How to use `psst`?

1. Download the `psst` worksheet: \
   [`psst` PDF (A4 paper)](docs/psst-worksheet.pdf) \
   [`psst` PDF (US Letter)](docs/psst-worksheet-usletter.pdf)
2. Print the worksheet.
3. Follow the instructions on the printed worksheet.

## Find out more

`psst` was built as a fun way to learn about topics like cryptography and
information theory. The [Motivation](docs/motivation.md) document describes why
we made `psst`, and explains its pros and cons.

The [Design Choices](docs/design-choices.md) document explains and justifies all
the choices that went into designing `psst`.

In [What Can Go Wrong](docs/what-can-go-wrong.md), you can read about insecure
ways of using `psst`, and potential attacks against its users.

[Where and How to Store Shares](docs/storing-shares.md) discusses what to
consider after someone has used `psst`, when they need a place to store their
secret shares.

The page [Supplemental Materials](docs/supplemental-materials.md) contains
tables that might be useful for some use cases, but did not fit onto the
worksheet.

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

BIP-39 Split Mnemonic is a simple 2-of-3 scheme implemented in
[Ian Coleman's BIP-39 tool](https://iancoleman.io/bip39/). It generates three
shares, each containing two thirds of the words in the seed phrase. The sets of
words overlap, so that any two shares contain the full phrase. Split Mnemonics
are much simpler to use than `psst`. On the other hand, each share only has a
third of the entropy of the full seed. For short seeds (e.g., 12 words), this is
only 42 bits, so the full seed can be brute-forced in relatively little time.
For 24-word seeds, the brute-force approach is prohibitively expensive.

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
