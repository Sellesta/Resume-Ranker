import os

# MySQL Database Configuration
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "yourpassword"
MYSQL_DB = "resume_matcher"

# Security Key for Sessions
SECRET_KEY = os.urandom(24)
