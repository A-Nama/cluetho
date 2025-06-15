import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import random

# Paths
SUSPECT_DIR = "assets/suspects"
WEAPON_DIR = "assets/weapons"
ROOM_DIR = "assets/rooms"

# Data
suspects = ["Dr Anna", "Mr John", "Prof Mike", "Mrs Queens", "Mr Ben", "Prof Alice"]
weapons = ["keyboard", "coffee mug", "pencil", "candlestick", "golfclub", "dagger"]
rooms = ["Hallway", "Dining Room", "Kitchen", "Library", "Office", "Attic", "Lounge", "Drawing Room"]

solution = {
    "suspect": random.choice(suspects),
    "weapon": random.choice(weapons),
    "room": random.choice(rooms)
}

# Tkinter Setup
root = tk.Tk()
root.title("Cluetho 🔍")
root.geometry("1000x750")
root.config(bg="#1a1a40")

canvas = tk.Canvas(root, width=1000, height=400, bg="#14213d")
canvas.pack()

# Load images
def load_images(name_list, folder):
    images = {}
    for name in name_list:
        path = os.path.join(folder, f"{name}.jpeg")
        img = Image.open(path).resize((60, 60))
        images[name] = ImageTk.PhotoImage(img)
    return images

suspect_imgs = load_images(suspects, SUSPECT_DIR)
weapon_imgs = load_images(weapons, WEAPON_DIR)
room_imgs = load_images(rooms, ROOM_DIR)

# Players
players = []
guess_counts = []
current_player_index = 0

# Frames
setup_frame = tk.Frame(root, bg="#1a1a40")
setup_frame.pack(pady=10)

selection_frame = tk.Frame(root, bg="#1a1a40")
selection_frame.pack(pady=10)

game_frame = tk.Frame(root, bg="#1a1a40")
game_frame.pack(pady=10)

# Setup Phase
player_num_var = tk.IntVar(value=2)
tk.Label(setup_frame, text="Select Number of Players:", font=("Arial", 14), fg="white", bg="#1a1a40").pack()
tk.Spinbox(setup_frame, from_=2, to=6, textvariable=player_num_var, font=("Arial", 14), width=5).pack(pady=5)

name_var = tk.StringVar()
tk.Label(setup_frame, text="Enter Player Name:", font=("Arial", 14), fg="white", bg="#1a1a40").pack()
tk.Entry(setup_frame, textvariable=name_var, font=("Arial", 14)).pack(pady=5)

def add_player():
    name = name_var.get().strip()
    if name:
        players.append(name)
        guess_counts.append(0)
        name_var.set("")
        if len(players) == player_num_var.get():
            setup_frame.pack_forget()
            draw_guess_options()
            update_info()

tk.Button(setup_frame, text="Add Player", command=add_player).pack(pady=10)

# Game Info Labels
info_label = tk.Label(game_frame, text="", font=("Arial", 12), fg="white", bg="#1a1a40")
info_label.pack(anchor="nw")
turn_label = tk.Label(game_frame, text="", font=("Arial", 16, "bold"), fg="white", bg="#1a1a40")
turn_label.pack(pady=10)

def update_info():
    info_label.config(text=f"👤 {players[current_player_index]} | Guesses: {guess_counts[current_player_index]}")
    turn_label.config(text=f"🎯 {players[current_player_index]}'s Turn")

# Guess variables
guess_selection = {"suspect": None, "weapon": None, "room": None}

# Guess selectors with images
def create_scrollable_list(parent, items, images, var, title):
    frame = tk.Frame(parent, bg="#1a1a40")
    tk.Label(frame, text=title, font=("Arial", 14), fg="white", bg="#1a1a40").pack()

    canvas = tk.Canvas(frame, width=280, height=150, bg="#14213d", highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    list_frame = tk.Frame(canvas, bg="#14213d")

    canvas.create_window((0, 0), window=list_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    list_frame.bind("<Configure>", on_configure)

    for name in items:
        row = tk.Frame(list_frame, bg="#14213d")
        tk.Radiobutton(row, text=name, variable=var, value=name, bg="#14213d", fg="white", font=("Arial", 12), selectcolor="#1a1a40").pack(side="left")
        tk.Label(row, image=images[name], bg="#14213d").pack(side="right")
        row.pack(anchor="w", pady=5, padx=5)

    canvas.pack(side="left")
    scrollbar.pack(side="right", fill="y")
    frame.pack(side="left", padx=20)

suspect_var = tk.StringVar()
weapon_var = tk.StringVar()
room_var = tk.StringVar()

def draw_guess_options():
    create_scrollable_list(selection_frame, suspects, suspect_imgs, suspect_var, "Suspects")
    create_scrollable_list(selection_frame, weapons, weapon_imgs, weapon_var, "Weapons")
    create_scrollable_list(selection_frame, rooms, room_imgs, room_var, "Rooms")

def submit_guess():
    global current_player_index
    if not (suspect_var.get() and weapon_var.get() and room_var.get()):
        messagebox.showwarning("Incomplete", "Please make a selection in all categories.")
        return

    guess_selection["suspect"] = suspect_var.get()
    guess_selection["weapon"] = weapon_var.get()
    guess_selection["room"] = room_var.get()

    player_name = players[current_player_index]
    guess_counts[current_player_index] += 1

    correct = [
        guess_selection["suspect"] == solution["suspect"],
        guess_selection["weapon"] == solution["weapon"],
        guess_selection["room"] == solution["room"]
    ]

    if all(correct):
        messagebox.showinfo("Winner 🎉", f"{player_name} won in {guess_counts[current_player_index]} guesses!")
        root.destroy()
    else:
        wrongs = []
        if not correct[0]: wrongs.append("suspect")
        if not correct[1]: wrongs.append("weapon")
        if not correct[2]: wrongs.append("room")
        reveal = random.choice(wrongs)
        messagebox.showinfo("Hint 💡", f"Oops! The {reveal} is wrong.")
        current_player_index = (current_player_index + 1) % len(players)
        update_info()

tk.Button(root, text="Submit Guess", font=("Arial", 14), command=submit_guess).pack(pady=10)

# Mainloop
root.mainloop()
