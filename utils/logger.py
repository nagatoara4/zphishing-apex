#!/usr/bin/env python3
"""
ZPHISHING APEX — Logger
"""

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Setup logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create logs directory
    os.makedirs('logs', exist_ok=True)

    # File handler
    file_handler = RotatingFileHandler(
        f'logs/{name}.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
