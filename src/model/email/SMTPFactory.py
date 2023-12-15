import smtplib
from typing import TypeAlias

from src.model.common.Config import Config
from src.model.exception.ModelException import ModelException

SMTPServer : TypeAlias = [smtplib.SMTP | smtplib.SMTP_SSL]

class SMTPFactory():

    def __new__(cls):
        if not hasattr(cls, '_singleton'):
            cls._singleton = super(SMTPFactory, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        if not hasattr(self, '_smtp_type'):
            config : Config = Config()
            try:
                self._smtp_type: str = config.get_str('SMTP', 'TYPE')
                self._smtp_server: str = config.get_str('SMTP', 'SERVER')
                self._smtp_port: int = config.get_int('SMTP', 'PORT')
            except ModelException as e:
                raise ModelException(f'Error reading SMTP configs: '+e.message)

    def get_smtp_server(self) -> SMTPServer:
        instance : SMTPServer = None
        try:
            match self._smtp_type:
                case 'SSL':
                    instance = smtplib.SMTP_SSL(self._smtp_server, self._smtp_port)
                case 'TLS':
                    instance = smtplib.SMTP(self._smtp_server, self._smtp_port)
                    instance.starttls()
                case other:
                    instance = smtplib.SMTP(self._smtp_server, self._smtp_port)
            return instance
        except smtplib.SMTPConnectError as e:
            raise ModelException(f'Error connecting to {self._smtp_type} SMTP server {self._smtp_server} \
                                 at port {self._smtp_port}')
        except Exception as e:
            raise ModelException("Unknown error getting SMTP server")