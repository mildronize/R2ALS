# R2ALS

Registration Assistant Application using Local-Search technique, it can call "R2ALS" shortly.

### Table of Contents
**[Motivation](#motivation)**  
**[Installation](#installation)**  
**[Running](#running)**  

## Motivation
Each curriculum in the university has a unique set of requirements such as the co-requisite and prerequisite which each student in the curriculum must follow. Furthermore, each university must enforce some rules and regulations on the student registration process in order to ensure the student status and ability to graduate. For example, the student with below average grades will be allowed to register fewer credits than regular students in order to make sure that the students can cope with the subjects at hand. Moreover, each student may not be able to register according to the study plan because he/she has withdrawal some subjects. Thus, this situation will add more constraints in the registration process/planning. As a result, there are lots of rules, regulations and constraints that each student must consider in order to plan his/her subjects for each semester.
As a student in the computer engineering undergraduate program at Prince of Songkla University, some of my friends are facing the difficulty in planning the subjects. Even though Prince of Songkla University already provided the study result simulation tool via sis.psu.ac.th for students to simulate their study results in order to see the status, the tool is not directly suggest the subjects to be taken in each semester. Furthermore, the Faculty of Engineering is also provided a web-based application for students to check their study progress according to their respective curriculum. However, the tool shows only the list of subjects in the curriculum and the grades of each subject in order for the students to see what subjects the student are still missing and what subjects the students are already passed. The task of planning the list of subjects to be taken in each semester is still relying on the student.
To solve such problem, this project aims to develop a tool that can help the student by providing a list of subjects to be taken each semester according to the rules and regulations of the curriculum and the university. The student’s preference, the student current status and grades. The proposed tool will be based on the 2010 Computer Engineering Undergraduate curriculum of the Department of Computer Engineering at Prince of Songkla University. Local search technique will be employed as the main solution searching technique in this project. The solution that satisfies all constraints is returned for the user to make the final decision.

## Installation
- Prerequistie
```
sudo aptitude install git python3 python3-venv python3-pip mongodb
```

- Create a vitual environment:
```pyvenv r2als-env```

- Activate the enviroment:
```source r2als-env/bin/activate```

- Setup project:
```python setup.py develop```

## Running

- Activate the enviroment:
```source r2als-env/bin/activate```

- Run the project:
```
r2las/bin/r2als
```

# Full Installation Guide
1.	Prepare server machine for the experiment by using Debian Jessie.
2.	Enter the terminal.
3.	Install prerequisite packages for this project. If all of those packages have installed, you can skip this step.
```
sudo aptitude install git python3 python3-venv python3-pip mongodb
```
4.	Access the target directory
```
mkdir ~/server
cd ~/server
```
5.	Place the source code in the target directory. Use the git command to download lastest version source code from github.
```
git clone https://github.com/mildronize/R2ALS.git
```
6.	Create a virtual environment.
```
pyvenv r2als-env
```
7.	Activate the virtual environment.
```
source r2als-env/bin/activate
```
8.	Access R2ALS directory that gets from step 5.
```
cd R2ALS
```
9.	Setup this project with command line. You should select one of ways below this depend on usage.
9.1.	Setup this project for production
```
python setup.py install
```
9.2.	Setup this project for development
```
python setup.py develop
```
10.	Setup the database. The file which describes the curriculum is located in R2ALS/data/coe_2553_curriculum.csv. You should select one of ways below this depend on usage.
10.1.	Setup the database for production
```
initialize_r2als_db production.ini data/coe_2553_curriculum.csv
```
10.2.	Setup the database for development
```
initialize_r2als_db development.ini data/coe_2553_curriculum.csv
```
11.	Run the project. You should select one of ways below this depend on usage.
11.1.	Run the project for production
```
pserve production.ini
```
11.2.	Run the project for development
```
pserve development.ini --reload
```
The URL that uses access this server
```
http://your_domain_name:6543/ 
```
Or for local only
```
http://localhost:6543/
```
If you would like to run again, you can follow step 7 and 11 only.
