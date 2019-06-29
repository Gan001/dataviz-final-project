from sqlalchemy import create_engine
from config import password
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from JPML import KNN
app = Flask(__name__)
#Connect to local database
rds_connection_string = f"root:{password}@localhost/jpdata"
engine = create_engine(f'mysql://{rds_connection_string}')
#Select X,y
X = pd.read_sql_query('select current_week,day_of_week,encode_air_area_name from jpdata_table', con=engine)
y = pd.read_sql_query('select visitors from jpdata_table', con=engine)
#Build KNN model
model = KNN(X,y)

@app.route("/")
def index():
   #Return to Home

   return render_template('index.html')

@app.route("/analysis")
def analysis():

    df = pd.read_csv('encode_unique.csv')

    return render_template("analysis.html")

@app.route("/services")
def service():
   #TEST small number
   service = pd.read_sql_query('select * from jpdata_table limit 100', con=engine)
   data = {
       "current_week": service.current_week.tolist(),
       "day_of_week": service.day_of_week.tolist(),
       "visitors": service.visitors.tolist(),
       "encode_air_area_name": service.encode_air_area_name.tolist(),
   }
   
   return jsonify(model.score())

@app.route("/metadata/<sample>")
def sample_metadata(sample):
   """Return the MetaData for a given sample."""
   sel = [
       Samples_Metadata.sample,
       Samples_Metadata.ETHNICITY,
       Samples_Metadata.GENDER,
       Samples_Metadata.AGE,
       Samples_Metadata.LOCATION,
       Samples_Metadata.BBTYPE,
       Samples_Metadata.WFREQ,
   ]

   results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

   # Create a dictionary entry for each row of metadata information
   sample_metadata = {}
   for result in results:
       sample_metadata["sample"] = result[0]
       sample_metadata["ETHNICITY"] = result[1]
       sample_metadata["GENDER"] = result[2]
       sample_metadata["AGE"] = result[3]
       sample_metadata["LOCATION"] = result[4]
       sample_metadata["BBTYPE"] = result[5]
       sample_metadata["WFREQ"] = result[6]

   print(sample_metadata)
   return jsonify(sample_metadata)

if __name__ == "__main__":
   app.run()