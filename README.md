# 💰 Expense Tracker

A simple and straightforward expense tracking application built with Python and Tkinter. Keep track of your spending habits by category, see your total expenses, and manage your budget all in one place.

## ✨ Features

- **Add Expenses**: Quickly log your spending with a description, amount, and category
- **Categorize Spending**: Organize expenses into Food, Transport, Shopping, or Other
- **Delete Entries**: Remove expenses you don't need anymore
- **Persistent Storage**: All your expenses are saved to a file and loaded automatically when you open the app
- **Total Calculation**: See your total spending at a glance
- **Simple UI**: Clean and easy-to-use interface built with Tkinter

## 🛠️ Requirements

- Python 3.x
- Tkinter (usually comes with Python)

## 📥 Installation

1. Clone this repository or download the code
2. Make sure you have Python installed on your system
3. No additional packages needed - Tkinter comes with Python by default

## 🚀 How to Run

Simply run the script:

```bash
python expense_tracker.py
```

The app will open a window where you can start tracking your expenses right away.

## 📖 How to Use

1. **Add an Expense**:
   - Enter the description of what you spent money on
   - Enter the amount (as a number)
   - Select a category from the dropdown
   - Click the "Add" button
   - Your expense gets saved automatically to a file

2. **View Your Expenses**:
   - All your expenses show up in the list below
   - Each entry displays: Description | Category | Amount
   - The total amount at the bottom updates automatically

3. **Delete an Expense**:
   - Click on an expense in the list to select it
   - Click the "Delete" button
   - The entry gets removed and your file is updated

## 📁 File Structure

```
expense_tracker.py       # Main application file
expenses.txt            # Auto-generated file where expenses are saved
```

## 💾 Data Storage

Your expenses are saved in a simple text file called `expenses.txt` in the same directory as the script. Each expense is stored on a new line with the format:

```
Description;Amount;Category
```

Example:
```
Coffee;5.50;Food
Bus Ticket;2.00;Transport
```

## 🎨 Customization

Want to add more categories or change the look? Here are some easy modifications:

- **Add Categories**: Find this line in the code and add more:
  ```python
  categories = ["Food", "Transport", "Shopping", "Other"]
  ```

- **Change Window Size**: Modify this line:
  ```python
  root.geometry("400x450")
  ```

- **Change the Filename**: Update this at the top:
  ```python
  FILE = "expenses.txt"
  ```

## ⚠️ Notes

- Make sure you enter the amount as a valid number (e.g., 5.50, not $5.50)
- The app will create the `expenses.txt` file automatically on first save
- If you delete the `expenses.txt` file, the app will start fresh with no expenses

## 🐛 Troubleshooting

**"Fill all fields" error**: Make sure you entered both a description and an amount before clicking Add

**"Amount must be a number" error**: Check that your amount is a valid number without currency symbols

**Nothing showing up when I open the app**: Check if `expenses.txt` exists in the same folder. It will be created automatically when you add your first expense.

## 📝 License

Feel free to use this project however you like. It's yours to modify and improve!

## 🤝 Contributing

Got ideas for improvements? Found a bug? Feel free to fork, modify, and make it better!

---

**Happy tracking! 📊**
