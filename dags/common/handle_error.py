from model.logger import Logger
import traceback

def handle_error(func):
    logger = Logger()
    def runner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error when running task: `{func.__name__}` with error\n```{traceback.format_exc()}```")
            print(e)
            raise e
    runner.__name__ = func.__name__
    return runner