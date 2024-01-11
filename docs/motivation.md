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
[alternatives](../README.md#alternatives).

---

Up: [README](../README.md) | Next: [Design Choices](design-choices.md)
