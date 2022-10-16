# Base image https://hub.docker.com/u/rocker/
FROM rocker/rstudio

## Copy requirements.R to container directory /tmp
COPY ./DockerConfig/requirements.R /tmp/requirements.R 
## install required libs on container
RUN Rscript /tmp/requirements.R

# create an R user
ENV USER rstudio

## Copy your working files over
## The $USER defaults to `rstudio` but you can change this at runtime
COPY ./Data/robokop_pos_nonsemantic.csv /home/$USER/Data/robokop_pos_nonsemantic.csv
COPY ./Data/robokop_pos_nonsemantic_lower.csv /home/$USER/Data/robokop_pos_nonsemantic_lower.csv 
COPY ./Data/runtime.csv /home/$USER/Data/runtime.csv

COPY ./figure_SRW.R /home/$USER/figure_SRW.R 
COPY ./figure_runtime.R /home/$USER/figure_runtime.R

