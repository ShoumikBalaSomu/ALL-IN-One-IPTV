# Security & Secrets Management

To run the automated CI/CD pipeline and the Phase 1 Aggregator successfully, you must configure GitHub Secrets to store your sensitive credentials safely.

**NEVER HARDCODE CREDENTIALS, TOKENS, OR KEYSTORES IN THE REPOSITORY CODE.**

## 1. Required Secrets for CI/CD (Phase 5)

To automatically compile and sign the Android release builds (`.apk` and `.aab`), navigate to:
**GitHub Repository -> Settings -> Secrets and variables -> Actions**, and add the following **Repository Secrets**:

| Secret Name | Description |
| :--- | :--- |
| `KEYSTORE_BASE64` | The Base64 encoded string of your Android `upload-keystore.jks` file. |
| `KEYSTORE_PASSWORD` | The password for your keystore file. |
| `KEY_ALIAS` | The alias of the key within the keystore. |
| `KEY_PASSWORD` | The password for the specific key alias. |

### How to generate `KEYSTORE_BASE64`
Run this command on your local terminal (Linux/macOS) to convert your `.jks` file to a Base64 string that can be pasted into GitHub Secrets:
```bash
base64 -i upload-keystore.jks > keystore_base64.txt
# Open keystore_base64.txt and copy its contents into GitHub Secrets
```

## 2. GitHub Action Token (`GITHUB_TOKEN`)
The `GITHUB_TOKEN` is automatically provided by GitHub Actions for creating releases. 
*   Ensure that your repository has the correct permissions. Go to **Settings -> Actions -> General**.
*   Under **Workflow permissions**, select **Read and write permissions**. This allows the `softprops/action-gh-release` step to attach the compiled binaries to the release.

## 3. Custom API Keys (Future Proofing)
If Phase 2 (The Player) integrates the TMDB API for movie posters, add the key as `TMDB_API_KEY`. The Dart compile step will inject this via `--dart-define=TMDB_API_KEY=${{ secrets.TMDB_API_KEY }}`.
