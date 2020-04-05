test:
	coverage run --source . app/manage.py  test
	coverage report
	coverage run --source . -m unittest -v
	coverage report

init_data:
	http POST localhost:8000/api/accounts/ 'Authorization:Token ${TOKEN}' name=andres1 external_id=10 
	http POST localhost:8000/api/accounts/1/hosts/ 'Authorization:Token ${TOKEN}' hostname=google.com type=ping 
	http POST localhost:8000/api/accounts/1/contacts/ 'Authorization:Token ${TOKEN}' name='Andres Vargas' phone='99991231' email='zodman@gmail.com' 
	http GET localhost:8000/api/accounts/1/contacts/ 'Authorization:Token ${TOKEN}' 

	
