# HW2

## Dummy docker file with a simple server

#### Files:
- hw1\container\app.py - script with the server
- hw1\container\Dockerfile - dockerfile to create container with the server

#### Build Docker image
- go to the `<root>\ `
- run `docker build -t ghcr.io/maximkartsev/prjctr-ml-in-prod-course/dummy-fastapi-server:latest .`

#### Push the Docker image to GitHub Packages
- run `docker push ghcr.io/maximkartsev/prjctr-ml-in-prod-course/dummy-fastapi-server:latest`

#### Docker image can be pulled from GitHub Packages
- run `docker pull ghcr.io/maximkartsev/prjctr-ml-in-prod-course/dummy-fastapi-server:latest`
