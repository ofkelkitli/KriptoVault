import os
import struct
import random
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# --- ALGORİTMİK ARKA PLAN (ÖZEL C ALGORİTMASI) ---
TUR1 = 25
TUR2 = 15

def ToplamaRastgeleCift(msg_len, k1, k2): return (((msg_len ^ k1[0]) ^ len(k2)) + 27) & 0xFF
def ToplamaRastgeleTek(msg_len, k1, k2): return (((msg_len ^ k2[0]) ^ len(k1)) + 16) & 0xFF
def CikarmaRastgeleCift(msg_len, k1, k2): return (((len(k1) ^ k2[0]) ^ msg_len) - 25) & 0xFF
def CikarmaRastgeleTek(msg_len, k1, k2): return (((len(k2) ^ msg_len) ^ k1[0]) - 48) & 0xFF

def ToplamaCift(b, k1, k2):
    val = ToplamaRastgeleCift(len(b), k1, k2)
    for i in range(0, len(b), 2): b[i] = (b[i] + val) & 0xFF
def ToplamaTek(b, k1, k2):
    val = ToplamaRastgeleTek(len(b), k1, k2)
    for i in range(1, len(b), 2): b[i] = (b[i] + val) & 0xFF
def CikarmaCift(b, k1, k2):
    val = CikarmaRastgeleCift(len(b), k1, k2)
    for i in range(0, len(b), 2): b[i] = (b[i] - val) & 0xFF
def CikarmaTek(b, k1, k2):
    val = CikarmaRastgeleTek(len(b), k1, k2)
    for i in range(1, len(b), 2): b[i] = (b[i] - val) & 0xFF
def XOR(b, k1, k2):
    msg_len = len(b)
    if not k1 or not k2: return
    for i in range(msg_len): b[i] ^= (k1[i % len(k1)] ^ msg_len) & 0xFF
    for i in range(0, msg_len, 3): b[i] ^= (k2[i % len(k2)] ^ msg_len) & 0xFF
def SagaKaydirma(b):
    for i in range(len(b)): b[i] = ((b[i] >> 1) | (b[i] << 7)) & 0xFF
def SolaKaydirma(b):
    for i in range(len(b)): b[i] = ((b[i] << 1) | (b[i] >> 7)) & 0xFF

def TersToplamaCift(b, k1, k2):
    val = ToplamaRastgeleCift(len(b), k1, k2)
    for i in range(0, len(b), 2): b[i] = (b[i] - val) & 0xFF
def TersToplamaTek(b, k1, k2):
    val = ToplamaRastgeleTek(len(b), k1, k2)
    for i in range(1, len(b), 2): b[i] = (b[i] - val) & 0xFF
def TersCikarmaCift(b, k1, k2):
    val = CikarmaRastgeleCift(len(b), k1, k2)
    for i in range(0, len(b), 2): b[i] = (b[i] + val) & 0xFF
def TersCikarmaTek(b, k1, k2):
    val = CikarmaRastgeleTek(len(b), k1, k2)
    for i in range(1, len(b), 2): b[i] = (b[i] + val) & 0xFF
def TersXOR(b, k1, k2):
    msg_len = len(b)
    if not k1 or not k2: return
    for i in range(0, msg_len, 3): b[i] ^= (k2[i % len(k2)] ^ msg_len) & 0xFF
    for i in range(msg_len): b[i] ^= (k1[i % len(k1)] ^ msg_len) & 0xFF
def TersSagaKaydirma(b):
    for i in range(len(b)): b[i] = ((b[i] << 1) | (b[i] >> 7)) & 0xFF
def TersSolaKaydirma(b):
    for i in range(len(b)): b[i] = ((b[i] >> 1) | (b[i] << 7)) & 0xFF

def encrypt_custom(data_bytes, k1_bytes, k2_bytes):
    b = bytearray(data_bytes)
    for _ in range(TUR1):
        ToplamaCift(b, k1_bytes, k2_bytes); CikarmaTek(b, k1_bytes, k2_bytes); XOR(b, k1_bytes, k2_bytes)
        ToplamaTek(b, k1_bytes, k2_bytes); CikarmaCift(b, k1_bytes, k2_bytes); SagaKaydirma(b)
        SagaKaydirma(b); CikarmaCift(b, k1_bytes, k2_bytes); CikarmaTek(b, k1_bytes, k2_bytes); SolaKaydirma(b)
    for _ in range(TUR2):
        ToplamaCift(b, k1_bytes, k2_bytes); CikarmaTek(b, k1_bytes, k2_bytes); XOR(b, k1_bytes, k2_bytes)
        ToplamaTek(b, k1_bytes, k2_bytes); CikarmaCift(b, k1_bytes, k2_bytes); SagaKaydirma(b)
        SagaKaydirma(b); CikarmaCift(b, k1_bytes, k2_bytes); CikarmaTek(b, k1_bytes, k2_bytes)
        SolaKaydirma(b); XOR(b, k1_bytes, k2_bytes); SagaKaydirma(b)
    for _ in range(TUR1):
        XOR(b, k1_bytes, k2_bytes); ToplamaCift(b, k1_bytes, k2_bytes); CikarmaTek(b, k1_bytes, k2_bytes)
        XOR(b, k1_bytes, k2_bytes); ToplamaTek(b, k1_bytes, k2_bytes); CikarmaCift(b, k1_bytes, k2_bytes)
        SagaKaydirma(b); SagaKaydirma(b); CikarmaCift(b, k1_bytes, k2_bytes)
        CikarmaTek(b, k1_bytes, k2_bytes); SolaKaydirma(b)
    return bytes(b)

def decrypt_custom(data_bytes, k1_bytes, k2_bytes):
    b = bytearray(data_bytes)
    for _ in range(TUR1):
        TersSolaKaydirma(b); TersCikarmaTek(b, k1_bytes, k2_bytes); TersCikarmaCift(b, k1_bytes, k2_bytes)
        TersSagaKaydirma(b); TersSagaKaydirma(b); TersCikarmaCift(b, k1_bytes, k2_bytes)
        TersToplamaTek(b, k1_bytes, k2_bytes); TersXOR(b, k1_bytes, k2_bytes); TersCikarmaTek(b, k1_bytes, k2_bytes)
        TersToplamaCift(b, k1_bytes, k2_bytes); TersXOR(b, k1_bytes, k2_bytes)
    for _ in range(TUR2):
        TersSagaKaydirma(b); TersXOR(b, k1_bytes, k2_bytes); TersSolaKaydirma(b)
        TersCikarmaTek(b, k1_bytes, k2_bytes); TersCikarmaCift(b, k1_bytes, k2_bytes); TersSagaKaydirma(b)
        TersSagaKaydirma(b); TersCikarmaCift(b, k1_bytes, k2_bytes); TersToplamaTek(b, k1_bytes, k2_bytes)
        TersXOR(b, k1_bytes, k2_bytes); TersCikarmaTek(b, k1_bytes, k2_bytes); TersToplamaCift(b, k1_bytes, k2_bytes)
    for _ in range(TUR1):
        TersSolaKaydirma(b); TersCikarmaTek(b, k1_bytes, k2_bytes); TersCikarmaCift(b, k1_bytes, k2_bytes)
        TersSagaKaydirma(b); TersSagaKaydirma(b); TersCikarmaCift(b, k1_bytes, k2_bytes)
        TersToplamaTek(b, k1_bytes, k2_bytes); TersXOR(b, k1_bytes, k2_bytes); TersCikarmaTek(b, k1_bytes, k2_bytes)
        TersToplamaCift(b, k1_bytes, k2_bytes)
    return bytes(b)


# --- UI VE UYGULAMA MİMARİSİ ---
class KriptoVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KriptoVault - Multi-Crypto Password Manager")
        self.root.geometry("800x650") # Tabloya yeni sütun geldiği için pencereyi biraz daha genişlettik
        self.root.configure(bg="#0D0D0F")

        self.bg_dark = "#0D0D0F"
        self.panel_dark = "#16161A"
        self.accent_color = "#00FF66" 
        self.accent_blue = "#00BFFF"
        self.text_color = "#E2E2E6"
        self.font_main = ("Consolas", 10)
        self.font_bold = ("Consolas", 11, "bold")

        self.key1 = b""
        self.key2 = b""
        
        self.main_frame = tk.Frame(self.root, bg=self.bg_dark)
        self.main_frame.pack(fill="both", expand=True)

        self.check_system_status()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- AES YARDIMCI FONKSİYONLARI ---
    def get_aes_key(self):
        # 32 byte AES anahtarı için kullanıcının anahtarlarını SHA-256 ile özetliyoruz
        birlestirilmis = self.key1 + self.key2
        return hashlib.sha256(birlestirilmis).digest()

    def encrypt_aes(self, metin):
        aesgcm = AESGCM(self.get_aes_key())
        nonce = os.urandom(12) # Her şifre için benzersiz IV (Çok Kritik)
        ciphertext = aesgcm.encrypt(nonce, metin.encode('utf-8'), None)
        return nonce + ciphertext # Diske yazılacak ham veri: IV + Şifreli Metin

    def decrypt_aes(self, data_bytes):
        aesgcm = AESGCM(self.get_aes_key())
        nonce = data_bytes[:12]
        ciphertext = data_bytes[12:]
        return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')

    # --- DOSYA SİSTEMİ KONTROL VE KURULUM ---
    def check_system_status(self):
        self.clear_frame()
        if not os.path.exists("password.bin"):
            self.build_setup_ui()
        else:
            self.build_login_ui()

    def build_setup_ui(self):
        tk.Label(self.main_frame, text="SİSTEM KURULUMU", fg=self.accent_color, bg=self.bg_dark, font=("Consolas", 16, "bold")).pack(pady=30)

        self.setup_master = self.create_input("Ana Şifre Oluşturun:", show="*")
        self.setup_k1 = self.create_input("İlk Keyi Giriniz (Key 1):", show="*")
        self.setup_k2 = self.create_input("İkinci Keyi Giriniz (Key 2):", show="*")

        tk.Button(self.main_frame, text="KURULUMU TAMAMLA", bg=self.panel_dark, fg=self.accent_color, font=self.font_bold, bd=1, relief="solid", padx=20, pady=5, command=self.save_setup).pack(pady=20)

    def save_setup(self):
        m_key = self.setup_master.get().encode('utf-8')
        k1 = self.setup_k1.get().encode('utf-8')
        k2 = self.setup_k2.get().encode('utf-8')

        if not m_key or not k1 or not k2:
            messagebox.showerror("Hata", "Tüm alanları doldurmalısın kanka!")
            return

        enc_master = encrypt_custom(m_key, k1, k2)
        enc_k1 = encrypt_custom(k1, enc_master, k2)
        enc_k2 = encrypt_custom(k2, enc_k1, enc_master)

        with open("password.bin", "wb") as f:
            f.write(struct.pack('<i', len(enc_k1)))
            f.write(struct.pack('<i', len(enc_k2)))
            f.write(struct.pack('<i', len(enc_master)))
            
            f.write(enc_k1)
            f.write(enc_k2)
            f.write(enc_master)

        messagebox.showinfo("Başarılı", "Kurulum Tamamlandı! Giriş ekranına yönlendiriliyorsun.")
        self.check_system_status()

    # --- GİRİŞ (LOGIN) EKRANI ---
    def build_login_ui(self):
        tk.Label(self.main_frame, text="SİSTEME GİRİŞ", fg=self.accent_color, bg=self.bg_dark, font=("Consolas", 16, "bold")).pack(pady=50)

        self.login_pass = self.create_input("Ana Şifrenizi Giriniz:", show="*")
        self.login_pass.bind("<Return>", lambda event: self.verify_login())

        tk.Button(self.main_frame, text="GİRİŞ YAP", bg=self.panel_dark, fg=self.accent_color, font=self.font_bold, bd=1, relief="solid", padx=20, pady=5, command=self.verify_login).pack(pady=20)

    def verify_login(self):
        try:
            with open("password.bin", "rb") as f:
                k1_len = struct.unpack('<i', f.read(4))[0]
                k2_len = struct.unpack('<i', f.read(4))[0]
                master_len = struct.unpack('<i', f.read(4))[0]

                enc_k1 = f.read(k1_len)
                enc_k2 = f.read(k2_len)
                enc_master = f.read(master_len)
        except Exception:
            messagebox.showerror("Hata", "password.bin dosyası bozuk veya okunamıyor!")
            return

        girilen_sifre = self.login_pass.get().encode('utf-8')
        
        dec_k2 = decrypt_custom(enc_k2, enc_k1, enc_master)
        dec_k1 = decrypt_custom(enc_k1, enc_master, dec_k2)
        girilen_enc = encrypt_custom(girilen_sifre, dec_k1, dec_k2)

        if len(girilen_enc) == master_len and girilen_enc == enc_master:
            self.key1 = dec_k1
            self.key2 = dec_k2
            self.build_vault_ui()
        else:
            messagebox.showerror("Hata", "Giriş Başarısız! Yanlış Şifre.")
            self.login_pass.delete(0, tk.END)

    # --- ANA KASA (VAULT) EKRANI ---
    def build_vault_ui(self):
        self.clear_frame()

        top_bar = tk.Frame(self.main_frame, bg=self.panel_dark, pady=10)
        top_bar.pack(fill="x")
        tk.Label(top_bar, text="Kayıtlı Şifreler (Vault)", fg=self.accent_color, bg=self.panel_dark, font=("Consolas", 14, "bold")).pack(side="left", padx=10)
        tk.Button(top_bar, text="Güçlü Şifre Üret", bg=self.bg_dark, fg=self.accent_blue, font=self.font_main, bd=1, relief="solid", command=self.generate_password).pack(side="right", padx=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=self.panel_dark, foreground=self.text_color, fieldbackground=self.panel_dark, borderwidth=0, font=self.font_main)
        style.configure("Treeview.Heading", background=self.bg_dark, foreground=self.accent_color, font=self.font_bold)
        style.map("Treeview", background=[('selected', '#2A2A35')])

        tree_frame = tk.Frame(self.main_frame, bg=self.bg_dark)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabloya yeni "algo" sütunu eklendi
        columns = ("platform", "user", "pass", "algo")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        self.tree.heading("platform", text="Platform")
        self.tree.heading("user", text="Kullanıcı Adı")
        self.tree.heading("pass", text="Şifre")
        self.tree.heading("algo", text="Algoritma")
        
        self.tree.column("platform", width=150)
        self.tree.column("user", width=200)
        self.tree.column("pass", width=200)
        self.tree.column("algo", width=150, anchor="center") # Algoritma sütunu ortalı
        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_vault()

        action_frame = tk.Frame(self.main_frame, bg=self.bg_dark, pady=10)
        action_frame.pack(fill="x", padx=10)

        center_wrapper = tk.Frame(action_frame, bg=self.bg_dark)
        center_wrapper.pack(anchor="center")

        tk.Label(center_wrapper, text="Platform:", bg=self.bg_dark, fg=self.text_color).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_plat = tk.Entry(center_wrapper, bg=self.panel_dark, fg=self.text_color, insertbackground=self.accent_color)
        self.entry_plat.grid(row=1, column=0, padx=5, pady=2)

        tk.Label(center_wrapper, text="Kullanıcı:", bg=self.bg_dark, fg=self.text_color).grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.entry_user = tk.Entry(center_wrapper, bg=self.panel_dark, fg=self.text_color, insertbackground=self.accent_color)
        self.entry_user.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(center_wrapper, text="Şifre:", bg=self.bg_dark, fg=self.text_color).grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.entry_pass = tk.Entry(center_wrapper, bg=self.panel_dark, fg=self.text_color, insertbackground=self.accent_color)
        self.entry_pass.grid(row=1, column=2, padx=5, pady=2)

        # Şifreleme Algoritması Seçimi (Eklemeden önce)
        algo_frame = tk.Frame(center_wrapper, bg=self.bg_dark)
        algo_frame.grid(row=2, column=0, columnspan=3, pady=(15, 5))
        
        self.vault_algo_var = tk.IntVar(value=2) # Varsayılan AES
        tk.Radiobutton(algo_frame, text="Özel Algoritma", variable=self.vault_algo_var, value=1, bg=self.bg_dark, fg=self.text_color, selectcolor=self.panel_dark, font=self.font_main, activebackground=self.bg_dark).pack(side="left", padx=10)
        tk.Radiobutton(algo_frame, text="AES-256-GCM", variable=self.vault_algo_var, value=2, bg=self.bg_dark, fg=self.accent_blue, selectcolor=self.panel_dark, font=self.font_main, activebackground=self.bg_dark).pack(side="left", padx=10)

        # Butonlar bir alt satıra (row 3) kaydırıldı
        btn_frame = tk.Frame(center_wrapper, bg=self.bg_dark)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))

        tk.Button(btn_frame, text="Ekle", bg=self.panel_dark, fg=self.accent_color, bd=1, relief="solid", width=15, command=self.add_password).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Sil", bg=self.panel_dark, fg="#FF4444", bd=1, relief="solid", width=15, command=self.delete_password).pack(side="left", padx=10)

    def create_input(self, label_text, show=None):
        tk.Label(self.main_frame, text=label_text, fg=self.text_color, bg=self.bg_dark, font=self.font_main).pack(pady=(10, 2))
        entry = tk.Entry(self.main_frame, bg=self.panel_dark, fg=self.text_color, insertbackground=self.accent_color, bd=1, relief="solid", font=self.font_main, show=show, width=30)
        entry.pack(ipady=5)
        return entry

    # --- VAULT İŞLEMLERİ (Çoklu Algoritma Okuma/Yazma) ---
    def load_vault(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not os.path.exists("vault.bin"): return

        with open("vault.bin", "rb") as f:
            while True:
                # 1. Adım: Verinin hangi algoritmayla şifrelendiğini oku (4 byte)
                algo_bytes = f.read(4)
                if not algo_bytes: break
                algo_type = struct.unpack('<i', algo_bytes)[0]
                
                algo_name = "AES-256-GCM" if algo_type == 2 else "Özel Algoritma"

                try:
                    s_len = struct.unpack('<i', f.read(4))[0]
                    s_data = f.read(s_len)
                    site = self.decrypt_aes(s_data) if algo_type == 2 else decrypt_custom(s_data, self.key1, self.key2).decode('utf-8', errors='ignore')

                    u_len = struct.unpack('<i', f.read(4))[0]
                    u_data = f.read(u_len)
                    user = self.decrypt_aes(u_data) if algo_type == 2 else decrypt_custom(u_data, self.key1, self.key2).decode('utf-8', errors='ignore')

                    p_len = struct.unpack('<i', f.read(4))[0]
                    p_data = f.read(p_len)
                    password = self.decrypt_aes(p_data) if algo_type == 2 else decrypt_custom(p_data, self.key1, self.key2).decode('utf-8', errors='ignore')

                    self.tree.insert("", "end", values=(site, user, password, algo_name))
                except Exception as e:
                    # MAC doğrulaması başarısız olursa veya dosya bozuksa o veriyi atla
                    continue

    def save_all_to_vault(self):
        with open("vault.bin", "wb") as f:
            for item in self.tree.get_children():
                vals = self.tree.item(item, 'values') # [platform, user, pass, algo_name]
                
                algo_type = 2 if vals[3] == "AES-256-GCM" else 1
                
                # Önce diske 4 byte'lık Algoritma ID'sini yaz
                f.write(struct.pack('<i', algo_type))
                
                # Seçilen algoritmaya göre veriyi şifrele
                if algo_type == 2:
                    site_enc = self.encrypt_aes(vals[0])
                    user_enc = self.encrypt_aes(vals[1])
                    pass_enc = self.encrypt_aes(vals[2])
                else:
                    site_enc = encrypt_custom(vals[0].encode('utf-8'), self.key1, self.key2)
                    user_enc = encrypt_custom(vals[1].encode('utf-8'), self.key1, self.key2)
                    pass_enc = encrypt_custom(vals[2].encode('utf-8'), self.key1, self.key2)

                # Şifreli verilerin uzunluğunu ve kendisini yaz
                f.write(struct.pack('<i', len(site_enc)))
                f.write(site_enc)
                f.write(struct.pack('<i', len(user_enc)))
                f.write(user_enc)
                f.write(struct.pack('<i', len(pass_enc)))
                f.write(pass_enc)

    def add_password(self):
        plat = self.entry_plat.get()
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        algo_name = "AES-256-GCM" if self.vault_algo_var.get() == 2 else "Özel Algoritma"

        if not plat or not user or not pwd: return

        self.tree.insert("", "end", values=(plat, user, pwd, algo_name))
        self.save_all_to_vault()
        
        self.entry_plat.delete(0, tk.END)
        self.entry_user.delete(0, tk.END)
        self.entry_pass.delete(0, tk.END)

    def delete_password(self):
        selected = self.tree.selection()
        if not selected: return
        
        for item in selected:
            self.tree.delete(item)
        self.save_all_to_vault()

    def generate_password(self):
        havuz = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
        olusturulan = "".join(random.choice(havuz) for _ in range(16)) 
        
        self.entry_pass.delete(0, tk.END)
        self.entry_pass.insert(0, olusturulan)
        messagebox.showinfo("Şifre Üretildi", f"Güçlü Şifren: {olusturulan}\n\nŞifre kutusuna otomatik eklendi.")

if __name__ == "__main__":
    root = tk.Tk()
    app = KriptoVaultApp(root)
    root.mainloop()