from src.model.parser.Parser import Parser
from src.model.email.Email import Email
from src.model.common.Config import Config

if __name__ == '__main__':
    parser = Parser()
    email = Email()
    
    parser.process()
    email.send()