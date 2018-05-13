# Easy Attendance

Attendance management system using face recognition

Easy Attendance is an attendance management system for windows pcs that uses face recognition for attendance marking. The system uses a web cam or any other attached camera to capture the faces of students or employee of an organization. It is recommended that the camera is mounted in the height of eyes near an entrance with good light condition.

Built using [dlib](http://dlib.net/)'s state-of-the-art face recognition built with deep learning. The model has an accuracy of 99.38% on the [Labeled Faces in the Wild](http://vis-www.cs.umass.edu/lfw/) benchmark.

## Installation

### Requirements

  * Python 3.3+ (recommended 3.6)
  * Windows (recommended 64 bit)

### Steps

1. download and extract zip file
2. open command prompt and navigate to the folder where requirements.txt file is located
3. run the command "pip install -r requirements.txt" (If you are using 32 bit python version you may have to install some modules seperately. Wheel files are not available for some modules in pip)
4. run the easyAttendance.exe file
5. click on play button. then system will open in your browser.

## Features

### Report generation

For every course section, the system generate two types of reports. Student based reports and session(lecture or class) based reports. In the student based report, you can see attendance of each student with their name and attendance precentage. In the session based report, you can see no of attendance and it's variance for each session throughout the semester. You can also download all the generated reports into pdf format.

### Portable application

Easy attendance application is portable. Therefore, even if you move it into another computer you will not lose any information stored in the system.
