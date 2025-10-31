
import base64
import os.path
import datetime
import mimetypes
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage
from email.utils import make_msgid
from email.charset import Charset
import pytz
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/calendar.events.owned"
    ]

def send_email(subject, message, attachments, to):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(BASE_DIR /"token.json"):
        creds = Credentials.from_authorized_user_file(BASE_DIR / "token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                BASE_DIR / "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(BASE_DIR / "token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        #Create Message
        message_text = MIMEText(message, 'text')
        message_html = MIMEText(message, 'html')
        mime_message = EmailMessage()
        mime_message.set_charset(Charset('utf-8'))
        mime_message.set_content(message_html)
        #mime_message.add_alternative(message_html)
        mime_message["To"] = to
        mime_message["From"] = "inovacaoead@unifil.br"
        mime_message["Subject"] = subject
        # Add Attachment# attachment
        # guessing the MIME type
        if attachments:
            print(BASE_DIR)
            attachment_filename = BASE_DIR / "static/pdf" / attachments
            print(attachments)
            print(attachment_filename)
            type_subtype, _ = mimetypes.guess_type(attachment_filename)
            maintype, subtype = type_subtype.split("/")
            with open(attachment_filename, "rb") as fp:
                attachment_data = fp.read()
            mime_message.add_attachment(attachment_data, maintype=maintype, subtype=subtype, filename=attachments)
        # encoded message
        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (service
                        .users()
                        .messages()
                        .send(userId='me',body=create_message)
                        .execute())
        print(f'Message Id: {send_message["id"]}')
        return "Ok"

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
        return "Error"
    
def define_student_email(ebook):
    
    html = open(BASE_DIR / "templates/student_email.html", encoding='utf-8').read()
    #print(html)
    html = ebook.join(html.split("-ebook-"))
    return html   
