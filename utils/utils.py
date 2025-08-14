import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

from configuration.configuration import CSV_FILE, DATE_FMT

from typing import Optional


def print_menu():
    print("""
==============================
      Expense Tracker
==============================
1) Add Expense
2) View All Expenses
3) Analyze Expenses
4) Visualize Expenses
5) Export Report
6) Quit
""")


def ensure_csv_exists(csv_path: str = CSV_FILE) -> None:
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(csv_path):
        with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "amount", "note"])



def read_expenses(csv_path: str = CSV_FILE) -> pd.DataFrame:
    """Read expenses into a DataFrame. Returns an empty DF with proper dtypes if file is empty."""
    ensure_csv_exists(csv_path)
    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=["date", "category", "amount", "note"])

    # Normalize data types
    if not df.empty:
        # Coerce date
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        # Coerce amount
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        # Fill NA note with empty string
        df["note"] = df["note"].fillna("")
        # Drop rows with invalid date or amount
        df = df.dropna(subset=["date", "amount"]).copy()
        # Sort by date
        df = df.sort_values("date").reset_index(drop=True)
    else:
        df = pd.DataFrame(columns=["date", "category", "amount", "note"])
    return df



def write_expense(date_str: str, category: str, amount: float, note: str = "", csv_path: str = CSV_FILE) -> None:
    """Append a single expense record to the CSV file."""
    ensure_csv_exists(csv_path)
    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date_str, category, f"{amount:.2f}", note])



def prompt_date(default: Optional[str] = None) -> str:
    """Prompt for a date in YYYY-MM-DD format and validate."""
    while True:
        user_in = input(f"Enter date (YYYY-MM-DD){' ['+default+']' if default else ''}: ").strip()
        if not user_in and default:
            return default
        try:
            dt = datetime.strptime(user_in, DATE_FMT)
            return dt.strftime(DATE_FMT)
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD (e.g., 2025-08-13).")



def prompt_category() -> str:
    """Prompt for a non-empty category."""
    while True:
        cat = input("Enter category (e.g., Food, Transport, Rent): ").strip()
        if cat:
            return cat
        print("Category cannot be empty.")


def prompt_amount() -> float:
    """Prompt for a positive numeric amount."""
    while True:
        amt = input("Enter amount (e.g., 249.50): ").strip()
        try:
            val = float(amt)
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            print("Amount must be a positive number.")


def prompt_note() -> str:
    return input("Enter note (optional): ").strip()
