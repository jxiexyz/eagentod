# Airdrop Identity Handling & Execution Pitfalls

## 1. Identity Data Handling (`airdrop_identity.py`)
- Data Utama: Gunakan `/home/ubuntu/airdrop_identity.py`. 
- Valid Keys: `evm_wallet`, `sol_wallet`, `x_handle`, `password_normal`, `password_long`, `password_symbol`.
- **CRITICAL PITFALL (Not JSON):** File `airdrop_identity.py` adalah skrip Python, **BUKAN JSON**. JANGAN parse menggunakan `json.load()` atau mengekstrak substring lalu `json.loads()`. Ini **AKAN GAGAL** dengan `JSONDecodeError` karena dictionary Python menggunakan single quotes (`'`) dan trailing commas.
- Untuk membaca secara programatis dalam skrip Playwright inline (di mana import path susah), gunakan Regex:
  ```python
  import re
  with open('/home/ubuntu/airdrop_identity.py', 'r') as f: content = f.read()
  x_user = re.search(r"'x_handle':\s*'([^']+)'", content).group(1).lstrip('@')
  ```
- Jika menggunakan skrip eksternal biasa, gunakan Python `import`:
  ```python
  import sys
  sys.path.append('/home/ubuntu')
  import airdrop_identity
  print(airdrop_identity.IDENTITY['main']['evm_wallet'])
  ```
- **Fake Data Forbid:** JANGAN mengarang data/fake UID (seperti UID BingX) jika tidak ada di identitas. Mengarang UID CEX menyebabkan diskualifikasi massal. Jika kosong, laporkan `❌ Failed (missing credential)` atau gunakan `'N/A'` jika form mengizinkan teks.

## 2. State & JSON Handling Pitfalls (`worker_done.json`)
- **JSON File Size Warning:** File state JSON berukuran sangat besar. **DILARANG KERAS** menggunakan `read_file` dilanjut `write_file` secara penuh karena berisiko terpotong (truncated) dan merusak JSON.
- **DILARANG Bikin Script On-The-Fly:** Jangan gunakan terminal heredoc (`cat << 'EOF' > add.py`) untuk memodifikasi state JSON. Selalu gunakan helper bawaan: `update_done.py "domain (Msg ID)"` dan `update_failed.py "domain (Msg ID)"`.
- **Corrupt Helper Script Check:** Selalu verifikasi singkat helper script via `cat update_done.py`. Jika kamu melihat function call hardcoded di paling bawah (misal `update_done("domain.xyz")`), itu adalah ulah agen sebelumnya yang ceroboh. Overwrite script menjadi parametrik (`sys.argv[1]`) sebelum digunakan.

## 3. Telethon / Bot HTTP Reporting (`post_topic42.py`)
- Laporan worker dikirim ke Topic 42 menggunakan Bot HTTP API (`MomosmartW_bot`).
- Jika pengiriman error dengan `HTTP 401 Unauthorized`, artinya Token Bot MATI. **LANGSUNG STOP EKSEKUSI!** Jangan lanjutkan proses antrean.
- JANGAN menyembunyikan API error dari web dApp sebagai error bot Telegram. Jika form dApp gagal disubmit, laporkan gagal karena dApp error.