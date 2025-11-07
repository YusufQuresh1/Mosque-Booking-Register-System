# Mosque Booking & Attendance System

A complete booking and attendance management system for a Mosque, built as an A-Level Computer Science project. It features separate user views ("Worshipper") and admin views ("Manager") and is built entirely in Python using Tkinter for the GUI and SQLite for the database.

## ✨ Features

The application is split into two distinct roles with different permissions:

### Worshipper (Standard User)
* Create a personal account with a unique login.
* Book a place for the upcoming Friday Jummah prayer.
* Log in and modify personal details (name, email, password, gender).

### Manager (Admin User)
* Access a separate, protected Manager Menu.
* Look up any user in the database by their `AccountID`.
* View all details for a user, including their attendance percentage.
* Promote users to 'Manager' or demote them to 'Worshipper'.
* View attendance records for all past events.
* Filter attendance lists by date or by individual person.
* Take the live attendance register for the day's Friday prayer.

## 🛠️ Technology Used

* **Python 3:** Core application logic.
* **Tkinter:** For all graphical user interface (GUI) windows and widgets.
* **SQLite3:** For all database storage (users, bookings, attendance).

## 🚀 How to Run

The required libraries (`tkinter`, `sqlite3`, `datetime`, `os`) are all part of the standard Python library, so no `pip install` is needed.

1.  Clone the repository (or download the `.py` file).
2.  Ensure you have Python 3 installed.
3.  Run the script from your terminal:
    ```bash
    python "mosque booking system 2.py"
    ```
4.  The database file (`mosque_database.db`) will be created automatically in the same directory.

## 🚨 IMPORTANT: Setting Up the First Admin Account

The system is designed so no admin accounts can be created from within the app. You must **manually** promote your first user to gain admin access.

1.  Run the program (`python "mosque booking system.py"`) and create a new account for yourself. This will be a "Worshipper" by default.
2.  Close the program.
3.  Open the newly created `mosque_database.db` file with a tool like [DB Browser for SQLite](https://sqlitebrowser.org/).
4.  Go to the "Execute SQL" tab and run the following command (this assumes your new user is `AccountID = 1`. If not, change the number).
    ```sql
    UPDATE Accounts 
    SET Role = 'Manager' 
    WHERE AccountID = 1;
    ```
5.  Click the **"Write Changes"** button (to save) in your DB tool.
6.  Done. You can now re-run the program and log in with that user to access the Manager Menu.

## ℹ️ Demonstration Note

For portfolio and demonstration purposes, two time-locks have been overridden in the code:

1.  **Booking:** The "Book Place" button is hardcoded to "Thursday" (`day=4`) to allow a booking to be made for the next day (Friday), bypassing the real-world "Booking is closed on Fridays" rule.
2.  **Register:** The Attendance Register is hardcoded to "Friday at 13:00" (`day=5`, `hour=13`) to allow a manager to *always* access and test the attendance-taking feature.

In a live production version, these hardcoded "FOR DEMO PURPOSES" lines would be removed to use the real system time.
