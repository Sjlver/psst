# psst: Paper-based Secret Sharing Technique

`psst` is a system for storing secrets in a secure way. At its core, it is an
implementation of Shamir's Secret Sharing with a strong emphasis on recovery.
`psst` produces paper documents ("shares") that contain information about a
secret, such that _k_ shares together can recover thbe secret. `psst` shares are
self-contained, containing all information needed to perform the recovery
procedure. At the same time, `psst` shares are secure in the sense that someone
with access to fewer than _k_ shares learns nothing about the secret.
