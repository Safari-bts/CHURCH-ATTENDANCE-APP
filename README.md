# CHURCH ATTENDANCE APP

A simple Flask application for managing church attendance records, user authentication, and data visualization.

## Features

*   **User Authentication:** Secure login and registration for users.
*   **Attendance Tracking:** Record attendance for various services or events.
*   **User Management:** Add, edit, and delete user accounts.
*   **Data Visualization:** View attendance data through interactive charts.
*   **Data Export:** Export attendance records to an Excel file.

## Setup Instructions

Follow these steps to set up and run the application locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Safari-bts/CHURCH-ATTENDANCE-APP
cd "CHURCH ATTENDANCE APP"
```

*(Note: Replace `<repository_url>` with the actual URL of your Git repository if applicable. If you downloaded the project, you can skip this step.)*

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

*   **On Linux/macOS:**

    ```bash
    source venv/bin/activate
    ```

*   **On Windows:**

    ```bash
    .\venv\Scripts\activate
    ```

### 4. Install Dependencies

```bash
pip install Flask pandas openpyxl matplotlib
```

### 5. Initialize Data Files

The application uses `users.json` and `attendance.json` for data storage. Ensure these files exist in the root directory. If they don't, create them as empty JSON arrays:

*   `users.json`:
    ```json
    []
    ```
*   `attendance.json`:
    ```json
    []
    ```

### 6. Run the Application

```bash
flask run
```

The application will typically run on `http://127.0.0.1:5000/`.

## Usage

1.  **Register:** Create a new user account.
2.  **Login:** Log in with your registered credentials.
3.  **Manage Attendance:** Record attendance, view records, and edit entries.
4.  **View Charts:** Access the chart page to visualize attendance data.
5.  **Export Data:** Use the export feature to download attendance records.

## Technologies Used

*   **Flask:** Web framework
*   **HTML/CSS/JavaScript:** Frontend developmentgemi22
*   **Pandas:** Data manipulation (inferred for Excel export and data processing)
*   **Openpyxl:** Reading and writing Excel files (inferred for Excel export)
*   **Matplotlib (or similar library):** Charting (inferred for data visualization)
*   **JSON:** Data storage