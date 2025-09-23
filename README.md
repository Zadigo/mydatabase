# My Database

An application that transforms any Google Sheet or Excel Sheet into a database.

## Features 🌳
- Import data from Google Sheets or Excel files
- Automatically create database tables and fields
- Map spreadsheet columns to database fields
- Support for multiple data types (text, number, date, etc.)
- User-friendly interface for managing your database
- Link your databases with modern applications and services like Zapier, Make, Airtable and Supabase

## Getting Started 🚀

1. Clone the repository
2. Install dependencies
3. Run the application
4. Connect to your Google Sheets or Excel files
5. Start transforming your data into a database!

## Technologies Used 🛠 

| Technology | version |
| --- | --- |
| Nuxt 4 | ✅ 4.0.0 |
| Python (Django) | ✅ 4.0.0 |
| Celery + Redis | ✅ 5.2.0 |
| Tailwindcss | ✅ 3.0.0 |
| Volt (PrimeVue) | ✅ 3.0.0 |

### How it is built? 🛖

The application uses websocket to communicate and exchange data between the frontend and backend in real-time for
building the databases. This allows for quick data manipulation during construction.

## How it works? 🔍

1. User uploads a Google Sheets or Excel file.
2. The application reads the file and extracts the data.
3. The user maps the spreadsheet columns to database fields.
4. The application creates the database schema and imports the data.
5. The user can then query and manage the data through the application interface.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
