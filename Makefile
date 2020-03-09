test:
	coverage run --source . app/manage.py  test
	coverage report
	coverage run --source . -m unittest -v
	coverage report

