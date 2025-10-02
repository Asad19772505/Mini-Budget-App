#!/usr/bin/env python3
"""
Simple Budget Tracker
Track expenses by category and view weekly summaries
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class BudgetTracker:
    def __init__(self, filename='expenses.json'):
        self.filename = filename
        self.expenses = self.load_expenses()
    
    def load_expenses(self):
        """Load expenses from JSON file"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []
    
    def save_expenses(self):
        """Save expenses to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.expenses, f, indent=2)
    
    def add_expense(self, amount, category, description=''):
        """Add a new expense"""
        expense = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'amount': float(amount),
            'category': category,
            'description': description
        }
        self.expenses.append(expense)
        self.save_expenses()
        print(f"✓ Added ${amount:.2f} to {category}")
    
    def get_week_range(self):
        """Get the current week's date range (Monday to Sunday)"""
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start.date(), end.date()
    
    def weekly_summary(self):
        """Display weekly summary of expenses"""
        start_date, end_date = self.get_week_range()
        
        print(f"\n{'='*50}")
        print(f"WEEKLY SUMMARY ({start_date} to {end_date})")
        print(f"{'='*50}\n")
        
        # Filter expenses for this week
        weekly_expenses = []
        for expense in self.expenses:
            expense_date = datetime.strptime(expense['date'], '%Y-%m-%d').date()
            if start_date <= expense_date <= end_date:
                weekly_expenses.append(expense)
        
        if not weekly_expenses:
            print("No expenses recorded this week.")
            return
        
        # Calculate totals by category
        category_totals = defaultdict(float)
        for expense in weekly_expenses:
            category_totals[expense['category']] += expense['amount']
        
        # Display by category
        total = 0
        for category, amount in sorted(category_totals.items()):
            print(f"{category:20} ${amount:>8.2f}")
            total += amount
        
        print(f"{'-'*50}")
        print(f"{'TOTAL':20} ${total:>8.2f}")
        print(f"{'='*50}\n")
    
    def list_all_expenses(self):
        """List all expenses"""
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        
        print(f"\n{'Date':12} {'Category':15} {'Amount':10} {'Description':30}")
        print('-'*70)
        
        for expense in sorted(self.expenses, key=lambda x: x['date'], reverse=True):
            desc = expense.get('description', '')[:28]
            print(f"{expense['date']:12} {expense['category']:15} ${expense['amount']:>8.2f} {desc:30}")
        print()

def main():
    tracker = BudgetTracker()
    
    while True:
        print("\n📊 BUDGET TRACKER")
        print("1. Add expense")
        print("2. Weekly summary")
        print("3. List all expenses")
        print("4. Exit")
        
        choice = input("\nChoose an option (1-4): ").strip()
        
        if choice == '1':
            try:
                amount = float(input("Amount: $"))
                category = input("Category (e.g., Food, Transport, Entertainment): ").strip()
                description = input("Description (optional): ").strip()
                tracker.add_expense(amount, category, description)
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")
        
        elif choice == '2':
            tracker.weekly_summary()
        
        elif choice == '3':
            tracker.list_all_expenses()
        
        elif choice == '4':
            print("Goodbye! 👋")
            break
        
        else:
            print("❌ Invalid option. Please choose 1-4.")

if __name__ == "__main__":
    main()
