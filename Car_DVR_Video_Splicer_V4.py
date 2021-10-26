
'''
What this does:
List files in direcotry
Sort them by name
Plays first file

Todo:
Fix folder issue
    Saving the temp file anywhere else other than temp folder causes issues
    For some reason
Deal with global variable issue
Add something for the last video file
    index out of range error
Progress bar
    One for every file
Add something for firtst video file
    Creating empty files
Could add encoding using ffmped to shrink the files down

Done:
20/04/2020
Save last frame
Fix frame numbering issue

21/04/2020
Added global statements to get functions working
If first video
    skip image check
Naming for output file
    Increment the name or copy input name

22/04/2020
Change output
    Stop displaying ever frame
Add delays
    so the NAS can keep up
Display how many remaining files
Fix folder issue
Chreate folders
    check if they exist, if not create them

'''

import glob #For reading directory
import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import imutils
from imutils.video import FPS
from imutils.video import FileVideoStream
from imutils.video import count_frames
import time
import os
#from tqdm import tqdm #For progress bars
#from tqdm import trange
import sys


frame_number = 0
frame_divider = 3
current_video_number = 0
video_files_directory = []
out_file_number = 0

#---------------------------------------------------------------------------------------------
#File stuff

os.chdir(".")
for file in glob.glob("*.MP4"):
    print (file)
    video_files_directory.append(file)

#Sort list of files
video_files_directory.sort()

number_of_files = len(video_files_directory)
#print number_of_files
print ("[INFO] There are %3d files to be processed" % (number_of_files))


#Print sorted list of files
for i in range(number_of_files):
    print ("{}".format(video_files_directory[i]))
    #print video_files_directory[i]

#Check if folder exits, if not create it
if not os.path.exists("temp"):
    os.makedirs("temp")

if not os.path.exists("output"):
    os.makedirs("output")


#---------------------------------------------------------------------------------------------
#Load video file
def load_video():
    print ("[SYSTEM] Load video")
    global video_path
    video_path = video_files_directory[current_video_number]

    global cap
    cap = FileVideoStream(video_path).start()
    time.sleep(1.0)
    frame = cap.read()
    if frame is None:
        print ("[ERROR] Could not open or find the image, exiting program")
        exit(0)

    #Get info of image
    global height, width, channels
    height, width, channels = frame.shape
    #centre = (width/frame_divider,height/frame_divider) #Calculate center of image
    #print ("[INFO] Original image details -> Height: {}".format(height),"Width: {}".format(width),"Channels: {}".format(channels))
    #return height, width, channels, centre


#---------------------------------------------------------------------------------------------
# count the total number of frames in the video file
def count_frames_in_vid():
    print ("[SYSTEM] Count number of frames")
    global total_number_frames, same_frame_number
    total_number_frames = count_frames(video_path, False) - 1
    print ("[INFO] There are %3d frames" % (total_number_frames))
    #This is a hack
    global same_frame_number
    same_frame_number = total_number_frames

def reset_numbers():
    print ("[SYSTEM] Reset variables")
    global frame_number
    frame_number = 0

def load_last_photo():
    print ("[SYSTEM] Load last photo")
    photo_path = "temp/Last_Frame.jpg"
    #Load that photo and check if correctly loaded
    global last_photo
    last_photo = cv2.imread(photo_path)
    if last_photo is None:
        print ("[ERROR] Could not open or find the image, exiting program")
        exit(0)
    print ("[INFO] Last photo loaded")


def export_video():
    print ("[SYSTEM] Set export path")
    #"output/output_{}.dat".format(i)
    #video_out_path = "output/output_2.avi"
    global out_file_number
    video_out_path = "output/output_{}.avi".format(out_file_number)
    global out_video
    out_video = cv2.VideoWriter(video_out_path ,cv2.VideoWriter_fourcc('M','J','P','G'), 30, (width,height))
    out_file_number += 1



#---------------------------------------------------------------------------------------------



#Main loop
while(True):

    load_video()
    count_frames_in_vid()
    reset_numbers()
    export_video()

    print ("Working on file {}".format(video_path))
    print ("This is file number %3d out of %3d files" % (current_video_number, number_of_files))

    #If first video, do not load picture to check
    if current_video_number != 0:
        load_last_photo()


    while frame_number < total_number_frames:
        #while frame_number < total_number_frames:

        #Grab the frame
        frame = cap.read()
        if frame is None:
            print ("[ERROR] Could not open or find the image, must be the end of the video file")
            exit(0)

        frame_number+= 1

        #Save the last frame
        if frame_number == total_number_frames:
            print("[INFO] Last frame reached! Saved to folder")
            cv2.imwrite("temp/Last_Frame.jpg", frame)
            break

        #Video preview
        frame_shrunk = cv2.resize(frame, (width/frame_divider,height/frame_divider))                   
        cv2.imshow("Video", frame_shrunk)

        #Compare video with last image and write to output file
        if current_video_number != 0:
            if frame_number >= same_frame_number:
                #print ("Write to output")
                out_video.write(frame)          #Write video file out
            else:
                difference = cv2.subtract(last_photo, frame)        #Compare the frame and last image
                gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY) #Make the image gray
                if np.average(gray) < 1:
                    print("-----The images are completely Equal-----")
                    same_frame_number = frame_number
                    print ("[INFO] The same frame is frame number %3d" % (same_frame_number))


        #Kill everything
        k = cv2.waitKey(2) & 0xFF   
        if k == 113 or k == 27:
            exit(0)
            #break


    #Move to next video
    current_video_number += 1
    out_video.release()
    time.sleep(3)





print ("[END] End of program")
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
exit(0)
