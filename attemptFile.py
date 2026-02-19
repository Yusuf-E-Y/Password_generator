import customtkinter as ctk
from tkinter import filedialog, messagebox
import random
import pyperclip
from datetime import datetime
import sqlite3

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main():
    root = ctk.CTk()
    root.title("🔐 Password Generator")
    root.geometry("520x640")
    root.resizable(False, False)

    # ── Tab system ──────────────────────────────────────────────
    tabview = ctk.CTkTabview(root, width=500, height=600)
    tabview.pack(padx=10, pady=10, fill="both", expand=True)

    tab1 = tabview.add("🏠 Ana Menü")
    tab2 = tabview.add("🗂 Arşiv")

    # ── Database ───────────────────────────────────────────────
    connect = sqlite3.connect("Archive.db")
    k = connect.cursor()
    k.execute("CREATE TABLE IF NOT EXISTS list (Password TEXT, Date TEXT)")
    connect.commit()

    # ── Algorithm ────────────────────────────────
    password = []

    def number_random(d):
        for _ in range(d):
            password.insert(random.randint(0, 3), random.randint(0, 9))

    def insert():
        global n_insert, n_insert_1
        n_insert = random.randint(-1, 6)
        n_insert_1 = random.randint(-1, 6)

    def string_random(f):
        for _ in range(f):
            n = random.randint(-1, 1)
            n_string = random.randint(1, 26)
            if n == 0:
                char = chr(64 + n_string)
                password.insert(n_insert, char)
            else:
                char = chr(96 + n_string)
                password.insert(n_insert_1, char)

    def special_char_random(g):
        special_chars = ['?', '@', '!', '#', '/', '&', '(', ')', '+', '-', '*', '%']
        for _ in range(g):
            password.insert(random.randint(0, len(password)), random.choice(special_chars))

    def show_data():
        global terminal_data
        terminal_data = "".join(map(str, password))
        password_display.configure(text=terminal_data)
        strength_bar.set(min(len(terminal_data) / 14, 1.0))
        color = "#e74c3c" if len(terminal_data) <= 6 else "#f39c12" if len(terminal_data) <= 10 else "#2ecc71"
        strength_bar.configure(progress_color=color)

    def collection_random():
        x = int(length_combo.get())
        g, d, f = {
            6: (1, 2, 3),
            8: (1, 3, 4),
            10: (3, 3, 4),
            12: (3, 3, 6),
            14: (4, 5, 5)
        }[x]
        number_random(d)
        insert()
        string_random(f)
        special_char_random(g)
        show_data()
        password.clear()

    def save_file():
        if not password_display.cget("text"):
            messagebox.showwarning("Uyarı", "Henüz bir şifre oluşturulmadı.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(password_display.cget("text"))
            messagebox.showinfo("Başarılı", "Dosya kaydedildi.")

    def label_copy():
        label = password_display.cget("text")
        if not label:
            return
        pyperclip.copy(label)
        k.execute("INSERT INTO list VALUES (?, ?)", (label, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        connect.commit()
        # Update archive list
        archive_list.insert("", "end", values=(label, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        copy_btn.configure(text="✅ Kopyalandı!")
        root.after(1500, lambda: copy_btn.configure(text="📋 Kopyala"))

    def copy_from_archive():
        selected = archive_list.selection()
        if selected:
            values = archive_list.item(selected[0], "values")
            pyperclip.copy(values[0])
            messagebox.showinfo("Kopyalandı", f"Şifre panoya kopyalandı:\n{values[0]}")

    def exits():
        connect.close()
        root.destroy()

    # ── TAB 1 - Main Menu UI ───────────────────────────────────────

    # Başlık
    title_label = ctk.CTkLabel(tab1, text="🔐 Şifre Oluşturucu",
                               font=ctk.CTkFont(size=22, weight="bold"))
    title_label.pack(pady=(25, 5))

    subtitle = ctk.CTkLabel(tab1, text="Güçlü ve rastgele şifreler oluşturun",
                            font=ctk.CTkFont(size=12), text_color="gray")
    subtitle.pack(pady=(0, 20))

    # Password length
    length_frame = ctk.CTkFrame(tab1, corner_radius=12)
    length_frame.pack(padx=30, pady=8, fill="x")

    ctk.CTkLabel(length_frame, text="Şifre Uzunluğu", font=ctk.CTkFont(size=13, weight="bold")).pack(
        side="left", padx=15, pady=12)

    length_combo = ctk.CTkComboBox(length_frame, values=["6", "8", "10", "12", "14"],
                                   width=100, state="readonly")
    length_combo.set("8")
    length_combo.pack(side="right", padx=15, pady=12)

    # Show password tab
    display_frame = ctk.CTkFrame(tab1, corner_radius=12, fg_color=("#1a1a2e", "#1a1a2e"))
    display_frame.pack(padx=30, pady=12, fill="x")

    ctk.CTkLabel(display_frame, text="Oluşturulan Şifre", font=ctk.CTkFont(size=11),
                 text_color="gray").pack(pady=(10, 0))

    password_display = ctk.CTkLabel(display_frame, text="—",
                                    font=ctk.CTkFont(size=20, weight="bold", family="Courier"),
                                    text_color="#00d4ff")
    password_display.pack(pady=(2, 8))

    # Power bar
    strength_bar = ctk.CTkProgressBar(display_frame, width=300, height=8)
    strength_bar.set(0)
    strength_bar.pack(pady=(0, 12))

    # Butons
    btn_frame = ctk.CTkFrame(tab1, fg_color="transparent")
    btn_frame.pack(padx=30, pady=10, fill="x")

    create_btn = ctk.CTkButton(btn_frame, text="⚡ Oluştur", command=collection_random,
                               font=ctk.CTkFont(size=14, weight="bold"),
                               height=44, corner_radius=10)
    create_btn.pack(fill="x", pady=(0, 8))

    action_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
    action_frame.pack(fill="x")

    copy_btn = ctk.CTkButton(action_frame, text="📋 Kopyala", command=label_copy,
                             width=130, height=38, corner_radius=10,
                             fg_color="#2c3e50", hover_color="#34495e")
    copy_btn.pack(side="left", padx=(0, 8), expand=True, fill="x")

    save_btn = ctk.CTkButton(action_frame, text="💾 Kaydet", command=save_file,
                             width=130, height=38, corner_radius=10,
                             fg_color="#27ae60", hover_color="#2ecc71")
    save_btn.pack(side="right", expand=True, fill="x")

    # Exit
    exit_btn = ctk.CTkButton(tab1, text="Çıkış", command=exits,
                             width=80, height=30, corner_radius=8,
                             fg_color="transparent", border_width=1,
                             border_color="gray", text_color="gray",
                             hover_color="#c0392b")
    exit_btn.pack(pady=(10, 0))

    # ── TAB 2 - Arhive UI ─────────────────────────────────────────
    from tkinter import ttk

    ctk.CTkLabel(tab2, text="📚 Şifre Arşivi",
                 font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 5))
    ctk.CTkLabel(tab2, text="Kopyalanan şifreler buraya kaydedilir",
                 font=ctk.CTkFont(size=11), text_color="gray").pack(pady=(0, 12))

    # Treeview 
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#2b2b2b", foreground="white",
                    rowheight=28, fieldbackground="#2b2b2b", font=("Courier", 10))
    style.configure("Treeview.Heading", background="#1f1f1f", foreground="#00d4ff",
                    font=("Arial", 11, "bold"))
    style.map("Treeview", background=[("selected", "#3498db")])

    tree_frame = ctk.CTkFrame(tab2, corner_radius=10)
    tree_frame.pack(padx=20, pady=5, fill="both", expand=True)

    archive_list = ttk.Treeview(tree_frame, columns=("Password", "Date"),
                                show="headings", style="Treeview")
    archive_list.heading("Password", text="Şifre")
    archive_list.heading("Date", text="Tarih")
    archive_list.column("Password", width=200)
    archive_list.column("Date", width=160)

    scrollbar = ctk.CTkScrollbar(tree_frame, command=archive_list.yview)
    archive_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y", padx=(0, 2), pady=2)
    archive_list.pack(fill="both", expand=True, padx=2, pady=2)

    for row in k.execute("SELECT * FROM list"):
        archive_list.insert("", "end", values=row)

    copy2_btn = ctk.CTkButton(tab2, text="📋 Seçileni Kopyala", command=copy_from_archive,
                              height=38, corner_radius=10)
    copy2_btn.pack(pady=12, padx=20, fill="x")

    # ── Keyboard sprtcuts ────────────────────────────────────────
    root.bind("<Control-c>", lambda e: copy_btn.invoke())
    root.bind("<Control-s>", lambda e: save_btn.invoke())
    root.bind("<Return>", lambda e: create_btn.invoke())

    root.mainloop()


if __name__ == '__main__':

    main()
