# Installing the SDK  
Follow guide at:  
http://doc.aldebaran.com/2-1/dev/python/install_guide.html#python-install-guide  

# Installing pipenv
`sudo pip install pipenv`  

# Installing dependencies  
This should install all modules in the Pipfile  
1. Change directory into project folder:  
> e.g. `cd ~/Documents/{foldername}`
2. Install dependencies after installing pipenv:  
> `pipenv install`

# Adding a dependency  
Just to help everyone keep track of what modules they need installed  
> `pipenv install {dependency}`

# Removing a dependency  
Again just to keep track  
> `pipenv uninstall {dependency}`

# Running project:
Install packages in Pipfile and then run through terminal  
If modules won't install via pipenv  
> `pip3 install {package}`  
Then make sure being ran in python2.7, can be set to default but if not like this works  
> `python2.7 {filename}`  

# Autoformatting:  
This formats all the code so it's the same style everywhere  
1. Install autopep8:  
> `pip3 install pycodestyle`  
> `pip3 install --upgrade autopep8`  
2. Run Makefile command:
> `make -f Makefile format`  

# Running tests:
1. Navigate to root folder  
> e.g. `cd ~Documents/{foldername}`
2. Run test script  
> `python scripts/test.py`  
Alternatively:  
> `make -f Makefile test`  
will run all tests.

# Writing tests:
Add 'test_' prefix to all test files

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
> `git -b {replace_with_branch_name}`  
Move to a different branch  
> `git checkout {branch_to_look_at}`  
