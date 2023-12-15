from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.errors import MessageError

from src.model.common.Config import Config
from src.model.email.SMTPFactory import SMTPFactory, SMTPServer

from src.model.exception.ModelException import ModelException

class Email():

    def __init__(self):
        config : Config = Config()

        try:
            self._file : str = config.get_str('GENERAL', 'FILE')

            self._smtp_user : str = config.get_str('SMTP', 'USER')
            self._smtp_password : str = config.get_str('SMTP', 'PASSWORD')

            self._email_from : str = config.get_str('EMAIL', 'FROM')
            self._email_to : str = config.get_str('EMAIL', 'TO')
            self._email_subject : str = config.get_str('EMAIL', 'SUBJECT')
            self._email_attachment : str = config.get_str('EMAIL', 'ATTACHMENT')
        except ModelException as e:
            raise ModelException(f'Error reading Email config: '+e.message)

    def _get_attachment(self) -> MIMEBase:
        try:
            attachment = open(self._file, "rb")        
            part : MIMEBase = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={self._email_attachment}')
            attachment.close()
            return part
        except FileNotFoundError as e:
            raise ModelException(f'Attached file {self._file} not found')
        except MessageError as e:
            raise ModelException(f'Error reading attached file to email')
        except Exception as e:
            raise ModelException('Unknow error getting attached file to email')

    def _compose_message(self) -> MIMEMultipart:
        try:
            msg : MIMEMultipart     = MIMEMultipart()
            msg['From'] = self._email_from
            msg['To'] = self._email_to
            msg['Subject'] = self._email_subject
            msg.attach(self._get_attachment())
            return msg
        except MessageError as e:
            raise ModelException(f'Error composing email')
        except Exception as e:
            raise ModelException('Unknow error composing email')

    def send(self) -> None:
        try:
            server : SMTPServer = SMTPFactory().get_smtp_server()
            server.login(self._smtp_user, self._smtp_password)
            text : str = self._compose_message().as_string()
            server.sendmail(self._email_from, self._email_to, text)
            server.quit()
        except MessageError as e:
            raise ModelException(f'Error sending email')
        except Exception as e:
            raise ModelException('Unknow error composing email')