# Install Instructions

## Pre-requisites

I am using an ubuntu machine for development and a raspberry pi for 'production', so my instructions are biased towards Linux but the only differences really are in how the environment variables would be set up.

## Step 1 - Install Python 2.7.x and dependencies

Head over to [python site](http://www.python.org) and install version 2.7.x. 

### Pip (mandatory)
The *pip* python package manager if you're a .net developer is like nuget. Package managers allow you to manage application 
dependencies for shared components and keeps distribution size of your application small. It also isolates the 
versions of these dependencies so you can set your application to use a specific or latest version of a library. You 
can find pip installation instructions [here](https://pip.pypa.io/en/stable/installing/). 

### Virtualenv (optional)
The thing about package managers is that they need a place to install things to. These packages can be installed to the global package store and overwrite any packages your other applications may be dependent on. [Virtualenv](https://virtualenv.pypa.io/en/stable/) is 
a tool that creates virtual environments which you can not only install specific packages into, but also specific versions of the python interpreter. Also, if you want to clean up from whatever you're installing here, well there'll just be one folder to delete afterwards. 
Since this is an optional install, I'm not going to cover it but I do recommend you use it.

### Install packages (mandatory)

Enter the command `pip install -r requirements.txt` into the command prompt. This will install all the required packages into your python libraries folder for your active environment (perhaps you'll polute your python packages if you're not using virtualenv).

## Step 2 - Create a database (optional)

This step is optional as the application will use (sqlite)[http://www.sqlite.org]. Don't worry about installing that part, it comes with python. You know (mysql)[http://www.mysql.com] right?

## Step 3 - Configuration time (mandatory)

Copy the file `production.env` to `dev.env`. This file contains configuration keys you would rather read 
from the environment than check into source-control. For the moment the application won't send emails out, but if you've configured a mysql database for it, you'd set up the connection string here. *Remove this line if you want to use sqlite defaults instead.*

## Step 4 - Database create (mandatory)

Enter 
```
flask db migrate
flask db upgrade
```

this creates the required database tables.

## Step 5 - Run set up (mandatory)

Now you need to configure the coins database and set up download urls for the download-data task. Enter
```
flask download-coin-data
flask load-coins
```
