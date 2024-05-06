import tkinter as tk
from tkinter import messagebox
import sqlite3

class Kitap:
    def _init_(self, kitap_id, ad, yazar, durum="Rafta"):
        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.durum = durum

    def durum_guncelle(self, durum):
        self.durum = durum

class Uye:
    def _init_(self, uye_id, ad, soyad):
        self.uye_id = uye_id
        self.ad = ad
        self.soyad = soyad

class Odunc:
    def _init_(self, kitap, uye):
        self.kitap = kitap
        self.uye = uye

def odunc_al():
    kitap_id = int(kitap_id_entry.get())
    uye_id = int(uye_id_entry.get())

    conn = sqlite3.connect('kutuphane.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM Kitaplar WHERE kitap_id=?", (kitap_id,))
    kitap = cur.fetchone()

    cur.execute("SELECT * FROM Uyeler WHERE uye_id=?", (uye_id,))
    uye = cur.fetchone()

    if kitap and uye:
        cur.execute("INSERT INTO Odunc (kitap_id, uye_id) VALUES (?, ?)", (kitap_id, uye_id))
        cur.execute("UPDATE Kitaplar SET durum='Ödünçte' WHERE kitap_id=?", (kitap_id,))
        conn.commit()
        messagebox.showinfo("Başarılı", "Kitap ödünç alındı.")
    else:
        messagebox.showerror("Hata", "Kitap veya üye bulunamadı.")

    conn.close()

def iade_et():
    kitap_id = int(iade_kitap_id_entry.get())

    conn = sqlite3.connect('kutuphane.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM Odunc WHERE kitap_id=?", (kitap_id,))
    odunc = cur.fetchone()

    if odunc:
        cur.execute("DELETE FROM Odunc WHERE kitap_id=?", (kitap_id,))
        cur.execute("UPDATE Kitaplar SET durum='Rafta' WHERE kitap_id=?", (kitap_id,))
        conn.commit()
        messagebox.showinfo("Başarılı", "Kitap iade edildi.")
    else:
        messagebox.showerror("Hata", "Ödünç alınmış kitap bulunamadı.")

    conn.close()

def kitaplari_goster():
    conn = sqlite3.connect('kutuphane.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Kitaplar")
    rows = cur.fetchall()
    conn.close()

    kitap_listbox.delete(0, tk.END)
    for row in rows:
        kitap_listbox.insert(tk.END, row)

def uyeleri_goster():
    conn = sqlite3.connect('kutuphane.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Uyeler")
    rows = cur.fetchall()
    conn.close()

    uye_listbox.delete(0, tk.END)
    for row in rows:
        uye_listbox.insert(tk.END, row)

def uye_ol():
    root_uye_ol = tk.Tk()
    root_uye_ol.title("Üye Ol")

    frame_uye_ol = tk.Frame(root_uye_ol)
    frame_uye_ol.pack(pady=20)

    tk.Label(frame_uye_ol, text="Ad:").grid(row=0, column=0)
    ad_uye_ol_entry = tk.Entry(frame_uye_ol)
    ad_uye_ol_entry.grid(row=0, column=1)

    tk.Label(frame_uye_ol, text="Soyad:").grid(row=1, column=0)
    soyad_uye_ol_entry = tk.Entry(frame_uye_ol)
    soyad_uye_ol_entry.grid(row=1, column=1)

    def kayit_ol():
        conn = sqlite3.connect('kutuphane.db')
        cur = conn.cursor()

        cur.execute("INSERT INTO Uyeler (ad, soyad) VALUES (?, ?)", (ad_uye_ol_entry.get(), soyad_uye_ol_entry.get()))
        conn.commit()
        conn.close()

        messagebox.showinfo("Başarılı", "Üye olma işlemi başarıyla tamamlandı.")
        root_uye_ol.destroy()

    uye_ol_button = tk.Button(frame_uye_ol, text="Üye Ol", command=kayit_ol)
    uye_ol_button.grid(row=2, columnspan=2, pady=10)

    root_uye_ol.mainloop()

def uye_iptal():
    root_uye_iptal = tk.Tk()
    root_uye_iptal.title("Üyelik İptal")

    frame_uye_iptal = tk.Frame(root_uye_iptal)
    frame_uye_iptal.pack(pady=20)

    tk.Label(frame_uye_iptal, text="Üye ID:").grid(row=0, column=0)
    uye_id_iptal_entry = tk.Entry(frame_uye_iptal)
    uye_id_iptal_entry.grid(row=0, column=1)

    def iptal_et():
        conn = sqlite3.connect('kutuphane.db')
        cur = conn.cursor()

        cur.execute("DELETE FROM Uyeler WHERE uye_id=?", (uye_id_iptal_entry.get(),))
        conn.commit()
        conn.close()

        messagebox.showinfo("Başarılı", "Üyelik iptali başarıyla tamamlandı.")
        root_uye_iptal.destroy()

    uye_iptal_button = tk.Button(frame_uye_iptal, text="Üyelik İptal Et", command=iptal_et)
    uye_iptal_button.grid(row=1, columnspan=2, pady=10)

    root_uye_iptal.mainloop()

# Veritabanı bağlantısı ve tablo oluşturma
conn = sqlite3.connect('kutuphane.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Kitaplar (
               kitap_id INTEGER PRIMARY KEY,
               ad TEXT NOT NULL,
               yazar TEXT NOT NULL,
               durum TEXT NOT NULL)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Uyeler (
               uye_id INTEGER PRIMARY KEY,
               ad TEXT NOT NULL,
               soyad TEXT NOT NULL)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Odunc (
               kitap_id INTEGER,
               uye_id INTEGER,
               FOREIGN KEY (kitap_id) REFERENCES Kitaplar(kitap_id),
               FOREIGN KEY (uye_id) REFERENCES Uyeler(uye_id))''')

# 10 tane kitap ekleme
kitaplar = [
    ("Suç ve Ceza", "Fyodor Dostoyevski"),
    ("Yüzüklerin Efendisi", "J.R.R. Tolkien"),
    ("1984", "George Orwell"),
    ("Savaş ve Barış", "Lev Tolstoy"),
    ("Anna Karenina", "Lev Tolstoy"),
    ("Simyacı", "Paulo Coelho"),
    ("Don Kişot", "Miguel de Cervantes"),
    ("Ulysses", "James Joyce"),
    ("Bülbülü Öldürmek", "Harper Lee"),
    ("Kürk Mantolu Madonna", "Sabahattin Ali")
]

for i, (kitap, yazar) in enumerate(kitaplar, start=1):
    cur.execute("INSERT OR IGNORE INTO Kitaplar (ad, yazar, durum) VALUES (?, ?, ?)", (kitap, yazar, "Rafta"))

conn.commit()
conn.close()

def show_usage_guide():
    usage_window = tk.Toplevel(root)
    usage_window.title("Kullanım Kılavuzu")

    usage_text = tk.Text(usage_window, wrap="word", bg="#F0F0F0", padx=10, pady=10)
    usage_text.insert("1.0", kilavuz_metni)
    usage_text.config(state="disabled")
    usage_text.pack(fill="both", expand=True)

root = tk.Tk()
root.title("Kütüphane Sistemi")
root.configure(bg="#D2B48C")

# İlk bölüm
left_frame = tk.Frame(root, bg="#D2B48C")
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Kitap ödünç alma bölümü
kitap_al_frame = tk.Frame(left_frame, bg="#D2B48C")
kitap_al_frame.pack(pady=10)

tk.Label(kitap_al_frame, text="Kitap ID:", bg="#D2B48C").grid(row=0, column=0)
kitap_id_entry = tk.Entry(kitap_al_frame)
kitap_id_entry.grid(row=0, column=1)

tk.Label(kitap_al_frame, text="Üye ID:", bg="#D2B48C").grid(row=1, column=0)
uye_id_entry = tk.Entry(kitap_al_frame)
uye_id_entry.grid(row=1, column=1)

odunc_al_button = tk.Button(kitap_al_frame, text="Kitap Ödünç Al", command=odunc_al)
odunc_al_button.grid(row=2, columnspan=2)

# Kitaplar bölümü
kitaplar_frame = tk.Frame(left_frame, bg="#D2B48C")
kitaplar_frame.pack(pady=10)

tk.Label(kitaplar_frame, text="Kitaplar", bg="#D2B48C").grid(row=0, column=0)
kitap_listbox = tk.Listbox(kitaplar_frame, width=50)
kitap_listbox.grid(row=1, column=0)

kitaplar_goster_button = tk.Button(kitaplar_frame, text="Kitapları Göster", command=kitaplari_goster)
kitaplar_goster_button.grid(row=2, column=0)

# Üyeler bölümü
uyeler_frame = tk.Frame(left_frame, bg="#D2B48C")
uyeler_frame.pack(pady=10)

tk.Label(uyeler_frame, text="Üyeler", bg="#D2B48C").grid(row=0, column=0)
uye_listbox = tk.Listbox(uyeler_frame, width=50)
uye_listbox.grid(row=1, column=0)

uyeleri_goster_button = tk.Button(uyeler_frame, text="Üyeleri Göster", command=uyeleri_goster)
uyeleri_goster_button.grid(row=2, column=0)

# İkinci bölüm
right_frame = tk.Frame(root, bg="#D2B48C")
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Kitap iade etme bölümü
kitap_iade_frame = tk.Frame(right_frame, bg="#D2B48C")
kitap_iade_frame.pack(pady=10)

tk.Label(kitap_iade_frame, text="Kitap ID:", bg="#D2B48C").grid(row=0, column=0)
iade_kitap_id_entry = tk.Entry(kitap_iade_frame)
iade_kitap_id_entry.grid(row=0, column=1)

iade_et_button = tk.Button(kitap_iade_frame, text="Kitap İade Et", command=iade_et)
iade_et_button.grid(row=1, columnspan=2)

# Üye olma bölümü
uye_ol_frame = tk.Frame(right_frame, bg="#D2B48C")
uye_ol_frame.pack(pady=10)

tk.Label(uye_ol_frame, text="Üye Ol", bg="#D2B48C").grid(row=0, column=0)
uye_ol_button = tk.Button(uye_ol_frame, text="Üye Ol", command=uye_ol)
uye_ol_button.grid(row=0, column=1)

# Üyelik iptal etme bölümü
uye_iptal_frame = tk.Frame(right_frame, bg="#D2B48C")
uye_iptal_frame.pack(pady=10)

tk.Label(uye_iptal_frame, text="Üyelik İptal", bg="#D2B48C").grid(row=0, column=0)
uye_iptal_button = tk.Button(uye_iptal_frame, text="Üyelik İptal Et", command=uye_iptal)
uye_iptal_button.grid(row=0, column=1)

# Kullanım kılavuzu metni
kilavuz_metni = """
Kütüphane Yönetim Sistemi Kullanım Kılavuzu

- Kitap Ödünç Alma:
  1. Kitap ID ve Üye ID alanlarına ilgili değerleri girin.
  2. "Kitap Ödünç Al" butonuna tıklayın.
  3. Kitap başarıyla ödünç alınmış olacaktır.

- Kitap İade Etme:
  1. İade etmek istediğiniz kitabın ID'sini girin.
  2. "Kitap İade Et" butonuna tıklayın.
  3. Kitap başarıyla iade edilmiş olacaktır.

- Kitapları Göster:
  Mevcut kitapların listesini görmek için "Kitapları Göster" butonuna tıklayın.

- Üyeleri Göster:
  Mevcut üyelerin listesini görmek için "Üyeleri Göster" butonuna tıklayın.

- Üye Ol:
  1. Ad ve Soyad alanlarına ilgili değerleri girin.
  2. "Üye Ol" butonuna tıklayın.
  3. Üyelik işlemi başarıyla tamamlanacaktır.

- Üyelik İptal Et:
  1. İptal etmek istediğiniz üyenin ID'sini girin.
  2. "Üyelik İptal Et" butonuna tıklayın.
  3. Üyelik başarıyla iptal edilecektir.
"""

# Kullanım kılavuzu butonu
usage_guide_button = tk.Button(root, text="Kullanım Kılavuzu", command=show_usage_guide)
usage_guide_button.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
