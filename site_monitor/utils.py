import os
import logging

REQUEST_TIMEOUT = 10  # Пауза между запросами в секундах
PAUSE_BETWEEN_CHECKS = 30  # Пауза между проверками в секундах
MONITORING_DAYS = 1  # Продолжительность мониторинга в днях
MONITORING_DURATION = MONITORING_DAYS * 86400  # Продолжительность мониторинга в секундах (24 часа)

LOG_FILE = 'site_availability.log'
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE) 
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
