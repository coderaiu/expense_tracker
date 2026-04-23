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

#main
# окно
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x450")

# ввод
tk.Label(root, text="Description").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

# категории
tk.Label(root, text="Category").pack()
category_var = tk.StringVar()
category_var.set("Food")

categories = ["Food", "Transport", "Shopping", "Other"]
tk.OptionMenu(root, category_var, *categories).pack()

# кнопки
tk.Button(root, text="Add", command=add).pack(pady=5)
tk.Button(root, text="Delete", command=delete).pack(pady=5)

# список
listbox = tk.Listbox(root)
listbox.pack(fill="both", expand=True, pady=10)

# итог
total_label = tk.Label(root, text="Total: $0")
total_label.pack()

# загрузка данных при запуске
load_data()
update_list()

root.mainloop()
