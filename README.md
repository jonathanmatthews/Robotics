# This project:  
In this repository you will find all the code associated with each part of the projct, e.g. machine learning
files, simulation from theory, and the actual code for running the robot. Machine learning and simulation
files have only been added at the end so there is version history for the code team but not for the other teams.



# Running project:
Install all packages in Pipfile and then run through terminal  
Linux:  
> `pip install {package}`  

Windows:
> `pip install {package}`  

Then make sure being ran in python2.7, can be set to default but if not like this works  
> `python2.7 {filename}`  

# Setting up Makefile:  
Install py-make  
Linux:  
> `pip3 install py-make`  

Windows:
> `pip install py-make`  

# Autoformatting:  
This formats all the code so it's the same style everywhere  
1. Install autopep8:  
> `pip3 install pycodestyle`  
> `pip3 install --upgrade autopep8`  

2. Run Makefile if has been installed:  
> `pymake format`  

# Using git:  
Check what branch you are on and other info  
> `git status`  

Add all files to next commit  
> `git add -A`  

Commit files added using previous command  
> `git commit`  

Push all changes to cloud for everyone  
> `git push`  

Create a branch to work on  
> `git branch replace_with_branch_name`    

Move to a different branch  
> `git checkout branch_to_look_at`    

Pull down any changes other people have pushed  
> `git pull`  

To put code onto master branch go to github, find your branch, and click create pull request,  
then get someone else to approve your code and after that it can be merged.  

