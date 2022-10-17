# Compactwalk

This repository is to reproduce the results that we have in the Compactwalk paper.

## Getting Started with Docker

Download and install [Docker](https://docs.docker.com/get-docker/). Once Docker is up and running, run the following commands in your terminal:

```bash
git clone https://github.com/pei-hou/compactwalk
cd compactwalk
docker build -t compactwalk .
docker run --rm -it -v "$(pwd)/plots:/plots" --name compactwalk-repro compactwalk
```
## Plots

To reproduce the plots that we created by R, see instruction here: [/plots/r-plots](https://github.com/pei-hou/compactwalk/tree/main/plots/r-plots).
