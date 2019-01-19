format:
	autopep8 -r --in-place --aggressive Code
	autopep8 -r --in-place --aggressive Tests
test:
	python2.7 -B Scripts/run_all_tests.py
