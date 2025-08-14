import sys

from utils.utils import ensure_csv_exists,print_menu

from expense_tracker.expense_tracker import ExpenseTracker

exptrack = ExpenseTracker()



def main():
    ensure_csv_exists()
    while True:
        print_menu()
        choice = input("Choose an option [1-6]: ").strip()
        if choice == "1":
            exptrack.add_expense()
        elif choice == "2":
            exptrack.view_expenses()
        elif choice == "3":
            exptrack.analyze_expenses()
        elif choice == "4":
            exptrack.visualize_expenses()
        elif choice == "5":
            exptrack.export_report()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-6.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")
        sys.exit(0)