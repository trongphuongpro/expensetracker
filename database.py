from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()


class ExpenseRecord(Base):
    __tablename__ = 'Expense Record'

    id_num = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    category = Column(String)
    amount = Column(Integer)
    content = Column(String)

    def __repr__(self):
        return f'<Expense(id: {self.id_num}, date: {self.date}, category: {self.category}, amount: {self.amount}, content: {self.content})>'


class BudgetRecord(Base):
    __tablename__ = 'Monthly Budget Record'

    month = Column(String, primary_key=True)
    income = Column(Integer)
    outcome = Column(Integer)
    saving = Column(Integer)

    def __repr__(self):
        return f'<Budget(month: {self.month}, income: {self.income}, outcome: {self.outcome}, saving: {self.saving}'  