# Contributing to Dundie Rewards

Thank you for considering contributing to Dundie Rewards! We welcome contributions from the community and are excited to work with you.

## How to Contribute

1. **Fork the repository**: Click the "Fork" button at the top right of the repository page.
1. **Clone your fork**: Clone your forked repository to your local machine.

        git clone https://github.com/your-username/dundie-rewards.git

1. **Create a branch**: Create a new branch for your feature or bugfix.

        git checkout -b my-feature-branch

1. **Make changes**: Make your changes to the codebase.
1. **Commit your changes**: Commit your changes with a descriptive commit message.

        git commit -m "Description of my changes"

1. **Push to your fork**: Push your changes to your forked repository.

        git push origin my-feature-branch

1. **Create a Pull Request**: Open a pull request to the main repository. Provide a clear description of your changes and any related issues.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](code_of_conduct.md). By participating in this project, you agree to abide by its terms.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub. Be sure to include as much detail as possible to help us understand and address the issue.

## Development Setup

To set up a development environment, follow these steps:

1. **Install dependencies**

    Install the required dependencies:

        make install

1. **Load Python virtual environment**

    Load Python virtual environment:

        # For 'sh' or 'bash' shell:
        source .venv/bin/activate
        # or for another supported shell
        source .venv/bin/activate.<shell>
        # Example for 'fish' shell
        source .venv/bin/activate.fish

1. **Run source code checker and formatting tools**

    Run source code checker and formatting tools before committing any changes:

        make lint
        make fmt

1. **Run tests**

   Run the test suite to ensure everything is working correctly:

        make test
        # or
        make watch

## Style Guide

Please adhere to the following style guides when contributing to this project:

- **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- **Commit messages**: Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages.

## Thank You

Thank you for your interest in contributing to Dundie Rewards! Your contributions are greatly appreciated.

[//]: # (This document uses the workaround mentioned in: https://stackoverflow.com/questions/57366489/code-block-in-a-numbered-list-messes-up-numbering-python-markdown-mkdocs)
