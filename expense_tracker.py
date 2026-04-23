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
