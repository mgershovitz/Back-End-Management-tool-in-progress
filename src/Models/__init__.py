from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getEnvVar('SECRET_KEY')

from src.Models import routes
from src.Models import utils
from src.Models.DB import db

# insert hospital statistic to the my_db
db.read_data_from_csv('total_statistic.csv')

# print all the docs in hospital collection
for doc in db.my_db.hospital_statistic_col.find():
    print(doc)
