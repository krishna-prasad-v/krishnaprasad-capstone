import json
import logging
import os

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            # "module": record.module,
            # "funcName": record.funcName,
            # "lineno": record.lineno,
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)

# define a function to set up logging with the JSON formatter    
def configure_logging(log_level=logging.WARNING):
    json_formatter = JsonFormatter(datefmt="%Y-%m-%d %H:%M:%S")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(json_formatter)

    file_handler = logging.FileHandler("pipeline_starter.log", mode = 'w')
    file_handler.setFormatter(json_formatter)

    logging.basicConfig(level=log_level, handlers=[file_handler])

     # Silence verbose 3rd-party library logs
    for stop_logger in ["httpx", "httpx2", "httpcore", "httpcore2", "anthropic"]:
       logging.getLogger(stop_logger).setLevel(logging.WARNING)