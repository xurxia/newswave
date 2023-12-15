from src.model.common.Config import Config
from src.model.exception.ModelException import ModelException
from src.controller.controller import app

if __name__ == '__main__':
    try:
        config = Config()
        port = config.get_int('SERVER', 'PORT')
        app.run(debug=True, port=port)
    except ModelException as e:
        raise ModelException('Error reading server config: '+e)
    except Exception as e:
        raise e