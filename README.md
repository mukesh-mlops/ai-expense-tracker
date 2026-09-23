# AI-Powered Expense Tracker

A CLI expense tracking application built with Python and SQLite that automatically categorizes expenses using OpenAI API.

## Features

- Add expenses with automatic AI categorization
- View all expenses in a table
- Monthly reports with category-wise breakdown
- Export data to CSV
- Delete expenses by ID

## Tech Stack

- Python 3.x
- SQLite (database)
- OpenAI API (AI categorization)
- CSV (data export)

## How It Works

1. User enters expense description and amount
2. System sends description to OpenAI API
3. AI returns the category (Food, Transport, etc.)
4. Expense is saved to SQLite database
5. Monthly reports show category-wise spending

## Installation

git clone https://github.com/mukesh-mlops/ai-expense-tracker.git
cd ai-expense-tracker
python expense_tracker.py

## Usage

1 - Add expense
2 - View all expenses
3 - Monthly report
4 - Export to CSV
5 - Delete expense
6 - Exit

## Built By

S. Mukesh Kumar
GitHub: https://github.com/mukesh-mlops
