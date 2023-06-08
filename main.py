import smtplib
import tkinter as tk
from tkinter import messagebox
import re
from dotenv import load_dotenv
import os

load_dotenv()

# File path to store recent recipients
RECIPIENTS_FILE = "recent_recipients.txt"

# Load recent recipients from file
def load_recent_recipients():
    try:
        with open(RECIPIENTS_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Save recent recipients to file
def add_item(recipient):
    if recipient not in recent_recipients:
        recent_recipients.append(recipient)
        with open(RECIPIENTS_FILE, "w") as file:
            file.write("\n".join(recent_recipients))
        # entry_new_item.delete(0, tk.END)
        # update_listbox_height()

# Store recent email recipients
recent_recipients = load_recent_recipients()
email = os.environ.get('email')
password = os.environ.get('pass')
def send_email():
    recipient = e1.get()
    content = text_input.get("1.0", tk.END).strip()

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(email, password)

            server.sendmail('', recipient, f'Subject: Code Example\n\n{content}')
            messagebox.showinfo("Email Status", "Email sent successfully!")

            add_item(recipient)


            # Refresh the listbox with similar email recipients
            # refresh_listbox()
            hide_listbox()
            text_input.delete('1.0', tk.END)
            # Clear the recipient input field
            e1.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Email Status", f"Error sending email: {str(e)}")


# Create a Tkinter window
window = tk.Tk()
window.title("Email Sender")
# window.geometry("500x500")

# Set the window position
x_pos = 500
y_pos = 100
window.geometry(f"+{x_pos}+{y_pos}")
font1 = ("Arial", 24, "bold")
font2 = ("Arial", 12)
# Create an autocomplete entry for recipient email
recipient_label = tk.Label(window, text="Recipient Email:")
recipient_label.grid(row = 0,column=1)
e1_str = tk.StringVar()
e1 = tk.Entry(window, textvariable=e1_str, font=font1)
e1.grid(row=1,column=1,sticky="nsew",padx=100)

def my_down(event):
    l1.focus()
    l1.selection_set(0)


def my_up(event):
    selected_indices = l1.curselection()
    if selected_indices:
        index = int(selected_indices[0])
        if index > 0:
            l1.selection_clear(0, tk.END)
            l1.selection_set(index - 1)
            l1.activate(index - 1)
            l1.see(index - 1)
        else:
            e1.focus()

def my_upd(event):
    if event.widget == l1:
        selected_indices = l1.curselection()
        # update_listbox_height()

        index = int(selected_indices[0])
        value = l1.get(index)
        e1_str.set(value)
        l1.config(height=0)
        l1.delete(0, tk.END)
        e1.focus()
        e1.icursor(tk.END)
    else:
        search_term = e1.get()
        l1.delete(0, tk.END)
        cnt = 0
        for item in recent_recipients:
            if re.match(search_term, item, re.IGNORECASE):
                l1.insert(tk.END, item)
                cnt += 1
        l1.config(height=min(4, cnt))
    hide_listbox()

def get_data(*args):
    search_term = e1.get()
    l1.delete(0, tk.END)
    hide_listbox()
    if(len(search_term)!=0):
        visible_listbox()
        cnt = 0
        for item in recent_recipients:
            if re.match(search_term, item, re.IGNORECASE):
                l1.insert(tk.END, item)
                cnt+=1
        if(cnt==0) :
            hide_listbox()
        else:
            l1.config(height=min(4,cnt))


def hide_listbox():
    scrollbar.grid_remove()
    l1.grid_remove()
def visible_listbox():
    l1.grid()
    scrollbar.grid()

l1_height = 0  # Set the initial height based on the length of my_list
l1 = tk.Listbox(window, height=l1_height, font=font2, relief='groove', bg='SystemButtonFace', highlightcolor='SystemButtonFace')
l1.grid(row=2, column=1, sticky="nsew",padx=100)
scrollbar = tk.Scrollbar(window, command=l1.yview)
scrollbar.grid(row=2, column=3, sticky="ns")
l1.configure(yscrollcommand=scrollbar.set)

e1.bind('<Down>', my_down)
l1.bind('<Return>', my_upd)
l1.bind('<Up>', my_up)
l1.bind('<ButtonRelease-1>', my_upd)
e1_str.trace('w', get_data)


# # Create a text input field for email content
text_label = tk.Label(window, text="Email Content:")
text_label.grid(row=3,column=1,pady=(10,0))
text_input = tk.Text(window,height=20)
text_input.grid(row=4,column=1)

# # Create a button to send the email
send_button = tk.Button(window, text="Send Email", command=send_email)
send_button.grid(row=5,column=1,pady=10)

hide_listbox()

# Start the Tkinter event loop
window.mainloop()
