from model.logger import Logger
from model.config import Config
import traceback

def handle_error(func):
    logger = Logger()
    config = Config()
    def runner(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logger.info(f"Run task: `{func.__name__}` successfully")
        except Exception as e:
            logger.error(f"Error when running task: `{func.__name__}` with error\n```{traceback.format_exc()}```env: `{config.get('ENV')}`")
            raise e
    runner.__name__ = func.__name__
    return runner