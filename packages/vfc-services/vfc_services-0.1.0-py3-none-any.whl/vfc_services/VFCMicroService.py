import os


class VFCMicroService:
    AUTH_MANAGER = os.getenv('AUTH_MANAGER', 'http://localhost:8082')
    TRACKER_MANAGER = os.getenv('TRACKER_MANAGER', 'http://localhost:8084')
    COACHING_MANAGER = os.getenv('COACHING_MANAGER', 'http://localhost:8080')
    PREDICTION_MANAGER = os.getenv('PREDICTION_MANAGER', 'http://localhost:8086')
