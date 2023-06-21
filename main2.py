import customtkinter as ctk
from tkinter import ttk, StringVar
import sqlite3

# import tkinter.font as tkfont
# from random import choice

# fuente emoji
emoji_font = ("Segoe UI Emoji", 16)
emoji = "🌙"
appearance_mode = "dark"
appearance = True

# MODEL


def create_db():
    connection = sqlite3.connect("db_test.db")
    return connection


def create_table():
    connection = create_db()
    cursor = connection.cursor()
    sql = "CREATE TABLE IF NOT EXISTS data_game (id INTEGER PRIMARY KEY,\
           title VARCHAR(255), category VARCHAR(255), developer\
           VARCHAR(255), price DECIMAL(10, 2), description TEXT)"
    cursor.execute(sql)
    connection.commit()


def load_data(var_title, var_category, var_developer, var_price, textbox):
    load = (
        var_title.get(),
        var_category.get(),
        var_developer.get(),
        var_price.get(),
        textbox,
    )
    connection = create_db()
    cursor = connection.cursor()
    sql = "INSERT INTO data_game (title, category, developer, price,\
        description) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql, load)
    connection.commit()


def connect():
    create_db()
    create_table()


def change_color(theme_color):
    global emoji, appearance_mode, appearance

    if appearance:
        ctk.set_appearance_mode("light")
        theme_color.configure(text="☀️")
        appearance = False

    else:
        ctk.set_appearance_mode("dark")
        theme_color.configure(text="🌙")
        appearance = True


class SlidePanel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos):
        super().__init__(master=parent)

        # general attributes
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = abs(start_pos - end_pos)

        # animated logic
        self.pos = self.start_pos
        self.in_start_pos = True

        # layout
        self.place(relx=self.start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

    def animate(self):
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True


# exercise
# 1. animate the button and move it to the right side the window
# 2. update the panel so it move in from the right


def move_btn():
    global button_x
    button_x += 0.001
    button.place(relx=button_x, rely=0.5, anchor="center")

    if button_x < 0.9:
        window.after(10, move_btn)


# VIEW

# window
window = ctk.CTk()
window.title("Animated Widgets")
window.geometry("800x1200")
ctk.set_appearance_mode(appearance_mode)

# variables
var_title = StringVar()
var_category = StringVar()
var_developer = StringVar()
var_price = StringVar()
var_description = StringVar()
var_search = StringVar()

# animated widget
animated_panel = SlidePanel(window, 0.96, 0.65)

# animated widget

# button toogle_sidebar
toogle_sidebar = ctk.CTkButton(
    animated_panel,
    text="toogle sidebar",
    font=("Arial", 20),
    corner_radius=0,
    command=animated_panel.animate,
).pack(expand=True, fill="both", pady=10)

# label and imputs
label_title = ctk.CTkLabel(animated_panel, text="Title").pack(
    expand=True, fill="both", padx=2, pady=10
)
entry_title = ctk.CTkEntry(animated_panel, textvariable=var_title).pack(
    expand=True, fill="both", padx=35, pady=10
)

label_category = ctk.CTkLabel(animated_panel, text="Category").pack(
    expand=True, fill="both", padx=2, pady=10
)
entry_category = ctk.CTkEntry(animated_panel, textvariable=var_category).pack(
    expand=True, fill="both", padx=35, pady=10
)
label_developer = ctk.CTkLabel(animated_panel, text="Developer").pack(
    expand=True, fill="both", padx=2, pady=10
)
entry_developer = ctk.CTkEntry(animated_panel, textvariable=var_developer).pack(
    expand=True, fill="both", padx=35, pady=10
)

label_price = ctk.CTkLabel(animated_panel, text="Price").pack(
    expand=True, fill="both", padx=2, pady=10
)
entry_price = ctk.CTkEntry(animated_panel, textvariable=var_price).pack(
    expand=True, fill="both", padx=35, pady=10
)

# textbox
label_description = ctk.CTkLabel(animated_panel, text="Description").pack(
    expand=True, fill="both", padx=2, pady=10
)
textbox = ctk.CTkTextbox(animated_panel)
textbox.pack(expand=True, fill="both", padx=35, pady=10)


# buttons
load = ctk.CTkButton(
    animated_panel,
    text="Load",
    font=("Arial", 20),
    corner_radius=5,
    width=180,
    height=40,
    command=lambda: load_data(
        var_title, var_category, var_developer, var_price, textbox
    ),
).pack(expand=True, fill="y", pady=10)
modify = ctk.CTkButton(
    animated_panel,
    text="Modify",
    font=("Arial", 20),
    corner_radius=5,
    width=180,
    height=40,
).pack(expand=True, fill="y", pady=10)
deleted = ctk.CTkButton(
    animated_panel,
    text="Deleted",
    font=("Arial", 20),
    corner_radius=5,
    width=180,
    height=40,
    command=animated_panel.animate,
).pack(expand=True, fill="y", pady=10)
clean = ctk.CTkButton(
    animated_panel,
    text="Clean",
    font=("Arial", 20),
    corner_radius=5,
    width=180,
    height=40,
    command=animated_panel.animate,
).pack(expand=True, fill="y", pady=10)

# window elements

# buttons
button = ctk.CTkButton(
    window,
    text="button",
    font=("Arial", 20),
    corner_radius=5,
    width=180,
    height=40,
)
button.place(relx=0.14, rely=0.03, anchor="center")

toogle = ctk.CTkButton(
    window,
    text="toogle",
    font=("Arial", 30),
    width=210,
    height=70,
    command=animated_panel.animate,
)
toogle.place(relx=0.5, rely=0.91, anchor="center")

theme_color = ctk.CTkButton(
    window,
    text=emoji,
    font=emoji_font,
    corner_radius=5,
    width=40,
    height=40,
    command=lambda: change_color(theme_color),
)
theme_color.place(relx=0.90, rely=0.03, anchor="center")

# imputs
search = ctk.CTkEntry(window, textvariable=var_search, width=180, height=40)
search.place(relx=0.75, rely=0.03, anchor="center")

# style treeview
style = ttk.Style()

# pick a theme
style.theme_use("clam")

# comfigure our treeview colors
style.configure(
    "Treeview", background="#dbdbdb", foreground="#3d3d3d", fieldbackground="#dbdbdb"
)

# change selected color
style.map("Treeview", background=[("selected", "green")])

# treeview
tree = ttk.Treeview(window)
tree["columns"] = ("title", "category", "developer", "price", "description")
tree.column("#0", width=0, minwidth=0)
tree.column("title", width=100, minwidth=100)
tree.column("category", width=100, minwidth=100)
tree.column("developer", width=100, minwidth=100)
tree.column("price", width=100, minwidth=100)
tree.column("description", width=300, minwidth=300)

# background=("selected", "#3d3d3d")
# foreground=("selected", "#dbdbdb")

tree.heading("#0", text="")
tree.heading("title", text="Title")
tree.heading("category", text="Category")
tree.heading("developer", text="Developer")
tree.heading("price", text="Price")
tree.heading("description", text="Description")
tree.place(relx=0.027, rely=0.08, relwidth=0.9, relheight=0.75)

animated_panel.lift()

connect()

window.mainloop()
