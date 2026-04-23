import tkinter as tk
from tkinter import messagebox

FILE = "expenses.txt"

expenses = []

# загрузка из файла
def load_data():
    try:
        with open(FILE, "r") as f:
         for line in f:
            parts = line.strip().split(";")
            if len(parts) == 3:
                desc = parts[0]
                amount = float(parts[1])
                category = parts[2]
                expenses.append([desc, amount, category])
    except FileNotFoundError:
        pass

# сохранение в файл
def save_data():
    with open(FILE, "w") as f:
        for item in expenses:
            line = f"{item[0]};{item[1]};{item[2]}\n"
            f.write(line)

def update_list():
    listbox.delete(0, tk.END)
    total = 0

    for item in expenses:
        text = f"{item[0]} | {item[2]} | ${item[1]}"
        listbox.insert(tk.END, text)
        total += item[1]

    total_label.config(text=f"Total: ${total}")

def add():
    desc = desc_entry.get()
    amount = amount_entry.get()
    category = category_var.get()

    if desc == "" or amount == "":
        messagebox.showerror("Error", "Fill all fields")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Amount must be a number")
        return

    expenses.append([desc, amount, category])

    save_data()

    desc_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    update_list()

def delete():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select item")
        return

    index = selected[0]
    del expenses[index]

    save_data()
    update_list()
