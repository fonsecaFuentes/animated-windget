import re
import customtkinter as ctk
from tkinter import ttk, messagebox
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


def load_data(title, category, developer, price, description, mitreview):
    re_number = r"^\d+(\.\d{1,2})?$"
    re_null = r"^(?!\s*$).+"
    field_empy = False

    data = (
        title.get(),
        category.get(),
        developer.get(),
        price.get(),
        description.get("1.0", "end-1c"),
    )

    for element in data:
        if not re.match(re_null, element):
            field_empy = True
            break
    if field_empy:
        messagebox.showwarning("Validación", "Tienes campos sin completar")

    elif not re.match(re_number, data[3]):
        messagebox.showwarning("Validación", "El valor en el imputs 'precio' no es válido")

    else:
        connection = create_db()
        cursor = connection.cursor()
        sql = "INSERT INTO data_game (title, category, developer, price, description) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql, data)
        connection.commit()
        update_tree(mitreview)
        messagebox.showinfo("Aviso", "Juego agregado exitosamente.")


def del_item(mitreview):
    value = mitreview.selection()
    if value:
        confirm = messagebox.askyesno(
            "Confirmación",
            "¿Estás seguro de que deseas borrar los datos seleccionados?",
        )
        if confirm:
            for element in value:
                item = mitreview.item(element)
                my_id = item["text"]

                connection = create_db()
                cursor = connection.cursor()
                data = (my_id,)
                sql = "DELETE FROM data_game WHERE id = ?"
                cursor.execute(sql, data)
                connection.commit()
                mitreview.delete(element)
        messagebox.showinfo("Aviso", "datos borrados exitosamente")


def modify_item(title, category, developer, price, description, mitreview):
    value = mitreview.selection()
    if value:
        re_number = r"^\d+(\.\d{1,2})?$"
        re_null = r"^(?!\s*$).+"
        field_empy = False

        re_data = (
            title.get(),
            category.get(),
            developer.get(),
            price.get(),
            description.get("1.0", "end-1c"),
        )

        for element in re_data:
            if not re.match(re_null, element):
                field_empy = True
                break
        if field_empy:
            messagebox.showwarning("Validación", "Tienes campos sin completar")

        elif not re.match(re_number, re_data[3]):
            messagebox.showwarning("Validación", "El valor en el imputs 'precio' no es válido")

        else:
            confirm = messagebox.askyesno(
                "Confirmación",
                "¿Estás seguro de que deseas modificar los datos seleccionados?",
            )
            if confirm:
                item = mitreview.item(value)
                my_id = item['text']

                data = (title.get(),
                        category.get(),
                        developer.get(),
                        price.get(),
                        description.get("1.0", "end-1c"),
                        my_id,
                        )

                connection = create_db()
                cursor = connection.cursor()
                sql = "UPDATE data_game SET title=?, category=?, developer=?, price=?, description=? WHERE id=?"
                cursor.execute(sql, data)
                connection.commit()
                update_tree(mitreview)
                messagebox.showinfo("Aviso", "datos modificados exitosamente")


def clean_fields(title, category, developer, price, description, search, mitreview):
    title.delete(0, "end")
    category.delete(0, "end")
    developer.delete(0, "end")
    price.delete(0, "end")
    description.delete("1.0", "end")
    search.delete(0, "end")
    update_tree(mitreview)


def fun_search(search, mitreview):
    imput_search = search.get()
    connection = create_db()
    cursor = connection.cursor()
    sql = "SELECT title, category, developer, price, description FROM data_game WHERE title=?OR category=? OR developer=?"
    data = cursor.execute(sql, (imput_search, imput_search, imput_search))

    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    result = data.fetchall()
    for file in result:
        mitreview.insert("", "end", values=(file[0], file[1], file[2], file[3], file[4]))


def tree_selected(event):
    value = tree.selection()
    if value:
        for element in value:
            item = tree.item(element)
            value = item['values']

            entry_title.delete(0, "end")
            entry_title.insert(0, value[0])

            entry_category.delete(0, "end")
            entry_category.insert(0, value[1])

            entry_developer.delete(0, "end")
            entry_developer.insert(0, value[2])

            entry_price.delete(0, "end")
            entry_price.insert(0, value[3])

            textbox.delete("1.0", "end")
            textbox.insert("1.0", value[4])


def update_tree(mitreview):
    record = mitreview.get_children()
    for element in record:
        mitreview.delete(element)

    connection = create_db()
    cursor = connection.cursor()
    sql = "SELECT * FROM data_game ORDER BY id ASC"
    data = cursor.execute(sql)

    result = data.fetchall()

    for fila in result:
        mitreview.insert("", "end", text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5]))


def connect(mitreview):
    create_db()
    create_table()
    update_tree(mitreview)


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
window.geometry("600x600")
ctk.set_appearance_mode(appearance_mode)

# animated widget
animated_panel = SlidePanel(window, 0.96, 0.65)

# animated widget

# button toogle_sidebar
toogle_sidebar = ctk.CTkButton(
    animated_panel,
    text="toogle sidebar",
    font=("Arial", 14),
    corner_radius=0,
    command=animated_panel.animate,
).pack(expand=True, fill="both", pady=10)

# label and imputs

entry_title = ctk.CTkEntry(animated_panel, placeholder_text="Title", width=130, height=5)
entry_title.pack(expand=True, fill="y", padx=10, pady=10)

entry_category = ctk.CTkEntry(animated_panel, placeholder_text="Category", width=130, height=5)
entry_category.pack(expand=True, fill="y", padx=10, pady=10)

entry_developer = ctk.CTkEntry(animated_panel, placeholder_text="Developer", width=130, height=5)
entry_developer.pack(expand=True, fill="y", padx=10, pady=10)

entry_price = ctk.CTkEntry(animated_panel, placeholder_text="Price", width=130, height=5)
entry_price.pack(expand=True, fill="y", padx=10, pady=10)

# textbox
label_description = ctk.CTkLabel(animated_panel, text="Description", width=130, height=3).pack(
    padx=1, pady=1)
textbox = ctk.CTkTextbox(animated_panel, width=130, height=5)
textbox.pack(expand=True, fill="y", padx=10, pady=10)


# buttons
load = ctk.CTkButton(
    animated_panel,
    text="Load",
    font=("Arial", 14),
    corner_radius=5,
    width=130,
    height=20,
    command= lambda: load_data(
        entry_title, entry_category, entry_developer, entry_price, textbox, tree
    ),
).pack(expand=True, fill="y", pady=10)
modify = ctk.CTkButton(
    animated_panel,
    text="Modify",
    font=("Arial", 14),
    corner_radius=5,
    width=130,
    height=20,
    command= lambda: modify_item(entry_title, entry_category, entry_developer, entry_price, textbox, tree
    ),
).pack(expand=True, fill="y", pady=10)
deleted = ctk.CTkButton(
    animated_panel,
    text="Deleted",
    font=("Arial", 14),
    corner_radius=5,
    width=130,
    height=20,
    command= lambda: del_item(tree),
).pack(expand=True, fill="y", pady=10)
clean = ctk.CTkButton(
    animated_panel,
    text="Clean",
    font=("Arial", 14),
    corner_radius=5,
    width=130,
    height=20,
    command= lambda: clean_fields(entry_title, entry_category, entry_developer, entry_price, textbox, entry_search, tree
    ),
).pack(expand=True, fill="y", pady=10)

# window elements

# buttons
button = ctk.CTkButton(
    window,
    text="button",
    font=("Arial", 14),
    corner_radius=5,
    width=100,
    height=30,
    command= lambda: fun_search(entry_search, tree)
)
button.place(relx=0.11, rely=0.035, anchor="center")

toogle = ctk.CTkButton(
    window,
    text="toogle",
    font=("Arial", 30),
    width=130,
    height=50,
    command=animated_panel.animate,
)
toogle.place(relx=0.5, rely=0.91, anchor="center")

theme_color = ctk.CTkButton(
    window,
    text=emoji,
    font=emoji_font,
    corner_radius=5,
    width=30,
    height=30,
    command=lambda: change_color(theme_color),
)
theme_color.place(relx=0.90, rely=0.035, anchor="center")

# imputs
entry_search = ctk.CTkEntry(window, placeholder_text="search", width=100, height=30)
entry_search.place(relx=0.78, rely=0.035, anchor="center")

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
tree.bind("<<TreeviewSelect>>", tree_selected)

animated_panel.lift()

connect(tree)

window.mainloop()