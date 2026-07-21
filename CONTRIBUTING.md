# 🤝 Contributing to ALL-IN-One-IPTV

First off, thank you for considering contributing! 🎉 This project exists because of amazing community members like you.

---

## 📋 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct:

- Be respectful and inclusive
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

---

## 🚀 How Can I Contribute?

### 🐛 Reporting Bugs

1. **Search** existing issues first to avoid duplicates
2. Use the **Bug Report** template
3. Include:
   - **Environment**: OS, app version, device
   - **Steps to reproduce** the issue
   - **Expected behavior** vs **Actual behavior**
   - **Screenshots/logs** if applicable

### ✨ Suggesting Features

1. **Search** existing issues to check if it's already proposed
2. Use the **Feature Request** template
3. Provide:
   - Clear description of the feature
   - **Why** it would benefit the project
   - Any relevant examples or mockups

### 🔧 Code Contributions

#### 1. Fork & Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/ALL-IN-One-IPTV.git
cd ALL-IN-One-IPTV
git remote add upstream https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV.git
```

#### 2. Create a Branch

```bash
# Always branch from main
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### 3. Make Your Changes

Follow the coding standards for each component:

| Component | Language | Linter | Formatter |
|-----------|----------|--------|-----------|
| Aggregator | Python 3.12+ | `ruff` | `black` |
| Flutter App | Dart 3.2+ | `flutter analyze` | `dart format` |
| Kotlin App | Kotlin 1.9+ | `ktlint` | ktlint format |
| Web Player | JavaScript/TS | `eslint` | `prettier` |
| Backend | Python 3.12+ | `ruff` | `black` |

#### 4. Test Your Changes

```bash
# Python Engine
cd engine
pip install -r requirements.txt
python -m pytest tests/

# Flutter App
cd apps/app_player
flutter test
flutter analyze

# Kotlin App
cd apps/app_proxy
./gradlew test
```

#### 5. Commit & Push

```bash
git add .
git commit -m "feat: add your descriptive commit message"
git push origin feature/your-feature-name
```

**Commit message format** (Conventional Commits):
- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation changes
- `style:` — Code style changes (formatting, semicolons, etc.)
- `refactor:` — Code refactoring
- `test:` — Adding/updating tests
- `chore:` — Maintenance tasks

#### 6. Open a Pull Request

- Fill out the PR template completely
- Link any related issues
- Include screenshots for UI changes
- Wait for review

---

## 📁 Project Structure & What to Contribute

### 🔧 Aggregator (`aggregator.py` + `services/backend/`)

**Good first issues:**
- Add new playlist sources to `DATA_SOURCES`
- Improve country detection logic
- Add new URL health-check strategies
- Write unit tests for parser functions
- Improve deduplication algorithm

### 📱 Flutter Player (`apps/app_player/`)

**Good first issues:**
- Add new UI themes
- Improve channel search
- Add parental controls UI
- Implement picture-in-picture mode
- Add EPG display improvements
- Support new input formats

### 🛡️ Kotlin Proxy (`apps/app_proxy/`)

**Good first issues:**
- Improve proxy routing algorithm
- Add VPN integration UI
- Implement notification system
- Add bandwidth meter
- Optimize background service

### 🌐 Web Player (`docs/`)

**Good first issues:**
- Add responsive design improvements
- Improve video player controls
- Add keyboard shortcuts
- Implement dark/light theme toggle
- Add channel favorites

### 🐳 Backend Services (`services/backend/`)

**Good first issues:**
- Add new DRM token fetcher plugins
- Improve EPG matching accuracy
- Add new transcoder presets
- Implement IPFS auto-publishing
- Add WebSocket health monitoring

---

## 🔐 Security

- **Never commit secrets, tokens, or credentials**
- Use GitHub Secrets for CI/CD credentials
- Report security vulnerabilities privately via [Security Advisories](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/security/advisories/new)
- Follow the guidelines in [SECURITY.md](./SECURITY.md)

---

## 📝 Documentation

Documentation improvements are always welcome:

- Fix typos or grammar in existing docs
- Add missing documentation for features
- Translate README to other languages
- Add screenshots or GIFs
- Improve the README structure

---

## 🧪 Testing Guidelines

- Always add tests for new features
- Ensure all existing tests pass before submitting
- Test on multiple platforms if your change affects UI
- For the aggregator, test with at least 3 different playlist formats

---

## 📦 Adding New Playlist Sources

To add a new playlist source:

1. Find a **publicly available** M3U/M3U8 playlist URL
2. Add it to the `DATA_SOURCES` list in `services/backend/scraper.py`
3. Add it to the `PLAYLISTS` list in `aggregator.py`
4. Test that it parses correctly:
   ```bash
   python aggregator.py
   ```
5. Verify the channel appears in `output/combined_by_country.m3u`
6. Thank the maintainer in [CREDITS.md](./CREDITS.md)

---

## 🎨 UI/UX Guidelines

- Follow existing design patterns in the codebase
- Use the established color scheme (Netflix red `#E50914`, Cyan `#00C6FF`, Purple `#8A2BE2`)
- Ensure accessibility (contrast ratios, font sizes)
- Support both light and dark themes where applicable
- Test on multiple screen sizes

---

## 🚫 What NOT to Do

- ❌ Don't commit generated playlist output files (they're in `.gitignore`)
- ❌ Don't hardcode credentials or API keys
- ❌ Don't break existing functionality without a good reason
- ❌ Don't add unnecessary dependencies
- ❌ Don't submit AI-generated code without reviewing it
- ❌ Don't include copyrighted content or private streams

---

## 💬 Getting Help

- **Questions**: Open a [Discussion](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/discussions)
- **Bugs**: Open an [Issue](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/issues)
- **Chat**: Join our community (link in README)

---

## 🏆 Becoming a Maintainer

Active contributors who consistently help the project may be invited to become maintainers. Requirements:

- 5+ merged PRs
- Active participation in issue reviews
- Deep understanding of the codebase
- Adherence to project values

---

<div align="center">

**Thank you for making ALL-IN-One-IPTV better! 🙏**

</div>