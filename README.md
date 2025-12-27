# 🛒 Supermarket Management System

A **desktop-based Supermarket Management System** built using **Python (Tkinter)** that handles billing, inventory management, customer records, and payment processing with a clean GUI interface.

This project demonstrates **modular programming**, **real-world workflow simulation**, and **GUI-driven business logic**, making it suitable for academic submissions, portfolios, and resume projects.

---

## 📌 Key Features

### 🧾 Billing System

* Generate new bills with multiple items
* Automatic GST calculation
* Supports item return before payment
* Displays bill in GUI format
* Prints physical receipt
* Generates PDF bill
* Sends bill to customer via email

### 🏬 Inventory Management

* View store inventory in tabular GUI
* Add new items
* Remove items
* Renew stock quantities
* Automatic out-of-stock detection

### 👤 Customer Management

* Register new customers
* Auto-generate unique User IDs
* Email verification
* View saved customer records

### 💳 Payment Processing

* Cash
* Debit Card (with OTP & expiry validation)
* UPI
* OTP-based transaction verification

### 🖥️ GUI Features

* Built entirely using **Tkinter**
* Pop-up dialogs for input, warnings, and confirmations
* Table-based views using Treeview
* Safe exit confirmation

---

## 🛠️ Technologies Used

* **Python 3.x**
* **Tkinter** – GUI
* **CSV** – Data storage
* **SMTP (Gmail)** – Email & OTP
* **ReportLab** – PDF bill generation

---

## 📂 Project Structure

```
Supermarket-Management-System/
│
├── PROJECT01.py          # Main application
├── market.csv            # Inventory data
├── customers.csv         # Customer data
├── bill_<orderid>.pdf    # Generated bills
├── icon.ico              # App icon (optional)
└── README.md
```

---

## ▶️ How to Run the Project

1. **Install Python 3.x**
2. Install required library:

   ```bash
   pip install reportlab
   ```
3. Ensure `market.csv` and `customers.csv` exist in the same folder
4. Run the application:

   ```bash
   python PROJECT01.py
   ```

---

## 🔐 Email Setup (Important)

This project sends OTPs and bills via Gmail.

## 🚀 Future Enhancements

* Role-based login (Admin / Staff)
* Database integration (SQLite/MySQL)
* Encrypted customer data
* Sales analytics dashboard
* Cloud-based bill storage

---

## 👨‍💻 Author

**Sohan M**
Aspiring Software Developer | Python & GUI Enthusiast

This project reflects my approach to modular design, real-world logic implementation, and continuous learning through hands-on development.*

---

⭐ If you like this project, feel free to **star** the repository!
