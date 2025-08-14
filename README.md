# Expense Tracker 💰

A simple, modular **Python CLI application** to record, manage, analyze, and visualize personal expenses.  
Stores expense data in a **CSV file**, provides insightful analysis, and generates visual charts for better understanding.

---

## 📂 Project Structure

ExpenseTracker/\
│
├── configuration/\
│ └── configuration.py # Application configuration (file paths, constants)\
│
├── utils/\
│ └── utils.py # Helper functions (file handling, formatting, etc.)\
│
├── expense_tracker/\
│ └── expense_tracker.py # Core expense tracker functionality\
│
├── main.py # Entry point for running the application\
└── README.md # Project documentation


---

## ✨ Features

1. **Add Expense**
   - Input: Date, Category, Amount, Note
   - Automatically saved in `expenses.csv`

2. **View All Expenses**
   - Displays records in a clean tabular format

3. **Analyze Expenses**
   - Total spend
   - Spend per category
   - Top 3 spending categories

4. **Visualize Expenses**
   - Pie chart: Percentage spend by category
   - Bar chart: Daily or monthly spend trends

5. **Export Report**
   - Export expense summaries to `.txt` or `.csv`

---

## 🛠 Requirements

- Python 3.8+
- pandas
- matplotlib

Install dependencies:
```bash
pip install -r requirements.txt


▶️ Usage

Run the application from the root folder:

python main.py


Menu Options:

1) Add Expense
2) View All Expenses
3) Analyze Expenses
4) Visualize Expenses
5) Export Report
6) Quit


📊 Example Visualizations

Pie Chart – expense share by category

Bar Chart – daily or monthly spending


📄 Reports & Data

expenses.csv – Stores all expense records

expense_report_*.txt – Text summary reports

expense_report_*.csv – CSV summary reports

Note: These generated files are ignored by Git via .gitignore to keep the repo clean.

⚙️ Configuration

Default configurations (like CSV file name, date formats, etc.) are set in:

configuration/configuration.py


📜 License

This project is licensed under the Apache License 2.0.
You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

