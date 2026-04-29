# 💸 Expense Tracker v2.0

A modern, feature-rich personal finance desktop application built with Python and Tkinter. Track expenses, manage budgets, and visualize spending patterns with beautiful charts and real-time analytics.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-orange)

---

## ✨ Features

- **Add & Manage Expenses** — Log expenses with description, amount, category, and date
- **Smart Categories** — Pre-built categories with emoji labels; create custom ones on the fly
- **Monthly Budget Tracking** — Set a budget limit and monitor spending against it with visual progress bars
- **Real-Time Dashboard** — View key metrics at a glance: total spent, transaction count, daily average, biggest single expense
- **Category Breakdown** — See spending distribution by category with horizontal bar charts and percentages
- **Top 3 Insights** — Instantly spot your three biggest expenses with medal rankings
- **Search & Filter** — Live search across descriptions and categories; filter by month
- **Edit & Delete** — Double-click any expense to edit, or delete with confirmation
- **Beautiful Charts** — Visualize spending patterns with interactive pie charts (by category) and line graphs (over time)
- **Smart Spending Tips** — AI-generated actionable tips based on your spending habits
- **Export to CSV** — Download your expense history anytime
- **Dark Theme** — Eye-friendly dark UI inspired by modern design systems
- **No Database Required** — Data stored in simple JSON and CSV files; perfect for privacy-conscious users

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Tkinter (comes with Python on most systems)
- matplotlib (optional, for charts)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```

2. **Install dependencies**
   ```bash
   # Tkinter comes with Python, but if it's missing:
   # On Ubuntu/Debian:
   sudo apt-get install python3-tk
   
   # On macOS:
   brew install python-tk
   
   # Install matplotlib for charts (optional but recommended):
   pip install matplotlib
   ```

3. **Run the application**
   ```bash
   python expense_tracker.py
   ```

That's it! The app creates its own data files on first run.

---

## 📖 Usage Guide

### Adding an Expense
1. Fill in the **Description** field (e.g., "Coffee at Starbucks")
2. Enter the **Amount** in your local currency
3. Select a **Category** from the dropdown, or create a new one by selecting "➕ Add New Category"
4. Confirm the **Date** (defaults to today in YYYY-MM-DD format)
5. Click **＋ Add Expense**

### Managing Budget
1. Go to the **MONTHLY BUDGET** section in the left panel
2. Enter your desired monthly limit
3. Click **Set Budget**
4. The visual progress bar updates in real time as you add expenses
5. Warnings appear when you reach 80% of your budget or exceed it

### Viewing Analytics
- **Dashboard Tab**: See stats, category breakdown, and top 3 expenses at a glance
- **History Tab**: Browse all transactions in a searchable, sortable table
  - Use the search box for live filtering
  - Double-click any row to edit
  - Select a row and click "🗑 Delete Selected" to remove it
- **Charts Tab**: Visualize spending by category (pie chart) and over time (line graph)

### Filtering by Month
Use the **Month** dropdown in the titlebar to filter all views by a specific month, or select "All" to see everything.

### Exporting Data
Click **📤 Export CSV** to download a timestamped CSV file of all your expenses for use in spreadsheets or other tools.

---

## 📁 File Structure

```
expense-tracker/
├── expense_tracker.py          # Main application (single file)
├── expenses.csv                # Expense data (auto-generated)
├── config.json                 # User config: budget, categories (auto-generated)
├── README.md                   # This file
├── LICENSE                     # MIT License
└── .gitignore                  # Git configuration
```

### Data Files

**expenses.csv** — Plain CSV format for easy import/export
```csv
description,amount,category,date
Coffee,3.50,🍕 Food & Drinks,2024-03-15
Gym membership,45.00,🏥 Health,2024-03-01
...
```

**config.json** — Stores your budget and custom categories
```json
{
  "budget": 2000.0,
  "categories": [
    "🍕 Food & Drinks",
    "🚌 Transport",
    "🎮 Entertainment",
    "...your custom categories..."
  ]
}
```

---

## 🛠 Architecture

The app follows the **Model-View-Controller (MVC)** pattern:

- **Model** — `load_config()`, `load_expenses()`, `save_all_expenses()` functions and CSV/JSON file I/O
- **View** — Tkinter widgets: frames, labels, entry fields, buttons, treeview, matplotlib figures
- **Controller** — `ExpenseTracker` class methods that handle user actions and refresh the UI

**Key Design Decisions:**

| Feature | Why |
|---------|-----|
| Single-file app | Easy to share and run anywhere |
| CSV + JSON storage | No database setup; human-readable; easy to backup |
| "Nuke & redraw" UI refresh | Simple to reason about; fast enough for typical datasets |
| Graceful matplotlib handling | App works without charts if matplotlib isn't installed |
| Dark theme by default | Modern aesthetic; easier on the eyes |

---

## 🎨 Customization

### Change Colors
Edit the color constants at the top of `expense_tracker.py`:
```python
BG_DARK    = "#1a1a2e"  # Main background
ACCENT     = "#e94560"  # Highlights, buttons
BLUE       = "#7ecef5"  # Secondary color
# ... etc
```

### Add/Remove Categories
Edit `DEFAULT_CATEGORIES`:
```python
DEFAULT_CATEGORIES = [
    "🍕 Food & Drinks",
    "🚗 Car Maintenance",   # Add your own
    "✈️ Travel",            # with emoji for personality
]
```

Or add them dynamically via the app's **"➕ Add New Category"** option.

### Adjust Window Size
Change the default geometry:
```python
self.geometry("1140x740")  # width x height
self.minsize(960, 640)     # minimum size
```

---

## 🐛 Troubleshooting

**Issue: "No module named 'tkinter'"**
- Tkinter doesn't come with all Python installations. Install it:
  - Ubuntu: `sudo apt-get install python3-tk`
  - macOS: `brew install python-tk@3.11` (adjust version as needed)
  - Windows: Tkinter is included with the official Python installer

**Issue: Charts tab shows "matplotlib not installed"**
- Install matplotlib: `pip install matplotlib`
- Restart the app

**Issue: Data not saving**
- Check that the app has write permissions in the current directory
- Ensure you're not running the app in a read-only location (e.g., inside a .zip)

**Issue: UI looks squished or stretched**
- This is usually a display scaling issue on Windows. Try running the app in compatibility mode or adjust your system DPI settings

---

## 💡 Tips & Tricks

- **Keyboard shortcuts**: Press Tab to move between fields; Enter to confirm dialogs
- **Smart tips**: The app analyzes your spending and offers personalized advice
- **Month filtering**: Use the month dropdown to compare spending across months
- **Search while filtering**: The search box works with the selected month for powerful filtering
- **Budget warnings**: Set your budget early to avoid overspending
- **Export regularly**: Keep CSV backups of your data for safety

---

## 🚀 Future Enhancements

Potential features for future versions:

- [ ] SQLite backend for larger datasets
- [ ] Light/dark mode toggle
- [ ] Recurring expenses with auto-add
- [ ] Multi-user support with login
- [ ] Cloud sync via REST API
- [ ] Tag system for cross-category tracking
- [ ] Budget sub-goals (e.g., "Food budget: 500, Transport: 200")
- [ ] Yearly trend analysis
- [ ] Import from CSV/Excel
- [ ] Keyboard shortcuts system
- [ ] Localization (multiple languages)

---

## 📝 Contributing

Contributions are welcome! Here's how to help:

1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feature/your-idea`
3. **Make your changes** and test thoroughly
4. **Commit** with clear messages: `git commit -m "Add feature: your feature"`
5. **Push** to your fork: `git push origin feature/your-idea`
6. **Open a Pull Request** with a description of your changes

### Code Style
- Follow PEP 8 (use `black` or `flake8` for linting)
- Keep methods focused and under 50 lines when possible
- Add docstrings to new functions
- Use descriptive variable names

### Testing
Before submitting a PR:
- Test adding, editing, and deleting expenses
- Test filtering and searching
- Test budget alerts
- Test CSV export
- Verify charts render correctly (if matplotlib is installed)

---

## 📜 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute it freely. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Created with ❤️ by [Your Name]  
Questions? Open an issue or reach out!

---

## 🙏 Acknowledgments

- **Tkinter** — Python's lightweight GUI toolkit
- **matplotlib** — Beautiful scientific visualizations
- **csvmodule** — Built-in CSV handling
- Inspired by modern personal finance apps like YNAB and Mint

---

## 📞 Support

Found a bug or have a suggestion?
- **Issues**: [Open a GitHub Issue](https://github.com/yourusername/expense-tracker/issues)
- **Discussions**: Start a GitHub Discussion for questions
- **Email**: your.email@example.com

---

## 📊 Project Stats

- **Lines of Code**: ~800
- **Time to Learn**: 30 minutes
- **Time to Master**: 2-3 hours
- **Fun Factor**: ⭐⭐⭐⭐⭐

Happy tracking! 💰
