#Steps:

Download the [ZIP](https://codeload.github.com/R1408/Techify_test/zip/techify_development) file

Extract the zip file

create a virtual environment with python 3.7

Activate virtual environment 

### Windows:
```bazaar
cd venv
cd Scripts
activate.bat
```

###Install Requirements
```bazaar
pip install -r requirements.txt
```

###Manually create a database
1. User MySQL database
2. Database name must be "techifydb"

go to the TestProject Directory
###Windows
```bazaar
cd TestProject
```

###Run below command for Database Migration
```bazaar
python manage.py makemigrations TestApp
python manage.py migrate
```

configure env file in your machine

###Start Django Application
Run below command
```bazaar
python manage.py runserver
```

###Run sql Query in database from sql file of TestApp directory
```bazaar
This Query create one Admin data Record Users table and 
create two records in user_role table. one for user and 
second for admin
```

###Admin user id and password
```bazaar
    "email": "admin@gmail.com",
    "password": "Admin@123#"
```

###Open the [URL](http://localhost:8000/signup/) in browser

This is signup page. You need to create a user

###Import [collection](https://www.getpostman.com/collections/d450039282a132145a13) and call API

When you call login API you will receive token and this barer token
you need to pass in Authorization for user list and user details API.




