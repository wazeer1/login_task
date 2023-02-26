echo " BUILD START"
python3.9 pip install -r requirement.txt
python3.9 manage.py collectstatic
python3.9 manage.py runserver
echo " BUILD END"
