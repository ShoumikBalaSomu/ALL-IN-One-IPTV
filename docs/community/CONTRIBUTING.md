# Contributing to ALL-IN-One IPTV

First off, thank you for considering contributing to ALL-IN-One IPTV! It's people like you that make this ecosystem great.

## 🚀 Environment Setup

### 1. Python Engine (Backend)
- Ensure **Python 3.12+** is installed.
- Install dependencies:
  ```bash
  cd engine
  pip install -r requirements.txt
  ```

### 2. Ktor Gateway (API)
- Ensure **JDK 17+** is installed.
- Run Gradle wrapper:
  ```bash
  cd api
  ./gradlew build
  ```

### 3. Flutter Client (Mobile/Desktop)
- Ensure **Flutter 3.24+** is installed.
- Get packages:
  ```bash
  cd clients/flutter_app
  flutter pub get
  ```

## 📐 Code Style Standards

We enforce strict coding standards to maintain a pristine codebase.

- **Python**: Follow [PEP 8](https://peps.python.org/pep-0008/). Use `black` for formatting and `mypy` for static type checking.
- **Dart (Flutter)**: Follow the official [Dart style guide](https://dart.dev/guides/language/effective-dart/style). Run `flutter format .`.
- **Kotlin**: Follow the official [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html). Use `ktlint`.

## 🌳 Git Workflow & Conventional Commits

We use the feature-branch workflow and enforce **Conventional Commits**.

### Branch Naming
- `feature/your-feature-name`
- `fix/bug-name`
- `docs/update-name`

### Commit Message Format
Must follow: `<type>(<scope>): <subject>`

Examples:
- `feat(engine): implement ai quantum healer algorithm`
- `fix(flutter): resolve UI overflow in multi-view grid`
- `refactor(api): migrate routes to separate modules`
- `docs(readme): update feature matrix`

## ✅ Pull Request Checklist

Before submitting a PR, please ensure:
- [ ] Code compiles and passes all CI tests.
- [ ] Code is formatted using the respective language tools (`black`, `flutter format`, `ktlint`).
- [ ] Commit messages follow the Conventional Commits standard.
- [ ] Documentation (and docstrings) has been updated if necessary.
- [ ] You have rebased against the latest `main` branch.

## 🐛 Bug Report Template

When opening an issue for a bug, please use the following format:

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run engine with '...'
2. Open Flutter app '...'
3. See error

**Expected behavior**
A clear description of what you expected to happen.

**Environment details**
- OS: [e.g. Ubuntu 22.04]
- Component: [e.g. Python Engine, Web Player]
- Version: [e.g. 2.1.0]