run_tests:
	PYTHONPATH=src pytest tests/

run_cov_tests:
	PYTHONPATH=src pytest --cov-config=.coveragerc --cov-report term-missing --cov=dce_identities tests/