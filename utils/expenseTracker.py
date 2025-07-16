import sqlite3
import pandas as pd
import streamlit as st

#expense manager class using db
class ExpenseManager:



    def __init__(self, db_name):

        self.db_name=db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        #Create the table if its doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                date DATE,
                                amount REAL,
                                category TEXT,
                                description TEXT)''')
        self.conn.commit()

    def addExpense(self, date, name, amount, category, description):
        self.cursor.execute('''INSERT INTO expenses(name, date, amount, category, description)
                                VALUES(?, ?, ?, ?, ?)''',
                                (name, date, amount, category, description))
        self.conn.commit()

    def viewExpenses(self):
        query = "SELECT * FROM expenses"
        return pd.read_sql(query,self.conn)
    
    def deleteExpense(self,expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id=?",(expense_id,))
        self.conn.commit()


class IncomeManager:

    def __init__(self,db_name):
        self.db_name=db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        #Create the table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS income(
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                date DATE,
                                amount REAL,
                                source TEXT,
                                description TEXT)''')
        self.conn.commit()

    def addIncome(self, date, name, amount, source, description):
        self.cursor.execute('''INSERT INTO income (name, date, amount, source, description)
                                VALUES(?, ?, ?, ?, ?)''',
                                (name, date, amount, source, description))
        self.conn.commit()

    def viewIncome(self):
        query = "SELECT * FROM income"
        return pd.read_sql(query, self.conn)
    
    def deleteIncome(self,income_id):
        self.cursor.execute("DELETE FROM income WHERE id=?",(income_id,))
        self.conn.commit()


class Account:
    def __init__(self,db_name):
        self.IncomeManager = IncomeManager(db_name)
        self.ExpenseManager = ExpenseManager(db_name)
        self.Balance = 0.0

    def getBalance(self):
        total_income = self.IncomeManager.viewIncome()["amount"].sum()
        total_expense = self.ExpenseManager.viewExpenses()["amount"].sum()
        self.Balance = total_income - total_expense
        return self.Balance
    
    def addExpense(self, date, name, amount, category, description):
        self.ExpenseManager.addExpense(date, name, amount, category, description)
        self.Balance -= amount
        st.success(f"Expense added succesfully!")

    def addIncome(self, date, name, amount, category, description):
        self.IncomeManager.addIncome(date, name, amount, category, description)
        self.Balance += amount
        st.success(f"Income added sucesfully!")

    def expenseList(self):
        return self.ExpenseManager.viewExpenses()
    
    def incomeList(self):
        return self.IncomeManager.viewIncome()

    def deleteExpense(self, expense_id):
        expenses =self.ExpenseManager.viewExpenses()
        if expenses.empty:
            st.warning("No expenses to delete.")
            return
        
        if expense_id in expenses["id"].values:
            amount = expenses.loc[expenses["id"] == expense_id, "amount"].iloc[0]
            self.ExpenseManager.deleteExpense(expense_id)
            self.Balance -=amount
            st.success(f"Expense {expense_id} deleted succesfully!")
        else:
            st.warning(f"Invalid Expense ID: {expense_id}")

    def deleteIncome(self, income_id):
        incomes = self.IncomeManager.viewIncome()
        if incomes.empty:
            st.Warning("No income records to delete.")
            return
        
        if income_id in incomes["id"].values:
            amount = incomes.loc[incomes["id"] == income_id, "amount"].iloc[0]
            self.IncomeManager.deleteIncome(income_id)
            self.Balance -= amount
            st.success(f"Income {income_id} deleted succesfully!")
        else:
            st.warning(f"Invalid Income ID: {income_id}")

#transactions list
    def format_transcations_for_ai(self):
        expenses = self.ExpenseManager.viewExpenses()
        income = self.IncomeManager.viewIncome()

        print("Expense columns:", expenses.columns.tolist())
        print("Income columns:", income.columns.tolist())

        expenses.columns = [col.lower() for col in expenses.columns]
        income.columns = [col.lower() for col in income.columns]

        print("After lowercase conversion:")
        print("Expense columns:", expenses.columns.tolist())
        print("Income columns:", income.columns.tolist())

        formatted_expenses = expenses[['name', 'date', 'amount', 'category', 'description']].to_dict(orient='records')
        formatted_income = income[['name', 'date', 'amount', 'source','description']].to_dict(orient='records')

        #final dectionary to be returned 
        transcations = {
            'income': formatted_income,
            'expenses': formatted_expenses
        }

        return transcations
        
