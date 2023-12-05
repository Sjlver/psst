# psst: Paper-based Secret Sharing Technique

`psst` is a system for storing secrets in a secure way. `psst` helps the user to
split a secret into up to four parts. Each part in isolation reveals nothing
about the secret (except its length). Any two parts combined allow the secret to
be restored.

The main goal of `psst` is simplicity. It is a system that can be used with just
pen, paper and a six-sided casino dice.

`psst` is a restricted case of Shamir's Secret Sharing, operating in GF(5) with
a threshold of two. See the [Rationale](#rationale) section below for more
information about that choice.

## How to use `psst`?

1. Download the [`psst` PDF (A4 paper)](TODO).
2. Print the PDF.
3. Grab a pen and a high-quality dice.
4. Follow the instructions on the printed PDF.

## Why to use `psst`?

- It's fun. You may officially call yourself a geek if you use it.
- You might learn something about finite fields and information theory :)
- That's all there is, really. Please don't use `psst` if you don't find it fun,
  or if you need a secure, tried, certified, compliant, or peer-reviewed system.

## Rationale

### Use cases for `psst`

Before using `psst`, the authors had paper copies of various important secrets,
such as cryptographic seeds used by cryptocurrency wallets, and master
passwords. This provides a basic level of _security_ and _availability_:

- **Security:** Malicious people need to know where the secret is stored, and
  get physical access to it. Users can improve security by hiding the secret,
  putting it in a bank vault, and similar techniques.
- **Availability:** The secret is backed up. Users can improve availability by
  creating multiple copies. They can make copies highly durable, for example by
  embossing the secret in a metal plate.

Users face various trade-offs between security and availability. For example,
hiding a secret can improve security, but also reduces availability because
recovering the secret becomes more difficult. Similarly, creating multiple
copies improves availability, but reduces security because any of the copies
could be compromised.

`psst` provides a different trade-off:

- **`psst` security:** `psst` improves security because malicious people need to
  obtain two of the shares. This can be significantly harder than accessing
  a single secret.

  Note, however, that `psst` still has single points of failure: two shares must
  be present at the time when the secret is split and when it is recovered, so
  these moments remain critical. Also, once the secret is to be used, it
  probably needs to be entered into some electronic device which could contain
  malware or otherwise be compromised.

- **`psst` availability:** `psst` improves availability because users can more
  safely create multiple copies of their shares. Social recovery becomes easier.
  Shares can be given to trusted people along with instructions that explain
  what to do in an emergency or if the original owner dies.

  Note, however, that `psst` adds complexity and introduces more opportunities
  for errors. If `psst` is used incorrectly, shares might contain the wrong data
  and the secret might be lost.

Before using `psst`, users should carefully consider what their security and
availability risks are, and whether `psst` provides a better trade-off than
their existing solution. Please also read about [alternatives](#alternatives)
below.

### Design choices

When designing `psst`, we wanted to create an implementation of Shamir's Secret
Sharing Scheme that is as simple, easy to use, and easy to understand as
possible. This ensures that recovery is possible even though the world might
have changed since the shares were created. It makes the system applicable to
many use-cases. It avoids vendor lock-in and dependence on proprietary
solutions.

We quickly realized that any full implementation of Shamir's Secret Sharing is
too complex for these goals. Implementations face a number of subtle choices:
how to encode shares, how to choose sizes and thresholds, which finite field to
use, etc. Most alternative implementations add encryption, checksums,
verifiability for shares and secrets, and other features. While these can
improve security and usability, they also increase the system's complexity.

- Why GF(5)?
- Why not a smaller field for even more simplicity?
- If dice are so cool, why not GF(6)?
- Why is there no checksum?
- Why 2-of-4?
- Why merge j and x?
- Why pad with q?

TODO: explain why each feature was chosen

- Don't add a checksum

- Add a checksum

  - TODO: unsure how this would work. I don't want to use a parity byte or
    Fletcher's Checksum, since these are linear => easy to predict how a change
    to a share affects the checksum.
  - Add the check values for each byte to obtain the checksum _s_
  - The four checksum bytes are `s % 251`, `s % 241`, `s % 239`, and `s % 233`

- No XOR: it only supports 2-of-2 or 3-of-3... It hides a number of tricky
  design choices, such as how to encode letters of the alphabet.

### Alternatives

A number of other implementations if Shamir's Secret Sharing exist:

- [SLIP-0039](https://github.com/satoshilabs/slips/blob/master/slip-0039.md)
- [SSKR](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-011-sskr.md)
- [EIP 3450](https://eips.ethereum.org/EIPS/eip-3450)
- The [ssss](http://point-at-infinity.org/ssss/) Unix utility

For many use cases, it is better to avoid secret sharing altogether. For example, to securely store cryptocurrency, a multisig scheme has advantages. For a detailed discussion, refer to [CasaBlog: Shamir's Secret Sharing Shortcomings](https://blog.keys.casa/shamirs-secret-sharing-security-shortcomings/).

For a good overview of considerations for storing secrets, see [How to Back Up a Seed Phrase](https://blog.lopp.net/how-to-back-up-a-seed-phrase/).

## Implementation

### Splitting a secret into shares

- Encode the secret _s_ as bytes
  - It could already be in hexadecimal form or bytewords
  - Users can use the provided ASCII table
  - For BIP-39 mnemonics, users can use the first four letters of each word and
    encode them as ASCII.
- Obtain a series of random bytes _r_, of the same length as the secret
- For each byte, compute _x_ the XOR (addition modulo 256) of the secret _si_
  and the corresponding random byte _ri_.
- The first share is _r_.
- The second share is _x_.

Final length of a share for a 24-word BIP-39 mnemonic: 24 \* 4 = 96 bytewords.

For offline randomness, can use 2 d20 (one for the row and one for the column of
a 16x16 grid) to generate _r_. That said, it's easier to generate the _r_ share
on a computer and print it (or store it in one or more safe digital places).

Recommend to create papers with instructions and space to write the secret.
Paper should be folded, then labeled, then the outermost layer cut, then sealed.

TODO: instructions on how to label shares.

## Outdated ideas

At its core, it is an implementation of Shamir's Secret Sharing with a strong
emphasis on recovery. `psst` produces paper documents ("shares") that contain
information about a secret, such that _k_ shares together can recover the
secret. `psst` shares are self-contained, containing all information needed to
perform the recovery procedure. At the same time, `psst` shares are secure in
the sense that someone with access to fewer than _k_ shares learns nothing about
the secret.

## psst encoding and decoding

`psst` is designed for short inputs such as passwords or cryptographic seeds.
These can contain up to 45 bytes of binary data.

Encoding proceeds as follows:

1. Encode the input _x_ with a variant of `bech32m`. This produces a number _b_
   in base 32. The number includes a checksum, which serves to check whether a
   secret has been successfully recovered.
   - The `bech32m` operation uses "psstx" as human-readable part. This is
     relevant for computing the checksum.
   - The number _b_ is the data part (including checksum but excluding the
     human-readable part) produced by `bech32m`.
2. Split _b_ into shares _s1_ ... _sn_ using an implementation of Shamir's
   Secret Sharing that works in the finite field GF(32) with primitive
   polynomial `x**5 + x**2 + 1`. Each digit of _b_ is shared separately.
3. Encode the shares (again) in `bech32m`. This produces output shares in the
   following format:
   - The human-readable part "psst" followed by the separator "1"
   - 1 character (5 bits of data) for the share number
   - The actual share _si_, 0 to 79 characters
   - 6 characters for the checksum

## Rationale

- **Why not include a version number?** `psst` shares are intended to be stored
  along with sufficient documentation for how to recover them. Even if there are
  multiple versions of `psst`, a share can be recovered with the help of that
  documentation. If all else fails, multiple recovery procedures can be tried in
  sequence until one is found for which all checksum checks pass.
