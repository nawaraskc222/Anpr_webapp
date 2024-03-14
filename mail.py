import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = "nawaras.kc@aiesec.net"
receiver_email = "fimenat857@hdrlog.com"
password = "demooo"

# Create a multipart message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Test email from Python"

# Add body to email
body = "This is a test email sent from Python."
message.attach(MIMEText(body, "plain"))

# Connect to the SMTP server
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    text = message.as_string()
    # Send email
    server.sendmail(sender_email, receiver_email, text)
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Disconnect from the server
    server.quit()
