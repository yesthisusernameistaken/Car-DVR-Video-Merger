<div align="center">
<h1> Car DVR Video Merger
</div>

The goal of this project is to use OpenCV to remove the overlap in video clips created by my car DVR. 
	
The code is written in python and tested on a Linux OS.
	
  
Below is a video example of the "jump" that happens when you just put the video files back to back.
  
https://user-images.githubusercontent.com/45125817/138907682-b2b092b2-8b22-4867-968b-67a7478ead5d.mov 

## Pseudo Code
  
List of directories
  
Organize by title
  
Open first video file
  
Read last frame, save it
  
Open following video file
  
Find most similar picture in first 100 frames of second clip
  
From then on, start saving the clip
 
  
## Current issues  

* OpenCV is for video, not audio - The audio from the video clips is lost when processed

* The output files are uncompressed - The 5 minute clips take up about 2.5GB 
