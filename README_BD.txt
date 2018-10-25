*******************************************************************************
* 
* DATABASE
*
*******************************************************************************

*******************************************************************************
*  Delete old data bases (if it's necessary)
*******************************************************************************

...buzzer$ rm -f tmp.db db.sqlite3
...buzzer$ rm -r ./buzzer/migrations

*******************************************************************************
*  Run migrate again to create those model tables in your database 
*******************************************************************************

...buzzer$ python3 manage.py makemigrations buzzer
...buzzer$ python3 manage.py migrate


*******************************************************************************
*  Load data 
*     1. user (user+profile)
*     2. buzz (buzz)          <-- buzzs of users 
*******************************************************************************

...buzzer$ python3 manage.py loaddata ./buzzer/fixtures/user.json  
...buzzer$ python3 manage.py loaddata ./buzzer/fixtures/buzz.json 
  

*******************************************************************************
*  Browse data
*     1. Browse list of all users
*     2. Browse one user (username)
*     3. Browse list of all users+profiles
*     4. Browse one user+profile (username)
*     5. Browse list of all buzzs
*     6. Browse list all buzzs of one users (username)
*******************************************************************************

http://localhost:8000/buzzer/users/
http://localhost:8000/buzzer/users/username1    <--user with username=username1
http://localhost:8000/buzzer/profiles/
http://localhost:8000/buzzer/profiles/username1  <-user with username=username1
http://localhost:8000/buzzer/buzzs/
http://localhost:8000/buzzer/buzzs/username1 <-buzzs of with username=username1
