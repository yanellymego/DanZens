from BVHView import *
from dtw import *
from BVHParser import *
from centerBVH import *
from scipy.spatial.distance import euclidean

import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import os.path
import os


###
### Parse and create empty array
###

base_sample = ''  #CHANGE PATH NAME TO ANY PARTICIPANT BVH FILE


parser = BVHParser(base_sample)
parser.parse()

joint_names = parser.get_joints_names()
movement_num = 30 #total num of movements
# movement_arr = [9] #only use if needing to select certain movements
channels = ['Xrotation', 'Yrotation', 'Zrotation']

x = 0
y = 0
z = 0

arr = [x, y, z]
norm_dtw = []

x_axis_labels = [] #labels for x-axis

# for n in movement_arr: #only use if movement_arr needed
#     x_axis_labels.append('M' + str(n))

for n in range(movement_num): #(30)
    x_axis_labels.append('M' + str(n+1))

chosen_participants = [97] #CHANGE BASED ON PARTICIPANT NUMBER CHOSEN IN DANCETAG
base_id = 8 #CHANGE


###
### Center and Transform all data (similar to centerBVHStore.py)
###

joints = np.array(["human_low:_root","human_low:_l_up_leg","human_low:_l_low_leg","human_low:_l_foot", "human_low:_l_toes","human_low:_r_up_leg","human_low:_r_low_leg","human_low:_r_foot","human_low:_r_toes","human_low:_torso_1","human_low:_torso_2","human_low:_torso_3","human_low:_torso_4","human_low:_torso_5","human_low:_torso_6","human_low:_torso_7","human_low:_l_shoulder","human_low:_l_up_arm","human_low:_l_low_arm","human_low:_l_hand","human_low:_neck_1","human_low:_neck_2","human_low:_head","human_low:_r_shoulder","human_low:_r_up_arm","human_low:_r_low_arm","human_low:_r_hand"])
print("Transforming...")
for p in chosen_participants:
    print("Participant: ", p)

    for m in range(1, movement_num): #num of movements (30)
        print("\tMovement ", m)

        file = '.../BVH Files/M' + str(m) + 'P' + str(p) + 'S1_TV.bvh' #CHANGE TO MATCH COMPUTER PATH NAME

        #checks if bvh file exists before transformation
        if ((os.path.isfile(file) == False)):
            print(file)
            print("Path not found")

            continue
        
        #checks if transformed csv file alreay exists
        if ((os.path.isfile('.../Transformed File/M' + str(m) + 'P' + str(p) + 'S1_TV.csv') == True)): #CHANGE TO MATCH COMPUTER PATH NAME
            print("Already transformed")

            continue


        # print(file)
        tt = Transformation(file)
        num_frames = tt.frames


        ## Create / Set up data frame
        data = {}

        for joint in joints:
            x_col = f'{joint}_X'
            y_col = f'{joint}_Y'
            z_col = f'{joint}_Z'

            data[x_col] = [float('NaN')] * num_frames
            data[y_col] = [float('NaN')] * num_frames
            data[z_col] = [float('NaN')] * num_frames

        df = pd.DataFrame(data)
        df.index.name = 'Frame'


        ## Fill in data frame with data
        for joint in joints:
            tt.transform(joint)

            df[joint + "_X"] = tt.new_x_coords
            df[joint + "_Y"] = tt.new_y_coords
            df[joint + "_Z"] = tt.z_coords


        ## Saving file
        folder_path = '.../Transformed File' #CHANGE TO MATCH COMPUTER PATH NAME
        os.makedirs(folder_path, exist_ok=True)

        csv_file_path = os.path.join(folder_path, 'M' + str(m) + 'P' + str(p) + 'S1_TV.csv')
        df.to_csv(csv_file_path, index=False)

        print(f"DataFrame saved to '{csv_file_path}' successfully.")



###
### Generate Heatmaps (Participants vs baseline)
###

f = open("DTW Norm For all Movements.txt", "a")
data = np.empty([len(joint_names), movement_num]) #num of joints (27) by num of movements (30)


for k in chosen_participants:
  print("\n\n\nParticipant: " + str(k))

  # for m in range(movement_num): #(30) num of movements
  idx = 0 
    
  for m in movement_arr:  
    participant = '.../Transformed File/M' + str(m) + 'P' + str(k) + 'S1_TV.csv' #CHANGE TO MATCH COMPUTER PATH NAME
    base = '...p/Transformed File/M' + str(m) + 'P' + str(base_id) + 'S2_TV.csv' #CHANGE TO MATCH COMPUTER PATH NAME

    print("Movement: " + str(m))

    if ((os.path.isfile(participant) == False) or (os.path.isfile(base) == False)):
      print(participant)
      print(base)
      print("Path not found")

      #makes missing values null on heatmap
      for j in range(len(joint_names)):
        data[j][idx] = np.nan

      continue

    #nums from csv files
    participant_df = pd.read_csv(participant)
    base_df = pd.read_csv(base)

    for joint in joint_names:
      # X
      alignment = dtw(base_df[joint + "_X"], participant_df[joint + "_X"])
      arr[0] = alignment.distance

      # Y
      alignment = dtw(base_df[joint + "_Y"], participant_df[joint + "_Y"])
      arr[1] = alignment.distance

      # Z
      alignment = dtw(base_df[joint + "_Z"], participant_df[joint + "_Z"])
      arr[2] = alignment.distance

      #normalize
      norm_dtw.append(np.sqrt(arr[0]**2 + arr[1]**2 + arr[2]**2))

    #appends joint data per participant in corresponding data column
    for j in range(len(joint_names)):
      data[j][idx] = norm_dtw[j]

    norm_dtw.clear()
    idx += 1

  plt.figure(figsize=(12, 7))

  hm = sn.heatmap(vmax = 302, data=data, xticklabels=x_axis_labels, yticklabels=joint_names, cmap="Reds")

  hm.xaxis.tick_top()

  hm.tick_params(axis='x', labelsize=7)
  hm.tick_params(axis='y', labelsize=10)

  hm.xaxis.set_label_position('top')
  hm.set_title('Movements from Participant ' + str(k) + ' vs Participant ' + str(base_id) + ' (baseline)')

  plt.show()


  # Text file
  avg_vals = np.empty(movement_num) #num of movements (30)

  for q in range(movement_num): #num of movements (30)
      total = 0.0
      for p in range(len(joint_names)): #num of joints (27)
          total += data[p][q]
      avg_vals[q] = round(total / len(joint_names), 2)


  f.write("Participant " + str(k) + "\n")
  for w in range(len(avg_vals)):
      f.write(str(avg_vals[w]) + "\n")

  f.write("\n\n")
f.close()
