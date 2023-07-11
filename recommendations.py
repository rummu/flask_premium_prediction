from flask import Flask ,render_template , request, Blueprint
import pandas as pd
import numpy as np

recApp = Blueprint('recommendations', __name__, template_folder='templates')

reducedUsers = pd.read_csv('reducedUsers.csv')
dummyCols = ['marital_status', 'permanent_state', 'highest_education', 'occupation', 'caste', 'sect', 'employed', 'income', 'permanent_city']
nanMap = dict(zip(dummyCols, [[f'{y}_{x}' for x in reducedUsers[y].astype(str).unique() if (x.endswith('nan'))] for y in dummyCols]))
encodedUsersOneHot = {}

for senderIsFemme in [True, False]: 
    tag = ('Female' if senderIsFemme else 'Male')
    temp = reducedUsers[(reducedUsers.gender != ('Female' if senderIsFemme else 'Male'))]
    encodedUsersOneHot[tag] = pd.get_dummies(temp[['member_id', 'age'] + dummyCols], columns=dummyCols, dummy_na=True)

    for col in dummyCols:
        nanCols = nanMap[col]
        dummiedCols = [x for x in encodedUsersOneHot[tag].columns if x.startswith(col)]
        idx = np.sum(encodedUsersOneHot[tag][nanCols].values, axis=1) > 0
        encodedUsersOneHot[tag].loc[idx, nanCols] = 0
        
    encodedUsersOneHot[tag] = encodedUsersOneHot[tag].astype(pd.SparseDtype("int32", 0))

interest_df = pd.read_csv('interestData.csv')

import datetime
import math
PROFILE_HALF_LIFE_WEEKS = 2 
PROFILE_DECAY_CONSTANT = math.log(2) / PROFILE_HALF_LIFE_WEEKS

def getTimeDecay(lastActiveTimestamp : int):
     weeksSinceActive = (datetime.date.today() - datetime.date.fromtimestamp(lastActiveTimestamp)).days // 7
     decay =  math.e**(-PROFILE_DECAY_CONSTANT*weeksSinceActive)
     return decay



@recApp.route("/test_recommendation", methods=['POST'])
def recommendationTest():
     errors = []

     global reducedUsers, encodedUsersOneHot, interest_df
     member_id = None
     try:
          member_id = int(request.form['member_id'])
     except ValueError as verr:
          return "Exception Encountered: supplied 'member_id' is not an integer!"
     except Exception as exc:
          return "Invalid input!"
     
     offset = 0
     try:
          offset = int(request.form['offset'])
     except:
          errors.append(f'Error: invalid offset using default values {offset}')

     count = 50
     try:
          count = int(request.form['count'])
     except:
          errors.append(f'Error: invalid count using default values {count}')

     withInfo = False
     try:
          withInfo = bool(request.form['withInfo'])
     except:
          errors.append(f'Error: invalid withInfo using default values {withInfo}')

     if errors:
          print('Errors:\n\t')
          print(*errors, sep='\n\t')

     if (reducedUsers.member_id == member_id).sum() == 0:
          return "Member id not in data!"

     senderInfo = reducedUsers[reducedUsers.member_id == member_id].to_dict(orient='records')[0]
     senderIsFemme = senderInfo['gender'] == 'Female'
     senderGender = ('Female' if senderIsFemme else 'Male')

     oneHotTieredUsers = encodedUsersOneHot[senderGender]
     match_df = oneHotTieredUsers[oneHotTieredUsers.member_id.isin(interest_df[interest_df.sender_id == member_id].receiver_id)]
     preferences = match_df.mean(axis=0)

     values = []
     cols = []
     for category in ['marital_status', 'permanent_state', 'highest_education', 'occupation', 'caste', 'sect', 'employed']:
          idx = [x for x in preferences.index if x.startswith(category)]
          weight = 5**(preferences[idx].max())    
          for tier in idx:
               values.append(weight * preferences[tier])
               cols.append(tier)

     vector = pd.Series(data=values, index=cols)
     ageLowerBound = match_df.age.quantile(q=0.5) if senderIsFemme else match_df.age.quantile(0.3)
     ageUpperBound = match_df.age.quantile(q=0.8) if senderIsFemme else match_df.age.quantile(0.7)
     # ageLowerBound, ageUpperBound = (match_df.age.quantile(q=0.4), match_df.age.quantile(q=0.6))
     scores = oneHotTieredUsers[vector.index].dot(vector)
     # scores -= (oneHotTieredUsers.age - preferences.age).abs()
     scores += oneHotTieredUsers.age.between(ageLowerBound, ageUpperBound).astype(float) * 2
     scoredUsers = pd.DataFrame({'member_id' : oneHotTieredUsers.member_id, 'score' : scores})
     
     predictions = pd.merge(scoredUsers[['member_id', 'score']].sparse.to_dense().nlargest(offset + count, columns='score').tail(count), reducedUsers, on='member_id')
     predictions.insert(1, 'already_liked', predictions.member_id.isin(match_df.member_id))

    #  percentage_recommendations_premium = predictions[predictions]

     return {
          'error' : errors,
          'user' : senderInfo,
          'userInterestCount' : match_df.shape[0],
          'userRecommendations' : predictions[predictions.columns if withInfo else ['member_id', 'score']].to_dict(orient='records')
          }
