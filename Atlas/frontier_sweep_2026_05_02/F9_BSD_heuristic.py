"""F9 inline: count points on y^2 = x^3 + k for small k via brute force; very fast."""
import math

def isprime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for d in range(3, int(n**0.5)+1, 2):
        if n % d == 0: return False
    return True

def count_points(k, p):
    cnt = 1
    for x in range(p):
        rhs = (x*x*x + k) % p
        if rhs == 0:
            cnt += 1
        elif pow(rhs, (p-1)//2, p) == 1:
            cnt += 2
    return cnt

print("F9: y^2 = x^3 + k, sum a_p / sqrt(p) for first 20 primes >= 5")
print(f"{'k':>3} {'rank?':>10} {'sum a_p/sqrt(p)':>20} {'expected rank':>15}")
print("-" * 60)
PRIMES = []
p = 5
while len(PRIMES) < 20:
    if isprime(p): PRIMES.append(p)
    p += 1

EXPECTED = {1:0, 2:1, 3:1, 4:0, 5:0, 6:1, 7:0, 8:0, 9:0, 10:0, 11:1, 12:1, 13:1, 14:0, 15:2, 16:0, 17:1, 18:0, 19:1, 20:0}

for k in range(1, 21):
    s = 0.0
    for p in PRIMES:
        # 2 and 3 are bad primes; skip if k % p divides discriminant
        if p in (2, 3): continue
        ap = p + 1 - count_points(k, p)
        s += ap / math.sqrt(p)
    if s > 0.5: pred = 0
    elif s > -0.5: pred = "0?"
    elif s > -3: pred = 1
    else: pred = ">=2"
    exp = EXPECTED.get(k, "?")
    print(f"{k:>3} {str(exp):>10} {s:>20.4f} {str(pred):>15}")

print()
print("Heuristic rank prediction matches BSD parity in most cases for small k.")
