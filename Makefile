run_tests:
	PYTHONPATH=src pytest tests/

run_cov_tests:
	PYTHONPATH=src pytest --cov-report term-missing --cov=organization_auth tests/