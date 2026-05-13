import tkinter as tk
import random
import time
import json
import pygame
import sys, os

root = tk.Tk()
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.geometry("1000x600")
root.title("Speed Click")
root.resizable(False, False)

score = 0
start_time = None
game_duration = 10
game_active = False
best_score = 0
current_volume = 0.5


def load_best_score():
    try:
        with open("score.json", "r") as f:
            data = json.load(f)
            return data["best_score"]
    except (FileNotFoundError, KeyError):
        return 0


def save_best_score(new_best):
    with open("score.json", "w") as f:
        json.dump({"best_score": new_best}, f)


def set_volume(val):
    global current_volume
    current_volume = int(val) / 100


def menu_page():
    for widget in root.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(root, width=600, height=200, bg="#222222")
    canvas.grid(row=0, column=0, pady=20)
    canvas.create_text(300, 100, text="Speed Click", fill="red", font=("Arial", 40, "bold"))

    btn_play = tk.Button(root, text="Play", font=("Arial", 16), width=20, bg="red", command=play_page)
    btn_play.grid(row=1, column=0, pady=8)

    btn_settings = tk.Button(root, text="Settings", font=("Arial", 16), width=20, bg="grey", command=setting_page)
    btn_settings.grid(row=2, column=0, pady=8)

    btn_quit = tk.Button(root, text="Quitter", font=("Arial", 16), width=20, bg="red", command=root.destroy)
    btn_quit.grid(row=3, column=0, pady=8)


def play_page():
    global score, game_active, start_time, best_score

    for widget in root.winfo_children():
        widget.destroy()
    best_score = load_best_score()
    score = 0
    game_active = False

    label_score = tk.Label(root, text="Score: 0", font=("Arial", 20))
    label_score.pack(pady=5)

    label_time = tk.Label(root, text="Temps: 10", font=("Arial", 20))
    label_time.pack(pady=5)

    label_best = tk.Label(root, text=f"Meilleur score: {best_score}", font=("Arial", 20))
    label_best.pack(pady=5)

    btn_back = tk.Button(root, text="Retour menu", font=("Arial", 16), bg="red", command=menu_page)
    btn_back.pack(side="bottom", pady=10)

    btn_click = tk.Button(root, text="CLIQUE MOI", font=("Arial", 20))
    btn_click.place(x=250, y=250)

    def move_button():
        max_x = root.winfo_width() - 130
        max_y = root.winfo_height() - 80
        x = random.randint(10, max(10, max_x))
        y = random.randint(100, max(100, max_y))
        btn_click.place(x=x, y=y)

    def on_click():
        global score, game_active, start_time

        if not game_active:
            start_game()
            return

        score += 1
        label_score.config(text=f"Score: {score}")
        move_button()

    btn_click.config(command=on_click)

    def start_game():
        global game_active, start_time, score
        game_active = True
        start_time = time.time()
        score = 0

        btn_click.config(text="CLIQUE !")
        label_score.config(text="Score: 0")
        label_time.config(text="Temps: 10")

        update_timer()

    def update_timer():
        if not game_active:
            return

        elapsed = time.time() - start_time
        remaining = max(0, game_duration - int(elapsed))
        label_time.config(text=f"Temps: {remaining}")

        if remaining <= 0:
            end_game()
        else:
            root.after(1000, update_timer)

    def end_game():
        global game_active, best_score, score

        game_active = False
        btn_click.config(text="FINI !")

        if score > best_score:
            best_score = score
            save_best_score(best_score)

        label_best.config(text=f"Meilleur score: {best_score}")


def setting_page():
    global current_volume

    for widget in root.winfo_children():
        widget.destroy()

    page = tk.Frame(root, bg="white")
    page.grid(row=0, column=0, sticky="nsew")

    titre = tk.Label(page, text="Settings", font=("Arial", 30, "bold"), bg="white")
    titre.grid(row=0, column=0, pady=20, padx=40)

    volume_label = tk.Label(page, text="Volume de la musique", font=("Arial", 16), bg="white")
    volume_label.grid(row=1, column=0, pady=(10, 0))

    volume_slider = tk.Scale(page,from_=0,to=100,orient="horizontal",command=set_volume,length=300,bg="white",font=("Arial", 12))
    volume_slider.set(int(current_volume * 100))
    volume_slider.grid(row=2, column=0, pady=5)

    frame_btns = tk.Frame(page, bg="white")
    frame_btns.grid(row=3, column=0, pady=5)

    btn_mute = tk.Button(frame_btns, text="🔇 Mute", font=("Arial", 13), bg="#dddddd",command=lambda: [volume_slider.set(0), set_volume(0)])
    btn_mute.pack(side="left", padx=10)

    btn_back = tk.Button(page, text="Retour menu", font=("Arial", 16), bg="red", command=menu_page)
    btn_back.grid(row=4, column=0, pady=20)


menu_page()
root.mainloop()
