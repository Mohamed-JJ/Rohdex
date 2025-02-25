from imap_tools import MailBox, MailMessage, A
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, List

class EmailReader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmailReader, cls).__new__(cls)
            load_dotenv()
            cls._instance.imap_server = os.getenv('IMAP_SERVER')
            cls._instance.email_user = os.getenv('EMAIL_USER')
            cls._instance.email_pass = os.getenv('EMAIL_PASS')
            cls._instance.mailbox = None
            cls._instance.connect()
        return cls._instance

    def connect(self):
        self.mailbox = MailBox(self.imap_server)
        self.mailbox.login(self.email_user, self.email_pass)

    def fetch_emails(self, since: datetime, until: datetime, folder='INBOX')-> List[MailMessage]:
        """
    Fetch emails from specified folder within given date range.
    
    Args:
        folder (str): Name of the mailbox folder to fetch from
        since (datetime): Start date for email fetch
        until (datetime): End date for email fetch
        
    Returns:
        list(dict): List of parsed email dictionaries
        """
        criteria = A(date_gte=since.date(), date_lt=until.date())
        emails = []
        for msg in self.mailbox.fetch(criteria=criteria, reverse=True, mark_seen=False):  # Fetch the last 30 emails
            print("the subjct is :", msg.subject)
            emails.append(msg)
        return emails

    def parse_email(self, msg: MailMessage):
        return {
            'From': msg.from_,
            'Subject': msg.subject,
            'Date': msg.date,
            # 'Body': msg.text,  # or msg.html for HTML content
        }

    def logout(self):
        self.mailbox.logout()

# Example usage:
# email_reader = EmailReader()
# emails = email_reader.fetch_emails()
# for email in emails:
#     print(email)
# email_reader.logout()