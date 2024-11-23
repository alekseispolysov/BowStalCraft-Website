from pathlib import Path
from os import path


BASE_DIR = Path(__file__).resolve().parent

DJANGO_ADMIN_FILTER_PATH_FILE = path.join(BASE_DIR, "venv\\Lib\\site-packages\\django_admin_filter\\urls.py")

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
