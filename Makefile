run_tests:
	AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test PYTHONPATH=src pytest tests/

run_cov_tests:
	PYTHONPATH=src pytest --cov-report term-missing --cov=organization_auth tests/