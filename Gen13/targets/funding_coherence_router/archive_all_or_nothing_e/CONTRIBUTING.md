# Contributing to Crystal Bug

This is an open research project. Contributions that advance understanding are welcome.

---

## What We're Looking For

### High Priority

1. **Rigorous quantum number analysis.** Do the (n, l, m, s) assignments satisfy selection rules? Can transitions between states be predicted?

2. **Higher-order operators.** What happens with cubic or quartic operators? Does the codec generalize?

3. **Avalanche statistics.** Better measurement of cascade distributions. Is there a parameter regime where true SOC emerges?

4. **Physical correspondence.** Can the Hamiltonian mapping be connected to known physical systems? Are there Hamiltonians whose iterate maps match the quadratic operator structure?

### Also Welcome

- Bug reports and test failures
- Performance improvements
- Visualization improvements to the React artifact
- Additional benchmark operators for the classifier
- Clearer exposition of the theory

---

## How to Contribute

1. Fork the repository
2. Create a branch for your work
3. Write tests for any new functionality
4. Run the existing test suite to ensure nothing breaks:
   ```bash
   node tests/test_engine_v2.js
   node tests/test_codec_final.js
   node tests/test_physics_w1w2w3.js
   ```
5. Submit a pull request with a clear description of what you changed and why

---

## Code Style

- Vanilla JavaScript (Node.js compatible)
- No external dependencies in core code
- Tests should print clear pass/fail output
- Comments should explain the physics, not just the code

---

## Reporting Issues

If you find a bug, a misclassification, or a theoretical error, please open an issue with:

- What you expected to happen
- What actually happened
- The operator coefficients (a, b, c) that triggered the issue
- Any relevant test output

---

## License Reminder

All contributions fall under the Human Use License v1.0 (see LICENSE). By contributing, you agree that your work will be available under the same non-commercial, humans-only terms.

---

## Contact

Brayden / brayden@7sitellc.com / https://7sitellc.com
