import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import model_selection
#from sklearn.tree import export_graphviz
import warnings
import app
import threading

warnings.filterwarnings("ignore", category=DeprecationWarning)


training = pd.read_csv('Training.csv')
testing  = pd.read_csv('Testing.csv')
cols     = training.columns
cols     = cols[:-1]
x        = training[cols]
y        = training['prognosis']
y1       = y

reduced_data = training.groupby(training['prognosis']).max()

#mapping strings to numbers
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx    = testing[cols]
testy    = testing['prognosis']
testy    = le.transform(testy)


clf1  = DecisionTreeClassifier()
clf = clf1.fit(x_train,y_train)
# print(clf.score(x_train,y_train))
# print ("cross result========")
# scores = model_selection.cross_val_score(clf, x_test, y_test, cv=3)
# print (scores)
# print (scores.mean())
# print(clf.score(testx,testy))
# with f as open('tree','wb'):
# export_graphviz(clf,out_file="tree")


importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

global msg
msg=[]
global inflag
global inpneed
global in_buff
global result
result=[]
inflag=False
inpneed=False
in_buff=""
#feature_importances
# for f in range(10):
#    print("%d. feature %d - %s (%f)" % (f + 1, indices[f], features[indices[f]] ,importances[indices[f]]))
global gavl
gavl=0
def chat():
    global msg
    global inflag
    global inpneed
    global in_buff
    msg=[]
    # global msghistory
    flag=True
    start_symptoms_present=[]
    print("Enter symptoms")
    line="Enter symptoms"
    msg.append(line)
    count=1
    while flag and count<3:
        print("inp!:-",flush=True)
        # app.msghistory.append(line)

        # ans = input()
        inpneed=True
        while not inflag:
            # print("waiting")
            if app.terminate_flag:
                return
            # time.sleep(1)
        if inflag:
            # write(chatbot, in_buff)
            ans=in_buff
            inflag=False
            print("Done")
            inpneed=False
            # time.sleep(1)


        ans = ans.lower()
        if "done" in ans:
            flag=False
        elif "" == ans:
            flag=False
        else:
            start_symptoms_present.append(ans)
        count+=1

    if app.terminate_flag:
                return

    # print("Please reply Yes or No for the following symptoms")
    line="Please reply Yes or No for the following symptoms"
    msg.append(line)



    def print_disease(node):
        #print(node)
        node = node[0]
        #print(len(node))
        val  = node.nonzero()
        #print(val)
        disease = le.inverse_transform(val[0])
        return disease
    def tree_to_code(tree, feature_names):
        tree_ = tree.tree_
        #print(tree_)
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        # print("def tree({}):".format(", ".join(feature_names)))
        symptoms_present = []
        # symptoms_present.extend(start_symptoms_present)
        global gval
        gval=0
        def recurse(node, depth):
            global gval
            global in_buff
            global inflag
            global inpneed
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                print(name + " ?")
                line=name + "?"
                msg.append(line)

                if name in start_symptoms_present:
                    ans="yes"
                    gval+=1
                else:
                    print("inp!:-",flush=True)
                    # ans = input()
                    # ans = input()
                    inpneed=True
                    while not inflag:
                        if app.terminate_flag:
                            return
                        app.time.sleep(1)
                    if inflag:
                        # write(chatbot, in_buff)
                        ans=in_buff
                        inflag=False
                        print("Done")
                        inpneed=False
                        # time.sleep(1)
                    ans = ans.lower()
                # print("/"+ans+"/")
                if "yes" in ans:
                    # val = gval+1
                    gval+=0.4
                else:
                    gval = 0
                if  gval <= threshold:
                    recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    recurse(tree_.children_right[node], depth + 1)
            else:

                present_disease = print_disease(tree_.value[node])
                print( "You may have " +  present_disease )
                line= str("You may have " +  present_disease)
                red_cols = reduced_data.columns
                symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
                for sym in start_symptoms_present:
                    if sym in symptoms_given:
                        symptoms_present.append(sym)
                print("symptoms present  " + str(list(symptoms_present)))
                line+=str("/symptoms present  " + str(list(symptoms_present)))
                print("symptoms given "  +  str(list(symptoms_given)) )
                line+= str("/symptoms given "  +  str(list(symptoms_given)))
                confidence_level = (1.0*len(symptoms_present))/len(symptoms_given)
                print("confidence level is " + str(confidence_level))
                line+=str("/confidence level is " + str(confidence_level))
                result.append(line)

        if app.terminate_flag:
                return
        recurse(0, 1)

    tree_to_code(clf,cols)

    diss=[  "itching"," skin_rash"," nodal_skin_eruptions",
        " continuous_sneezing"," shivering"," chills",
        " joint_pain"," stomach_pain"," acidity",
        " ulcers_on_tongue"," muscle_wasting"," vomiting",
        " burning_micturition"," spotting_ urination",
        " fatigue"," weight_gain"," anxiety"," cold_hands_and_feets",
        " mood_swings"," weight_loss"," restlessness"," lethargy",
        " patches_in_throat"," irregular_sugar_level"," cough",
        " high_fever"," sunken_eyes"," breathlessness"," sweating",
        " dehydration"," indigestion"," headache"," yellowish_skin",
        " dark_urine"," nausea"," loss_of_appetite",
        " pain_behind_the_eyes"," back_pain"," constipation",
        " abdominal_pain"," diarrhoea"," mild_fever"," yellow_urine",
        " yellowing_of_eyes"," acute_liver_failure"," fluid_overload",
        " swelling_of_stomach"," swelled_lymph_nodes"," malaise",
        " blurred_and_distorted_vision"," phlegm"," throat_irritation",
        " redness_of_eyes"," sinus_pressure"," runny_nose"," congestion",
        " chest_pain"," weakness_in_limbs"," fast_heart_rate",
        " pain_during_bowel_movements"," pain_in_anal_region"," bloody_stool",
        " irritation_in_anus"," neck_pain"," dizziness"," cramps"," bruising",
        " obesity"," swollen_legs"," swollen_blood_vessels",
        " puffy_face_and_eyes"," enlarged_thyroid"," brittle_nails",
        " swollen_extremeties"," excessive_hunger"," extra_marital_contacts",
        " drying_and_tingling_lips"," slurred_speech"," knee_pain",
        " hip_joint_pain"," muscle_weakness"," stiff_neck"," swelling_joints",
        " movement_stiffness"," spinning_movements"," loss_of_balance",
        " unsteadiness"," weakness_of_one_body_side"," loss_of_smell",
        " bladder_discomfort"," foul_smell_of urine"," continuous_feel_of_urine",
        " passage_of_gases"," internal_itching"," toxic_look_(typhos)"," depression",
        " irritability"," muscle_pain"," altered_sensorium"," red_spots_over_body",
        " belly_pain"," abnormal_menstruation"," dischromic _patches",
        " watering_from_eyes"," increased_appetite"," polyuria"," family_history",
        " mucoid_sputum"," rusty_sputum"," lack_of_concentration",
        " visual_disturbances"," receiving_blood_transfusion"," receiving_unsterile_injections",
        " coma"," stomach_bleeding"," distention_of_abdomen"," history_of_alcohol_consumption",
        " fluid_overload.1"," blood_in_sputum"," prominent_veins_on_calf"," palpitations",
        " painful_walking"," pus_filled_pimples"," blackheads"," scurring"," skin_peeling",
        " silver_like_dusting"," small_dents_in_nails"," inflammatory_nails"," blister",
        " red_sore_around_nose"," yellow_crust_ooze"]
