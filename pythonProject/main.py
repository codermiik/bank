import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from Bank import BankAccount  # Assuming BankAccount class is defined elsewhere


class FacialDetector:
    def __init__(self):
        # Initialize facial detection model
        self.face_cascade = cv2.CascadeClassifier(
            'C:/Users/User/PycharmProjects/pythonProject/data/haarcascade_frontalface_default.xml')  # Path to the cascade classifier

    def detect_face(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces

    def draw_rectangle(self, image, faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    def display_image(self, image):
        cv2.imshow('Facial Detection', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def facial_authentication(detector):
    # Capture video from camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video feed
        ret, frame = cap.read()

        # Detect faces
        faces = detector.detect_face(frame)

        # Display the video feed with face detection
        detector.draw_rectangle(frame, faces)
        cv2.imshow('Facial Detection', frame)

        # Check if exactly one face is detected
        if len(faces) == 1:
            # Close the window after detecting a face
            cv2.waitKey(3000)  # Wait for 3 seconds before closing
            cap.release()
            cv2.destroyAllWindows()
            return True

        # Check if 'q' is pressed to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return False


class BankGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Banking System")
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))  # Set window size to fullscreen
        self.master.attributes('-fullscreen', True)  # Make window fullscreen
        self.master.resizable(False, False)  # Disable window resizing

        self.customer_dict = {}
        self.mobile_acc_link = {}
        self.current_step = 0  # Variable to track the current step
        self.logged_in_account = None  # Variable to store the logged in account number
        self.detector = FacialDetector()  # Initialize facial detector

        self.face_authenticated = False  # Flag to indicate face authentication during account creation

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', foreground='green', font=('Arial', 12))
        style.configure('TLabel', foreground='blue', font=('Arial', 12))
        style.configure('TEntry', foreground='black', font=('Arial', 12))
        style.configure('Bank.TFrame', background='#e6e6e6')

        frame = ttk.Frame(self.master, style='Bank.TFrame')
        frame.place(relx=0.5, rely=0.5, anchor='center')

        if self.current_step == 0:
            # Registration widgets
            self.label_name = ttk.Label(frame, text="Name:")
            self.label_name.grid(row=0, column=0, pady=10, padx=10, sticky=tk.E)
            self.entry_name = ttk.Entry(frame)
            self.entry_name.grid(row=0, column=1, pady=10, padx=10)

            self.label_mobile = ttk.Label(frame, text="Mobile Number:")
            self.label_mobile.grid(row=1, column=0, pady=10, padx=10, sticky=tk.E)
            self.entry_mobile = ttk.Entry(frame)
            self.entry_mobile.grid(row=1, column=1, pady=10, padx=10)

            self.label_deposit = ttk.Label(frame, text="Initial Deposit:")
            self.label_deposit.grid(row=2, column=0, pady=10, padx=10, sticky=tk.E)
            self.entry_deposit = ttk.Entry(frame)
            self.entry_deposit.grid(row=2, column=1, pady=10, padx=10)

            self.btn_create = ttk.Button(frame, text="Create User", command=self.create_user)
            self.btn_create.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

            self.btn_login = ttk.Button(frame, text="Login", command=self.switch_to_login)
            self.btn_login.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

        elif self.current_step == 1:
            # Login widgets
            self.label_acc_no = ttk.Label(frame, text="Account Number:")
            self.label_acc_no.grid(row=0, column=0, pady=10, padx=10, sticky=tk.E)
            self.entry_acc_no = ttk.Entry(frame)
            self.entry_acc_no.grid(row=0, column=1, pady=10, padx=10)

            self.btn_login = ttk.Button(frame, text="Login", command=self.login)
            self.btn_login.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

    def switch_to_login(self):
        # Destroy current registration widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Change current step to login
        self.current_step = 1

        # Recreate login widgets
        self.create_widgets()

    def create_user(self):
        name = self.entry_name.get()
        mobile_no = int(self.entry_mobile.get())
        initial_depo = int(self.entry_deposit.get())

        if initial_depo <= 0:
            messagebox.showerror("Error", "Invalid Amount")
            return

        self.face_authenticated = facial_authentication(self.detector)

        if self.face_authenticated:
            customer = BankAccount(name=name, mobile_no=mobile_no, initial_depo=initial_depo)
            self.customer_dict[customer.cust_acc_num] = customer
            self.mobile_acc_link[customer.mobile_no] = customer.cust_acc_num

            messagebox.showinfo("Success",
                                f"New User Created! Welcome {customer.name} to Corporate Bank. {customer.cust_acc_num} is your account number")

            # Remove all widgets related to user creation
            for widget in self.master.winfo_children():
                widget.destroy()

            # Display only the login widgets
            self.current_step = 1
            self.create_widgets()
        else:
            messagebox.showerror("Error", "Face authentication failed during account creation.")

    def login(self):
        account_no = int(self.entry_acc_no.get())

        # Perform face authentication
        self.face_authenticated = facial_authentication(self.detector)

        if account_no in self.customer_dict.keys() and self.face_authenticated:
            messagebox.showinfo("Success", f"{self.customer_dict[account_no].name} Logged in")

            # Clear login widgets
            for widget in self.master.winfo_children():
                widget.destroy()

            # Store logged in account number
            self.logged_in_account = account_no

            # Show menu widgets
            self.show_menu()
        else:
            messagebox.showerror("Error", "Account either does not exist or facial authentication failed")

    def show_menu(self):
        # Placeholder for menu options
        self.balance_label = ttk.Label(self.master, text="")
        self.balance_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.update_balance_label()

        btn_deposit = ttk.Button(self.master, text="Deposit", command=self.deposit)
        btn_deposit.grid(row=1, column=0, pady=10, padx=10)

        btn_withdraw = ttk.Button(self.master, text="Withdraw", command=self.withdraw)
        btn_withdraw.grid(row=1, column=1, pady=10, padx=10)

        btn_logout = ttk.Button(self.master, text="Logout", command=self.logout)
        btn_logout.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    def update_balance_label(self):
        if self.logged_in_account is not None:
            balance = self.customer_dict[self.logged_in_account].acc_balance
            self.balance_label.config(text=f"Your current balance is: ₹{balance}", font=('Arial', 14))

    def deposit(self):
        # Create a new window for deposit
        deposit_window = tk.Toplevel(self.master)
        deposit_window.title("Deposit")
        width = 300
        height = 150
        x_offset = (self.master.winfo_screenwidth() - width) // 2
        y_offset = (self.master.winfo_screenheight() - height) // 2
        deposit_window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

        # Create entry for deposit amount
        ttk.Label(deposit_window, text="Enter Deposit Amount:", font=('Arial', 12)).pack()
        entry_deposit_amount = ttk.Entry(deposit_window)
        entry_deposit_amount.pack()

        # Create button to confirm deposit
        ttk.Button(deposit_window, text="Confirm", command=lambda: self.confirm_deposit(deposit_window, entry_deposit_amount)).pack()

    def confirm_deposit(self, deposit_window, entry_deposit_amount):
        account_no = self.logged_in_account
        if account_no is not None:
            amount = entry_deposit_amount.get()
            if amount.isdigit() and int(amount) > 0:
                self.customer_dict[account_no].deposit(int(amount))
                messagebox.showinfo("Deposit", f"Deposit successful. Amount: {amount}")
                deposit_window.destroy()
                self.update_balance_label()
            else:
                messagebox.showerror("Error", "Invalid amount. Please enter a valid positive integer.")
        else:
            messagebox.showerror("Error", "Please log in first.")

    def withdraw(self):
        # Create a new window for withdrawal
        withdraw_window = tk.Toplevel(self.master)
        withdraw_window.title("Withdraw")
        width = 300
        height = 150
        x_offset = (self.master.winfo_screenwidth() - width) // 2
        y_offset = (self.master.winfo_screenheight() - height) // 2
        withdraw_window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

        # Create entry for withdrawal amount
        ttk.Label(withdraw_window, text="Enter Withdrawal Amount:", font=('Arial', 12)).pack()
        entry_withdraw_amount = ttk.Entry(withdraw_window)
        entry_withdraw_amount.pack()

        # Create button to confirm withdrawal
        ttk.Button(withdraw_window, text="Confirm", command=lambda: self.confirm_withdraw(withdraw_window, entry_withdraw_amount)).pack()

    def confirm_withdraw(self, withdraw_window, entry_withdraw_amount):
        account_no = self.logged_in_account
        if account_no is not None:
            amount = entry_withdraw_amount.get()
            if amount.isdigit() and int(amount) > 0:
                current_balance = self.customer_dict[account_no].acc_balance
                if int(amount) <= current_balance:
                    self.customer_dict[account_no].acc_balance -= int(amount)
                    messagebox.showinfo("Withdraw", f"Withdrawal successful. Amount: {amount}")
                    withdraw_window.destroy()
                    self.update_balance_label()
                else:
                    messagebox.showerror("Error", "Insufficient balance.")
            else:
                messagebox.showerror("Error", "Invalid amount. Please enter a valid positive integer.")
        else:
            messagebox.showerror("Error", "Please log in first.")

    def logout(self):
        # Clear existing widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Reset current step, logged in account, and recreate initial widgets
        self.current_step = 0
        self.logged_in_account = None
        self.create_widgets()


def main():
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
