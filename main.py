import smtplib
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
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

def clear_text_input():
    text_input.delete('1.0', tk.END)
    e1.delete(0, tk.END)
    subj.delete(0, tk.END)
    attachment_label.config(text="No file selected")
    file_combobox["values"] = []
    file_combobox.set("")

def browse_file():
    file_paths = filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])
    if len(file_paths) == 0 and attachment_label["text"] == "No file selected":
        attachment_label.config(text="No file selected")
        file_combobox["values"] = []
    else:
        attachment_path = attachment_label["text"]
        if attachment_path!='No file selected':
            file_paths = [file_path for file_path in file_paths if file_path not in attachment_path.split(", ")]
            file_paths = (attachment_path.split(", ")) + file_paths
        file_combobox["values"] = [file_name.split('/')[-1] for file_name in file_paths]
        attachment_label.config(text=", ".join(file_paths))
        file_combobox.current(len(file_paths)-1)

def remove_file():
    selected_item = file_combobox.get()
    if len(selected_item)!=0:
        attachment_path = attachment_label["text"]
        attachment_path = attachment_path.split(", ")
        attachment_path = [path for path in attachment_path if path.split('/')[-1] != selected_item]
        attachment_label.config(text=", ".join(attachment_path))
        file_combobox["values"] = [file_name.split('/')[-1] for file_name in attachment_path]
        if(len(attachment_path)==0):
            file_combobox.set("")
            attachment_label.config(text="No file selected")
        else:
            file_combobox.current(0)
    else:
        messagebox.showerror("Error", "No file selected")

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# Store recent email recipients
recent_recipients = load_recent_recipients()
email = os.environ.get('email')
password = os.environ.get('pass')
def send_email():
    recipient = e1.get()
    if not is_valid_email(recipient):
        messagebox.showerror("Error", "Please enter a valid email address!")
        return
    subject = subj.get()
    content = text_input.get("1.0", tk.END).strip()

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(email, password)

            message = MIMEMultipart()
            message["From"] = email
            message["To"] = recipient
            message["Subject"] = subject

            # Attach the email content
            message.attach(MIMEText(content, "plain"))

            # Attach the file
            attachment_path = attachment_label["text"]
            if attachment_path!='No file selected':
                for path in attachment_path.split(", "):
                    with open(path, "rb") as attachment_file:
                        attachment = MIMEApplication(attachment_file.read())

                    attachment.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=os.path.basename(path)
                    )
                    message.attach(attachment)

            # Send the email
            server.send_message(message)
            messagebox.showinfo("Email Status", "Email sent successfully!")

            add_item(recipient)

            clear_text_input()

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
recipient_label.grid(row = 0,column=0,sticky='w',padx=(25,0))
e1_str = tk.StringVar()
e1 = tk.Entry(window, textvariable=e1_str, font=font1)
e1.grid(row=0,column=1,sticky="nsew",padx=(0,20))



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
l1.grid(row=2, column=1, sticky="nsew",padx=(0,20))
scrollbar = tk.Scrollbar(window, command=l1.yview)
scrollbar.grid(row=2, column=2, sticky="ns")
l1.configure(yscrollcommand=scrollbar.set)

e1.bind('<Down>', my_down)
l1.bind('<Return>', my_upd)
l1.bind('<Up>', my_up)
l1.bind('<ButtonRelease-1>', my_upd)
e1_str.trace('w', get_data)

subject = tk.Label(window, text="Subject:",anchor='w')
subject.grid(row = 3,column=0,sticky='w',padx=(25,0))
subj_str = tk.StringVar()
subj = tk.Entry(window, textvariable=subj_str, font=font1)
subj.grid(row=3,column=1,sticky="nsew",padx=(0,20),pady=(10,0))

# # Create a text input field for email content
text_label = tk.Label(window, text="Email Content:")
text_label.grid(row=4,column=0,pady=(10,0),sticky='w',padx=(25,0))
text_input = tk.Text(window,height=20)
text_input.grid(row=5,column=0, columnspan=2)


# Create a label to display the attachment file path
attachment_label = tk.Label(window, text="No file selected", anchor="w")
# attachment_label.grid(row=7, column=0, columnspan=2, sticky="w", padx=(25, 0))
style = ttk.Style()
style.configure("Custom.TButton", padding=(0,0,0,0), font=('Arial', 16),anchor='center')
style.map("Custom.TButton",
          foreground=[('pressed', 'black'), ('active', 'black'), ('!disabled', 'black')],
          background=[('pressed', '!disabled', 'white'), ('active', 'white')])


# # Create a button to browse and select a file
file_combobox = ttk.Combobox(window, state="readonly", font=font2, width=20)
file_combobox.grid(row=6, column=0, sticky='w',padx=(25,0),pady=(10,0))
browse_button = ttk.Button(window, text="📎", command=browse_file,style='Custom.TButton',width=3)
browse_button.grid(row=6, column=1, pady=(10, 0),sticky='w',padx=(0,0))
browse_button.configure(compound='center')
dlt_button = ttk.Button(window, text="❌", command=remove_file,style='Custom.TButton',width=3)
dlt_button.grid(row=6, column=1, pady=(10, 0),sticky='w',padx=(50,0))
dlt_button.configure(compound='center')

# remove_button = tk.Button(window, text="Remove Attachments", command=remove_attachments)
# remove_button.grid(row=8, column=1, pady=(10, 0))

# # Create a button to send the email
send_button = tk.Button(window, text="Send Email", command=send_email,bd='5',anchor='e')
send_button.grid(row=6,column=1,pady=(10,0),columnspan=2,sticky='e',padx=10)

hide_listbox()

# Start the Tkinter event loop
window.mainloop()
