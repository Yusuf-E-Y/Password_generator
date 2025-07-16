from datetime import datetime
import keyboard
import random
import pyperclip
import sqlite3

password1 = []

class Generator:

    def password(l1, l2, l3):
        for i in range(l1):  
            n_1 = random.randint(0, 9)
            password1.insert(random.randint(0, len(password1)), str(n_1))

        for i in range(l2):  
            n = random.randint(0, 1)
            n_string = random.randint(1, 26)
            if n == 0:
                n_big = chr(64 + n_string)
                password1.insert(random.randint(0, len(password1)), n_big)
            else:
                n_little = chr(96 + n_string)
                password1.insert(random.randint(0, len(password1)), n_little)

        special_chars = ['?', '@', '!', '#', '%', '+', '-', '*']
        for i in range(l3):  
            special = random.choice(special_chars)
            password1.insert(random.randint(0, len(password1)), special)

        terminal_data1 = "".join(password1)
        pyperclip.copy(terminal_data1)
        
        conn = sqlite3.connect("Archive.db")
        k = conn.cursor()
        k.execute("INSERT INTO list (Password, Date) VALUES (?, ?)", (terminal_data1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        password1.clear()

keyboard.add_hotkey('ctrl+shift+f', lambda: Generator.password(7, 6, 6))
keyboard.add_hotkey('ctrl+shift+t', lambda: Generator.password(6, 6, 5))
keyboard.add_hotkey('ctrl+shift+r', lambda: Generator.password(5, 4, 4))
keyboard.add_hotkey('ctrl+shift+e', lambda: Generator.password(4, 4, 3))
keyboard.add_hotkey('ctrl+shift+s', lambda: Generator.password(4, 3, 1))

keyboard.wait()
