import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email config
sender_email = input("Enter your email address: ")
sender_password = input("Enter your email password: ")
recipient_email = input("Enter recipient email address: ")

# File upload and email sending
def send_email_with_attachment(file_path):
    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "File Sharing Bot - New File Uploaded"

    # Add the message body
    body = "A new file has been uploaded. Please find the attached file."
    message.attach(MIMEText(body, "plain"))

    # Add the file attachment
    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(file_path)}")
    message.attach(part)

    # Send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender_email, sender_password)
        smtp.send_message(message)
    print("Email sent successfully.")

# File upload and storage
def upload_file():
    file_path = input("Enter the file path: ")
    if os.path.exists(file_path):
        # Store the file in a designated folder
        destination_folder = "file_storage"
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        destination_path = os.path.join(destination_folder, os.path.basename(file_path))
        os.rename(file_path, destination_path)

        # Send email with the file information
        send_email_with_attachment(destination_path)
    else:
        print("File not found.")

# Main program
upload_file()