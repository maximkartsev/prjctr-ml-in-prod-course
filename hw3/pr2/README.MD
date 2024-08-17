# Homework 3 - PR2: Develop a CRUD Python client for MinIO and accompany it with comprehensive tests.

## Files
- minio_client.py - client to connect MinIO server
- test_minio_client.py - test of the client
- Dockerfile - docker file to prepare environment for tests
- requirements.txt - file with all requires libs for the minio client and tests
- docker-compose.yml - docker compose file. Run minio server for tests and run tests

## How to run tests
1. Open console , go to the `hw3/pr2` folder
2. Run `docker-compose build` command
3. Run `docker-compose up --abort-on-container-exit` command

The result of the tests will be in the `hw3/pr2/test_results` folder.