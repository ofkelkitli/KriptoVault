# 🔑 KriptoVault — Encrypted Password Manager in C & Python

> A terminal-based and GUI-based encrypted password manager, featuring a custom multi-layer cipher to securely store and manage credentials locally.

---

## 📋 About the Project

KriptoVault is a local password manager for Windows. It comes in two flavors: a **C terminal application** and a **Python GUI application** — both sharing the same custom multi-layer symmetric cipher at their core.

All credentials (platform, username, password) are encrypted before being written to disk, and decrypted only when accessed after a successful login. The master password itself is also stored encrypted — never in plaintext. The application supports full CRUD operations on saved credentials and includes a strong password generator.

---

## 🗂️ File Structure

```
.
├── main.c          # Main flow: setup, login, menu, and all vault operations
├── encrypter.h     # Encrypt function declaration and round constants
├── encrypter.c     # Encryption logic (multi-round)
├── decrypter.h     # Decrypt function declaration and round constants
├── decrypter.c     # Decryption logic (reverse of encryption)
├── functions.h     # Helper function declarations and ANSI color macros
├── functions.c     # Core cipher operations (XOR, shift, add, subtract)
├── gui.py          # Python GUI application (tkinter) — standalone, same cipher
├── password.bin    # Generated on first run — stores encrypted keys & master password
└── vault.bin       # Generated on first use — stores all encrypted credentials
```

---

## 🔐 Security Model

KriptoVault uses a **three-key encryption system**. On first run, the user sets:

- A **Master Password** — used to authenticate on every login
- **Key 1** and **Key 2** — used together as the encryption keys for all vault data

These three values are cross-encrypted with each other before being saved to `password.bin`:

```
masterKey  → encrypted with (key1, key2)
key1       → encrypted with (masterKey, key2)
key2       → encrypted with (key1, masterKey)
```

On login, the stored keys are partially decrypted and the entered password is re-encrypted to compare — the master password is **never decrypted and stored in plaintext** at any point.

All vault entries (platform name, username, password) are encrypted using the same custom cipher before being written to `vault.bin`.

> ⚠️ If `password.bin` is deleted, all stored credentials become permanently inaccessible.

---

## 🔒 Encryption Algorithm

KriptoVault reuses the same **custom symmetric multi-layer cipher** used in KriptoChat. It operates in 3 phases across a total of 65 rounds.

### Operations Used

| Function | Description |
|----------|-------------|
| `ToplamaCift` / `TersToplamaCift` | Add a derived value to even-indexed bytes |
| `ToplamaTek` / `TersToplamaTek` | Add a derived value to odd-indexed bytes |
| `CikarmaCift` / `TersCikarmaCift` | Subtract a derived value from even-indexed bytes |
| `CikarmaTek` / `TersCikarmaTek` | Subtract a derived value from odd-indexed bytes |
| `XOR` / `TersXOR` | XOR bytes using both keys and message length |
| `SagaKaydirma` / `TersSagaKaydirma` | Bitwise right circular shift per byte |
| `SolaKaydirma` / `TersSolaKaydirma` | Bitwise left circular shift per byte |

### Round Structure

```
Phase 1 — TUR1 (25) rounds:
  AddEven → SubOdd → XOR → AddOdd → SubEven → ShiftRight×2 → SubEven → SubOdd → ShiftLeft

Phase 2 — TUR2 (15) rounds:
  Same as Phase 1 + XOR → ShiftRight

Phase 3 — TUR1 (25) rounds:
  XOR → AddEven → SubOdd → XOR → AddOdd → SubEven → ShiftRight×2 → SubEven → SubOdd → ShiftLeft
```

Decryption applies all operations **in exact reverse order** across the 3 phases.

---

## 🖥️ GUI Application (gui.py)

`gui.py` is a standalone Python reimplementation of KriptoVault with a graphical interface built using **tkinter**. It shares the exact same custom cipher logic as the C version, ported line-by-line to Python.

### Key Differences from the Terminal Version

- **Graphical UI** — dark-themed window (800×650) with a Consolas font, green/blue accent colors, and a credential table built with `ttk.Treeview`
- **Dual encryption mode** — each credential can be individually encrypted with either the **custom algorithm** or **AES-256-GCM** (via the `cryptography` library). The algorithm used is saved alongside the entry in `vault.bin` and automatically applied on decryption
- **No restart required after setup** — after completing first-run setup, the app transitions directly to the login screen without needing a restart
- **Enter key support** — pressing Enter on the login screen submits the password
- **Inline password generator** — generates a 16-character strong password and pastes it directly into the password field

### Requirements

```bash
pip install cryptography
```

> `tkinter` is included with standard Python on Windows. No other dependencies needed.

### Run

```bash
python gui.py
```

### GUI Preview

```
┌──────────────────────────────────────────────┐
│  SİSTEM KURULUMU                             │  ← First run
│                                              │
│  Ana Şifre Oluşturun:  [***]                 │
│  İlk Keyi Giriniz:     [***]                 │
│  İkinci Keyi Giriniz:  [***]                 │
│                                              │
│           [ KURULUMU TAMAMLA ]               │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  SİSTEME GİRİŞ                              │  ← Login
│                                              │
│  Ana Şifrenizi Giriniz: [***]                │
│           [ GİRİŞ YAP ]                      │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Kayıtlı Şifreler (Vault)        [ Güçlü Şifre Üret ]           │
│                                                                  │
│  Platform     │ Kullanıcı Adı  │ Şifre         │ Algoritma      │
│  ─────────────┼────────────────┼───────────────┼──────────────  │
│  github       │ faruk          │ G7#kP!...     │ AES-256-GCM    │
│  discord      │ faruk          │ xT2$mR...     │ Özel Algoritma │
│                                                                  │
│  Platform: [      ]  Kullanıcı: [      ]  Şifre: [      ]       │
│  ● Özel Algoritma   ○ AES-256-GCM                               │
│            [ Ekle ]        [ Sil ]                               │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started (C Terminal Version)

### Requirements

- Windows OS
- GCC (MinGW recommended)

### Compilation

```bash
gcc main.c functions.c encrypter.c decrypter.c -o kriptovault
```

### Run

```bash
./kriptovault
```

---

## 🎮 How to Use

### First Run — Setup

On the first launch, `password.bin` does not exist, so the system enters **setup mode**:

1. Create a **Master Password**
2. Enter **Key 1** and **Key 2**
3. The program encrypts and saves them, then exits — **restart required** *(terminal version only)*

### Subsequent Runs — Login & Menu

1. Enter your **Master Password** to log in
2. On success, the main menu appears with the following options:

| Option | Action |
|--------|--------|
| `1` | List all saved credentials |
| `2` | Add a new credential |
| `3` | Update an existing credential |
| `4` | Delete a credential |
| `5` | Generate a strong random password |
| `9` | Exit |

- To exit a sub-menu at any prompt, enter `9`
- After login, keys are **cleared from memory** on exit (`memset`)

---

## ⚙️ Features

- ✅ Encrypted local credential storage (`vault.bin`)
- ✅ Encrypted master password storage (`password.bin`) — never stored in plaintext
- ✅ Three-key cross-encryption for the authentication system
- ✅ Add, list, update, and delete credentials (full CRUD)
- ✅ Strong random password generator (up to 99 characters in terminal / 16 characters in GUI)
- ✅ Keys wiped from memory on exit
- ✅ Custom multi-layer symmetric cipher (65 total rounds)
- ✅ Colorful terminal UI using ANSI color codes *(C version)*
- ✅ Dark-themed graphical UI with tkinter *(Python version)*
- ✅ Per-entry algorithm selection: custom cipher or AES-256-GCM *(Python version)*

---

## 📸 Terminal Preview

```
-----SISTEM KURULUMU-----          (First run — setup)

Ana Sifre Olusturun: ****
Ilk Keyi Giriniz: ****
Ikinci Keyi Giriniz: ****

Kurulum Tamamlandi! Lutfen Programi Yeniden Baslatiniz!

---

Sifrenizi Giriniz: ****            (Subsequent runs — login)
>>Giris Basarili!

---ANA MENU---
1 * Sifreleri Listeleme
2 * Sifre Ekleme
3 * Sifre Guncelleme
4 * Sifre Silme
5 * Guclu Sifre Onerici
9 * Cikis
```

---

## 📌 Notes

- `password.bin` and `vault.bin` are created automatically in the same directory as the executable / script.
- Losing `password.bin` makes all stored vault data permanently unrecoverable.
- The strong password generator draws from lowercase, uppercase, digits, and special characters.
- The encryption algorithm is a **custom academic cipher** and is not intended for production-grade security.
- The `vault.bin` format is **shared** between the C and Python versions — both can read entries written by the other, as long as the same keys are used and the entry was encrypted with the custom algorithm. AES-256-GCM entries are Python-only.

---

## 👤 Developer

**Ömer Faruk Kelkitli**  
Mechatronics Engineering — 1st Year Student
