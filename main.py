from src.model.parser.Parser import Parser
from src.model.email.Email import Email
from src.model.common.Config import Config

import sys

if __name__ == '__main__':
    config_file : str = './src/config/config.ini'
    if len(sys.argv)==2:
        config_file = sys.argv[1]
        
    config : Config = Config(file=config_file)
    parser : Parser = Parser()
    email : Email = Email()
    
    html : str = parser.process()
    email.send(html)