"""Exact verifier for a step-function upper bound on C_1d.

For a step function f with n equal cells on [-1/4,1/4] and cell values v_0..v_{n-1},
f*f is piecewise linear with knots at multiples of h=1/(2n), and
    (f*f)(mh) = h * sum_{i+j=m} v_i v_j,
so the ratio  max_t |f*f| / (int f)^2  equals
    2n * max_m |sum_{i+j=m} v_i v_j| / (sum_i v_i)^2,
an exact rational number.  Values are read as exact binary64 rationals.

Usage:  python -I verify.py construction.json
Standard library only.
"""
import json, sys
from fractions import Fraction

def ratio(v):
    n = len(v)
    S = sum(v)
    if S == 0:
        raise ValueError("sum of cell values is zero")
    best = Fraction(0)
    for m in range(2*n - 1):
        lo = max(0, m - n + 1)
        hi = min(m, n - 1)
        s = sum((v[i] * v[m-i] for i in range(lo, hi+1)), Fraction(0))
        if abs(s) > best:
            best = abs(s)
    return Fraction(2*n) * best / (S * S)

def decimal(fr, digits=40):
    sign = "-" if fr < 0 else ""
    num, den = abs(fr.numerator), fr.denominator
    ip, rem = divmod(num, den)
    out = sign + str(ip) + "."
    for _ in range(digits):
        rem *= 10
        out += str(rem // den)
        rem %= den
    return out

if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    vals = d["values"] if isinstance(d, dict) else d
    v = [Fraction(float(x)) for x in vals]
    r = ratio(v)
    print("n =", len(v))
    print("ratio =", decimal(r))
    print("exact = %d/%d" % (r.numerator, r.denominator))
