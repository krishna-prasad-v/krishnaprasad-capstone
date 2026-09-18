from pathlib import Path
import json
import logging

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

# Set the stream handler - if required.
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(json_formatter)

# Set the file path for the log file
    current_file_path = Path(__file__).resolve()
    src_folder = current_file_path.parent
    week2_folder = src_folder.parent
    log_file = week2_folder / "Logs" / "pipeline_starter.log"

# Set the file handler
    file_handler = logging.FileHandler(log_file, mode = 'w', encoding = 'utf-8')
    file_handler.setFormatter(json_formatter)

    logging.basicConfig(level=log_level, handlers=[file_handler])

# Silence 3rd-party library logs
    for prevent_logger in ["httpx", "httpx2", "httpcore", "httpcore2", "anthropic"]:
       logging.getLogger(prevent_logger).setLevel(logging.WARNING)