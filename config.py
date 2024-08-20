import os
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    # Add other configuration variables here if needed