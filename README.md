# Wedlock Wonders

An all-in-one online wedding management platform designed to simplify planning and make your big day stress-free.

## 📂 Project Structure

The repository contains the following key components:

* **`app.py`**: The main application file that runs the Flask web server.
* **`requirements.txt`**: Lists all the Python dependencies required to run the project.
* **`static/`**: Contains static files like CSS, JavaScript, and images.
* **`templates/`**: Holds the HTML templates rendered by Flask.
* **`sql/schema.sql`**: Contains the SQL queries to create the necessary database and tables for the application.
* **`README.md`**: This file, providing an overview of the project.

## 🚀 Installation

To run Wedlock Wonders locally:

1.  Clone the repository:

    ```bash
    git clone https://github.com/vamshi-afk/wedlock-wonders.git
    ```

2.  Navigate into the project directory:

    ```bash
    cd wedlock-wonders
    ```

3.  **Database Setup:**
    * Ensure you have MySQL installed and running.
    * Open your MySQL client (e.g., MySQL Command Line Client, MySQL Workbench, phpMyAdmin).
    * Execute the queries in `sql/schema.sql` to create the `wedlockwonders` database and its tables.
      
        ```bash
        # From your terminal, assuming you are in the project root
        mysql -u your_username -p < sql/schema.sql
        # (Enter your MySQL password when prompted)
        ```
        
    * **Important:** Update the `user` and `password` in the `get_db_connection()` function in `app.py` to match your MySQL credentials.

4.  Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5.  Run the application:

    ```bash
    python app.py
    ```

The application will start on `http://127.0.0.1:5000/` by default.

## 📝 About

**Wedlock Wonders** is a Database Management System (DBMS) project aimed at creating a comprehensive platform for managing wedding events. It allows users to plan and organize various aspects of a wedding, ensuring a seamless experience.

## 🛠️ Tech Stack

* **Frontend**: HTML, CSS, JavaScript
* **Backend**: Python (Flask)
* **Database**: MySQL
* **Architecture**: Modular design with ER diagrams and database schema.

## Acknowledgment

This project was completed in collaboration with [@srikark7](https://github.com/srikark7), and [@allureddy985](https://github.com/allureddy985), who each contributed significantly to its development.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
