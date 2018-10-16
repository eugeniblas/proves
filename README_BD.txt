*******************************************************************************
* 
* BASES DE DADES
*
*******************************************************************************

*******************************************************************************
*  Run migrate again to create those model tables in your database
*  Load data 
*******************************************************************************

...buzzer$ python3 manage.py makemigrations buzzer
...buzzer$ python3 manage.py migrate
...buzzer$ python3 manage.py loaddata ./buzzer/fixtures/buser.json


*******************************************************************************
*  Browse list of all users
*******************************************************************************

http://localhost:8000/buzzer/users/


*******************************************************************************
*  Browse list of one users (username)
*******************************************************************************

http://localhost:8000/buzzer/users/@user1      <---- user with username=@user1
