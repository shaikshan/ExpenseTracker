
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime
from typing import Optional
from configuration.configuration import CSV_FILE,DATE_FMT
from utils.utils import prompt_amount,prompt_date,prompt_category,print_menu,prompt_note,read_expenses,write_expense


class ExpenseTracker:
    def __init__(self):
        pass

    def add_expense(self):
        """CLI for adding an expense."""
        today = datetime.today().strftime(DATE_FMT)
        print("\nAdd Expense")
        date_str = prompt_date(default=today)
        category = prompt_category()
        amount = prompt_amount()
        note = prompt_note()

        write_expense(date_str, category, amount, note)
        print(" Expense added successfully!\n")


    def view_expenses(self):
        """Display all expenses in a clean table."""
        print("\nAll Expenses")
        df = read_expenses()
        if df.empty:
            print("No expenses found.")
            return

        # Format for display
        out = df.copy()
        out["date"] = out["date"].dt.strftime(DATE_FMT)
        out["amount"] = out["amount"].map(lambda x: f"{x:,.2f}")
        print(out.to_string(index=False))
        print(f"\nTotal records: {len(out)}\n")


    def analyze_expenses(self):
        """Show total spend, per-category spend, top 3 categories."""
        print("\nAnalyze Expenses")
        df = read_expenses()
        if df.empty:
            print("No expenses to analyze.")
            return

        total = df["amount"].sum()
        by_cat = df.groupby("category", dropna=False)["amount"].sum().sort_values(ascending=False)
        top3 = by_cat.head(3)

        print(f"Total spend: {total:,.2f}")
        print("\nSpend by category:")
        print(by_cat.to_frame(name="amount").to_string())
        print("\nTop 3 categories:")
        print(top3.to_frame(name="amount").to_string())
        print("")


    def choose_aggregation(self,) -> str:
        """Ask user to choose daily or monthly aggregation for bar chart."""
        while True:
            choice = input("Bar chart aggregation - (D)aily or (M)onthly? [M]: ").strip().lower()
            if choice in ("", "m", "monthly"):
                return "M"
            if choice in ("d", "daily"):
                return "D"
            print("Please enter 'D' for daily or 'M' for monthly.")


    def visualize_expenses(self,):
        """Generate pie chart (category share) and bar chart (daily or monthly spend)."""
        print("\nVisualize Expenses")
        df = read_expenses()
        if df.empty:
            print("No expenses to visualize.")
            return

        # Pie chart by category
        by_cat = df.groupby("category", dropna=False)["amount"].sum().sort_values(ascending=False)
        if by_cat.empty or by_cat.sum() == 0:
            print("Not enough data to plot category pie chart.")
        else:
            plt.figure()
            plt.pie(by_cat.values, labels=by_cat.index, autopct="%1.1f%%", startangle=90)
            plt.title("Expense Share by Category")
            plt.axis("equal")
            plt.tight_layout()
            plt.show()

        # Bar chart daily or monthly
        how = self.choose_aggregation()
        df2 = df.set_index("date").copy()
        if how == "D":
            grouped = df2["amount"].resample("D").sum()
            title = "Daily Spend"
            xlabel = "Date"
        else:
            grouped = df2["amount"].resample("M").sum()
            title = "Monthly Spend"
            xlabel = "Month"

        if grouped.empty:
            print("Not enough data to plot time-based bar chart.")
            return

        plt.figure()
        grouped.plot(kind="bar")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel("Amount")
        plt.tight_layout()
        plt.show()


    def export_report(self,):
        """Export a summary report to CSV or text file."""
        print("\nExport Report")
        df = read_expenses()
        if df.empty:
            print("No expenses to export.")
            return

        total = df["amount"].sum()
        by_cat = df.groupby("category", dropna=False)["amount"].sum().sort_values(ascending=False)
        top3 = by_cat.head(3)

        while True:
            fmt = input("Export format: (C)SV or (T)ext? [T]: ").strip().lower()
            if fmt in ("", "t", "text"):
                fmt = "text"
                break
            if fmt in ("c", "csv"):
                fmt = "csv"
                break
            print("Please enter 'C' for CSV or 'T' for text.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if fmt == "text":
            fname = f"expense_report_{timestamp}.txt"
            lines = []
            lines.append("Expense Summary Report\n")
            lines.append(f"Generated at: {datetime.now().isoformat(timespec='seconds')}\n")
            lines.append("=" * 40 + "\n")
            lines.append(f"Total spend: {total:,.2f}\n\n")
            lines.append("Spend by category:\n")
            for cat, amt in by_cat.items():
                lines.append(f"  - {cat}: {amt:,.2f}\n")
            lines.append("\nTop 3 categories:\n")
            for cat, amt in top3.items():
                lines.append(f"  1) {cat}: {amt:,.2f}\n")
            with open(fname, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f" Text report exported: {fname}")
        else:
            # CSV with two sheets isn't possible with pure CSV; we create two files.
            fname_summary = f"expense_report_summary_{timestamp}.csv"
            fname_bycat = f"expense_report_by_category_{timestamp}.csv"
            # Summary as a tiny DataFrame
            pd.DataFrame({"metric": ["total_spend"], "value": [total]}).to_csv(fname_summary, index=False)
            by_cat.reset_index().rename(columns={"amount": "total_by_category"}).to_csv(fname_bycat, index=False)
            print(f" CSV reports exported:\n  - {fname_summary}\n  - {fname_bycat}")