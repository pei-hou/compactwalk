# Compactwalk

This repository is to reproduce the results that we have in the Compactwalk paper.

## Environment

The experiments were done on a computer with an Intel i5-7200U CPU processor running at 2.5 MHz with 8GB of RAM and Windows v. 10.

## Getting Started with Docker

Download and install [Docker](https://docs.docker.com/get-docker/). Once Docker is up and running, run the following commands in your terminal:

```bash
git clone https://github.com/pei-hou/compactwalk
cd compactwalk
docker build -t compactwalk .
docker run --rm -it -v "$(pwd)/plots:/plots" --name compactwalk-repro compactwalk
```

## Experiments

The same running process of using jupyter-notebook is also provided [here](https://github.com/pei-hou/compactwalk/blob/main/demo/experiment_compactwalk.ipynb).

## Plots

To reproduce the plots that we created by R, see instruction here: [/plots/r-plots](https://github.com/pei-hou/compactwalk/tree/main/plots/r-plots).
