import subprocess
import sys
from pathlib import Path
from os import path

BASE_DIR = Path(__file__).resolve().parent

commands_instalation = [
	"python -m pip install upgrade pip",
	"pip install wheel",
	"pip install setuptools",
	"pip install -r requirements.txt"
]

commands_migrations = [
	"python manage.py makemigrations",
	"python manage.py makemigrations mainapp",
	"python manage.py makemigrations forum",
	"python manage.py makemigrations authentication",
	"python manage.py migrate"
]

virtual_env_path = path.join(BASE_DIR, "venv", "Scripts", "activate")

exec(open(virtual_env_path).read(), dict(__file__=virtual_env_path))

def commands_run():
	result = subprocess.run(commands_instalation, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	print(result.stdout.decode())
	print(result.stderr.decode())


for com in commands_instalation:
	commands_run(com)


DJANGO_ADMIN_FILTER_PATH_FILE = path.join(BASE_DIR, "venv","Lib","site-packages","django_admin_filter","urls.py")

check_path = Path(DJANGO_ADMIN_FILTER_PATH_FILE)

if check_path.exists():
	pass
else:
	print(f"Error, file does not exist at path: {DJANGO_ADMIN_FILTER_PATH_FILE}")
	print("Please check if your virual enviroment name matching 'venv' and file urls.py at path exists.")
	quit()


REPLACEMENT = "from django.urls import re_path\n"

with open(DJANGO_ADMIN_FILTER_PATH_FILE, 'r') as file:
	lines = file.readlines()

if 0 <= 0 < len(lines):
	lines[0] = REPLACEMENT
	print("Operation Successful")
else:
	print(f"Operation Unsuccessful. Please check file located: {DJANGO_ADMIN_FILTER_PATH_FILE}.")
	quit()

with open(DJANGO_ADMIN_FILTER_PATH_FILE, 'w') as file:
	file.writelines(lines)


for com in commands_migrations:
	commands_run(com)