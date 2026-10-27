# A 400-cell step-function upper bound for C_1d

A step function $f$ with $400$ equal cells on $[-1/4,1/4]$ whose ratio

$$
\frac{\max_{t}|(f*f)(t)|}{\left(\int f\right)^2}
$$

equals

```
4563650116209721766004955898613711667200
------------------------------------------ = 1.45915622115964902113867025598980308725579358542519...
3127595284199802099438492053245424408273
```

exactly. This is an upper bound for the signed third autocorrelation constant
$C_{1d}$ in Terence Tao's
[Optimization Constants in Mathematics](https://teorth.github.io/optimizationproblems/constants/1d.html).

## Relation to previously recorded bounds

The bounds recorded for $C_{1d}$ (as of 27 October 2026) are:

| bound | cells | source |
| --- | --- | --- |
| $1.4630715826075594$ | 300 | CERT2026, independently replayed |
| $1.4602172840228739$ | 600 | STEPS2026 |
| $1.4599890469053832$ | 600 | AlphaEvolve (AER2026) |
| $1.4578548849219886$ | 800 | SCiEL (SCIEL2026), certificate restricted |

The construction in this repository is a **new 400-cell bound**, smaller than the
recorded 300-cell and 600-cell values. It does **not** improve on the 800-cell
SCiEL bound $1.4578548849\ldots$, whose certificate is a restricted-access Zenodo
deposit and could not be replayed here.

## Verification

```
python -I verify.py construction.json
```

`verify.py` uses only the Python standard library. For a step function on a uniform
grid with $n=400$ cells and cell width $h=1/800$, $f*f$ is piecewise linear with
knots at integer multiples of $h$, so

$$
\max_t |(f*f)(t)| = h \max_{0\le m\le 2n-2}\left|\sum_{i+j=m} v_i v_j\right|,
\qquad
\int f = h\sum_i v_i,
$$

and the ratio above is computed in exact rational arithmetic. The verifier prints
the ratio rounded up, together with the exact fraction. The same fraction was
obtained by a second, independent implementation that scales all cell values to
integers over a common power-of-two denominator and computes the autoconvolution
in integer arithmetic.

- `construction.json`: 400 cell values as binary64 numbers, each read as an exact
  rational.
- SHA-256 of `construction.json`: `c489b46b894358d8934b378a577c04bd442d5dc784799de62b61d2f79a0358df`

## Method

Sequential linear-programming descent on the exact two-sided discrete objective

$$
\min_v\ \frac{2n\max_m\left|\sum_{i+j=m}v_iv_j\right|}{\left(\sum_i v_i\right)^2},
$$

initialized from the state-of-the-art construction for the **one-sided** variant
(minimize $\max_m \sum_{i+j=m}v_iv_j$; the 400-cell Together AI construction from
EinsteinArena / arXiv:2606.10402, whose one-sided score is $1.4545549$), then
refined by repeated perturbation and descent at $n=400$.

## AI disclosure

The optimization, verification and drafting were carried out with Claude Code
(Anthropic) under the direction of the contributor. The contributor has reviewed
the numerical claims.
