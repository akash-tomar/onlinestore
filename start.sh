#pip install virtualenvwrapper;
#mkvirtualenv akash_onlinestore;
pip install --upgrade -r requirements.txt;
python manage.py makemigrations;
python manage.py migrate;
python manage.py migrate --run-syncdb;
python manage.py runserver;
