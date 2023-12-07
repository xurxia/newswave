import smtplib

from src.model.common.Config import Config

class SMTPFactory():

    def __new__(cls):
        if not hasattr(cls, '_singleton'):
            cls._singleton = super(SMTPFactory, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        if not hasattr(self, '_smtp_type'):
            config = Config()
            self._smtp_type: str = config.get_str('SMTP', 'TYPE')
            self._smtp_server: str = config.get_str('SMTP', 'SERVER')
            self._smtp_port: int = config.get_int('SMTP', 'PORT')

    def get_smtp_server(self) -> [smtplib.SMTP | smtplib.SMTP_SSL]:
        match self._smtp_type:
            case 'SSL':
                instance = smtplib.SMTP_SSL(self._smtp_server, self._smtp_port)
            case 'TLS':
                instance = smtplib.SMTP(self._smtp_server, self._smtp_port)
                instance.starttls()
            case other:
                instance = smtplib.SMTP(self._smtp_server, self._smtp_port)
        return instance