# Bowstal-Craft



## Instalation

To successefully install Bowstal-Craft django website project on your machine, you will need python version 3.12.5 or higher. 

To check your python version type this command in command prompt:
```
python --version
```

Don't forget to check if your python is in system path variable on Windows

If you have right python version you can continue by installing virtual enviroment package with pip package manager. Open your command prompt and type this command:
```
pip install virtualenv
```

After you downloaded or cloned project, navigate to its folder and activate virtual enviroment by typing in command prompt:
```
python -m venv venv
```
**Important: the virtual enviroment name should be venv, otherwise you will have conflicts with paths in execution code bellow**

Then activate your virtual enviroment:
```
.\venv\Scripts\activate
```

Now you can install required packages to your virtual enviroment, type this commands into your command prompt:
```
python.exe -m pip install --upgrade pip
pip install wheel
pip install setuptools
pip install -r requirements.txt
```

When you done installing all packages type this command, to fix django admin filters package:
```
python fix_admin_filter.py
```

Then, once operation is a success, we can start creating our database:
```
python manage.py makemigration
python manage.py makemigration mainapp
python manage.py makemigration forum
python manage.py makemigration authentication
```

Now run migrations:
```
python manage.py migrate
```

After this if you want, you can create test data to be able to view project functionality:
```
python manage.py create_test_data
```
**Password for all test user is:password123**


Once you done, type this command to launch the server:
```
python manage.py runserver
```

Now open your browser and navigate to http://127.0.0.1:8000/ to see, if it is running

When you done you can stop server by CTRL + BREAK and deactivate your virtual enviroment:
```
deactivate
```


