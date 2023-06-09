# TkinterMailer

This is a simple Python application built using the Tkinter library for sending emails. The application allows users to compose and send emails, upload multiple files, and manage recipients. It provides suggestions for email addresses, a subject field, and a text window for entering the body of the email.

## Features

- Email address suggestions: The application suggests email addresses based on previous entries, making it convenient for users to select recipients.
- Subject field: Users can specify the subject of the email.
- Body text entry: A text window is provided for users to enter the main content of the email.
- File upload: Users can upload multiple files to attach them to the email.
- File removal: The uploaded file names are displayed in a combobox, allowing users to select and remove files if needed.
- Email verification before sending

## Requirements

- Python
- Tkinter library (usually included in standard Python installations)
- SMTP library (usually included in standard Python installations)
- re library (usually included in standard Python installations)
- os library (usually included in standard Python installations)
- dotenv library
- email library (usually included in standard Python installations)

## Installation

1. Clone the repository or download the source code.
```
git clone https://github.com/aryanda1/TkinterMailer.git
```
2. Install the required dependencies using pip:
```
pip install -r requirements.txt
```
3. Obtain an app password from Google to authenticate your email account. You can follow Google's instructions on how to generate an app password.

## Configuration

1. Create a `.env` file.
2. Open the `.env` file and add the following variables:
- email = YOUR GMAIL ADDRESS
- pass = YOUR APP PASSWORD GENERATED ABOVE

## Usage

Run the application by executing the `main.py` file:
```
  python main.py
```
