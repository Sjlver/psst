"""Generates linear polynomials for Shamir's Secret Sharing with threshold 2."""

def add(x, y):
    """Addition in GF(5)."""
    return (x + y) % 5

def mul(x, y):
    """Multiplication in GF(5)"""
    return (x * y) % 5

DICES = "⚀⚁⚂⚃⚄⚅"

# Generate `a*x + b`` for all `a` and `b`, evaluated at all `x`.
polys = []
for a in range(5):
    for b in range(5):
        polys.append([add(mul(a, x), b) for x in range(5)])

# Print tables for generating shares.
#
# We use `x=0`` for the secret, and `x=1...4` for the four shares.
print("Table for generating shares:")
for i, poly in enumerate(sorted(polys, key=tuple)):
    if i > 0 and i % 5 == 0:
        print()
    print(f"{poly[0]}  {DICES[i % 5]}  {'  '.join(str(y) for y in poly[1:])}")
    if i % 5 == 4:
        print(f"{poly[0]}  {DICES[5]}  re-throw")

for i in range(1, 5):
    print()
    print(f"Table for share #{i}")
    for j, poly in enumerate(sorted(polys, key=lambda x: (x[i], x[0]))):
        if j > 0 and j % 5 == 0:
            print()
        print("  ".join(str(y) for y in poly))
