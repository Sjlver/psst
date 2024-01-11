"""Generates conversion tables between ASCII and base five triplets."""

print("| Char | ASCII | Digits | Char | ASCII | Digits | Char | ASCII | Digits |")
print("|------|-------|--------|------|-------|--------|------|-------|--------|")

num_rows = (128 + 2) // 3
for char_base in range(num_rows):
    print("|", end="")
    for col in range(3):
        char = char_base + col * num_rows
        if char > 127:
           print("      |       |        |", end="")
           continue

        formatted = chr(char) if 32 <= char < 127 else " "
        if char >= 3:
          d25 = (char - 3) // 25
          d5 = (char - 3 - 25 * d25) // 5
          d1 = (char - 3 - 25 * d25 - 5 * d5)
        else:
           d25 = d5 = d1 = " "
        print(f"    {formatted} |  {char:3d}  |   {d25}{d5}{d1}  |", end="")
    print()
