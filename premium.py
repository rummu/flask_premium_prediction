from flask import Flask ,render_template , request
import pandas as pd
import numpy as np
import pickle
import json
from flask_cors import CORS
import time

import matplotlib.pyplot as plt
import urllib.parse
pd.set_option('display.max_columns', None)


app = Flask(__name__)
CORS(app)



@app.route("/")
def home():
     return "<h1 style='color:blue'>Hello pycharm!</h1>"


@app.route('/test',methods = ['GET','POST'])
def test1():
     return str(2)

@app.route('/test_premium',methods = ['GET','POST'])
def test2():
     data = request.form['user_data']
     data = json.loads(data)

     user = pd.DataFrame()

     try: 
          if(data["gender"]==""):
               user["gender"] = [np.nan]
          else:
              user["gender"] = [data['gender']]
     except:
          user['gender'] = [np.nan]

     try: 
          if(data["age"]==""):
               user["age"] = [26]
          else:
              user["age"] = [data['age']]
     except:
          user['age'] = [26]

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
               user["income_rs"] = [0]
          else:
              user["income_rs"] = [data['income_rs']]
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
     except:
          user['income_rs'] = [0]
     



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
     other_states = ['Tripura','Manipur','Lakshadweep','Nagaland','Andaman and Nicobar Islands','Arunachal Pradesh','Mizoram',
                 'Dadra and Nagar Haveli','Sikkim','Himachal Pradesh','Meghalaya','Chandigarh','Daman and Diu','Pogradec']

     try:
          if user['present_state'][0] in other_states:
               user['present_state'] = ['Other_states']
     except:
          user['present_state'][0] = [np.nan]

    



     #Education
     
     e1=['Doctor of Philosophy - Ph.D. ', 'M.D.S.', 'Doctorate of Medicine - D.M.', 'Master of Surgery - M.S.', 'Doctor of Medicine - M.D.', 'M.Tech / M.E', 'M.P.T.', 'B.D.S.', 'L.L.M.']

     e2 = ['M.D. (Homoeopathy)', 'Bachelor of Law - L.L.B.', 'B.H.M.S', 'Master of Education - M.Ed.', 'M.Pharm ', 'Chartered Accountant - CA', 'M.Des./ M.Design.', 'B.P.T.', 'B.Tech / B.E.', 'M.B.A.', 'M.B.B.S.', 'Master of Fine Arts - MFA / MVA', 'B.Des. / B.D.', 'M.C.A.', 'M.M.C / M.M.M / M.J.M.C', 'M.Com.', 'M.Arch.', 'B.U.M.S', 'M.Sc.', 'Doctor of Pharmacy - Pharm.D ', 'Master of Arts - M.A.']
     
     e3=['B.Ed', 'CS', 'ICWA', 'M.S. (Engineering)', 'B.Com.', 'B.Arch', 'M.Phil. ', 'Bachelor of Nursing ', 'Master of Library Science', 'CFA', 'B.IT', 'BVSc.']

     e4=['B.C.A.', 'Master of Physical Education', 'BHM', 'B.Sc.', 'Diploma', 'M.Sc. (Agriculture)', 'B.B.A.', 'Trade School', 'B.A.M.S.', 'B.Pharm / B.Pharma.', 'Bachelor of Library Science', 'Bachelor of Fine Arts - BFA / BVA', 'B.Sc. - Bachelor of Science', 'Master of Social Work / M.A. Social Work', 'Bachelor of Physical Education']

     e5=['Bachelor of Social Work', 'Intermediate (12th)', 'M.V.Sc.', 'B.A. ', 'B.M.C. / B.M.M./ B.J.M.C.', 'Master of Chirurgiae - M.Ch.', 'Other', 'High School', 'D.Pharma', 'Aalim Hafiz / Alaima Hafiza']

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
     else:
          user['highest_education'] = [np.nan]



     #Occupation

     o1=['Scientist', 'Project Manager - IT', 'Software Professional', 'Professor/Lecturer', 'VP/ AVP/ GM/ DGM', 'CxO/ Chairman/ President/ Director', 'Research Professional', 'Consultant']

     o2=['Mariner', 'Sr. Manager/ Manager', 'Subject Matter Expert', 'Cyber/Network Security', 'Quality Assurance Engineer', 'Finance Professional', 'HR Professional', 'Research Assistant', 'Program Manager', 'Dentist', 'Project Lead - IT', 'Physiotherapist', 'Surgeon', 'Operations Management', 'Engineer']

     o3=['Medical/ Healthcare Professional', 'UI/UX designer', 'Banking Professional', 'BPO/ITes Professional', 'Teacher', 'Non – IT Engineer', 'Business Owner/ Entrepreneur', 'Lawyer &amp; Legal Pro', 'Doctor', 'Project Manager - Non IT', 'Education Professional', 'Sales Professional', 'Psychologist', 'Auditor', 'Science Professional', 'Product manager', 'Corporate Communication', 'Analyst']

     o4=['Chartered Accountant', 'Fashion Designer', 'Educational Institution Owner', 'Hotels/Hospitality Professional', 'Flight Attendant', 'Airline Professional', 'Interior Designer', 'Pharmacist', 'Not working', 'Customer Service', 'Veterinary Doctor', 'Corporate Planning', 'Marketing Professional', 'Web/Graphic Designer', 'Electronics Engineer', 'Businessperson', 'Security Professional', 'Other', 'Architect', 'Merchant Naval Officer', 'Beautician', 'Paramedic']

     o5=['Law Enforcement Officer', 'Student', 'Nurse', 'Secretary/Front Office', 'Social Services/ NGO/ Volunteer', 'Defence Services', 'Travel Professional', 'Police', 'Accounting Professional', 'Hardware/Telecom Engineer', 'Artist', 'Animator', 'Media Professional', 'Navy', 'PR Professional']

     o6=['Politician', 'Writer', 'Sportsperson', 'Admin Professional', 'Operator/Technician', 'Fitness Professional', 'Singer', 'Civil Services (IAS/ IPS/ IRS/ IES/ IFS)', 'Farming', 'Army', 'Film/ Entertainment Professional', 'Broker', 'Actor/Model', 'Advertising Professional', 'Clerk', 'Librarian', 'Agriculture Professional', 'Retired', 'Agent', 'Pilot', 'Journalist', 'Looking for job', 'Air Force']


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

     c3=['Salmani', 'Muslim Choudhary', 'Malik', 'Dawoodi Bohra', 'Usmani', 'Shah', 'Rehman', 'Lababin', 'Gaddi', 'Other', 'Naqvi', 'Punjabi Muslim', 'Shafi', 'Muslim Rajput', 'Idrisi', 'Turq or Turk', 'Quraishi', 'Saifi', 'Alvi']

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
     try:
          if(user['platform'][0].lower()=='website'):
               user['platform'] = ['WEBSITE']

          elif(user['platform'][0].lower()=='android'):
               user['platform'] = ['ANDROID']

          elif(user['platform'][0].lower()=='ios'):
               user['platform'] = ['IOS']

          else:
               user['platform'] = ['Other_platforms']
     except:
          user['platform'] = ['Other_platforms']


     columns_to_encode = ['gender', 'marital_status', 'on_behalf','ads','present_state','highest_education','occupation','employed',
                     'caste','sect','family_type','platform']
     # one_hot_df = pd.read_csv('one_hot_data_premium_columns.csv',encoding='utf-8')
     features=[
    'gender_Female', 'gender_Male', 'marital_status_Divorced', 'marital_status_Never Married',
    'marital_status_Separated', 'marital_status_Widowed', 'marital_status_null',
    'on_behalf_Brother', 'on_behalf_Daughter', 'on_behalf_Relative/Friend', 'on_behalf_Self',
    'on_behalf_Sister', 'on_behalf_Son', 'on_behalf_null', 'ads_Funnel', 'ads_fb', 'ads_gclid',
    'ads_matrimony', 'ads_not set', 'ads_organic', 'ads_other_ads', 'ads_potential_ads',
    'present_state_Andaman and Nicobar Is', 'present_state_Andhra Pradesh', 'present_state_Assam',
    'present_state_Bihar', 'present_state_Chhattisgarh', 'present_state_Delhi', 'present_state_Goa',
    'present_state_Gujarat', 'present_state_Haryana', 'present_state_Jammu and Kashmir',
    'present_state_Jharkhand', 'present_state_Karnataka', 'present_state_Kerala', 'present_state_Madhya Pradesh',
    'present_state_Maharashtra', 'present_state_Odisha', 'present_state_Other_states', 'present_state_Pondicherry',
    'present_state_Punjab', 'present_state_Rajasthan', 'present_state_Tamil Nadu', 'present_state_Telangana',
    'present_state_Uttar Pradesh', 'present_state_Uttarakhand', 'present_state_West Bengal', 'present_state_null',
    'highest_education_Education_category_1', 'highest_education_Education_category_2',
    'highest_education_Education_category_3', 'highest_education_Education_category_4',
    'highest_education_Education_category_5', 'highest_education_null', 'occupation_occupation_category_1',
    'occupation_occupation_category_2', 'occupation_occupation_category_3', 'occupation_occupation_category_4',
    'occupation_occupation_category_5', 'occupation_occupation_category_6', 'occupation_occupation_category_7',
    'employed_Business/Self Employed', 'employed_Civil Services', 'employed_Defence',
    'employed_Government/Public Sect', 'employed_Not Working', 'employed_Private Sector', 'employed_null',
    'caste_caste_category_1', 'caste_caste_category_2', 'caste_caste_category_3', 'caste_caste_category_4',
    'caste_null', 'sect_Shia', 'sect_Sunni', 'sect_null', 'family_type_Joint Family', 'family_type_Nuclear Family',
    'family_type_null', 'platform_ANDROID', 'platform_IOS', 'platform_Other_platforms', 'platform_WEBSITE',
    'member_id', 'age', 'income_rs', 'membership']
     one_hot_df = pd.DataFrame(columns=features)


     
     # load the encoder object from file
     with open('encoder.pkl', 'rb') as f:
               encoder_model = pickle.load(f)

     one_hot_df = one_hot_df.drop(columns=['member_id','age','income_rs','membership'])

     # create a new DataFrame for the one-hot encoded user
     one_hot_user = pd.DataFrame(columns=one_hot_df.columns)
     encoded_data = encoder_model.transform(user[columns_to_encode].fillna('null'))
     one_hot_df = pd.DataFrame(encoded_data, columns=[one_hot_df.columns])

     #Normalize Age
     lst_age=[]
     def normalize(age):
          return (age-17)/(50-17)
     one_hot_df['age'] = normalize(user['age'][0])

     #Normalize Income_rs
     one_hot_df['income_rs'] = np.log(user['income_rs'] + 1)


     # Load the saved model from file using pickle
     with open('model.pkl', 'rb') as f:
          model = pickle.load(f)
     

     return str(model.predict_proba(one_hot_df)[0][1])




@app.route('/premium_percent',methods = ['GET','POST'])
def test():


     #Request data and decode
     data = request.form['user_data']
     data = json.loads(data)

     user = pd.DataFrame()
     if(data['present_country']=='India'):

          try: 
               if(data["gender"]==""):
                    user["gender"] = [np.nan]
               else:
                    user["gender"] = [data['gender']]
          except:
               user['gender'] = [np.nan]

          try: 
               if(data["age"]==""):
                    user["age"] = [26]
               else:
                    user["age"] = [data['age']]
          except:
               user['age'] = [26]

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
                    user["income_rs"] = [0]
               else:
                    user["income_rs"] = [data['income_rs']]
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
          except:
               user['income_rs'] = [0]
          



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
          other_states = ['Tripura','Manipur','Lakshadweep','Nagaland','Andaman and Nicobar Islands','Arunachal Pradesh','Mizoram',
                    'Dadra and Nagar Haveli','Sikkim','Himachal Pradesh','Meghalaya','Chandigarh','Daman and Diu','Pogradec']

          try:
               if user['present_state'][0] in other_states:
                    user['present_state'] = ['Other_states']
          except:
               user['present_state'][0] = [np.nan]

     



          #Education
          e1=['Doctor of Philosophy - Ph.D. ', 'M.D.S.', 'Doctorate of Medicine - D.M.', 'Master of Surgery - M.S.', 'Doctor of Medicine - M.D.', 'M.Tech / M.E', 'M.P.T.', 'B.D.S.', 'L.L.M.']

          e2 = ['M.D. (Homoeopathy)', 'Bachelor of Law - L.L.B.', 'B.H.M.S', 'Master of Education - M.Ed.', 'M.Pharm ', 'Chartered Accountant - CA', 'M.Des./ M.Design.', 'B.P.T.', 'B.Tech / B.E.', 'M.B.A.', 'M.B.B.S.', 'Master of Fine Arts - MFA / MVA', 'B.Des. / B.D.', 'M.C.A.', 'M.M.C / M.M.M / M.J.M.C', 'M.Com.', 'M.Arch.', 'B.U.M.S', 'M.Sc.', 'Doctor of Pharmacy - Pharm.D ', 'Master of Arts - M.A.']
          
          e3=['B.Ed', 'CS', 'ICWA', 'M.S. (Engineering)', 'B.Com.', 'B.Arch', 'M.Phil. ', 'Bachelor of Nursing ', 'Master of Library Science', 'CFA', 'B.IT', 'BVSc.']

          e4=['B.C.A.', 'Master of Physical Education', 'BHM', 'B.Sc.', 'Diploma', 'M.Sc. (Agriculture)', 'B.B.A.', 'Trade School', 'B.A.M.S.', 'B.Pharm / B.Pharma.', 'Bachelor of Library Science', 'Bachelor of Fine Arts - BFA / BVA', 'B.Sc. - Bachelor of Science', 'Master of Social Work / M.A. Social Work', 'Bachelor of Physical Education']

          e5=['Bachelor of Social Work', 'Intermediate (12th)', 'M.V.Sc.', 'B.A. ', 'B.M.C. / B.M.M./ B.J.M.C.', 'Master of Chirurgiae - M.Ch.', 'Other', 'High School', 'D.Pharma', 'Aalim Hafiz / Alaima Hafiza']

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
          else:
               user['highest_education'] = [np.nan]



          #Occupation
          o1=['Scientist', 'Project Manager - IT', 'Software Professional', 'Professor/Lecturer', 'VP/ AVP/ GM/ DGM', 'CxO/ Chairman/ President/ Director', 'Research Professional', 'Consultant']

          o2=['Mariner', 'Sr. Manager/ Manager', 'Subject Matter Expert', 'Cyber/Network Security', 'Quality Assurance Engineer', 'Finance Professional', 'HR Professional', 'Research Assistant', 'Program Manager', 'Dentist', 'Project Lead - IT', 'Physiotherapist', 'Surgeon', 'Operations Management', 'Engineer']

          o3=['Medical/ Healthcare Professional', 'UI/UX designer', 'Banking Professional', 'BPO/ITes Professional', 'Teacher', 'Non – IT Engineer', 'Business Owner/ Entrepreneur', 'Lawyer &amp; Legal Pro', 'Doctor', 'Project Manager - Non IT', 'Education Professional', 'Sales Professional', 'Psychologist', 'Auditor', 'Science Professional', 'Product manager', 'Corporate Communication', 'Analyst']

          o4=['Chartered Accountant', 'Fashion Designer', 'Educational Institution Owner', 'Hotels/Hospitality Professional', 'Flight Attendant', 'Airline Professional', 'Interior Designer', 'Pharmacist', 'Not working', 'Customer Service', 'Veterinary Doctor', 'Corporate Planning', 'Marketing Professional', 'Web/Graphic Designer', 'Electronics Engineer', 'Businessperson', 'Security Professional', 'Other', 'Architect', 'Merchant Naval Officer', 'Beautician', 'Paramedic']

          o5=['Law Enforcement Officer', 'Student', 'Nurse', 'Secretary/Front Office', 'Social Services/ NGO/ Volunteer', 'Defence Services', 'Travel Professional', 'Police', 'Accounting Professional', 'Hardware/Telecom Engineer', 'Artist', 'Animator', 'Media Professional', 'Navy', 'PR Professional']

          o6=['Politician', 'Writer', 'Sportsperson', 'Admin Professional', 'Operator/Technician', 'Fitness Professional', 'Singer', 'Civil Services (IAS/ IPS/ IRS/ IES/ IFS)', 'Farming', 'Army', 'Film/ Entertainment Professional', 'Broker', 'Actor/Model', 'Advertising Professional', 'Clerk', 'Librarian', 'Agriculture Professional', 'Retired', 'Agent', 'Pilot', 'Journalist', 'Looking for job', 'Air Force']


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

          c3=['Salmani', 'Muslim Choudhary', 'Malik', 'Dawoodi Bohra', 'Usmani', 'Shah', 'Rehman', 'Lababin', 'Gaddi', 'Other', 'Naqvi', 'Punjabi Muslim', 'Shafi', 'Muslim Rajput', 'Idrisi', 'Turq or Turk', 'Quraishi', 'Saifi', 'Alvi']

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
          try:
               if(user['platform'][0].lower()=='website'):
                    user['platform'] = ['WEBSITE']

               elif(user['platform'][0].lower()=='android'):
                    user['platform'] = ['ANDROID']

               elif(user['platform'][0].lower()=='ios'):
                    user['platform'] = ['IOS']

               else:
                    user['platform'] = ['Other_platforms']
          except:
               user['platform'] = ['Other_platforms']



          columns_to_encode = ['gender', 'marital_status', 'on_behalf','ads','present_state','highest_education','occupation','employed',
                         'caste','sect','family_type','platform']
          features=[
                    'gender_Female', 'gender_Male', 'marital_status_Divorced', 'marital_status_Never Married',
                    'marital_status_Separated', 'marital_status_Widowed', 'marital_status_null',
                    'on_behalf_Brother', 'on_behalf_Daughter', 'on_behalf_Relative/Friend', 'on_behalf_Self',
                    'on_behalf_Sister', 'on_behalf_Son', 'on_behalf_null', 'ads_Funnel', 'ads_fb', 'ads_gclid',
                    'ads_matrimony', 'ads_not set', 'ads_organic', 'ads_other_ads', 'ads_potential_ads',
                    'present_state_Andaman and Nicobar Is', 'present_state_Andhra Pradesh', 'present_state_Assam',
                    'present_state_Bihar', 'present_state_Chhattisgarh', 'present_state_Delhi', 'present_state_Goa',
                    'present_state_Gujarat', 'present_state_Haryana', 'present_state_Jammu and Kashmir',
                    'present_state_Jharkhand', 'present_state_Karnataka', 'present_state_Kerala', 'present_state_Madhya Pradesh',
                    'present_state_Maharashtra', 'present_state_Odisha', 'present_state_Other_states', 'present_state_Pondicherry',
                    'present_state_Punjab', 'present_state_Rajasthan', 'present_state_Tamil Nadu', 'present_state_Telangana',
                    'present_state_Uttar Pradesh', 'present_state_Uttarakhand', 'present_state_West Bengal', 'present_state_null',
                    'highest_education_Education_category_1', 'highest_education_Education_category_2',
                    'highest_education_Education_category_3', 'highest_education_Education_category_4',
                    'highest_education_Education_category_5', 'highest_education_null', 'occupation_occupation_category_1',
                    'occupation_occupation_category_2', 'occupation_occupation_category_3', 'occupation_occupation_category_4',
                    'occupation_occupation_category_5', 'occupation_occupation_category_6', 'occupation_occupation_category_7',
                    'employed_Business/Self Employed', 'employed_Civil Services', 'employed_Defence',
                    'employed_Government/Public Sect', 'employed_Not Working', 'employed_Private Sector', 'employed_null',
                    'caste_caste_category_1', 'caste_caste_category_2', 'caste_caste_category_3', 'caste_caste_category_4',
                    'caste_null', 'sect_Shia', 'sect_Sunni', 'sect_null', 'family_type_Joint Family', 'family_type_Nuclear Family',
                    'family_type_null', 'platform_ANDROID', 'platform_IOS', 'platform_Other_platforms', 'platform_WEBSITE',
                    'member_id', 'age', 'income_rs', 'membership']
          one_hot_df = pd.DataFrame(columns=features)

          
          # load the encoder object from file
          with open('encoder.pkl', 'rb') as f:
                    encoder_model = pickle.load(f)

          one_hot_df = one_hot_df.drop(columns=['member_id','age','income_rs','membership'])

          # create a new DataFrame for the one-hot encoded user
          one_hot_user = pd.DataFrame(columns=one_hot_df.columns)
          encoded_data = encoder_model.transform(user[columns_to_encode].fillna('null'))
          one_hot_df = pd.DataFrame(encoded_data, columns=[one_hot_df.columns])

     
          
          #Normalize Age
          lst_age=[]
          def normalize(age):
               return (age-17)/(50-17)
          one_hot_df['age'] = normalize(user['age'][0])

          #Normalize Income_rs
          one_hot_df['income_rs'] = np.log(user['income_rs'] + 1)


          # Load the saved model from file using pickle
          with open('model.pkl', 'rb') as f:
               model = pickle.load(f)          

          return str(model.predict_proba(one_hot_df)[0][1])     
     
     else:
               try: 
                    if(data["gender"]==""):
                         user["gender"] = [np.nan]
                    else:
                         user["gender"] = [data['gender']]
               except:
                    user['gender'] = [np.nan]

               try: 
                    if(data["age"]==""):
                         user["age"] = [26]
                    else:
                         user["age"] = [data['age']]
               except:
                    user['age'] = [26]

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
                    if(data["present_country"]==""):
                         user["present_country"] = [np.nan]
                    else:
                         user["present_country"] = [data['present_country']]
               except:
                    user['present_country'] = [np.nan]

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
                         user["income_rs"] = [0]
                    else:
                         user["income_rs"] = [data['income_rs']]
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
               except:
                    user['income_rs'] = [0]
               



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


               middle_eastern_paying = ['Kuwait','Qatar','Saudi Arabia','United Arab Emirates','Oman','Bahrain','Palestinian Territory ']
               middle_eastern_not_paying = ['Turkey','Israel','Lebanon','Iran','Iraq','Syria','Egypt','Jordan','Yemen','Palestine','Cyprus']


               #Europe With Russia
               europe_paying=['Albania', 'Andorra', 'Austria', 'Azerbaijan', 'Czech Republic',
                              'Denmark', 'Finland', 'France', 'Germany', 'Hungary', 'Ireland',
                              'Lithuania', 'Malta', 'Norway', 'Poland', 'Spain', 'Sweden',
                              'Switzerland', 'United Kingdom']

               europe_non_paying=['Armenia', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 
                                   'Bulgaria', 'Croatia', 'Estonia', 'Georgia', 'Greece', 
                                   'Iceland', 'Italy','Kosovo', 'Latvia', 'Liechtenstein',
                                   'Luxembourg', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia',
                                   'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia',
                                   'Ukraine', 'Vatican City']

               #African Countries
               africa_paying=['Algeria', 'Angola', 'Comoros', 'Gabon',
                              'Mauritius','Nigeria', 'South Africa', 'Tanzania', 
                              'Zambia', 'Zimbabwe', 'Uganda','Morocco'] 

               africa_non_paying=['Benin', 'Botswana', 'Burkina Faso', 'Burundi', 
                                   'Cabo Verde', 'Cameroon', 'Central African Republic',
                                   'Chad', 'Democratic Republic of the Congo', 'Republic of the Congo', 
                                   'Djibouti', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 
                                   'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya',
                                   'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania',
                                   'Mozambique', 'Namibia', 'Niger', 'Rwanda', 'Sao Tome and Principe', 'Senegal',
                                   'Seychelles', 'Sierra Leone', 'Somalia', 'South Sudan',
                                   'Sudan', 'Togo', 'Tunisia']


               #Australia + North and South America 
               america_paying=['Australia', 'New Zealand','Ecuador','Canada', 'United States']
               america_non_paying=['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia',
                                   'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay',
                                   'Venezuela', 'Antigua and Barbuda', 'Bahamas',
                                   'Barbados', 'Belize', 'Costa Rica', 'Cuba', 'Dominica',
                                   'Dominican Republic', 'El Salvador', 'Grenada',
                                   'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico',
                                   'Nicaragua', 'Panama', 'Saint Kitts and Nevis',
                                   'Saint Lucia', 'Saint Vincent and the Grenadines',
                                   'Trinidad and Tobago', 'United States of AmericaAustralia',
                                   'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia',
                                   'Nauru', 'Palau', 'Papua New Guinea', 'Samoa',
                                   'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu']


               #Asian Countris
               south_asia = ['Brunei','Cambodia','Indonesia','Laos','Malaysia','Myanmar',
                              'Philippines','Singapore','Thailand','Timor-Leste','Vietnam']
               indian_neighbours=['Bangladesh', 'Bhutan', 'China','Nepal', 'Pakistan',
                                   'Afghanistan','Maldives',]
               asia_non_paying=['Japan','Korea North','Korea South',
                              'Kazakhstan', 'Kyrgyzstan', 'Mongolia', 
                              'North Korea','South Korea', 'Sri Lanka', 
                              'Taiwan', 'Tajikistan', 'Turkmenistan', 
                              'Uzbekistan','Hong Kong S.A.R.']
               
               try:
                    lst_country=[]
                    if user['present_country'][0] in middle_eastern_paying:
                         lst_country.append('middle_eastern_paying')
                    elif user['present_country'][0] in middle_eastern_not_paying:
                         lst_country.append('middle_eastern_non_paying')
                    elif user['present_country'][0] in europe_paying:
                         lst_country.append('europe_paying')
                    elif user['present_country'][0] in europe_non_paying:
                         lst_country.append('europe_non_paying')
                    elif user['present_country'][0] in africa_paying:
                         lst_country.append('africa_paying')
                    elif user['present_country'][0] in africa_non_paying:
                         lst_country.append('africa_non_paying')
                    elif user['present_country'][0] in america_paying:
                         lst_country.append('america_paying')
                    elif user['present_country'][0] in america_non_paying:
                         lst_country.append('america_non_paying')
                    elif user['present_country'][0] in south_asia:
                         lst_country.append('south_asia')
                    elif user['present_country'][0] in indian_neighbours:
                         lst_country.append('indian_neighbours')
                    elif user['present_country'][0] in asia_non_paying:
                         lst_country.append('asia_non_paying')
                    else:
                         lst_country.append('other_country')
                    user['present_country']=lst_country[0]
               except:
                     user['present_country'][0] = [np.nan]

          



               #Education
               
               e1=['M.P.T.','B.Tech / B.E.','M.Tech / M.E','B.D.S.','Doctor of Philosophy - Ph.D.','Master of Chirurgiae - M.Ch.',
                    'Doctor of Medicine - M.D.','M.S. (Engineering)','ICWA']

               e2 = ['B.B.A.', 'Diploma', 'Master of Arts - M.A.', 'M.Com.', 'M.D.S.', 'M.Sc. (Agriculture)', 'M.Sc.', 'M.Arch.', 'Master of Library Science', 'Chartered Accountant - CA', 'M.B.A.', 'M.C.A.', 'M.Des./ M.Design.', 'CFA', 'B.P.T.', 'B.C.A.', 'L.L.M.', 'B.Com.', 'B.IT', 'M.B.B.S.', 'BHM']
               
               e3=['Bachelor of Fine Arts - BFA / BVA', 'Bachelor of Law - L.L.B.', 'Doctor of Pharmacy - Pharm.D', 'Intermediate (12th)', 'Master of Social Work / M.A. Social Work', 'B.Pharm / B.Pharma.', 'Aalim Hafiz / Alaima Hafiza', 'B.Ed', 'B.Sc. - Bachelor of Science']

               e4=['Trade School', 'Master of Education - M.Ed.', 'B.Arch', 'B.Sc.', 'High School', 'B.Sc. - Bachelor of Science']

               e5=['M.V.Sc.', 'B.U.M.S', 'Master of Physical Education', 'B.A.M.S.', 'Bachelor of Physical Education', 'Master of Surgery - M.S.', 'M.Sc. (Agriculture)', 'CS', 'M.D. (Homoeopathy)', 'B.M.C. / B.M.M./ B.J.M.C.', 'Doctorate of Medicine - D.M.', 'Master of Fine Arts - MFA / MVA', 'M.M.C / M.M.M / M.J.M.C', 'BVSc.', 'D.Pharma', 'B.H.M.S', 'B.Des. / B.D.', 'Bachelor of Social Work', 'Bachelor of Library Science']

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
               else:
                    user['highest_education'] = [np.nan]



               #Occupation

               o1=['Corporate Planning', 'Software Professional', 'Research Professional', 'Project Manager - IT', 'Dentist', 'Project Lead - IT', 'Scientist', 'Finance Professional']

               o2=['Quality Assurance Engineer', 'CxO/ Chairman/ President/ Director', 'Hardware/Telecom Engineer', 'VP/ AVP/ GM/ DGM', 'Corporate Communication', 'Science Professional', 'UI/UX designer', 'PR Professional', 'Surgeon', 'Consultant', 'Analyst', 'Flight Attendant', 'Operations Management', 'Engineer', 'Security Professional']

               o3=['Program Manager', 'Medical/ Healthcare Professional', 'Professor/Lecturer', 'Chartered Accountant', 'Marketing Professional', 'Travel Professional', 'Doctor', 'Accounting Professional', 'Educational Institution Owner', 'Airline Professional', 'Auditor', 'Sr. Manager/ Manager', 'Project Manager - Non IT', 'Banking Professional', 'Product manager', 'Subject Matter Expert', 'Paramedic', 'Research Assistant', 'Electronics Engineer']

               o4=['Non – IT Engineer', 'Businessperson', 'Customer Service', 'Others', 'Army', 'Not working', 'Admin Professional', 'Pharmacist', 'Sales Professional', 'HR Professional', 'Pilot', 'Hotels/Hospitality Professional', 'Nurse', 'Web/Graphic Designer', 'Teacher', 'Cyber/Network Security', 'Interior Designer', 'Architect', 'Operator/Technician', 'Business Owner/ Entrepreneur']

               o5=['Media Professional', 'Secretary/Front Office', 'Student', 'Agriculture Professional', 'Agent', 'Film/ Entertainment Professional', 'Education Professional', 'Advertising Professional', 'Looking for job', 'Writer']

               o6=['Sportsperson', 'Defence Services', 'Merchant Naval Officer', 'Broker', 'BPO/ITes Professional', 'Physiotherapist', 'Retired', 'Beautician', 'Social Services/ NGO/ Volunteer', 'Veterinary Doctor', 'Navy', 'Civil Services (IAS/ IPS/ IRS/ IES/ IFS)', 'Clerk', 'Actor/Model', 'Fashion Designer', 'Psychologist', 'Animator', 'Librarian', 'Journalist', 'Farming', 'Fitness Professional', 'Artist', 'Law Enforcement Officer', 'Mariner', 'Air Force', 'Singer', 'Police']


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
               c1=['No Caste', 'Sheikh or Shaikh', 'Mallick-Bihar', 'Kalal (Iraqi)', 'Syed', 'Farooqui', 'Memon', 'Siddique']

               c2=['Dawoodi Bohra', 'Usmani', 'Shafi', 'Rayeen', 'Nomani', 'Lababin', 'Gujrati', 'Khan or Pathan', 'Others']

               c3=['Quraishi', 'Shah', 'Turq or Turk', 'Muslim Rajput', 'Zaidi', 'Salmani', 'Ansari', 'Ahmad or Ahmed', 'Bhat', 'Mughal', 'Punjabi Muslim', 'Rehman', 'Idrisi', 'Muslim Choudhary', 'Saifi']

               c4=['Alvi', 'Bengali', 'Hawrai', 'Mewati', 'Fatmi', 'Mansoori', 'Naqvi', 'Gaddi', 'Tyagi', 'Kunwar', 'Khwaja', 'Abdal', 'Muslim Chauhan', 'Shams or Shamsi', 'Abbasi', 'Ali', 'Muslim Rajput Thakur', 'Qasmi', 'Malik']

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
               try:
                    if(user['platform'][0].lower()=='website'):
                         user['platform'] = ['WEBSITE']

                    elif(user['platform'][0].lower()=='android') :
                         user['platform'] = ['ANDROID']

                    elif(user['platform'][0].lower()=='ios'):
                         user['platform'] = ['IOS']

                    else:
                         user['platform'] = ['Other_platforms']
               except:
                    user['platform'] = ['Other_platforms']



               
               columns_to_encode = ['gender', 'marital_status', 'on_behalf','ads','present_country','highest_education','occupation','employed',
                         'caste','sect','family_type','platform']
               features=[
                    'gender_Female', 'gender_Male', 'marital_status_Divorced', 'marital_status_Never Married', 'marital_status_Separated',
                    'marital_status_Widowed', 'marital_status_null', 'on_behalf_Brother', 'on_behalf_Daughter', 'on_behalf_Relative/Friend',
                    'on_behalf_Self', 'on_behalf_Sister', 'on_behalf_Son', 'ads_Funnel', 'ads_fb', 'ads_gclid', 'ads_matrimony', 'ads_not set',
                    'ads_organic', 'ads_other_ads', 'ads_potential_ads', 'present_country_africa_non_paying', 'present_country_africa_paying',
                    'present_country_america_non_paying', 'present_country_america_paying', 'present_country_asia_non_paying',
                    'present_country_europe_non_paying', 'present_country_europe_paying', 'present_country_indian_neighbours',
                    'present_country_middle_eastern_non_paying', 'present_country_middle_eastern_paying', 'present_country_other_country',
                    'present_country_south_asia', 'highest_education_Education_category_1', 'highest_education_Education_category_2',
                    'highest_education_Education_category_3', 'highest_education_Education_category_5', 'highest_education_null',
                    'occupation_occupation_category_1', 'occupation_occupation_category_2', 'occupation_occupation_category_3',
                    'occupation_occupation_category_4', 'occupation_occupation_category_6', 'occupation_occupation_category_7',
                    'employed_Business/Self Employed', 'employed_Civil Services', 'employed_Defence', 'employed_Government/Public Sect',
                    'employed_Not Working', 'employed_Private Sector', 'employed_null', 'caste_caste_category_1', 'caste_caste_category_2',
                    'caste_caste_category_3', 'caste_caste_category_4', 'caste_null', 'sect_Shia', 'sect_Sunni', 'sect_null',
                    'family_type_Joint Family', 'family_type_Nuclear Family', 'family_type_null', 'platform_ANDROID', 'platform_IOS',
                    'platform_Other_platforms', 'platform_WEBSITE', 'member_id', 'age', 'income_rs', 'membership']

               one_hot_df = pd.DataFrame(columns=features)

               
               # load the encoder object from file
               with open('encoder_nri.pkl', 'rb') as f:
                         encoder_model = pickle.load(f)

               one_hot_df = one_hot_df.drop(columns=['member_id','age','income_rs','membership'])

               # create a new DataFrame for the one-hot encoded user
               one_hot_user = pd.DataFrame(columns=one_hot_df.columns)
               encoded_data = encoder_model.transform(user[columns_to_encode].fillna('null'))
               one_hot_df = pd.DataFrame(encoded_data, columns=[one_hot_df.columns])

               
               
               #Normalize Age
               lst_age=[]
               def normalize(age):
                    return (age-17)/(50-17)
               one_hot_df['age'] = normalize(user['age'][0])

               #Normalize Income_rs
               one_hot_df['income_rs'] = np.log(user['income_rs'] + 1)

               # Load the saved model from file using pickle
               with open('model_nri.pkl', 'rb') as f:
                    model = pickle.load(f)

               thershold=0.42
               def rescale_value(value):
                    if value <= thershold:
                         return 0.5 * (value / thershold)
                    else:
                         return 0.5 + 0.5 * ((value - thershold) / (1.0 - thershold))
               
               return str(rescale_value(model.predict_proba(one_hot_df)[0][1]))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)

