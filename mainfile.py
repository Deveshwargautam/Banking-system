import os

FILE_NAME = "bank_data.txt"

# Create Account
def create_account():
    acc_no = input("Enter Account Number: ")
    name = input("Enter Name: ")
    pin = input("Set 4-digit PIN: ")
    balance = float(input("Enter Initial Balance: "))

    with open(FILE_NAME, "a") as f:
        f.write(f"{acc_no},{name},{pin},{balance}\n")

    print("✅ Account Created Successfully!")

# Search Account
def search_account(acc_no):
    if not os.path.exists(FILE_NAME):
        return None

    with open(FILE_NAME, "r") as f:
        for line in f:
            data = line.strip().split(",")
            if data[0] == acc_no:
                return data
    return None

# Update Account
def update_account(acc_no, new_balance):
    lines = []
    with open(FILE_NAME, "r") as f:
        lines = f.readlines()

    with open(FILE_NAME, "w") as f:
        for line in lines:
            data = line.strip().split(",")
            if data[0] == acc_no:
                f.write(f"{data[0]},{data[1]},{data[2]},{new_balance}\n")
            else:
                f.write(line)

# Authenticate User
def authenticate(account):
    entered_pin = input("Enter PIN: ")
    if entered_pin == account[2]:
        return True
    else:
        print("❌ Incorrect PIN!")
        return False

# Deposit
def deposit():
    acc_no = input("Enter Account Number: ")
    account = search_account(acc_no)

    if account and authenticate(account):
        amount = float(input("Enter amount to deposit: "))
        new_balance = float(account[3]) + amount
        update_account(acc_no, new_balance)
        print("💰 Deposit Successful!")
    else:
        print("❌ Authentication Failed!")

# Withdraw
def withdraw():
    acc_no = input("Enter Account Number: ")
    account = search_account(acc_no)

    if account and authenticate(account):
        amount = float(input("Enter amount to withdraw: "))
        balance = float(account[3])

        if amount > balance:
            print("❌ Insufficient Balance!")
        else:
            new_balance = balance - amount
            update_account(acc_no, new_balance)
            print("💸 Withdrawal Successful!")
    else:
        print("❌ Authentication Failed!")

# Check Balance
def check_balance():
    acc_no = input("Enter Account Number: ")
    account = search_account(acc_no)

    if account and authenticate(account):
        print(f"💳 Account Holder: {account[1]}")
        print(f"💰 Balance: ₹{account[3]}")
    else:
        print("❌ Authentication Failed!")

# View Accounts (Admin purpose)
def view_accounts():
    if not os.path.exists(FILE_NAME):
        print("No records found!")
        return

    with open(FILE_NAME, "r") as f:
        print("\n--- All Accounts ---")
        for line in f:
            acc_no, name, pin, balance = line.strip().split(",")
            print(f"Acc No: {acc_no}, Name: {name}, Balance: ₹{balance}")

# Menu
def menu():
    while True:
        print("\n===== BANK MENU =====")
        print("1. Create Account")
        print("2. View All Accounts")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Check Balance")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            view_accounts()
        elif choice == "3":
            deposit()
        elif choice == "4":
            withdraw()
        elif choice == "5":
            check_balance()
        elif choice == "6":
            print("Thank you for using Bank System!")
            break
        else:
            print("Invalid choice!")

# Run
menu()
