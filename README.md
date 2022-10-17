# Compactwalk

This repository is to reproduce the results that we have in the Compactwalk paper.

## Getting Started with Docker

Download and install [Docker](https://docs.docker.com/get-docker/). Once Docker is up and running, run the following commands in your terminal:

```
docker build -t compactwalk .
```
```
docker run -it -v <path to repo>/plots:/plots --name my-running-app compactwalk
```
Note that the \<path to repo\> needs to be changed to the directory of this repository.
