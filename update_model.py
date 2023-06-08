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


@app.route('/update_model',methods = ['GET','POST'])
def test2():

     #Request data and decode
     data = request.form['change_model']
     data = json.loads(data)

     full_data = pd.read_csv('premium_update.csv',encoding='utf-8')

     #Country : India
     full_data = full_data.query('(present_country=="India") and (permanent_country=="India")')
     full_data = full_data.drop(columns=['present_country','permanent_country'])

     #OTP : No
     full_data = full_data[full_data['otp']!='No']
     full_data = full_data.drop(columns=['otp'])


     def income(x):
          if x is np.nan:
               return x
          elif x =='No Income':
               return 0
          else:
               if x.split(' ')[1]=='0':
                    return int(x.split(' ')[3])
               return int(x.split(' ')[1])
        

     full_data['income_rs']=full_data['income'].apply(lambda x: income(x))


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


     lst_ads = []
     for i in full_data['ads']:
          try:
               str_res = get_first_word(i,ads_list)
               if(str_res==None):
                    lst_ads.append('other_ads')
               elif(str_res=='set'):
                    lst_ads.append('not set')
               else:
                    lst_ads.append(str_res)
          except:
               lst_ads.append('potential_ads')
               continue;             
     full_data['ads'] = lst_ads

     print("Done 1")


     #States
     other_states = ['Tripura','Manipur','Lakshadweep','Nagaland','Andaman And Nicobar','Arunachal Pradesh','Mizoram',
                 'Dadra and Nagar Haveli','Sikkim','Himachal Pradesh','Meghalaya','Chandigarh','Daman and Diu','Pogradec']
     full_data['present_state'] = full_data['present_state'].replace(to_replace=other_states, value="Other_states")
     
     #highest_education
     #Pivot table for Highest Education
     a = pd.pivot_table(full_data, index='membership', columns='highest_education',
                          aggfunc='count')['age']
     Percentage = a.loc['Premium']/(a.loc['Premium'] + a.loc['Free'])
     a.loc['Percentage'] = Percentage*100

     

     # select the 'Percentage' row from pivot table a
     percentage_row = a.loc['Percentage']
 
     # sort pivot table a based on percentage in descending order
     sorted_a = a[percentage_row.sort_values(ascending=False).index]

     list_education=[]
     e1=[]
     e2=[]
     e3=[]
     e4=[]
     e5=[]
     for i in full_data['highest_education']:
         try:
            if sorted_a[i][2]>=sorted_a.iloc[:,8:9].iloc[2].values[0]:
                   list_education.append('Education_category_1')
                   e1.append(i)
            elif sorted_a[i][2]>=sorted_a.iloc[:,29:30].iloc[2].values[0]:
                   list_education.append('Education_category_2')
                   e2.append(i)
            elif sorted_a[i][2]>sorted_a.iloc[:,42:43].iloc[2].values[0]:
                   list_education.append('Education_category_3')
                   e3.append(i)
            elif sorted_a[i][2]>sorted_a.iloc[:,57:58].iloc[2].values[0]:
                   list_education.append('Education_category_4')
                   e4.append(i)
            else:
                   list_education.append('Education_category_5')
                   e5.append(i)
         except:
                 list_education.append(np.nan)

     print("Done 2")

     #     print('highest_education : ',len(full_data['highest_education']))
     #     print('list_education : ',len(list_education))
     #     print(list_education)
     #     print(len(e1))
         



     full_data['highest_education'] = list_education

     print("done 3")

         


         
     #Occupation
     #Pivot table for Highest Occupation
     a = pd.pivot_table(full_data, index='membership', columns='occupation',
                         aggfunc='count')['age']
     Percentage = a.loc['Premium']/(a.loc['Premium'] + a.loc['Free'])
     a.loc['Percentage'] = Percentage*100

     # select the 'Percentage' row from pivot table a
     percentage_row = a.loc['Percentage']

     # sort pivot table a based on percentage in descending order
     sorted_a = a[percentage_row.sort_values(ascending=False).index]
        
         
     list_occupation=[]
     o1 = []
     o2 = []
     o3 = []
     o4 = []
     o5 = []
     o6 = []
     o7 = []
     for i in full_data['occupation']:
          try:
               if sorted_a[i][2]>=sorted_a.iloc[:,7:8].iloc[2].values[0]:
                    list_occupation.append('occupation_category_1')
                    o1.append(i)
               elif sorted_a[i][2]>sorted_a.iloc[:,22:23].iloc[2].values[0]:
                    list_occupation.append('occupation_category_2')
                    o2.append(i)
               elif sorted_a[i][2]>=sorted_a.iloc[:,40:41].iloc[2].values[0]:
                    list_occupation.append('occupation_category_3')
                    o3.append(i)
               elif sorted_a[i][2]>sorted_a.iloc[:,62:63].iloc[2].values[0]:
                    list_occupation.append('occupation_category_4')
                    o4.append(i)
               elif sorted_a[i][2]>=sorted_a.iloc[:,77:78].iloc[2].values[0]:
                    list_occupation.append('occupation_category_5')
                    o5.append(i)
               else:
                    list_occupation.append('occupation_category_6')
                    o6.append(i)
          except:
                list_occupation.append('occupation_category_7')
                o7.append(i)

     full_data['occupation'] = list_occupation

     print('Done 4')



        #Caste
         #Pivot table for mother_tongue
     a = pd.pivot_table(full_data, index='membership', columns='caste',
                         aggfunc='count')['age']
     Percentage = a.loc['Premium']/(a.loc['Premium'] + a.loc['Free'])
     a.loc['Percentage'] = Percentage*100

     # select the 'Percentage' row from pivot table a
     percentage_row = a.loc['Percentage']

     # sort pivot table a based on percentage in descending order
     sorted_a = a[percentage_row.sort_values(ascending=False).index]

     list_caste=[]
     c1=[]
     c2=[]
     c3=[]
     c4=[]

     for i in full_data['caste']:
          try:
               if sorted_a[i][2]>sorted_a.iloc[:,8:9].iloc[2].values[0]:
                    list_caste.append('caste_category_1')
                    c1.append(i)
               elif sorted_a[i][2]>sorted_a.iloc[:,17:18].iloc[2].values[0]:
                    list_caste.append('caste_category_2')
                    c2.append(i)
               elif sorted_a[i][2]>sorted_a.iloc[:,32:33].iloc[2].values[0]:
                    list_caste.append('caste_category_3')
                    c3.append(i)
               else:
                    list_caste.append('caste_category_4')
                    c4.append(i)
          except:
               list_caste.append(np.nan)

     
     full_data['caste'] = list_caste

     print("Done 5")

         
     #Platform
     full_data['platform'] = full_data['platform'].replace("Website",'WEBSITE')
     full_data['platform'] = full_data['platform'].replace("Android",'ANDROID')
     full_data['platform'] = full_data['platform'].replace("Ios",'IOS')

     full_data['platform'].replace(to_replace=full_data['platform'].unique()[3:].tolist()[1:], value='Other_platforms', inplace=True)
     full_data['platform'].replace('HD1901','Other_platforms',inplace=True)



     #Replacing Null values from Income
#     lst_new_income = []
#     e=0
#     l=0
#     k=0
#     for i in range(0,len(lst_income)):
#        if math.isnan(lst_income[i]):
#            lst_new_income.append(full_data.groupby('employed')['income_rs'].median().loc[lst_employed[i]])
#            print(i)
#        else:
#            lst_new_income.append(lst_income[i])
     full_data['income_rs'].fillna(0,inplace=True)
         
     #     full_data['income_rs'] = lst_new_income



     #Removing all the  Null values
     full_data.dropna(inplace=True)




     #Null User
     user = pd.DataFrame()
     user['member_id'] = [232237]
     user['gender'] = [np.nan]
     user['age'] = [28]
     user[['marital_status', 'on_behalf', 'ads',
     'present_state', 'highest_education', 'occupation', 'employed', 'caste',
     'sect', 'family_type', 'platform']] = np.nan

     user['membership'] = ['Free']
     user['income_rs'] = [0]

     full_data = pd.concat([full_data ,user])


     #One Hot Encoding
     columns_to_encode = ['gender', 'marital_status', 'on_behalf','ads','present_state','highest_education','occupation','employed',
               'caste','sect','family_type','platform']
     
     encoder = OneHotEncoder(sparse=False)

     # fit and transform the encoder on the example data
     encoded_data = encoder.fit_transform(full_data[columns_to_encode].fillna('null'))

     # create a DataFrame with the encoded data
     encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names(columns_to_encode))
     encoded_df
     
     

     #Saved The encoded model
     import pickle
     with open('encoder_update.pkl', 'wb') as f:
          pickle.dump(encoder, f)


     print("Done 6")


     
     lst_member_id=[]
     for i in full_data['member_id']:
               lst_member_id.append(i)
     encoded_df['member_id'] = lst_member_id

     lst_age=[]
     for i in full_data['age']:
               lst_age.append(i)
     encoded_df['age'] = lst_age

     lst_income_rs=[]
     for i in full_data['income_rs']:
               lst_income_rs.append(i)
     encoded_df['income_rs'] = lst_income_rs

     lst_membership=[]
     for i in full_data['membership']:
          lst_membership.append(i)
     encoded_df['membership'] = lst_membership


     from sklearn.preprocessing import LabelEncoder
     encoder = LabelEncoder()
     encoded_df['membership'] = encoder.fit_transform(encoded_df['membership'])



     #Model Training
     df = encoded_df

     # perform undersampling using RandomUnderSampler
     rus = RandomUnderSampler(sampling_strategy='majority', random_state=40)
     x_resampled, y_resampled = rus.fit_resample(df.drop(columns=['membership']), df['membership'])
     x_resampled['membership'] = y_resampled
     undersampled_data = x_resampled
     undersampled_data = undersampled_data.drop(columns=['member_id'])


     df_train_test_free = undersampled_data[undersampled_data['membership']==0]
     x_train_free = df_train_test_free.head(int(len(df_train_test_free)*.75))
     x_test_free = df_train_test_free.tail(len(df_train_test_free)-int(len(df_train_test_free)*.75))


     df_train_test_premium = undersampled_data[undersampled_data['membership']==1]
     x_train_premium = df_train_test_premium.head(int(len(df_train_test_premium)*.75))
     x_test_premium = df_train_test_premium.tail(len(df_train_test_premium)-int(len(df_train_test_premium)*.75))


     #Defining Train_data
     x_train_data = pd.concat([x_train_free,x_train_premium])
     x_train_data = x_train_data.sample(frac=1, random_state=np.random.seed())
     x_train = x_train_data.drop(columns=['membership'])
     y_train = x_train_data['membership'] 


     #Defining Testing data
     x_test_data = pd.concat([x_test_free, x_test_premium])
     x_test_data = x_test_data.sample(frac=1, random_state=np.random.seed())
     x_test = x_test_data.drop(columns=['membership'])
     y_test = x_test_data['membership']

     print("Done 7")


         
     cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

     model = KNeighborsClassifier()
     calibrated = CalibratedClassifierCV(model)
     grid = GridSearchCV(estimator=calibrated, param_grid=dict(cv=[2], method=['sigmoid']), n_jobs=-1, cv=cv,scoring='roc_auc')
     grid_result = grid.fit(x_train, y_train)
     
     if(data=='Change'):
          with open('model.pkl', 'rb') as f:
               model = pickle.load(f)
          print("Previous model : " ,model.score(x_test,y_test))
     else:
          #New Model
          print("New Model Accuracy : ",grid.score(x_test,y_test))

          #Previous Model
          with open('model.pkl', 'rb') as f:
               model = pickle.load(f)
          print("Previous model Accuracy : " ,model.score(x_test,y_test))
           

     return "Rumman"
     



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
