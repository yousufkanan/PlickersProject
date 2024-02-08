import smtplib
import ssl
from email.message import EmailMessage
import time
import imghdr
import numpy as np
import csv
import time
import random
import os
import dotenv

dotenv.load_dotenv()

email_sender = 'ykanan2004@gmail.com'
email_password = os.environ.get('EMAIL_PASSWORD')
email_receiver = ["ahyaya3@gmail.com", "kanany@moravian.edu"]
subject = "Plickers Card"

body_template = """Hello,
Attached below is your Plickers card for the DevOps class.
Please use it as needed.
Thank you,
Yousuf Kanan
"""

# Base folder containing the Plickers files
folder_path = 'Plickers'

# Example mapping plickernumber to each email_receiver
# This is a basic example assuming sequential assignment or you can define it as needed
plicker_numbers = {email_receiver[i]: i+1 for i in range(len(email_receiver))}
print(plicker_numbers)
number = 1
for i, email in enumerate(email_receiver):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email
    em['Subject'] = subject
    em.set_content(body_template)
    
    # Construct file path based on the plicker number
    plicker_number = plicker_numbers[email]
    file_path = os.path.join(folder_path, f"plicker-{plicker_number}")
    
    # Assuming files might not have a standard extension, we try to find the file by prefix
    for file in os.listdir(folder_path):
        if file.startswith(f"plicker-0{plicker_number}") or file.startswith(f"plicker-{plicker_number}"):
            full_file_path = os.path.join(folder_path, file)
            with open(full_file_path, 'rb') as file:
                file_data = file.read()
                file_type = imghdr.what(file.name)
                file_name = file.name
                
                if file_type:
                    em.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
                else:
                    # For non-image files, adjust maintype/subtype if known
                    em.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

            break  # Found the file, no need to continue the loop

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

    time.sleep(1)  # Adjust the sleep time as needed
