import os

class User:
    def __init__(self, username, father_name, cnic, address, pin, balance=0.0):
        self.username = username
        self.father_name = father_name
        self.cnic = cnic
        self.address = address
        self.pin = pin
        self.balance = float(balance)

    def deposit(self, amount):
        self.balance += amount
        print(f"\n✅ Rs. {amount} deposited successfully.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("\n❌ Insufficient balance.")
        else:
            self.balance -= amount
            print(f"\n💸 Rs. {amount} withdrawn successfully.")

    def check_balance(self):
        print(f"\n💰 Current Balance: Rs. {self.balance:.2f}")

    def to_string(self):
        return f"{self.username}|{self.father_name}|{self.cnic}|{self.address}|{self.pin}|{self.balance}"

    @staticmethod
    def from_string(data_str):
        username, father_name, cnic, address, pin, balance = data_str.strip().split("|")
        return User(username, father_name, cnic, address, pin, float(balance))


class ATM:
    def __init__(self, data_file="user_data.txt"):
        self.data_file = data_file
        self.users = self.load_all_users()
        self.current_user = None

    def load_all_users(self):
        users = {}
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                for line in file:
                    if line.strip():
                        user = User.from_string(line)
                        users[user.username] = user
        return users

    def save_all_users(self):
        with open(self.data_file, "w") as file:
            for user in self.users.values():
                file.write(user.to_string() + "\n")

    def register(self):
        print("\n--- 📝 Register New User ---")
        username = input("Enter your username: ")
        if username in self.users:
            print("❌ Username already exists.")
            return

        father_name = input("Enter your father's name: ")
        cnic = input("Enter your 13-digit CNIC number: ")
        if not (cnic.isdigit() and len(cnic) == 13):
            print("❌ Invalid CNIC. It must be 13 digits.")
            return
        address = input("Enter your house address: ")
        pin = input("Set a 4-digit PIN: ")
        if not (pin.isdigit() and len(pin) == 4):
            print("❌ PIN must be 4 digits.")
            return

        try:
            initial_balance = float(input("Enter initial deposit: "))
        except ValueError:
            print("❌ Please enter a valid amount.")
            return

        new_user = User(username, father_name, cnic, address, pin, initial_balance)
        self.users[username] = new_user
        self.save_all_users()
        print(f"\n✅ Account created successfully for {username}!")

    def login(self):
        username = input("\n👤 Enter your username: ")
        pin = input("🔐 Enter your 4-digit PIN: ")
        user = self.users.get(username)
        if user and user.pin == pin:
            self.current_user = user
            print(f"\n✅ Welcome back, {user.username}!")
            self.menu()
        else:
            print("\n❌ Incorrect username or PIN.")

    def delete_account(self):
        username = input("\n🗑 Enter the username to delete: ")
        if username in self.users:
            confirm = input(f"Are you sure you want to delete account '{username}'? (yes/no): ").lower()
            if confirm == "yes":
                del self.users[username]
                self.save_all_users()
                print(f"✅ Account '{username}' deleted successfully.")
            else:
                print("❌ Deletion cancelled.")
        else:
            print("❌ Username not found.")

    def menu(self):
        while True:
            print("\n--- 💼 ATM MENU ---")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Delete My Account")
            print("5. Logout")

            choice = input("Choose an option (1-5): ")

            if choice == "1":
                self.current_user.check_balance()
            elif choice == "2":
                try:
                    amount = float(input("Enter amount to deposit: "))
                    self.current_user.deposit(amount)
                    self.save_all_users()
                except ValueError:
                    print("❌ Please enter a valid amount.")
            elif choice == "3":
                try:
                    amount = float(input("Enter amount to withdraw: "))
                    self.current_user.withdraw(amount)
                    self.save_all_users()
                except ValueError:
                    print("❌ Please enter a valid amount.")
            elif choice == "4":
                confirm = input("Are you sure you want to delete your account? (yes/no): ").lower()
                if confirm == "yes":
                    del self.users[self.current_user.username]
                    self.current_user = None
                    self.save_all_users()
                    print("✅ Your account has been deleted.")
                    break
            elif choice == "5":
                print("\n👋 Logging out. Goodbye!\n")
                break
            else:
                print("❌ Invalid option. Please try again.")

    def start(self):
        while True:
            print("\n========= 🏧 Welcome to ATM Machine =========")
            print("1. Register")
            print("2. Login")
            print("3. Delete Any Account")
            print("4. Exit ATM")
            choice = input("Choose an option (1-4): ")

            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                self.delete_account()
            elif choice == "4":
                print("\n👋 Exiting ATM system. Have a nice day!\n")
                break
            else:
                print("❌ Invalid choice. Please try again.")


# Run the ATM System
if __name__ == "__main__":
    atm = ATM()
    atm.start()
