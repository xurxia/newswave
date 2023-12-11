import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.model.common.Config import Config
from src.model.email.SMTPFactory import SMTPFactory, SMTPServer

class Email():

    def __init__(self):
        config : Config = Config()

        self._file : str = config.get_str('GENERAL', 'FILE')

        self._smtp_user : str = config.get_str('SMTP', 'USER')
        self._smtp_password : str = config.get_str('SMTP', 'PASSWORD')

        self._email_from : str = config.get_str('EMAIL', 'FROM')
        self._email_to : str = config.get_str('EMAIL', 'TO')
        self._email_subject : str = config.get_str('EMAIL', 'SUBJECT')
        self._email_attachment : str = config.get_str('EMAIL', 'ATTACHMENT')

    def _get_attachment(self) -> MIMEBase:
        attachment = open(self._file, "rb")
        part : MIMEBase = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={self._email_attachment}')
        attachment.close()
        return part

    def _compose_message(self) -> MIMEMultipart:
        msg : MIMEMultipart     = MIMEMultipart()
        msg['From'] = self._email_from
        msg['To'] = self._email_to
        msg['Subject'] = self._email_subject
        msg.attach(self._get_attachment())
        return msg

    def send(self) -> None:
        server : SMTPServer = SMTPFactory().get_smtp_server()
        server.login(self._smtp_user, self._smtp_password)
        text : str = self._compose_message().as_string()
        server.sendmail(self._email_from, self._email_to, text)
        server.quit()