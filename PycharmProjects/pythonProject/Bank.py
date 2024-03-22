class BankAccount:
    no_of_cust = 0
    acc_num = 42010

    def __init__(self, name, mobile_no, initial_depo):
        self.name = name
        self.cust_acc_num = BankAccount.acc_num
        self.mobile_no = mobile_no
        self.acc_balance = initial_depo

        BankAccount.acc_num += 1
        BankAccount.no_of_cust += 1

    def basic_details(self):
        return f'User: {self.name}\t Account No: {self.cust_acc_num}\t Balance: ₹{self.acc_balance}'

    def deposit(self, amount):
        if amount > 0:
            self.acc_balance += amount
            return f'Transaction completed. Current Balance: ₹{self.acc_balance}'
        else:
            return 'Invalid amount transaction aborted'

    def withdrawl(self, amount):
        if amount <= self.acc_balance and amount > 0:
            self.acc_balance -= amount
            return f'Transaction completed. Current Balance: ₹{self.acc_balance}'
        else:
            return 'Invalid amount transaction aborted'

    def payment(self, other, amount):
        if amount <= self.acc_balance and amount > 0:
            self.acc_balance -= amount
            other.acc_balance += amount
            return f'Transaction completed. Current Balance: ₹{self.acc_balance}'
        else:
            return 'Invalid amount transaction aborted'


if __name__ == '__main__':
    cust1 = BankAccount(name='Ishaan', mobile_no=9876543210, initial_depo=1000)
    cust2 = BankAccount(name='Akash', mobile_no=9876543212, initial_depo=2000)
    print('No. of customers is', BankAccount.no_of_cust)
    print(cust1.basic_details())
    print(cust2.basic_details())
    # Example transactions
    amount = 500
    print(cust1.deposit(amount))
    print(cust1.withdrawl(amount))
    print(cust1.payment(cust2, amount))
    print(cust2.basic_details())
