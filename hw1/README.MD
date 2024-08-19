# HW2

## Dummy docker file with a simple server

#### Files:
- hw1\container\app.py - script with the server
- hw1\container\Dockerfile - dockerfile to create container with the server

#### Build Docker image
- go to the `<root>\hw1\container`
- run `docker build -t ghcr.io/maximkartsev/prjctr-ml-in-prod-course/dummy-fastapi-server:latest .`

#### Push the Docker image to GitHub Packages
- run `docker push ghcr.io/maximkartsev/prjctr-ml-in-prod-course/dummy-fastapi-server:latest`

#### Docker image can be pulled from GitHub Packages
- run `docker pull ghcr.io/maximkartsev/prjctr-ml-in-prod-course/dummy-fastapi-server:latest`


## The CI/CD pipeline

#### Files:
- .github/workflows - GitHub action that triggers a Docker container build on each pr merge into the main branch and pushes the image to GitHub packages.

It's necessary to add two secret variables - USER and TOKEN.  
Repository Settings -> Secrets and variables -> Actions -> New repository secret

GitHub Personal Access Token (PAT) should have correct permissions. `read:packages` and `write:packages` required.
Settings -> Developer Settings -> Personal access tokens -> Tokens (classic)
