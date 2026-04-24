# BHML disambiguation — the two determinants

There are two BHML matrices. Both determinants are correct; they refer to different tables.

| Table | Shape | det | Primes | Source |
|---|---|---:|---|---|
| `BHML_10` | 10×10 | `−7002` | {2, 3, 389} | `papers/ck_tables.py`; `FORMULAS_AND_TABLES.md` §6 |
| `BHML_8`  | 8×8   | `+70`   | {2, 5, 7}   | BHML_10 with rows/cols {0, 7} removed; WP15 §0 |

Verify:

```bash
python -c "from sympy import Matrix; BHML=[[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],[3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],[6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],[9,6,6,6,7,7,7,0,8,0]]; C=[1,2,3,4,5,6,8,9]; sub=[[BHML[i][j] for j in C] for i in C]; print(Matrix(BHML).det(), Matrix(sub).det())"
# -> -7002 70
```

When reading any file that says "`det(BHML) = X`", match the context to the table:
- 10×10 / full / canonical §6 → `BHML_10`, det `−7002`
- 8×8 / core / transfer matrix / WP15 spectral → `BHML_8`, det `+70`

Canonical registry: `FORMULAS_AND_TABLES.md` §6.7.
