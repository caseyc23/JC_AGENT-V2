# JC Key Locker

JC Agent now ships with a local **Key Locker** that lets you store API keys securely, monitor usage per key, and control budgets from a browser UI.

## What it does

- Stores secrets in your OS keychain via `keyring` if available, and otherwise encrypts secrets at rest with a passphrase.
- Provides a web UI at [http://localhost:8000/keys.html](http://localhost:8000/keys.html) to add, rotate, delete, and budget keys.
- Exposes REST endpoints under `/keys/*` for automation or scripting (listed below).
- Logs token usage per key so you can see estimated spend, usage trends, and enforce budgets.
- Supports `HUGGINGFACE_KEY_FILE` for locked file-based keys and integrates with the `JC_STORAGE_PATH` vault path.

## Getting started

1. Install the new dependencies: `pip install -r requirements.txt` (includes `keyring` and `cryptography`).
2. Start the JC API server (`python jc_agent_api.py` or `uvicorn jc_agent_api:app`).
3. Open <http://localhost:8000/keys.html> and paste your provider key. The UI masks secrets and never returns raw values.
4. Use the passphrase field when you are on the encrypted-file fallback (no keyring). The server also honors `JC_SECRETS_PASSPHRASE` to unlock keys at startup.
5. Once a key is stored, JC adapters automatically retrieve it and log usage (you can view usage details from the UI).

## Environment variables

- `JC_STORAGE_PATH` – Directory where metadata, locked files, and usage logs live. Defaults to `~/.jc-agent` (create it on your 8TB drive if you want long-term storage).
- `JC_SECRETS_PASSPHRASE` – Passphrase that unlocks the encrypted secrets file when keyring is unavailable. Keep it secret and do not check it into git.
- `HUGGINGFACE_KEY_FILE` – Point this to a file that contains your Hugging Face API key if you prefer to store it as a locked file (the server will load it automatically and treat it like a key locker entry).

## Storage modes

1. **Keyring mode (preferred)**
   - If the Python `keyring` package detects your OS keychain (macOS Keychain, Windows Credential Vault, Linux secret service), secrets are stored there and the UI does not require a passphrase.
   - Metadata still lives under `JC_STORAGE_PATH`, but secrets are never written to disk.
2. **Encrypted file mode (fallback)**
   - When keyring is unavailable, the server creates an encrypted file `JC_STORAGE_PATH/secrets.enc` (AES-256-GCM) using the passphrase you provide.
   - The UI asks for the passphrase when listing or modifying keys. The server also reads `JC_SECRETS_PASSPHRASE` so adapters can access secrets without UI interaction.

## API overview

| Endpoint               | Method | Description                                                                  |
| ---------------------- | ------ | ---------------------------------------------------------------------------- |
| `/keys/add`            | POST   | Add a key (name, provider, secret, optional budget). Use JSON payload.       |
| `/keys/list`           | GET    | List stored keys (passphrase query needed for file mode).                    |
| `/keys/edit`           | POST   | Update name/provider/budget or rotate a secret.                              |
| `/keys/delete`         | POST   | Delete a key.                                                                |
| `/keys/get-secret`     | POST   | Internal route that returns the secret (requires passphrase when encrypted). |
| `/keys/usage/{key_id}` | GET    | Get usage summary for a key (tokens, USD costs, entries).                    |

### Example cURL flows

```bash
curl -X POST http://localhost:8000/keys/add \
  -H "Content-Type: application/json" \
  -d '{"name":"HF-main","provider":"huggingface","secret":"hf_xxx","budget":10.0}'

curl "http://localhost:8000/keys/list?passphrase=mysupersecret"

curl "http://localhost:8000/keys/usage/<key-id>?days=30"

curl -X POST http://localhost:8000/keys/delete \
  -H "Content-Type: application/json" \
  -d '{"id":"<key-id>","passphrase":"mysupersecret"}'
```

## Usage logging & budgets

- JC adapters now call `UsageLogger.log` after each LLM request when the key locker supplies the key, so the UI can show estimated spend and usage.
- When you provide a budget, a progress bar shows how much of that budget the key has consumed.
- Usage logs persist under `JC_STORAGE_PATH/usage.log` (JSONL).

## Security best practices

- **Never paste API keys in chat.** Use the UI or CLI to add keys directly on the server.
- Prefer OS keychains (via `keyring`) over the encrypted file fallback.
- Pick a strong `JC_SECRETS_PASSPHRASE` and keep it out of version control.
- Rotate keys by editing an entry and providing the new secret; history is recorded in `keys-audit.log`.
- The UI never receives raw secret values (only masked placeholders).
- `HUGGINGFACE_KEY_FILE` lets you store a locked file locally and keep the key out of the environment.

## Next steps

- Hook usage alerts when a key approaches 80% of its budget (future enhancement).
- Add CLI tooling that wraps the `/keys` API (for scripted automation).
- Extend adapters beyond OpenAI/HuggingFace to log usage when they start using key locker keys.

## Suggested Hugging Face models

Notes on picking a model for the Key Locker / LLM adapter:

- Free / lightweight fallback (good for offline testing and low-cost usage):
  - `google/flan-t5-base` or `google/flan-t5-large` — instruction-capable encoder-decoder models useful for short prompts and development testing.
- Higher-quality (recommended for production if you have an HF plan):
  - `tiiuae/falcon-7b-instruct` — a compact instruction-tuned model with good quality/latency tradeoffs.
  - `tiiuae/falcon-40b-instruct` or other large instruction models — higher quality but more expensive.

How to configure the model used by JC (examples):

```bash
# Set a production HF model (recommended if you have paid quota)
export JC_LLM_PROVIDER=huggingface
export JC_HUGGINGFACE_MODEL=tiiuae/falcon-7b-instruct

# Or set a lightweight fallback for development/testing
export JC_HUGGINGFACE_MODEL=google/flan-t5-base

# Point to a locked file containing your HF token (preferred for local security)
export HUGGINGFACE_KEY_FILE=/path/to/locked/hf_key.txt
```

Remember: you must generate your own Hugging Face API token from https://huggingface.co/settings/tokens and store it securely (the Key Locker UI or `HUGGINGFACE_KEY_FILE` as above). I cannot create or distribute keys for you.
