import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os
from datetime import datetime, date
import json

# ── matplotlib ────────────────────────────────────────────────────────────────
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ══════════════════════════════════════════════════════════════════════════════
#  THEME
# ══════════════════════════════════════════════════════════════════════════════
BG_DARK    = "#1a1a2e"
BG_PANEL   = "#16213e"
BG_INPUT   = "#0f3460"
ACCENT     = "#e94560"
BLUE       = "#7ecef5"
PURPLE     = "#c778dd"
GREEN      = "#27c93f"
YELLOW     = "#ffc107"
ORANGE     = "#ff9f43"
PINK       = "#fd79a8"
TEXT_MAIN  = "#eeeeee"
TEXT_DIM   = "#a8a8b3"
FONT_MAIN  = ("Courier New", 11)
FONT_BOLD  = ("Courier New", 11, "bold")
FONT_SMALL = ("Courier New", 9)
FONT_BIG   = ("Courier New", 18, "bold")

CAT_COLORS = [ACCENT, BLUE, PURPLE, GREEN, YELLOW, ORANGE, PINK, "#a29bfe", "#55efc4"]

DATA_FILE   = "expenses.csv"
CONFIG_FILE = "config.json"

DEFAULT_CATEGORIES = [
    "🍕 Food & Drinks",
    "🚌 Transport",
    "🎮 Entertainment",
    "🏥 Health",
    "📚 Education",
    "🏠 Housing",
    "👗 Shopping",
]

# ══════════════════════════════════════════════════════════════════════════════
#  DATA LAYER
# ══════════════════════════════════════════════════════════════════════════════

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"budget": 0, "categories": DEFAULT_CATEGORIES[:]}

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def load_expenses():
    expenses = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["amount"] = float(row["amount"])
                expenses.append(row)
    return expenses

def save_all_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["description", "amount", "category", "date"])
        writer.writeheader()
        writer.writerows(expenses)

def append_expense(description, amount, category, date_str):
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["description", "amount", "category", "date"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"description": description, "amount": amount,
                         "category": category, "date": date_str})

def totals_by_category(expenses):
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return totals

def totals_by_date(expenses):
    totals = {}
    for e in expenses:
        totals[e["date"]] = totals.get(e["date"], 0) + e["amount"]
    return dict(sorted(totals.items()))

def smart_tip(expenses):
    """Generate one actionable money tip based on data."""
    if not expenses:
        return "💡 Add your first expense to get personalized tips!"
    totals  = totals_by_category(expenses)
    top_cat = max(totals, key=totals.get)
    top_val = totals[top_cat]
    total   = sum(totals.values())
    pct     = int(top_val / total * 100)
    name    = top_cat.split(" ", 1)[-1] if " " in top_cat else top_cat

    if pct > 60:
        return f"💡 {pct}% of your money goes to {name}. Could you cut it by 10%?"
    elif len(totals) < 3:
        return f"💡 You have {len(totals)} categories — tracking more = saving more!"
    else:
        return f"💡 Your top category is {name} (₸{top_val:,.0f}). Try setting a sub-budget!"

# ══════════════════════════════════════════════════════════════════════════════
#  EDIT DIALOG
# ══════════════════════════════════════════════════════════════════════════════

class EditDialog(tk.Toplevel):
    def __init__(self, parent, expense, categories, on_save):
        super().__init__(parent)
        self.title("✏  Edit Expense")
        self.configure(bg=BG_PANEL)
        self.resizable(False, False)
        self.grab_set()
        self.on_save = on_save

        tk.Label(self, text="EDIT EXPENSE", bg=BG_PANEL,
                 fg=ACCENT, font=FONT_SMALL).pack(anchor="w", padx=20, pady=(16, 6))

        fields = [("Description", "description"), ("Amount (₸)", "amount"),
                  ("Date (YYYY-MM-DD)", "date")]
        self._entries = {}
        for lbl, key in fields:
            tk.Label(self, text=lbl, bg=BG_PANEL, fg=TEXT_DIM,
                     font=FONT_SMALL).pack(anchor="w", padx=20, pady=(6, 1))
            e = tk.Entry(self, bg=BG_INPUT, fg=TEXT_MAIN,
                         insertbackground=TEXT_MAIN, relief="flat",
                         font=FONT_MAIN, highlightthickness=1,
                         highlightcolor=ACCENT, highlightbackground=BG_INPUT, width=34)
            e.insert(0, str(expense[key]))
            e.pack(fill="x", padx=20, pady=2, ipady=5)
            self._entries[key] = e

        tk.Label(self, text="Category", bg=BG_PANEL, fg=TEXT_DIM,
                 font=FONT_SMALL).pack(anchor="w", padx=20, pady=(6, 1))
        self.cat_var = tk.StringVar(value=expense["category"])
        ttk.Combobox(self, textvariable=self.cat_var, values=categories,
                     font=FONT_MAIN, state="readonly",
                     width=32).pack(fill="x", padx=20, pady=2)

        bf = tk.Frame(self, bg=BG_PANEL)
        bf.pack(fill="x", padx=20, pady=(14, 16))
        tk.Button(bf, text="💾 Save", bg=ACCENT, fg="white", font=FONT_BOLD,
                  relief="flat", cursor="hand2",
                  command=self._save).pack(side="left", fill="x", expand=True, ipady=6)
        tk.Button(bf, text="Cancel", bg=BG_INPUT, fg=TEXT_DIM, font=FONT_MAIN,
                  relief="flat", cursor="hand2",
                  command=self.destroy).pack(side="left", fill="x",
                                              expand=True, ipady=6, padx=(8, 0))

    def _save(self):
        desc   = self._entries["description"].get().strip()
        amount = self._entries["amount"].get().strip()
        date_s = self._entries["date"].get().strip()
        cat    = self.cat_var.get()
        if not desc:
            messagebox.showwarning("Missing", "Description required.", parent=self); return
        try:
            amount = float(amount.replace(" ", "").replace(",", "."))
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid", "Enter a valid amount.", parent=self); return
        try:
            datetime.strptime(date_s, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid", "Use YYYY-MM-DD format.", parent=self); return
        self.on_save({"description": desc, "amount": amount, "category": cat, "date": date_s})
        self.destroy()

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════════════════════

class ExpenseTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💸 Expense Tracker v2.0")
        self.geometry("1140x740")
        self.minsize(960, 640)
        self.configure(bg=BG_DARK)

        self.config_data   = load_config()
        self.expenses      = load_expenses()
        self._filter_month = tk.StringVar(value="All")
        self._search_var   = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh_history_table())

        self._build_titlebar()
        self._build_main()
        self.refresh_all()
        self.after(150, self._animate_stats)

    # ══════════════════════════════════════════════════════════════════════════
    #  TITLEBAR
    # ══════════════════════════════════════════════════════════════════════════
    def _build_titlebar(self):
        bar = tk.Frame(self, bg=BG_PANEL, height=40)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        for color in ("#ff5f56", "#ffbd2e", "#27c93f"):
            tk.Canvas(bar, bg=color, width=12, height=12,
                      highlightthickness=0).pack(side="left", padx=(10, 2), pady=14)

        tk.Label(bar, text="💸  Expense Tracker v2.0",
                 bg=BG_PANEL, fg=ACCENT, font=FONT_BOLD).pack(side="left", padx=12)

        # Month filter in titlebar
        tk.Label(bar, text="Month:", bg=BG_PANEL,
                 fg=TEXT_DIM, font=FONT_SMALL).pack(side="left", padx=(20, 4))
        months = ["All"] + [f"{y}-{m:02d}"
                             for y in range(date.today().year - 1, date.today().year + 1)
                             for m in range(1, 13)]
        self._month_combo = ttk.Combobox(bar, textvariable=self._filter_month,
                                          values=months, font=FONT_SMALL,
                                          state="readonly", width=10)
        self._month_combo.pack(side="left")
        self._month_combo.bind("<<ComboboxSelected>>", lambda _: self.refresh_all())

        tk.Label(bar, text=datetime.now().strftime("  %A, %d %B %Y"),
                 bg=BG_PANEL, fg=TEXT_DIM, font=FONT_SMALL).pack(side="right", padx=12)

    # ══════════════════════════════════════════════════════════════════════════
    #  LAYOUT
    # ══════════════════════════════════════════════════════════════════════════
    def _build_main(self):
        main = tk.Frame(self, bg=BG_DARK)
        main.pack(fill="both", expand=True)

        left = tk.Frame(main, bg=BG_PANEL, width=390)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        right = tk.Frame(main, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)

        self._build_left(left)
        self._build_right(right)

    # ══════════════════════════════════════════════════════════════════════════
    #  LEFT PANEL
    # ══════════════════════════════════════════════════════════════════════════
    def _build_left(self, parent):
        # Plain scrollable frame — use a tk.Frame directly inside a canvas
        # so the combobox arrow is never clipped by a nested window boundary.
        outer = tk.Frame(parent, bg=BG_PANEL)
        outer.pack(fill="both", expand=True)

        p = outer

        # ── ADD EXPENSE ───────────────────────────────────────────────────────
        self._section(p, "ADD EXPENSE")
        self._lbl(p, "Description")
        self.entry_desc = self._entry(p)

        self._lbl(p, "Amount (₸)")
        self.entry_amount = self._entry(p)

        self._lbl(p, "Category")
        self.cat_var = tk.StringVar()
        self._style_combobox()   # style first, then create widget
        self.cat_combo = ttk.Combobox(p, textvariable=self.cat_var,
                                       font=FONT_MAIN, state="readonly", width=30)
        self.cat_combo.pack(fill="x", padx=16, pady=4, ipadx=2, ipady=4)
        self._refresh_categories()
        self.cat_combo.bind("<<ComboboxSelected>>", self._on_cat_selected)

        self._lbl(p, "Date (YYYY-MM-DD)")
        self.entry_date = self._entry(p)
        self.entry_date.insert(0, datetime.today().strftime("%Y-%m-%d"))

        bf = tk.Frame(p, bg=BG_PANEL)
        bf.pack(fill="x", padx=16, pady=(10, 4))
        tk.Button(bf, text="＋ Add Expense", bg=ACCENT, fg="white",
                  font=FONT_BOLD, relief="flat", cursor="hand2",
                  command=self._add_expense).pack(side="left", fill="x", expand=True, ipady=7)
        tk.Button(bf, text="📤 Export CSV", bg=BG_INPUT, fg=BLUE,
                  font=FONT_MAIN, relief="flat", cursor="hand2",
                  command=self._export_csv).pack(side="left", fill="x",
                                                  expand=True, ipady=7, padx=(6, 0))

        # ── BUDGET ────────────────────────────────────────────────────────────
        tk.Frame(p, bg=BG_INPUT, height=1).pack(fill="x", padx=16, pady=(16, 8))
        self._section(p, "MONTHLY BUDGET")
        self._lbl(p, "Budget Limit (₸)")
        self.entry_budget = self._entry(p)
        bv = self.config_data.get("budget", 0)
        self.entry_budget.insert(0, str(int(bv)) if bv else "")

        tk.Button(p, text="Set Budget", bg=BG_INPUT, fg=YELLOW,
                  font=FONT_MAIN, relief="flat", cursor="hand2",
                  command=self._set_budget).pack(fill="x", padx=16, pady=(6, 4), ipady=5)

        self.budget_canvas = tk.Canvas(p, bg=BG_PANEL, height=16, highlightthickness=0)
        self.budget_canvas.pack(fill="x", padx=16, pady=(4, 0))

        self.budget_info_var = tk.StringVar(value="Set a budget to track spending")
        tk.Label(p, textvariable=self.budget_info_var, bg=BG_PANEL,
                 fg=TEXT_DIM, font=FONT_SMALL).pack(anchor="w", padx=16)

        self.budget_warn_var = tk.StringVar()
        tk.Label(p, textvariable=self.budget_warn_var, bg=BG_PANEL,
                 fg=YELLOW, font=FONT_SMALL).pack(anchor="w", padx=16, pady=(2, 8))

        # ── SMART TIP ─────────────────────────────────────────────────────────
        tk.Frame(p, bg=BG_INPUT, height=1).pack(fill="x", padx=16, pady=(8, 8))
        self._section(p, "SMART TIP")
        self.tip_var = tk.StringVar()
        tk.Label(p, textvariable=self.tip_var, bg=BG_PANEL,
                 fg=BLUE, font=FONT_SMALL,
                 wraplength=310, justify="left").pack(anchor="w", padx=16, pady=(0, 16))

    # ══════════════════════════════════════════════════════════════════════════
    #  RIGHT PANEL  (tabs)
    # ══════════════════════════════════════════════════════════════════════════
    def _build_right(self, parent):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Dark.TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("Dark.TNotebook.Tab",
                        background=BG_INPUT, foreground=TEXT_DIM,
                        font=FONT_MAIN, padding=[14, 6], borderwidth=0)
        style.map("Dark.TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])

        nb = ttk.Notebook(parent, style="Dark.TNotebook")
        nb.pack(fill="both", expand=True, padx=8, pady=8)

        self.tab_dash    = tk.Frame(nb, bg=BG_DARK)
        self.tab_history = tk.Frame(nb, bg=BG_DARK)
        self.tab_charts  = tk.Frame(nb, bg=BG_DARK)

        nb.add(self.tab_dash,    text="📊  Dashboard")
        nb.add(self.tab_history, text="📋  History")
        nb.add(self.tab_charts,  text="📈  Charts")

        self._build_dashboard(self.tab_dash)
        self._build_history(self.tab_history)
        self._build_charts(self.tab_charts)

    # ── DASHBOARD ─────────────────────────────────────────────────────────────
    def _build_dashboard(self, parent):
        # Stat cards
        cards_f = tk.Frame(parent, bg=BG_DARK)
        cards_f.pack(fill="x", padx=10, pady=(12, 6))

        self.stat_vars = {}
        for key, label, default, color in [
            ("total_spent",  "Total Spent",    "₸0", ACCENT),
            ("transactions", "Transactions",   "0",  BLUE),
            ("avg_per_day",  "Avg / Day",      "₸0", PURPLE),
            ("biggest",      "Biggest Single", "₸0", YELLOW),
        ]:
            card = tk.Frame(cards_f, bg=BG_PANEL)
            card.pack(side="left", fill="x", expand=True, padx=4)
            var = tk.StringVar(value=default)
            self.stat_vars[key] = var
            tk.Label(card, textvariable=var, bg=BG_PANEL,
                     fg=color, font=FONT_BIG).pack(pady=(12, 0))
            tk.Label(card, text=label, bg=BG_PANEL,
                     fg=TEXT_DIM, font=FONT_SMALL).pack(pady=(0, 12))

        # Two-column mid: category bars + top 3
        mid = tk.Frame(parent, bg=BG_DARK)
        mid.pack(fill="both", expand=True, padx=10)

        left_mid = tk.Frame(mid, bg=BG_DARK)
        left_mid.pack(side="left", fill="both", expand=True)

        right_mid = tk.Frame(mid, bg=BG_DARK, width=230)
        right_mid.pack(side="left", fill="y", padx=(8, 0))
        right_mid.pack_propagate(False)

        tk.Label(left_mid, text="BY CATEGORY", bg=BG_DARK,
                 fg=ACCENT, font=FONT_SMALL).pack(anchor="w", padx=4, pady=(10, 2))
        self.cat_frame = tk.Frame(left_mid, bg=BG_DARK)
        self.cat_frame.pack(fill="x")

        tk.Label(right_mid, text="🏆 TOP 3 BIGGEST", bg=BG_DARK,
                 fg=ACCENT, font=FONT_SMALL).pack(anchor="w", padx=4, pady=(10, 2))
        self.top3_frame = tk.Frame(right_mid, bg=BG_DARK)
        self.top3_frame.pack(fill="x")

    # ── HISTORY ───────────────────────────────────────────────────────────────
    def _build_history(self, parent):
        # Search bar
        sf = tk.Frame(parent, bg=BG_DARK)
        sf.pack(fill="x", padx=14, pady=(10, 4))
        tk.Label(sf, text="🔍", bg=BG_DARK, fg=TEXT_DIM,
                 font=FONT_MAIN).pack(side="left", padx=(0, 6))
        se = tk.Entry(sf, textvariable=self._search_var,
                      bg=BG_INPUT, fg=TEXT_MAIN,
                      insertbackground=TEXT_MAIN, relief="flat",
                      font=FONT_MAIN, highlightthickness=1,
                      highlightcolor=ACCENT, highlightbackground=BG_INPUT)
        se.pack(side="left", fill="x", expand=True, ipady=5)
        se.insert(0, "")
        tk.Button(sf, text="✕", bg=BG_INPUT, fg=TEXT_DIM,
                  font=FONT_SMALL, relief="flat", cursor="hand2",
                  command=lambda: self._search_var.set("")).pack(
                  side="left", padx=(4, 0), ipady=5, ipadx=6)

        # Treeview
        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background=BG_PANEL, foreground=TEXT_MAIN,
                        fieldbackground=BG_PANEL, rowheight=28,
                        font=FONT_MAIN, borderwidth=0)
        style.configure("Dark.Treeview.Heading",
                        background=BG_INPUT, foreground=ACCENT,
                        font=FONT_SMALL, relief="flat")
        style.map("Dark.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])

        cols = ("#", "Description", "Amount", "Category", "Date")
        self.tree = ttk.Treeview(parent, columns=cols, show="headings",
                                  style="Dark.Treeview", selectmode="browse")
        self.tree.pack(fill="both", expand=True, padx=14, pady=(0, 4))

        for col, w in zip(cols, [40, 220, 110, 180, 100]):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=w, anchor="w")

        # Color tags per category
        for i, color in enumerate(CAT_COLORS):
            self.tree.tag_configure(f"cat{i}", foreground=color)

        self.tree.bind("<Double-1>", lambda e: self._edit_selected())

        bf = tk.Frame(parent, bg=BG_DARK)
        bf.pack(fill="x", padx=14, pady=(0, 4))
        tk.Button(bf, text="✏  Edit (or double-click)", bg=BG_INPUT, fg=BLUE,
                  font=FONT_MAIN, relief="flat", cursor="hand2",
                  command=self._edit_selected).pack(side="left", fill="x",
                                                     expand=True, ipady=6)
        tk.Button(bf, text="🗑  Delete Selected", bg=BG_INPUT, fg=ACCENT,
                  font=FONT_MAIN, relief="flat", cursor="hand2",
                  command=self._delete_selected).pack(side="left", fill="x",
                                                       expand=True, ipady=6, padx=(6, 0))

        self.history_count_var = tk.StringVar(value="")
        tk.Label(parent, textvariable=self.history_count_var,
                 bg=BG_DARK, fg=TEXT_DIM, font=FONT_SMALL).pack(anchor="e", padx=14)

    # ── CHARTS ────────────────────────────────────────────────────────────────
    def _build_charts(self, parent):
        if not MATPLOTLIB_AVAILABLE:
            tk.Label(parent,
                     text="⚠  matplotlib not installed.\nRun:  pip install matplotlib",
                     bg=BG_DARK, fg=YELLOW, font=FONT_MAIN,
                     justify="center").pack(expand=True)
            self.chart_parent = None
            return
        self.chart_parent = parent
        self.chart_frame  = tk.Frame(parent, bg=BG_DARK)
        self.chart_frame.pack(fill="both", expand=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  ACTIONS
    # ══════════════════════════════════════════════════════════════════════════

    def _filtered(self):
        month = self._filter_month.get()
        if month == "All":
            return self.expenses[:]
        return [e for e in self.expenses if e["date"].startswith(month)]

    def _add_expense(self):
        desc   = self.entry_desc.get().strip()
        amount = self.entry_amount.get().strip()
        cat    = self.cat_var.get().strip()
        date_s = self.entry_date.get().strip()

        if not desc:
            messagebox.showwarning("Missing", "Please enter a description."); return
        try:
            amount = float(amount.replace(" ", "").replace(",", "."))
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid", "Enter a valid positive number."); return
        if not cat or cat == "➕ Add New Category":
            messagebox.showwarning("Missing", "Please select a category."); return
        try:
            datetime.strptime(date_s, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid date", "Use format YYYY-MM-DD."); return

        append_expense(desc, amount, cat, date_s)
        self.expenses = load_expenses()
        self.entry_desc.delete(0, "end")
        self.entry_amount.delete(0, "end")
        self.refresh_all()
        self._check_budget()

    def _on_cat_selected(self, event):
        if self.cat_var.get() == "➕ Add New Category":
            new_cat = simpledialog.askstring(
                "New Category",
                "Enter category name (you can add an emoji first!):",
                parent=self)
            if new_cat and new_cat.strip():
                new_cat = new_cat.strip()
                if new_cat not in self.config_data["categories"]:
                    self.config_data["categories"].append(new_cat)
                    save_config(self.config_data)
                self._refresh_categories()
                self.cat_var.set(new_cat)
            else:
                self.cat_var.set(self.config_data["categories"][0])

    def _set_budget(self):
        val = self.entry_budget.get().strip()
        try:
            budget = float(val.replace(" ", "").replace(",", "."))
        except ValueError:
            messagebox.showwarning("Invalid", "Enter a valid budget amount."); return
        self.config_data["budget"] = budget
        save_config(self.config_data)
        self.refresh_all()
        messagebox.showinfo("Budget Set ✅", f"Monthly budget set to ₸{budget:,.0f}")

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select row", "Click a row first."); return
        idx = int(self.tree.item(sel[0], "values")[0]) - 1
        if messagebox.askyesno("Delete", "Delete this expense?"):
            self.expenses.pop(idx)
            save_all_expenses(self.expenses)
            self.refresh_all()

    def _edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select row", "Click a row first."); return
        idx     = int(self.tree.item(sel[0], "values")[0]) - 1
        expense = self.expenses[idx]

        def on_save(updated):
            self.expenses[idx] = updated
            save_all_expenses(self.expenses)
            self.refresh_all()

        EditDialog(self, expense, self.config_data["categories"], on_save)

    def _export_csv(self):
        if not self.expenses:
            messagebox.showinfo("Empty", "No expenses to export."); return
        name = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(name, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["description", "amount", "category", "date"])
            writer.writeheader()
            writer.writerows(self.expenses)
        messagebox.showinfo("Exported ✅", f"Saved as:\n{name}")

    # ══════════════════════════════════════════════════════════════════════════
    #  REFRESH
    # ══════════════════════════════════════════════════════════════════════════

    def refresh_all(self):
        filtered = self._filtered()
        self._refresh_stats(filtered)
        self._refresh_category_bars(filtered)
        self._refresh_top3(filtered)
        self._refresh_history_table()
        self._refresh_charts(filtered)
        self._refresh_budget_bar(filtered)
        self.tip_var.set(smart_tip(filtered))

    def _refresh_stats(self, filtered):
        total   = sum(e["amount"] for e in filtered)
        count   = len(filtered)
        dates   = set(e["date"] for e in filtered)
        avg     = total / len(dates) if dates else 0
        biggest = max((e["amount"] for e in filtered), default=0)

        self.stat_vars["total_spent"].set(f"₸{total:,.0f}")
        self.stat_vars["transactions"].set(str(count))
        self.stat_vars["avg_per_day"].set(f"₸{avg:,.0f}")
        self.stat_vars["biggest"].set(f"₸{biggest:,.0f}")

    def _refresh_category_bars(self, filtered):
        for w in self.cat_frame.winfo_children():
            w.destroy()

        totals = totals_by_category(filtered)
        if not totals:
            tk.Label(self.cat_frame, text="No expenses yet.",
                     bg=BG_DARK, fg=TEXT_DIM, font=FONT_MAIN).pack()
            return

        max_val   = max(totals.values())
        grand_tot = sum(totals.values())

        for i, (cat, val) in enumerate(sorted(totals.items(), key=lambda x: -x[1])):
            color = CAT_COLORS[i % len(CAT_COLORS)]
            row = tk.Frame(self.cat_frame, bg=BG_DARK)
            row.pack(fill="x", pady=3)

            tk.Label(row, text=cat, bg=BG_DARK, fg=TEXT_MAIN,
                     font=FONT_SMALL, width=22, anchor="w").pack(side="left")

            bar_bg = tk.Frame(row, bg=BG_INPUT, height=8)
            bar_bg.pack(side="left", fill="x", expand=True, padx=8)
            bar_bg.pack_propagate(False)

            pct      = val / max_val
            bar_fill = tk.Frame(bar_bg, bg=color, height=8)
            bar_bg.bind("<Configure>",
                        lambda e, bf=bar_fill, p=pct:
                        bf.place(x=0, y=0, relwidth=p, relheight=1))

            share = f"{int(val / grand_tot * 100)}%"
            tk.Label(row, text=f"₸{val:,.0f} {share}", bg=BG_DARK,
                     fg=color, font=FONT_SMALL, width=16, anchor="e").pack(side="left")

    def _refresh_top3(self, filtered):
        for w in self.top3_frame.winfo_children():
            w.destroy()
        if not filtered:
            return
        top3   = sorted(filtered, key=lambda x: -x["amount"])[:3]
        medals = ["🥇", "🥈", "🥉"]
        for i, e in enumerate(top3):
            card = tk.Frame(self.top3_frame, bg=BG_PANEL)
            card.pack(fill="x", pady=4)
            tk.Label(card, text=medals[i], bg=BG_PANEL,
                     font=("Courier New", 14)).pack(side="left", padx=8, pady=6)
            info = tk.Frame(card, bg=BG_PANEL)
            info.pack(side="left", fill="x", expand=True, pady=6)
            tk.Label(info, text=e["description"][:22], bg=BG_PANEL,
                     fg=TEXT_MAIN, font=FONT_SMALL, anchor="w").pack(anchor="w")
            tk.Label(info, text=e["category"], bg=BG_PANEL,
                     fg=TEXT_DIM, font=FONT_SMALL, anchor="w").pack(anchor="w")
            tk.Label(card, text=f"₸{e['amount']:,.0f}", bg=BG_PANEL,
                     fg=ACCENT, font=FONT_BOLD).pack(side="right", padx=10)

    def _refresh_history_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query    = self._search_var.get().strip().lower()
        month    = self._filter_month.get()
        cat_idx  = {cat: i for i, cat in enumerate(self.config_data["categories"])}
        shown    = 0

        for idx, e in enumerate(reversed(self.expenses)):
            row_num = len(self.expenses) - idx
            if month != "All" and not e["date"].startswith(month):
                continue
            if query and query not in e["description"].lower() \
               and query not in e["category"].lower():
                continue
            tag = f"cat{cat_idx.get(e['category'], 0) % len(CAT_COLORS)}"
            self.tree.insert("", "end", tags=(tag,), values=(
                row_num,
                e["description"],
                f"₸{e['amount']:,.0f}",
                e["category"],
                e["date"],
            ))
            shown += 1

        self.history_count_var.set(
            f"Showing {shown} of {len(self.expenses)} expenses")

    def _refresh_charts(self, filtered):
        if not MATPLOTLIB_AVAILABLE or not self.chart_parent:
            return
        for w in self.chart_frame.winfo_children():
            w.destroy()
        if not filtered:
            tk.Label(self.chart_frame, text="Add expenses to see charts.",
                     bg=BG_DARK, fg=TEXT_DIM, font=FONT_MAIN).pack(expand=True)
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4),
                                        facecolor=BG_DARK)

        # ── Pie chart ──────────────────────────────────────────────────────────
        totals = totals_by_category(filtered)
        ax1.set_facecolor(BG_DARK)
        wedges, texts, autotexts = ax1.pie(
            list(totals.values()),
            labels=list(totals.keys()),
            colors=CAT_COLORS[:len(totals)],
            autopct="%1.1f%%",
            startangle=140,
            wedgeprops={"linewidth": 2, "edgecolor": BG_DARK},
            textprops={"color": TEXT_MAIN, "fontsize": 7},
        )
        for at in autotexts:
            at.set_color(BG_DARK); at.set_fontweight("bold"); at.set_fontsize(7)
        ax1.set_title("By Category", color=ACCENT, fontsize=10, pad=8)

        # ── Line / bar chart by day ────────────────────────────────────────────
        by_date = totals_by_date(filtered)
        ax2.set_facecolor(BG_DARK)
        for spine in ax2.spines.values():
            spine.set_color(BG_INPUT)
        ax2.tick_params(colors=TEXT_DIM, labelsize=7)

        if len(by_date) >= 2:
            dates_list = list(by_date.keys())
            amounts    = list(by_date.values())
            ax2.plot(dates_list, amounts, color=ACCENT,
                     linewidth=2, marker="o", markersize=5,
                     markerfacecolor=YELLOW)
            ax2.fill_between(dates_list, amounts, alpha=0.12, color=ACCENT)
            plt.setp(ax2.xaxis.get_majorticklabels(),
                     rotation=38, ha="right", fontsize=6)
        elif len(by_date) == 1:
            d, v = list(by_date.items())[0]
            ax2.bar([d], [v], color=ACCENT, width=0.4)
        ax2.set_title("Spending Over Time", color=ACCENT, fontsize=10, pad=8)
        ax2.set_xlabel("Date", color=TEXT_DIM, fontsize=7)
        ax2.set_ylabel("Amount (₸)", color=TEXT_DIM, fontsize=7)
        ax2.grid(True, alpha=0.1, color=TEXT_DIM)

        fig.tight_layout(pad=1.5)
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def _refresh_budget_bar(self, filtered):
        budget = self.config_data.get("budget", 0)
        total  = sum(e["amount"] for e in filtered)
        self.budget_canvas.delete("all")
        w = self.budget_canvas.winfo_width() or 330
        self.budget_canvas.create_rectangle(0, 4, w, 12, fill=BG_INPUT, outline="")
        if budget > 0:
            pct   = min(total / budget, 1.0)
            color = ACCENT if pct >= 1.0 else (YELLOW if pct >= 0.8 else GREEN)
            fill_w = max(int(w * pct), 4)
            self.budget_canvas.create_rectangle(0, 4, fill_w, 12, fill=color, outline="")
            self.budget_info_var.set(
                f"Spent: ₸{total:,.0f}   |   Left: ₸{max(budget - total, 0):,.0f}")
            pct_int = int(pct * 100)
            if pct >= 1.0:
                self.budget_warn_var.set("🚨 Budget exceeded!")
            elif pct >= 0.8:
                self.budget_warn_var.set(f"⚠  {pct_int}% used — getting close!")
            else:
                self.budget_warn_var.set(f"✅  {pct_int}% of budget used")
        else:
            self.budget_info_var.set(f"Total spent: ₸{total:,.0f}")
            self.budget_warn_var.set("")

    def _check_budget(self):
        budget = self.config_data.get("budget", 0)
        if budget <= 0: return
        total = sum(e["amount"] for e in self._filtered())
        if total > budget:
            messagebox.showwarning("🚨 Budget Exceeded!",
                f"You spent ₸{total:,.0f} — over your ₸{budget:,.0f} budget!")
        elif total >= budget * 0.8:
            messagebox.showwarning("⚠ Budget Warning",
                f"You've used {int(total/budget*100)}% of your budget.\n"
                f"Only ₸{budget - total:,.0f} left!")

    def _animate_stats(self):
        """Count-up animation for Total Spent on startup."""
        filtered = self._filtered()
        target   = sum(e["amount"] for e in filtered)
        steps    = 15
        for i in range(steps + 1):
            val = int(target * (i / steps))
            self.stat_vars["total_spent"].set(f"₸{val:,.0f}")
            self.update_idletasks()
        self._refresh_stats(filtered)

    # ══════════════════════════════════════════════════════════════════════════
    #  HELPERS
    # ══════════════════════════════════════════════════════════════════════════

    def _section(self, parent, text):
        tk.Label(parent, text=text, bg=BG_PANEL,
                 fg=ACCENT, font=FONT_SMALL).pack(anchor="w", padx=16, pady=(10, 2))

    def _lbl(self, parent, text):
        tk.Label(parent, text=text, bg=BG_PANEL,
                 fg=TEXT_DIM, font=FONT_SMALL).pack(anchor="w", padx=16, pady=(6, 1))

    def _entry(self, parent):
        e = tk.Entry(parent, bg=BG_INPUT, fg=TEXT_MAIN,
                     insertbackground=TEXT_MAIN, relief="flat",
                     font=FONT_MAIN, highlightthickness=1,
                     highlightcolor=ACCENT, highlightbackground=BG_INPUT)
        e.pack(fill="x", padx=16, pady=2, ipady=6)
        return e

    def _style_combobox(self):
        s = ttk.Style()
        s.configure("TCombobox",
                    fieldbackground=BG_INPUT, background=BG_INPUT,
                    foreground=TEXT_MAIN, arrowcolor=TEXT_MAIN,
                    selectbackground=BG_INPUT, selectforeground=TEXT_MAIN,
                    insertcolor=TEXT_MAIN,
                    bordercolor=ACCENT, lightcolor=BG_INPUT,
                    darkcolor=BG_INPUT, relief="flat",
                    font=FONT_MAIN, padding=6)
        s.map("TCombobox",
              fieldbackground=[("readonly", BG_INPUT),
                                ("active",   BG_INPUT),
                                ("focus",    BG_INPUT)],
              foreground=[("readonly", TEXT_MAIN),
                           ("active",   TEXT_MAIN)],
              background=[("readonly", BG_INPUT),
                           ("active",   BG_INPUT),
                           ("pressed",  BG_INPUT)],
              arrowcolor=[("readonly", TEXT_MAIN),
                           ("active",   ACCENT),
                           ("pressed",  ACCENT)],
              bordercolor=[("focus", ACCENT),
                            ("active", ACCENT)])

    def _refresh_categories(self):
        cats = self.config_data["categories"] + ["➕ Add New Category"]
        self.cat_combo["values"] = cats
        if self.cat_var.get() not in cats:
            self.cat_var.set(cats[0])


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()
