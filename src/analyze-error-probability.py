"""Analyze the effect of single-letter errors on bip-39 words."""

# Alphabet for psst; note that "j" is missing (it's the same as "x").
alphabet = "abcdefghiklmnopqrstuvwxyz"

def count_errors(words):
    num_changes = 0
    num_errors = 0
    word_set = set(words)

    for word in words:
        for pos in range(len(word)):
            for c in alphabet:
                modified = list(word)
                modified[pos] = c
                modified = "".join(modified)
                if modified != word:
                    num_changes += 1
                    if modified in word_set:
                        num_errors += 1

    return (num_changes, num_errors)

with open('src/bip39-wordlist-en.txt') as f:
    words = [w.strip() for w in f]

# In psst, "j" is the same as "x"
words = [w.replace("j", "x") for w in words]

for length in [4, 5, 6]:
    truncated = [w[:length] for w in words]
    assert len(truncated) == len(set(truncated))

    num_changes, num_errors = count_errors(truncated)
    print(f"With {length} letters: {num_changes:8d} substitutions, {num_errors:5d} errors")
    print(f"  error probability: {100 * num_errors / num_changes:.2f}%")

# With 4 letters:   194136 substitutions,  9936 errors
#   error probability: 5.12%
# With 5 letters:   230208 substitutions,  1702 errors
#   error probability: 0.74%
# With 6 letters:   252960 substitutions,  1238 errors
#   error probability: 0.49%
