from loguru import logger
import os


os.makedirs("logs", exist_ok=True)

logger.remove()  
logger.add(
    "logs/app.log",
    rotation="1 day",  
    level="INFO",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
)


logger.add(lambda msg: print(msg, end=""), level="DEBUG")


app_logger = logger
