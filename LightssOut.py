import tkinter as tk
from tkinter import scrolledtext
import random
import time
from collections import deque

class PermainanLightsOut:
    def __init__(self, root):
        # Inisialisasi jendela Tkinter
        self.root = root
        self.root.title("Permainan Lights Out")
        # Ukuran grid permainan
        self.ukuran = 3
        # Matriks untuk menyimpan tombol-tombol
        self.tombol = [[None for _ in range(self.ukuran)] for _ in range(self.ukuran)]
        # Daftar untuk menyimpan langkah-langkah yang diambil pemain
        self.langkah = []

        # Membuat tombol-tombol dalam grid
        for baris in range(self.ukuran):
            for kolom in range(self.ukuran):
                # Menggunakan lambda untuk memasukkan argumen ke dalam fungsi ubah_lampu
                tombol = tk.Button(self.root, width=10, height=5, command=lambda r=baris, c=kolom: self.ubah_lampu(r, c))
                tombol.grid(row=baris, column=kolom, padx=0, pady=0)
                self.tombol[baris][kolom] = tombol

        # Membuat area untuk menampilkan langkah-langkah
        self.langkah_tampilan = scrolledtext.ScrolledText(self.root, width=40, height=10)
        self.langkah_tampilan.grid(row=self.ukuran, column=0, columnspan=self.ukuran)

        # Tombol untuk memecahkan permainan dengan brute force
        tombol_selesaikan = tk.Button(self.root, text="Selesaikan (Brute Force)", command=self.selesaikan_dan_tampilkan_brute_force)
        tombol_selesaikan.grid(row=self.ukuran + 1, column=0, columnspan=self.ukuran)

        # Tombol untuk memecahkan permainan dengan backtracking
        tombol_selesaikan = tk.Button(self.root, text="Selesaikan (Backtracking)", command=self.selesaikan_dan_tampilkan_backtrack)
        tombol_selesaikan.grid(row=self.ukuran + 2, column=0, columnspan=self.ukuran)

        # Mengacak grid awal
        self.acak_grid()
        # Menampilkan langkah-langkah awal
        self.perbarui_tampilan_langkah()

    def ubah_lampu(self, baris, kolom):
        # Menambah langkah ke daftar langkah-langkah
        self.langkah.append((baris, kolom))
        self.perbarui_tampilan_langkah()

        # Memanggil metode ubah_tombol untuk mengubah status tombol yang dipilih dan tetangganya
        self.ubah_tombol(baris, kolom)
        if baris > 0:
            self.ubah_tombol(baris-1, kolom)
        if baris < self.ukuran - 1:
            self.ubah_tombol(baris+1, kolom)
        if kolom > 0:
            self.ubah_tombol(baris, kolom-1)
        if kolom < self.ukuran - 1:
            self.ubah_tombol(baris, kolom+1)
        
        # Memeriksa apakah pemain menang setelah setiap langkah
        if self.periksa_kemenangan():
            self.tampilkan_pesan_kemenangan()
            return True

        return False

    def ubah_tombol(self, baris, kolom):
        # Mengubah warna latar belakang tombol yang dipilih antara kuning dan default
        tombol = self.tombol[baris][kolom]
        if tombol["bg"] == "SystemButtonFace":
            tombol.config(bg="yellow")
        else:
            tombol.config(bg="SystemButtonFace")

    def periksa_kemenangan(self):
        # Memeriksa apakah semua lampu sudah dimatikan (warna default)
        for baris in range(self.ukuran):
            for kolom in range(self.ukuran):
                if self.tombol[baris][kolom]["bg"] == "yellow":
                    return False
        return True

    def tampilkan_pesan_kemenangan(self):
        # Menampilkan pesan "Anda Menang!" saat pemain menang
        pesan_kemenangan = tk.Label(self.root, text="Anda Menang!", font=("Arial", 24))
        pesan_kemenangan.grid(row=self.ukuran + 3, column=0, columnspan=self.ukuran)

    def perbarui_tampilan_langkah(self):
        # Memperbarui area tampilan dengan langkah-langkah terbaru yang diambil oleh pemain
        langkah_teks = "Langkah yang diambil:\n" + "\n".join([f"Langkah {i+1}: Tombol ({r},{c})" for i, (r, c) in enumerate(self.langkah)])
        self.langkah_tampilan.delete("1.0", tk.END)  # Hapus teks yang ada
        self.langkah_tampilan.insert(tk.END, langkah_teks)  # Masukkan teks langkah-langkah baru

    def acak_grid(self):
        # Mengacak grid awal dengan mengubah warna sejumlah tombol secara acak
        for _ in range(random.randint(5, 15)):
            baris = random.randint(0, self.ukuran - 1)
            kolom = random.randint(0, self.ukuran - 1)
            self.ubah_tombol(baris, kolom)

    def selesaikan_brute_force(self):
        # Mencoba semua kemungkinan langkah dengan menggunakan pendekatan brute force
        keadaan_awal = [[tombol["bg"] for tombol in baris] for baris in self.tombol]
        langkah_awal = []
        antrian = deque([(keadaan_awal, langkah_awal)])  # Antrian untuk menyimpan keadaan dan langkah-langkah yang diambil
        keadaan_dikunjungi = set()  # Set untuk menyimpan keadaan yang sudah dikunjungi

        if self.periksa_keadaan_kemenangan(keadaan_awal):
            return langkah_awal

        while antrian:
            keadaan_sekarang, langkah_sekarang = antrian.popleft()  # Mengambil keadaan dan langkah-langkah saat ini dari antrian
            keadaan_tuple = tuple(tuple(baris) for baris in keadaan_sekarang)

            if keadaan_tuple not in keadaan_dikunjungi:
                keadaan_dikunjungi.add(keadaan_tuple)

                if self.periksa_keadaan_kemenangan(keadaan_sekarang):
                    return langkah_sekarang

                # Memeriksa setiap tombol dalam keadaan saat ini dan mencoba semua kemungkinan langkah
                for baris in range(self.ukuran):
                    for kolom in range(self.ukuran):
                        keadaan_baru = self.ubah_keadaan_lampu(keadaan_sekarang, baris, kolom)
                        langkah_baru = langkah_sekarang + [(baris, kolom)]
                        antrian.append((keadaan_baru, langkah_baru))

        return None

    def ubah_keadaan_lampu(self, keadaan, baris, kolom):
        # Mengubah keadaan tombol dalam matriks keadaan
        keadaan_baru = [list(baris) for baris in keadaan]
        self.ubah_tombol_keadaan(keadaan_baru, baris, kolom)
        if baris > 0:
            self.ubah_tombol_keadaan(keadaan_baru, baris-1, kolom)
        if baris < self.ukuran - 1:
            self.ubah_tombol_keadaan(keadaan_baru, baris+1, kolom)
        if kolom > 0:
            self.ubah_tombol_keadaan(keadaan_baru, baris, kolom-1)
        if kolom < self.ukuran - 1:
            self.ubah_tombol_keadaan(keadaan_baru, baris, kolom+1)
        return keadaan_baru

    def ubah_tombol_keadaan(self, keadaan, baris, kolom):
        # Mengubah keadaan tombol dalam matriks keadaan antara kuning dan default
        if keadaan[baris][kolom] == "SystemButtonFace":
            keadaan[baris][kolom] = "yellow"
        else:
            keadaan[baris][kolom] = "SystemButtonFace"

    def periksa_keadaan_kemenangan(self, keadaan):
        # Memeriksa apakah semua tombol dalam keadaan sudah dimatikan
        for baris in range(self.ukuran):
            for kolom in range(self.ukuran):
                if keadaan[baris][kolom] == "yellow":
                    return False
        return True

    def selesaikan_dan_tampilkan_brute_force(self):
        # Memecahkan permainan dengan brute force dan menampilkan langkah-langkah solusi serta waktu eksekusi
        waktu_mulai = time.time()
        solusi = self.selesaikan_brute_force()
        waktu_selesai = time.time()

        if solusi:
            langkah_teks = "\n".join([f"Langkah {i+1}: Tombol ({r},{c})" for i, (r, c) in enumerate(solusi)])
            self.langkah_tampilan.insert(tk.END, "\n\nLangkah-langkah (Brute Force):\n" + langkah_teks)
        else:
            self.langkah_tampilan.insert(tk.END, "\n\nTidak ditemukan solusi.")

        waktu_eksekusi = waktu_selesai - waktu_mulai
        self.langkah_tampilan.insert(tk.END, f"\n\nWaktu Eksekusi (Brute Force): {waktu_eksekusi:.4f} detik")

    def selesaikan_backtrack(self, kedalaman_maks=5):
        # Mencoba memecahkan permainan dengan pendekatan backtracking dengan batasan kedalaman pencarian
        keadaan_awal = [[tombol["bg"] for tombol in baris] for baris in self.tombol]
        langkah_awal = []
        keadaan_dikunjungi = set()  # Set untuk menyimpan keadaan yang sudah dikunjungi
        solusi = self.backtrack(keadaan_awal, langkah_awal, kedalaman_maks, keadaan_dikunjungi)
        return solusi

    def backtrack(self, keadaan, langkah, kedalaman_maks, keadaan_dikunjungi):
        tumpukan = [(keadaan, langkah, kedalaman_maks)]  # Stack untuk menyimpan keadaan, langkah, dan kedalaman saat ini

        while tumpukan:
            keadaan_sekarang, langkah_sekarang, kedalaman_sekarang = tumpukan.pop()  # Mengambil elemen dari stack

            if self.periksa_keadaan_kemenangan(keadaan_sekarang):
                return langkah_sekarang

            if kedalaman_sekarang == 0:
                continue

            # Mengonversi keadaan ke tupel hashable
            keadaan_tuple = tuple(tuple(baris) for baris in keadaan_sekarang)

            # Memeriksa apakah keadaan saat ini sudah dikunjungi sebelumnya
            if keadaan_tuple in keadaan_dikunjungi:
                continue

            keadaan_dikunjungi.add(keadaan_tuple)  # Menambah keadaan saat ini ke set keadaan yang sudah dikunjungi

            for baris in range(self.ukuran):
                for kolom in range(self.ukuran):
                    keadaan_baru = self.ubah_keadaan_lampu(keadaan_sekarang, baris, kolom)
                    langkah_baru = langkah_sekarang + [(baris, kolom)]
                    tumpukan.append((keadaan_baru, langkah_baru, kedalaman_sekarang - 1))  # Menambah elemen baru ke tumpukan

        return None

    def selesaikan_dan_tampilkan_backtrack(self):
        # Memecahkan permainan dengan pendekatan backtracking dan menampilkan langkah-langkah solusi serta waktu eksekusi
        kedalaman_awal =5  # Kedalaman pencarian awal
        kedalaman_maks = kedalaman_awal  # Menyimpan nilai kedalaman awal

        self.langkah_tampilan.insert(tk.END, f"\n\nMencoba dengan Kedalaman Maksimal: {kedalaman_maks}\n")  # Memasukkan kedalaman maksimal saat ini

        while True:
            waktu_mulai = time.time()
            solusi = self.selesaikan_backtrack(kedalaman_maks)
            waktu_selesai = time.time()
            
            if solusi:
                langkah_teks = "\n".join([f"Langkah {i+1}: Tombol ({r},{c})" for i, (r, c) in enumerate(solusi)])
                self.langkah_tampilan.insert(tk.END, "\nLangkah-langkah Backtracking):\n" + langkah_teks)
                break  # Keluar dari loop jika ditemukan solusi
            else:
                kedalaman_maks += 5  # Menambah kedalaman pencarian sebesar 5
                self.langkah_tampilan.insert(tk.END, f"\nKedalaman maksimum ditingkatkan menjadi: {kedalaman_maks}\n")  # Memasukkan kedalaman maksimal saat ini

        waktu_eksekusi = waktu_selesai - waktu_mulai
        self.langkah_tampilan.insert(tk.END, f"\n\nWaktu Eksekusi (Backtracking): {waktu_eksekusi:.4f} detik")

# Membuat jendela utama
root = tk.Tk()

# Inisialisasi permainan
permainan = PermainanLightsOut(root)

# Memulai loop peristiwa Tkinter
root.mainloop()


