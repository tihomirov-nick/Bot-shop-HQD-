@echo off 

call %~dp0venv\Scripts\activate

cd %~dp0bot

set TOKEN=5215598767:AAE-gqjWdMsM9sVP_84j_43YvneT9zZpj8Y

python bot_telegram.py 

pause