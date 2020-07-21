
# Project Title

DoctorApp backend.

## Getting Started.

These instructions will get you a copy of the project up and running on your local machine for development purposes.

### Prerequisites

```
Python
```

You need to have python installed in your system since this is mainly a python project.
Please go to https://wiki.python.org/moin/BeginnersGuide/Download to setup your python installation depending on your OS

```
Terminal
```
We need the terminal to run commands. For unix users, terminals are easily available. For windows users, access either your Windows command line (search > cmd > right-click > run as administrator) OR Windows PowerShell (Search > Powershell > right-click > run as administration)

### Installing

After verifying if the prerequisites are met, here are additional stuff you need to run the project.

Install pip. Please go through the link below and choose the installation method of your liking depending on your OS. Pip is going to be the package manager for python.

Please download the latest version of python.
```
https://pip.pypa.io/en/stable/installing/
```

Install Git by following the guide in this link.
```
https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
```

Setup ssh for your account using the link below (only if you haven't set it up yet)
```
https://docs.github.com/en/enterprise/2.15/user/articles/adding-a-new-ssh-key-to-your-github-account
```

Go to the git repository
```
https://github.com/aleisley/ta_frontend
```

Clone the repo to a directory of your choosing.
```
$ git clone git@github.com:aleisley/ta_frontend.git
```
Note: you don't have to type the `$` sign. It just signifies that it's the command entered in the command line.


### Running the project

Create a virtualenvironment anywhere as long as it's outside of the project directory.
```
$ python3 -m venv backend_env
```

Activate the virtualenvironment
```
$ source test/bin/activate
```

`cd` inside the github repo
```
$ cd <where you saved>/ta_frontend
```

Install the packages listed in requirements.txt
```
$ pip install -r requirements.txt
```

Run the project
```
$ uvicorn app.main:app --reload
```








## How to run the project in your dev environment

- Go inside the project directory
- Create and activate virtualenv
- Run this command `uvicorn app.main:app --reload`
- API is now accessible! For the api documentations, go to `http://localhost:8000/docs
