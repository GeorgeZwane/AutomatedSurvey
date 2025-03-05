import pdfplumber
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def extract_student_numbers(pdf_path):
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        student_emails = []
        
        # Loop through each page of the PDF
        for page in pdf.pages:
            text = page.extract_text()
            
            # If text extraction is successful
            if text:
                # Use a regular expression to find student numbers 
                # Adjust the regex to fit the student number format
                student_numbers = re.findall(r'\b\d{9}\b', text)  # Student number is 9 digits long 
                
                for student_number in student_numbers:
                    # Append @student.uj.ac.za to each student number
                    email = f"{student_number}@student.uj.ac.za"
                    student_emails.append(email)
                    
        return student_emails

def send_email(recipient_email, subject, body, sender_email, sender_password):
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    try:
        # Log in to the server using your Gmail account
        server.login(sender_email, sender_password)
        
        # Create the email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
    finally:
        server.quit()


pdf_path = ''
emails = extract_student_numbers(pdf_path)

# Google Form link to be sent to each student
google_form_link = " "

# Email subject and body
subject = "Textbook Rental Survey"
body = f"Dear Student,\n\nPlease take a moment to complete the following survey regarding textbook rentals: {google_form_link}\n\nThank you!"

# Email account details
sender_email = "" # The senders email address
sender_password = ""  # If you're using Gmail with 2FA, you'll need an app-specific password

# Send the email to all extracted student emails
for email in emails:
    print(email)
    send_email(email, subject, body, sender_email, sender_password)
