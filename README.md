\# 🔑 KriptoVault — Encrypted Password Manager in C



> A terminal-based encrypted password manager written in C, featuring a custom multi-layer cipher to securely store and manage credentials locally.



\---



\## 📋 About the Project



KriptoVault is a local password manager for Windows, built in C. All credentials (platform, username, password) are encrypted with a custom multi-layer symmetric cipher before being written to disk, and decrypted only when accessed after a successful login. The master password itself is also stored encrypted — never in plaintext. The application supports full CRUD operations on saved credentials and includes a strong password generator.



\---



\## 🗂️ File Structure



```

.

├── main.c          # Main flow: setup, login, menu, and all vault operations

├── encrypter.h     # Encrypt function declaration and round constants

├── encrypter.c     # Encryption logic (multi-round)

├── decrypter.h     # Decrypt function declaration and round constants

├── decrypter.c     # Decryption logic (reverse of encryption)

├── functions.h     # Helper function declarations and ANSI color macros

├── functions.c     # Core cipher operations (XOR, shift, add, subtract)

├── password.bin    # Generated on first run — stores encrypted keys \& master password

└── vault.bin       # Generated on first use — stores all encrypted credentials

```



\---



\## 🔐 Security Model



KriptoVault uses a \*\*three-key encryption system\*\*. On first run, the user sets:



\- A \*\*Master Password\*\* — used to authenticate on every login

\- \*\*Key 1\*\* and \*\*Key 2\*\* — used together as the encryption keys for all vault data



These three values are cross-encrypted with each other before being saved to `password.bin`:



```

masterKey  → encrypted with (key1, key2)

key1       → encrypted with (masterKey, key2)

key2       → encrypted with (key1, masterKey)

```



On login, the stored keys are partially decrypted and the entered password is re-encrypted to compare — the master password is \*\*never decrypted and stored in plaintext\*\* at any point.



All vault entries (platform name, username, password) are encrypted using the same custom cipher before being written to `vault.bin`.



> ⚠️ If `password.bin` is deleted, all stored credentials become permanently inaccessible.



\---



\## 🔒 Encryption Algorithm



KriptoVault reuses the same \*\*custom symmetric multi-layer cipher\*\* used in KriptoChat. It operates in 3 phases across a total of 65 rounds.



\### Operations Used



| Function | Description |

|----------|-------------|

| `ToplamaCift` / `TersToplamaCift` | Add a derived value to even-indexed bytes |

| `ToplamaTek` / `TersToplamaTek` | Add a derived value to odd-indexed bytes |

| `CikarmaCift` / `TersCikarmaCift` | Subtract a derived value from even-indexed bytes |

| `CikarmaTek` / `TersCikarmaTek` | Subtract a derived value from odd-indexed bytes |

| `XOR` / `TersXOR` | XOR bytes using both keys and message length |

| `SagaKaydirma` / `TersSagaKaydirma` | Bitwise right circular shift per byte |

| `SolaKaydirma` / `TersSolaKaydirma` | Bitwise left circular shift per byte |



\### Round Structure



```

Phase 1 — TUR1 (25) rounds:

&#x20; AddEven → SubOdd → XOR → AddOdd → SubEven → ShiftRight×2 → SubEven → SubOdd → ShiftLeft



Phase 2 — TUR2 (15) rounds:

&#x20; Same as Phase 1 + XOR → ShiftRight



Phase 3 — TUR1 (25) rounds:

&#x20; XOR → AddEven → SubOdd → XOR → AddOdd → SubEven → ShiftRight×2 → SubEven → SubOdd → ShiftLeft

```



Decryption applies all operations \*\*in exact reverse order\*\* across the 3 phases.



\---



\## 🚀 Getting Started



\### Requirements



\- Windows OS

\- GCC (MinGW recommended)



\### Compilation



```bash

gcc main.c functions.c encrypter.c decrypter.c -o kriptovault

```



\### Run



```bash

./kriptovault

```



\---



\## 🎮 How to Use



\### First Run — Setup



On the first launch, `password.bin` does not exist, so the system enters \*\*setup mode\*\*:



1\. Create a \*\*Master Password\*\*

2\. Enter \*\*Key 1\*\* and \*\*Key 2\*\*

3\. The program encrypts and saves them, then exits — \*\*restart required\*\*



\### Subsequent Runs — Login \& Menu



1\. Enter your \*\*Master Password\*\* to log in

2\. On success, the main menu appears with the following options:



| Option | Action |

|--------|--------|

| `1` | List all saved credentials |

| `2` | Add a new credential |

| `3` | Update an existing credential |

| `4` | Delete a credential |

| `5` | Generate a strong random password |

| `9` | Exit |



\- To exit a sub-menu at any prompt, enter `9`

\- After login, keys are \*\*cleared from memory\*\* on exit (`memset`)



\---



\## ⚙️ Features



\- ✅ Encrypted local credential storage (`vault.bin`)

\- ✅ Encrypted master password storage (`password.bin`) — never stored in plaintext

\- ✅ Three-key cross-encryption for the authentication system

\- ✅ Add, list, update, and delete credentials (full CRUD)

\- ✅ Strong random password generator (up to 99 characters, full character set)

\- ✅ Keys wiped from memory on exit

\- ✅ Custom multi-layer symmetric cipher (65 total rounds)

\- ✅ Colorful terminal UI using ANSI color codes



\---



\## 📸 Terminal Preview



```

\-----SISTEM KURULUMU-----          (First run — setup)



Ana Sifre Olusturun: \*\*\*\*

Ilk Keyi Giriniz: \*\*\*\*

Ikinci Keyi Giriniz: \*\*\*\*



Kurulum Tamamlandi! Lutfen Programi Yeniden Baslatiniz!



\---



Sifrenizi Giriniz: \*\*\*\*            (Subsequent runs — login)

>>Giris Basarili!



\---ANA MENU---

1 \* Sifreleri Listeleme

2 \* Sifre Ekleme

3 \* Sifre Guncelleme

4 \* Sifre Silme

5 \* Guclu Sifre Onerici

9 \* Cikis

```



\---



\## 📌 Notes



\- `password.bin` and `vault.bin` are created automatically in the same directory as the executable.

\- Losing `password.bin` makes all stored vault data permanently unrecoverable.

\- The strong password generator draws from lowercase, uppercase, digits, and special characters.

\- The encryption algorithm is a \*\*custom academic cipher\*\* and is not intended for production-grade security.



\---



\## 👤 Developer



\*\*Ömer Faruk Kelkitli\*\*  

Mechatronics Engineering — 1st Year Student

