# FEL
 CVUT-FEL is a project for creating a website for VOT Challenge.  
 Link to the website: https://www.votchallenge.net/vots2023/  
 This repository was created by Matej Marek stealing its structure from Tomas Peterka.  

## Preparations

I assume that your structure looks like this:
<i>
* (source folder)
    * (folder with name of the video)
        * color
            * photo1.png/.jpeg/.jpg
            * photo2.png/.jpeg/.jpg
            * photo3.png/.jpeg/.jpg
            * ...
        * (other files e.g. ground truth)
    * (folder with name of the video)
    * (folder with name of the video)
    * (folder with name of the video)
    * ...
</i>
Copy the following Python script, change <i>source_folder<i>, and <i>output_folder<i>, and run it. It will create a new folder in the output folder for every video, and other files in the folder with the name of the video.
