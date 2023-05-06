from flask import Flask ,render_template , request
import pandas as pd
import numpy as np
import pickle
import json
from flask_cors import CORS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)



app = Flask(__name__)
CORS(app)



@app.route("/")
def home():
     return "<h1 style='color:blue'>Hello pycharm!</h1>"


@app.route('/test',methods = ['GET','POST'])
def test1():
     return str(2)


@app.route('/premium_percent',methods = ['GET','POST'])
def test():


     #Request data and decode
     # data = request.form['user_data']
     # data = json.loads(data)

     # user = pd.DataFrame()

     # try: 
     #      user["gender"] = [data['gender']]
     # except:
     #      user['gender'] = [np.nan]
     
     # try: 
     #      user["age"] = [data['age']]
     # except:
     #      user['age'] = [np.nan]

     # try: 
     #      user["marital_status"] = [data['marital_status']]
     # except:
     #      user['marital_status'] = [np.nan]
     
     # try: 
     #      user["ads"] = [data['ads']]
     # except:
     #      user['ads'] = [np.nan]
     
     # try: 
     #      user["present_state"] = [data['present_state']]
     # except:
     #      user['present_state'] = [np.nan]

     # try: 
     #      user["highest_education"] = [data['highest_education']]
     # except:
     #      user['highest_education'] = [np.nan]

     # try: 
     #      user["occupation"] = [data['occupation']]
     # except:
     #      user['occupation'] = [np.nan]

     # try: 
     #      user["employed"] = [data['employed']]
     # except:
     #      user['employed'] = [np.nan]

     # try: 
     #      user["caste"] = [data['caste']]
     # except:
     #      user['caste'] = [np.nan]

     # try: 
     #      user["sect"] = [data['sect']]
     # except:
     #      user['sect'] = [np.nan]

     # try: 
     #      user["family_type"] = [data['family_type']]
     # except:
     #      user['family_type'] = [np.nan]

     # try: 
     #      user["platform"] = [data['platform']]
     # except:
     #      user['platform'] = [np.nan]

     # try: 
     #      user["income_rs"] = [data['income_rs']]
     # except:
     #      user['income_rs'] = [np.nan]


     user = pd.read_csv('one_user_data.csv',encoding='utf-8')
     # print(user.columns)



     #Income_rs
     def income(x):
          if x is np.nan:
               return x
          elif x =='No Income':
               return 0
          else:
               if x.split(' ')[1]=='0':
                    return int(x.split(' ')[3])
               return int(x.split(' ')[1])
          
     user['income_rs'] = income(user['income_rs'][0])
     
 
     
     #Ads
     ads_list = ["gclid", 'organic',"set", 'fb','Funnel','matrimony']

     def get_first_word(string, words_list):
          words = string.split()
          for word in words:
               for item in words_list:
                    if word.lower() == item.lower():
                         return item
                    elif item.lower() in word.lower():
                         return item
          return None
     
     try:
        str_res = get_first_word(user['ads'][0],ads_list)
        if(str_res==None):
            user['ads'] = ['other_ads']
        elif(str_res=='set'):
            user['ads'] = ['not set']
        else:
            user['ads'] = [str_res]
     except:
        user['ads'] = ['potential_ads']



     #States
     other_states = ['Tripura','Manipur','Lakshadweep','Nagaland','Andaman And Nicobar','Arunachal Pradesh','Mizoram',
                 'Dadra and Nagar Haveli','Sikkim','Himachal Pradesh','Meghalaya','Chandigarh','Daman and Diu','Pogradec']
        
     if user['present_state'][0] in other_states:
               user['present_state'] = ['Other_states']


     #Education
     e1=['Doctorate of Medicine ', 'M.P.T.', 'Master of Surgery - M.', 'L.L.M.', 'M.D.S.', 'Chartered Accountant -', 'Doctor of Medicine - M', 'Doctor of Philosophy -', 'M.Tech / M.E' ]

     e2 = ['M.Des./ M.Design.', 'Master of Library Scie', 'M.Com.', 'Master of Arts - M.A.', 'M.Phil. ', 'M.B.A.', 'Master of Education - ', 'Master of Fine Arts - ', 
              'B.Tech / B.E.', 'Master of Chirurgiae -', 'M.C.A.', 'B.H.M.S', 'ICWA', 'M.Sc.', 'M.Pharm ', 'M.M.C / M.M.M / M.J.M.', 'B.U.M.S', 'B.D.S.', 'M.B.B.S.', 'M.Arch.']

     e3=['Doctor of Pharmacy - P', 'BVSc.', 'M.S. (Engineering)', 'CS', 'Master of Physical Edu', 'B.Ed', 'B.IT', 'CFA', 'B.C.A.', 'B.Com.', 'B.Sc. - Bachelor of Sc', 'B.P.T.', 'Bachelor of Law - L.L.', 'B.Des. / B.D.', 'M.D. (Homoeopathy)', 'Master of Social Work ']

     e4=['B.A.M.S.', 'B.A. ', 'Others', 'B.Arch', 'Bachelor of Nursing ', 'B.Pharm / B.Pharma.', 'Bachelor of Library Sc', 'Trade School', 'BHM', 'B.B.A.', 'Bachelor of Fine Arts ', 'B.Sc.', 'M.Sc. (Agriculture)', 'Diploma']

     e5=['High School', 'M.V.Sc.', 'D.Pharma', 'Bachelor of Physical E', 'B.M.C. / B.M.M./ B.J.M', 'Bachelor of Social Wor', 'Aalim Hafiz / Alaima H', 'Intermediate (12th)']

     if user['highest_education'][0] in e1:
               user['highest_education'] = ['Education_category_1']
    
     elif user['highest_education'][0] in e2:
               user['highest_education'] = ['Education_category_2']
        
     elif user['highest_education'][0] in e3:
               user['highest_education'] = ['Education_category_3']
        
     elif user['highest_education'][0] in e4:
               user['highest_education'] = ['Education_category_4']
        
     elif user['highest_education'][0] in e5:
               user['highest_education'] = ['Education_category_5']

     #print(user['highest_education'][0])

     # print(user['highest_education'][0])
     # print(e4[0])

     



     
     #Occupation

     o1=['VP/ AVP/ GM/ DGM', 'Research Professional', 'Surgeon', 'Consultant', 'CxO/ Chairman/ Preside', 'Professor/Lecturer', 'Software Professional', 'Scientist', 'Program Manager', 'Research Assistant', 'Subject Matter Expert']

     o2=['Dentist', 'Cyber/Network Security', 'Finance Professional', 'Engineer', 'HR Professional', 'Physiotherapist', 'Quality Assurance Engi', 'Sr. Manager/ Manager', 'Operations Management', 'Doctor', 'Science Professional']

     o3=['Project Lead - IT', 'Business Owner/ Entrep', 'Teacher', 'Project Manager - IT', 'Corporate Communicatio', 'Chartered Accountant', 'Medical/ Healthcare Pr', 'Lawyer &amp; Legal Pro', 'Navy', 'UI/UX designer', 'Educational Institutio', 'Project Manager - Non ', 'Auditor', 'Non – IT Engineer', 'Mariner', 'Psychologist', 'Corporate Planning', 'Analyst', 'Education Professional']

     o4=['Hardware/Telecom Engin', 'Sales Professional', 'Security Professional', 'Flight Attendant', 'Not working', 'Fashion Designer', 'Product manager', 'Interior Designer', 'Beautician', 'Hotels/Hospitality Pro', 'Social Services/ NGO/ ', 'Businessperson', 'Police', 'Others', 'Paramedic', 'Banking Professional', 'Airline Professional', 'BPO/ITes Professional', 'Defence Services', 'Marketing Professional', 'Architect']

     o5=['Media Professional', 'Travel Professional', 'Secretary/Front Office', 'Journalist', 'Nurse', 'Writer', 'Electronics Engineer', 'Web/Graphic Designer', 'PR Professional', 'Pharmacist', 'Advertising Profession', 'Agriculture Profession', 'Accounting Professiona', 'Student', 'Customer Service', 'Librarian', 'Army', 'Artist']

     o6=['Retired', 'Operator/Technician', 'Broker', 'Veterinary Doctor', 'Air Force', 'Film/ Entertainment Pr', 'Animator', 'Sportsperson', 'Looking for job', 'Civil Services (IAS/ I', 'Agent', 'Farming', 'Pilot', 'Law Enforcement Office', 'Merchant Naval Officer', 'Fitness Professional', 'Clerk', 'Actor/Model', 'Singer', 'Politician', 'Admin Professional']


     if user['occupation'][0] in o1:
          user['occupation'] = ['occupation_category_1']
    
     elif user['occupation'][0] in o2:
          user['occupation'] = ['occupation_category_2']
        
     elif user['occupation'][0] in o3:
          user['occupation'] = ['occupation_category_3']
        
     elif user['occupation'][0] in o4:
          user['occupation'] = ['occupation_category_4']
        
     elif user['occupation'][0] in o5:
          user['occupation'] = ['occupation_category_5']

     elif user['occupation'][0] in o6:
          user['occupation'] = ['occupation_category_6']

     else:
          user['occupation'] = ['occupation_category_7']

     





     #Caste
     c1=['Kalal (Iraqi)', 'Sunni Ehle-Hadith', 'Sheikh or Shaikh', 'Memon', 'Khan or Pathan', 'Syed', 'Mallick-Bihar', 'Shams or Shamsi']

     c2=['Rayeen', 'Zaidi', 'Mughal', 'Farooqui', 'Ansari', 'Siddique', 'Mansoori', 'No Caste', 'Hawrai']

     c3=['Salmani', 'Muslim Choudhary', 'Malik', 'Dawoodi Bohra', 'Usmani', 'Shah', 'Rehman', 'Lababin', 'Gaddi', 'Others', 'Naqvi', 'Punjabi Muslim', 'Shafi', 'Muslim Rajput', 'Idrisi', 'Turq or Turk', 'Quraishi', 'Saifi', 'Alvi']

     c4=['Abdal', 'Kunwar', 'Tyagi', 'Gujrati', 'Bengali', 'Khwaja', 'Qasmi', 'Nomani', 'Abbasi', 'Sunni', 'Bhat', 'Muslim Rajput Thakur', 'Ali', 'Fatmi', 'Mewati', 'Muslim Chauhan', 'Ahmad or Ahmed']

     if user['caste'][0] in c1:
          user['caste'] = ['caste_category_1']
    
     elif user['caste'][0] in c2:
          user['caste'] = ['caste_category_2']
        
     elif user['caste'][0] in c3:
          user['caste'] = ['caste_category_3']
        
     elif user['caste'][0] in c4:
          user['caste'] = ['caste_category_4']
     else:
          user['caste'] = [np.nan]



     #Platform

     if(user['platform'][0]==['Website']):
          user['platform'] = ['WEBSITE']

     elif(user['platform'][0]==['Android']):
          user['platform'] = ['ANDROID']

     elif(user['platform'][0]==['Ios']):
          user['platform'] = ['IOS']

     else:
          user['platform'] = ['Other_platforms']


     # print(user['highest_education'])
     # print(user.columns)


     # #One Hot Encoding
     # columns_to_encode = ['gender', 'marital_status', 'on_behalf','ads','present_state','highest_education','occupation','employed',
     #                'caste','sect','family_type','platform']
     
     # one_hot_df = pd.read_csv('one_hot_data_premium.csv',encoding='utf-8')

     # # print(user)

     # # load the encoder object from file
     # with open('encoder.pkl', 'rb') as f:
     #      encoder_model = pickle.load(f)
     

     # # print(len(encoder_model.transform(user[columns_to_encode]).toarray()[0]))
     
     # one_hot_df =  one_hot_df.drop(columns=['member_id','age','income_rs','membership'])
     # # print(one_hot_df.columns)
     # one_hot_user = pd.DataFrame()
     # one_hot_user[one_hot_df.columns] = encoder_model.transform(user[columns_to_encode]).toarray()

     columns_to_encode = ['gender', 'marital_status', 'on_behalf','ads','present_state','highest_education','occupation','employed',
                     'caste','sect','family_type','platform']
     
     one_hot_df = pd.read_csv('one_hot_data_premium_null.csv',encoding='utf-8')

     # load the encoder object from file
     with open('encoder.pkl', 'rb') as f:
               encoder_model = pickle.load(f)

     one_hot_df = one_hot_df.drop(columns=['member_id','age','income_rs','membership'])

     # create a new DataFrame for the one-hot encoded user
     one_hot_user = pd.DataFrame(columns=one_hot_df.columns)
     # print(one_hot_user)

     encoded_data = encoder_model.transform(user[columns_to_encode].fillna('null'))
     one_hot_df = pd.DataFrame(encoded_data, columns=[one_hot_df.columns])

     # print(one_hot_df)

     


     lst_age=[]
     for i in user['age']:
         lst_age.append(i)
     one_hot_df['age'] = lst_age

     lst_income_rs=[]
     for i in user['income_rs']:
         lst_income_rs.append(i)
     one_hot_df['income_rs'] = lst_income_rs

     # print(one_hot_df)



     # Load the saved model from file using pickle
     with open('model.pkl', 'rb') as f:
          model = pickle.load(f)

     # print(model.predict_proba(one_hot_df))

     return str(model.predict_proba(one_hot_df)[0][1])


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)

