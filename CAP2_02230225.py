import random  # We import random module in order to generate random numbers for Accounts
import os  # We import os module to interact with the operating system

# Base Account class
class Account:
    # Constructor with correct __init__ method
    def __init__(self, account_number, password, account_type, balance=0):
        self.account_number = account_number  # Initialize account number
        self.password = password  # Initialize password
        self.account_type = account_type  # Initialize account type
        self.balance = balance  # Initialize account balance, default is 0

    # Method to deposit amount
    def deposit(self, amount):
        self.balance += amount  # Depositing amount to the account balance
        print(f"Deposited Ngultrum {amount}. New balance: Ngultrum {self.balance}")  # Generating deposit receipt

    # Method to withdraw amount
    def withdraw(self, amount):
        if amount > self.balance:  # Verifying if the withdrawal amount exceeds the account balance
            print("Insufficient funds.")  # If the withdrawal amount exceeds the account balance
        else:
            self.balance -= amount  # Deducting withdrawal amount from account balance
            print(f"Withdrew Ngultrum {amount}. New balance: Ngultrum {self.balance}")  # Generating withdrawal receipt

    # Method to check balance
    def check_balance(self):
        return self.balance  # Returning the current balance

    # Method to transfer amount to another account
    def transfer(self, amount, recipient_account):
        if amount > self.balance:  # Verifying if transfer amount exceeds account balance
            print("Insufficient funds.")  # If the transfer amount exceeds the account balance
        else:
            self.withdraw(amount)  # Withdrawing the amount from current account
            recipient_account.deposit(amount)  # Depositing the amount into recipient's account
            print(f"Transferred Ngultrum {amount} to account {recipient_account.account_number}")  # Generating transfer receipt

    # Method to change account number
    def change_account_number(self, new_account_number):
        self.account_number = new_account_number  # Updating account number

    # Method to change password
    def change_password(self, new_password):
        self.password = new_password  # Updating account password


# BusinessAccount class inheriting from Account
class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0, business_name=""):
        super().__init__(account_number, password, "Business", balance)  # Initialize the base Account class
        self.business_name = business_name  # Initialize business name


# PersonalAccount class inheriting from Account
class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0, owner_name=""):
        super().__init__(account_number, password, "Personal", balance)  # Initialize the base Account class
        self.owner_name = owner_name  # Initialize account holder's name


# Function to save accounts to a file
def save_account(account):
    accounts = load_accounts()  # Load existing accounts from file
    accounts[account.account_number] = account  # Update or add the account
    with open('accounts.txt', 'w') as f:  # Opening accounts file in write mode
        for acc in accounts.values():  # Iterating through all accounts using for loop
            f.write(f"{acc.account_number},{acc.password},{acc.account_type},Ngultrum {acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")  # Writing account details to file


# Function to load accounts from a file
def load_accounts():
    accounts = {}  # Initialize empty dictionary to store accounts
    if os.path.exists('accounts.txt'):  # Verifying whether the accounts file exists
        with open('accounts.txt', 'r') as f:  # Opening accounts file in read mode
            for line in f:  # Iterating through each line in the file
                parts = line.strip().split(',')  # Splitting line
                account_number, password, account_type, balance = parts[:4]  # Retrieving account details
                balance = float(balance.split()[1])  # Converting account balance back to float after removing the prefix 'Ngultrum'
                if account_type == "Business":  # Verifying if account is a business account
                    business_name = parts[4]  # Retrieving business name
                    accounts[account_number] = BusinessAccount(account_number, password, balance, business_name)  # Creating BusinessAccount object
                elif account_type == "Personal":  # Verifying if account type is personal account
                    owner_name = parts[5]  # Retrieving owner's name
                    accounts[account_number] = PersonalAccount(account_number, password, balance, owner_name)  # Creating PersonalAccount object
    return accounts  # Return accounts dictionary


# Function to create a new account
def create_account():
    account_number = str(random.randint(100000000, 999999999))  # Generating a random 9-digit account number
    password = str(random.randint(1000, 9999))  # Generating a random 4-digit password
    account_type = input("Enter account type (Business/Personal): ")  # Prompt user to enter account type

    if account_type == "Business":  # Verifying if account type is business
        business_name = input("Enter business name: ")  # Prompt user to enter business name
        account = BusinessAccount(account_number, password, business_name=business_name)  # Creating BusinessAccount object
    else:  # If account type is personal
        owner_name = input("Enter holder name: ")  # Prompt user to enter account owner's name
        account = PersonalAccount(account_number, password, owner_name=owner_name)  # Creating PersonalAccount object

    save_account(account)  # To save the new account to file
    print(f"Account created! Your account number is {account_number} and password is {password}")  # Generating account creation receipt


# Function to login to an account
def login(accounts):
    account_number = input("Enter account number: ")  # Prompt user to enter account number
    password = input("Enter password: ")  # Prompt user to enter account password

    account = accounts.get(account_number)  # To retrieve account from accounts dictionary
    if account and account.password == password:  # Verifying whether account exists and if the password is correct
        print(f"Welcome, {account.account_type} account holder!")  # To print the welcome message
        return account  # Returning the logged-in account
    else:  # If account does not exist or if the password entered is incorrect
        print("Invalid account number or password.")  # Printing error message for invalid login
        return None  # Returning None for invalid login


# Function to delete an account
def delete_account(account):
    accounts = load_accounts()  # To load existing accounts from file
    if account.account_number in accounts:  # To check whether account exists
        del accounts[account.account_number]  # To delete the account from dictionary
        with open('accounts.txt', 'w') as f:  # Opening accounts file in write mode
            for acc in accounts.values():  # Iterating through all remaining accounts
                f.write(f"{acc.account_number},{acc.password},{acc.account_type},Ngultrum {acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")  # Writing account details to file
        print("Account deleted successfully.")  # Generating account deletion receipt
    else:
        print("Account not found.")


# Function to change account details
def change_account_details(account):
    print("\n1. Change Account Number\n2. Change Password")  # Generating options to change the account details
    choice = input("Enter choice: ")  # Prompt user to enter their choice

    if choice == '1':  # To change account number
        new_account_number = input("Enter new account number: ")  # Prompt user to enter new account number
        accounts = load_accounts()  # To load existing accounts from file
        if new_account_number in accounts:  # Verifying if new account number already exists or not
            print("Account number already exists.")  # If the account number already exists
        else:
            old_account_number = account.account_number  # To store old account number
            account.change_account_number(new_account_number)  # To change account numbers
            save_account(account)  # Saving account with new account number
            # To delete old account
            if old_account_number in accounts:
                del accounts[old_account_number]  # To delete old account from dictionary
                with open('accounts.txt', 'w') as f:  # Opening accounts file in write mode
                    for acc in accounts.values():  # Iterating through remaining accounts
                        f.write(f"{acc.account_number},{acc.password},{acc.account_type},Ngultrum {acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")  # Writing account details to file
            print("Account number changed successfully.")  # Printing confirmation message
    elif choice == '2':  # To change account password
        new_password = input("Enter new password: ")  # Prompt the user to enter new password
        account.change_password(new_password)  # To change account password
        save_account(account)  # Saving account with new password
        print("Password changed successfully.")  # Printing confirmation message
    else:
        print("Invalid choice.")


# Main function
def main():
    while True:  # Infinite loop
        print("\n1. Create Account\n2. Login\n3. Exit")  # Generating options
        choice = input("Enter choice: ")  # Prompt user to enter their choice

        if choice == '1':  # To create account
            create_account()  # Calling create_account function
        elif choice == '2':  # To login
            accounts = load_accounts()  # Loading existing accounts
            account = login(accounts)  # Logging in
            if account:  # Verifying whether the login was successful
                while True:
                    print("\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transfer\n5. Delete Account\n6. Change Account Details\n7. Logout")  # Printing options
                    trans_choice = input("Enter choice: ")  # Prompt user to enter their choice

                    if trans_choice == '1':  # To deposit the amount
                        amount = float(input("Enter amount to deposit: "))  # Prompt the user to enter the amount to deposit
                        account.deposit(amount)  # Depositing amount
                        save_account(account)  # Saving updated account details
                    elif trans_choice == '2':  # To withdraw
                        amount = float(input("Enter amount to withdraw: "))  # Prompt the user to enter the amount to withdraw
                        account.withdraw(amount)  # Withdrawing amount
                        save_account(account)  # Saving updated account details
                    elif trans_choice == '3':  # To check account balance
                        print(f"Balance: Ngultrum {account.check_balance()}")  # Printing current balance
                    elif trans_choice == '4':  # To transfer the amount
                        recipient_number = input("Enter recipient account number: ")  # Prompt the user to enter the recipient account number
                        recipient = accounts.get(recipient_number)  # Getting recipient account
                        if recipient:  # Verifying if recipient account exists
                            amount = float(input("Enter amount to transfer: "))  # Prompt the user to enter the amount to transfer
                            account.transfer(amount, recipient)  # Transferring amount
                            save_account(account)  # Saving sender's updated account details
                            save_account(recipient)  # Saving recipient's updated account details
                        else:
                            print("Recipient account does not exist.")
                    elif trans_choice == '5':  # To delete account
                        delete_account(account)
                        break  # Exiting loop
                    elif trans_choice == '6':  # To change account details
                        change_account_details(account)
                    elif trans_choice == '7':  # To logout
                        save_account(account)  # Saving account details
                        print("Logged out.")
                        break  # Exiting loop
        elif choice == '3':  # To exit the program
            print("Thank You!")
            break  # Exiting loop
        else:
            print("Invalid choice. Try again.")


# Ensures the main function runs when the script is executed
if __name__ == "__main__":
    main()  # Calling main function
