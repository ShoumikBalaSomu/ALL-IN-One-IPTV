# 🛡️ Security Policy

## Supported Versions

Only the current major release branch is actively supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 2.1.x   | :white_check_mark: |
| 2.0.x   | :white_check_mark: |
| 1.5.x   | :x:                |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability within ALL-IN-One IPTV, please **DO NOT** disclose it publicly via GitHub Issues. 

Instead, please send an email to:
**security@all-in-one-iptv.local** (placeholder) or contact the core maintainer directly.

We will acknowledge receipt of your vulnerability report within 48 hours and strive to provide a patch or mitigation strategy within 7 days.

## Encryption Guidelines

- **API Keys & Secrets:** The system uses an AES-256 XOR vault structure for storing any necessary API keys or proxy credentials in memory. Do not hardcode credentials in source code.
- **Client-Server Communication:** Ensure that the Ktor Gateway is always deployed behind an HTTPS reverse proxy (e.g., Nginx, Traefik) in production. The engine supports TLS out of the box.

## Release Security Matrix

Before every release, we audit the codebase against the following matrix:
1. **Dependency Audit:** Run `pip-audit` on the Python Engine and `npm audit` on the Web Player.
2. **Network Isolation:** Ensure the Verifier cleanly closes sockets and does not expose local ports unnecessarily.
3. **Input Sanitization:** Validate all incoming M3U strings to prevent buffer overflows or code injection via maliciously crafted `#EXTINF` tags.
