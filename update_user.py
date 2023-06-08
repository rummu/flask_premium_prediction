from flask import Flask ,render_template , request
import pandas as pd
import numpy as np
import pickle
import json
import matplotlib.pyplot as plt
import time
import urllib.parse

from flask_cors import CORS
from imblearn.under_sampling import RandomUnderSampler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import OneHotEncoder


pd.set_option('display.max_columns', None)


app = Flask(__name__)
CORS(app)



@app.route("/")
def home():
     return "<h1 style='color:blue'>Hello pycharm!</h1>"



@app.route('/test',methods = ['GET','POST'])
def test1():
     return str(2)



@app.route('/update_user',methods = ['GET','POST'])
def test2():
     df = pd.read_csv('premium_update.csv',encoding='utf-8')
     # print(df[['member_id','age']])
     # print(len(df))

     #Request data and decode
     data = request.form['user_data']
     data = json.loads(data)
     # print(data['member_id'])

     user = pd.DataFrame()
     
     user["member_id"] = [int(data['member_id'])]
     

     try: 
          if(data["gender"]==""):
               user["gender"] = [np.nan]
          else:
              user["gender"] = [data['gender']]
     except:
          user['gender'] = [np.nan]

     try: 
          if(data["age"]==""):
               user["age"] = [20]
          else:
              user["age"] = [data['age']]
     except:
          user['age'] = [20]

     try: 
          if(data["marital_status"]==""):
               user["marital_status"] = [np.nan]
          else:
              user["marital_status"] = [data['marital_status']]
     except:
          user['marital_status'] = [np.nan]

     try: 
          if(data["marital_status"]==""):
               user["marital_status"] = [np.nan]
          else:
              user["marital_status"] = [data['marital_status']]
     except:
          user['marital_status'] = [np.nan]
     
     try: 
          if(data["on_behalf"]==""):
               user["on_behalf"] = [np.nan]
          else:
              user["on_behalf"] = [data['on_behalf']]
     except:
          user['on_behalf'] = [np.nan]
     
     try: 
          if(data["ads"]==""):
               user["ads"] = [np.nan]
          else:
              user["ads"] = [urllib.parse.unquote(data['ads'])]
     except:
          user['ads'] = [np.nan]

     try: 
          if(data["present_state"]==""):
               user["present_state"] = [np.nan]
          else:
              user["present_state"] = [data['present_state']]
     except:
          user['present_state'] = [np.nan]

     try: 
          if(data["highest_education"]==""):
               user["highest_education"] = [np.nan]
          else:
              user["highest_education"] = [data['highest_education']]
     except:
          user['highest_education'] = [np.nan]
     
     try: 
          if(data["occupation"]==""):
               user["occupation"] = [np.nan]
          else:
              user["occupation"] = [data['occupation']]
     except:
          user['occupation'] = [np.nan]
     
     try: 
          if(data["employed"]==""):
               user["employed"] = [np.nan]
          elif(data['employed']=="Government/Public Sector"):
               user['employed'] = ["Government/Public Sect"]
          else:
              user["employed"] = [data['employed']]
     except:
          user['employed'] = [np.nan]
     
     try: 
          if(data["caste"]==""):
               user["caste"] = [np.nan]
          else:
              user["caste"] = [data['caste']]
     except:
          user['caste'] = [np.nan]

     try: 
          if(data["sect"]==""):
               user["sect"] = [np.nan]
          else:
              user["sect"] = [data['sect']]
     except:
          user['sect'] = [np.nan]
     
     try: 
          if(data["family_type"]==""):
               user["family_type"] = [np.nan]
          else:
              user["family_type"] = [data['family_type']]
     except:
          user['family_type'] = [np.nan]

     try: 
          if(data["platform"]==""):
               user["platform"] = [np.nan]
          else:
              user["platform"] = [data['platform']]
     except:
          user['platform'] = [np.nan]

     try: 
          if(data["income_rs"]==""):
               user["income_rs"] = [np.nan]
          else:
              user["income_rs"] = [data['income_rs']]
     except:
          user['income_rs'] = [np.nan]


     
     try: 
          if(data["ads"]==""):
               user["ads"] = [np.nan]
          else:
              user["ads"] = [data['ads']]
     except:
          user['ads'] = [np.nan]
     
     
     #Delete if Exist
     df = df[~df['member_id'].isin(user['member_id'])]
     df = pd.concat([df, user], ignore_index=True)
    

     df = df.sort_values('member_id')
     full_data = df.reset_index(drop=True)
     # end_time = time.time()
     # print(end_time-start_time)

     full_data.to_csv('premium_update.csv',index=False)

     return "Data Updated Successfully"




if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)



