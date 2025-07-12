import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import pyperclip
from datetime import datetime
import sqlite3

def main():
    root = tk.Tk()
    root.title("Password Generator")
    root.geometry("450x575")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Ana menü")
    tab2 = ttk.Frame(notebook)

    options = [6, 8, 10, 12, 14]
    combo = ttk.Combobox(tab1, values=options, state="readonly")  
    combo.set(8)  
    combo.place(x=158, y=170)

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
        text_label.config(text=terminal_data)

    def collection_random():
        x = int(combo.get())
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
        if not text_label.cget("text"):
            messagebox.showwarning("Warning", "No data")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]) # <-- Saved files with type of txt in optionel files
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_label.cget("text"))
            messagebox.showinfo("File saved")

    def Sett():
        notebook.add(tab2, text="Settings")

    def exits():
        connect.close()
        root.destroy()

# Buttons and Labels with commands

    button = tk.Button(tab1, text="Create", command=collection_random, bg="Black", fg="white", width=14)
    button.place(x=174, y=221)

    Setting = tk.Button(tab1, text="Settings", bg="Black", fg="white", command=Sett)
    Setting.place(x=20, y=30)

    save_button = tk.Button(tab1, text="Save", command=save_file)
    save_button.place(x=230, y=250)

    exit_btn = tk.Button(tab1, text="Exit", command=exits)
    exit_btn.place(x=400, y=500)

    text_label = tk.Label(tab1, width=16)
    text_label.place(x=170, y=200)

    def label_copy():
        label = text_label.cget("text")
        pyperclip.copy(label)
        k.execute("INSERT INTO list VALUES (?, ?)", (label, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        connect.commit()

    copy = tk.Button(tab1, text="Copy", command=label_copy)
    copy.place(x=175, y=250)

    def copy_keyboard(event): copy.invoke()
    def press_keyboard(event): button.invoke()
    def save_func(event): save_button.invoke()

    #Shortcuts

    root.bind("<Control-c>", copy_keyboard)
    root.bind("<Control-s>", save_func)
    root.bind("<Return>", press_keyboard)

    #Database transactions

    connect = sqlite3.connect("Archive.db")
    k = connect.cursor()
    k.execute("CREATE TABLE IF NOT EXISTS list (Password TEXT, Date TEXT)")
    connect.commit()

    ttreeview = ttk.Treeview(tab2, columns=("Password", "Date"), show="headings")
    ttreeview.heading("Password", text="Password")
    ttreeview.heading("Date", text="Date")
    ttreeview.place(x=10, y=300)

    for i in k.execute("SELECT * FROM list"):
        ttreeview.insert("", "end", values=i)

    def copyTo_archive():
        selected = ttreeview.selection()
        if selected:
            values = ttreeview.item(selected[0], "values")
            pyperclip.copy(values[0])

    copy2 = tk.Button(tab2, text="Copy", command=copyTo_archive)
    copy2.place(x=20, y=250)

    root.mainloop()

if __name__ == '__main__':
    main()
