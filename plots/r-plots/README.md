# Reproducing R-plots 

This repository is to reproduce the figures that we put in the paper.

## Getting Started

Once Docker is up and running, run the following commands:

```
docker build --rm --force-rm -t rocker/rstudio .

docker run -d --rm -p 8787:8787 -e PASSWORD=mypassword --name r-plots rocker/rstudio

```

After setting up the R-studio container, open your brower and link to "http://localhost:8787".

The R-studio will need the username and password. 

The username is "rstudio", and the password is "mypassword".

Once the console is shown, click the "figure_SRW.R" file in the files section (right-bottom) and the R-script file will open. 

By selecting all code and clicking the "Run" button, the figure should output in the current directory. 

Same process for the "figure_runtime.R".
