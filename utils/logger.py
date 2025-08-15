import logging

def get_logger(name="qa_logger", log_file="test_results.log"):
    logger = logging.getLogger(name)
    if not logger.handlers:  # Avoid duplicate logs
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file, mode='w')
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
