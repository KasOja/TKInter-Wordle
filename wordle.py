import tkinter as tk
import random
import json

class Wordle:

    def __init__(self):
        with open("wordles.json", "r") as wordfile:
            self.wordles = json.load(wordfile)
        with open("nonwordles.json", "r") as wordfile:
            self.nonwordles = json.load(wordfile)
        self.guielements()
        self.init_game()
        self.game_over = False
        self.window.mainloop()

    def guielements(self):
        self.window = tk.Tk()
        self.window.configure(bg="black")
        self.window.title("WORDLE")
        self.window.rowconfigure([i for i in range(3)], weight=1)
        self.window.columnconfigure(0, weight=1)

        btn_new = tk.Button(master=self.window, text= "WORDLE", font=("TkHeadingFont",20), bg="black", fg="white", command= lambda: self.init_game())
        btn_new.grid(row=0, column=0, sticky="nsew")
        # Wordle spaces
        fr_wordle = tk.Frame(master=self.window)
        fr_wordle.rowconfigure([i for i in range(6)], weight=1,pad=3)
        fr_wordle.columnconfigure([i for i in range(5)], weight=1,pad=3)
        fr_wordle.grid(row=1, column=0, sticky="nsew")
        
        self.letterspaces = []
        for i in range(6):
            row = []
            for j in range(5):
                label = tk.Label(master= fr_wordle, relief=tk.RAISED, border=5, foreground="white", background= "black", width=3, height=3)
                label.grid(row=i, column=j, sticky="nsew")
                row.append(label)
            self.letterspaces.append(row)
        
        # Virtual keyboard
        # Keys saved to list so they can be easily accessed later
        fr_keys = tk.Frame(master=self.window, background="black")
        fr_keys.rowconfigure([i for i in range(3)], weight=1,pad=3)
        fr_keys.columnconfigure([i for i in range(20)], weight=1,pad=3)
        fr_keys.grid(row=3, column=0, sticky="nsew")
        self.keys = []
        
        # Row 1:
        letters = "QWERTYUIOP"
        for i in range(10):
            button = tk.Button(master=fr_keys, bg="#959595", relief=tk.GROOVE, text=letters[i], font=("arial",15),width=2, foreground="white", command=lambda l=letters[i]: self.playerinput(l))
            button.grid(row=0, column=i*2, columnspan=2, padx=2, pady=2, sticky="nsew")
            self.keys.append(button)
       
        # Row 2:
        letters="ASDFGHJKL"
        for i in range(9):
            button = tk.Button(master=fr_keys, bg="#959595", relief=tk.GROOVE, text=letters[i], font=("arial",15),width=2, foreground="white", command=lambda l=letters[i]: self.playerinput(l))
            button.grid(row=1, column=i*2+1, columnspan=2, padx=2, pady=2, sticky="nsew")
            self.keys.append(button)

        # Row 3:
        btn_check = tk.Button(master=fr_keys, bg="#959595", relief=tk.GROOVE, text="ENTER", font=("arial",10),width=2, foreground="white", command= lambda: self.check())
        btn_check.grid(row=2, column=0, columnspan=3, padx=2, pady=2, sticky="nsew")
        btn_back = tk.Button(master=fr_keys, bg="#959595", relief=tk.GROOVE, text="<<", font=("arial",10),width=2, foreground="white", command= lambda: self.backspace())
        btn_back.grid(row=2, column=17, columnspan=3, padx=2, pady=2, sticky="nsew")

        letters="ZXCVBNM"
        for i in range(7):
            button = tk.Button(master=fr_keys, bg="#959595", relief=tk.GROOVE, text=letters[i], font=("arial",15),width=2, foreground="white", command=lambda l=letters[i]: self.playerinput(l))
            button.grid(row=2, column=i*2+3, columnspan=2, padx=2, pady=2, sticky="nsew")
            self.keys.append(button)
        
        self.keys.append(btn_back)
        self.keys.append(btn_check)

        # Keybinds:
        for key in self.keys[:-2]:
            self.window.bind(key["text"], lambda x, y=key: y.invoke())
            self.window.bind(key["text"].lower(), lambda x, y=key: y.invoke())

        self.window.bind("<Return>", lambda x: btn_check.invoke())
        self.window.bind("<BackSpace>", lambda x: btn_back.invoke())

    def randomword(self):
        word = random.choice(self.wordles)
        print(word)
        return word
    
    def init_game(self):
        self.game_over = False
        for key in self.keys:
            key["state"] = tk.NORMAL
            key["background"] = "#959595"
        for row in self.letterspaces:
            for space in row:
                space["text"] = ""
                space["background"] = "black"
        self.currentword = self.randomword()
        self.row = 0
        self.row_letters = []
        self.update()
        
    def update(self):
        for i in range(5):
            if i >= len(self.row_letters):
                self.letterspaces[self.row][i]["text"] = ""
            else:
                self.letterspaces[self.row][i]["text"] = self.row_letters[i].upper()
        for space in self.letterspaces[self.row]:
            space["background"] = "black"
        if len(self.row_letters) < 5:
            self.letterspaces[self.row][len(self.row_letters)]["background"] = "#212121"

    def check(self):
        if self.game_over == True:
            self.init_game()
        if len(self.row_letters) < 5:
            return
        if "".join(self.row_letters) not in self.nonwordles and "".join(self.row_letters) not in self.wordles:
            errorlabel = tk.Label(background= "white", text="NOT IN WORD LIST", font=("impact",20))
            errorlabel.place(relx=0.5, rely=0.5, anchor="center")
            errorlabel.after(1000, lambda: errorlabel.destroy())
            return
        
        greencount = 0
        for i, letter in enumerate(self.row_letters):
            if letter in self.currentword:
                for j , l in enumerate(self.currentword):
                    if l == letter and self.letterspaces[self.row][i]["background"] != "#08A400":
                        self.letterspaces[self.row][i]["background"] = "#7B8200"
                    if l == letter and j == i:
                        self.letterspaces[self.row][i]["background"] = "#08A400"
                        greencount += 1
            else:
                for key in self.keys:
                    if key["text"].lower() == letter:
                        key["background"] = "#3E3E3E"
                self.letterspaces[self.row][i]["background"] = "#3E3E3E"

        # Remove extra yellow markings
        for letter in set(self.row_letters):
            if letter in self.currentword:
                extras = self.row_letters.count(letter) - self.currentword.count(letter)
                while extras > 0:
                    for space in reversed(self.letterspaces[self.row]):
                        if space["text"].lower() == letter and space["background"] =="#7B8200":
                            space["background"] = "#3E3E3E"
                            break
        if greencount >= 5:
            self.gameover()
            for key in self.keys:
                key["background"] = "#08A400"
        self.row += 1
        if self.row > 5:
            self.gameover()
        self.row_letters = []

    def gameover(self):
        for key in self.keys[:-1]:
            key["state"] = tk.DISABLED
        self.game_over = True
    
    def backspace(self):
        if self.row_letters != []:
            self.row_letters.pop()
            self.update()
        
    def playerinput(self, letter):
        if len(self.row_letters) >= 5:
            return
        self.row_letters.append(letter.lower())
        self.update()

if __name__ == "__main__":
    Wordle()