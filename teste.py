from app import *
from sqlalchemy import text
import pandas as pd
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

pwd = '123'
hashed_pwd = generate_password_hash(pwd, method="SHA256")
h = f"'{hashed_pwd}'"
print(check_password_hash(h.replace("'", ""), pwd))