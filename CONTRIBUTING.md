# Contributing to Hued

Thank you for considering contributing to **Hued**! Contributions, whether they are bug fixes, new features, or documentation improvements, are always welcome.

## Getting Started

1. **Fork and Clone**
   Fork this repository to your GitHub account and clone it locally.

2. **Set Up a Development Environment**
   Hued requires Python **3.9+** and has zero runtime dependencies. Install editable mode with development tools:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Run Linter and Tests**

   ```bash
   ruff check .
   pytest
   ```

## How to Contribute

1. **Report Issues**
   Use the [GitHub Issues page](https://github.com/Infinitode/Hued/issues) to report bugs or suggest features with clear descriptions and reproduction steps.

2. **Make Changes**
   - Write clear, descriptive commit messages.
   - Follow [PEP 8](https://peps.python.org/pep-0008/) and ensure `ruff check .` passes cleanly.
   - Add or update unit tests in `Tests/` covering your changes.

3. **Submit a Pull Request**
   - Push your changes to a feature branch in your fork.
   - Open a pull request explaining what changed and why.
   - Ensure all CI checks pass.

## Community Guidelines

1. **Be Respectful** — Treat everyone with respect, regardless of background or experience.
2. **Provide Constructive Feedback** — Offer helpful, actionable suggestions in code reviews.
3. **Follow Licensing Requirements** — Ensure derivative works comply with the [LICENSE](LICENSE).

By contributing, you agree to abide by these guidelines and this project's [LICENSE](LICENSE). Thank you for helping make **Hued** better!
