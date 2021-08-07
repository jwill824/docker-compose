# docker-compose
Docker Compose for Java/SpringBoot, with Grafana and Prometheus integrations, for chained SpringBoot services. Uses Maven to interact with custom docker compose script. Place all of this code inside your root SpringBoot application.

This project uses [docker compose](https://docs.docker.com/compose/). Docker compose allows a project that has multiple dependencies to be ran in tandem across a network so that the whole project can be tested.

## Pre-Requisites

* Install [docker-compose](https://docs.docker.com/compose/) (it should come with the docker cli -> `brew install docker`)
* Install python dependencies:
  * `pip3 install docker`
  * `pip3 install pyyaml`

## Docker Compose Suite

There are five components that make the docker compose suite:

* docker-compose/docker-compose-template.yaml
* docker-compose/docker-compose-debug-template.yaml
* docker-compose/docker-compose-script.py
* .gitignore
* pom.xml

Firstly, in the parent pom.xml, there's the maven profile `-PdockerCompose`. What this does is:

1. Copy both the templates into the input files that docker compose will use, i.e. `docker-compose.yaml`
2. Run the `docker-compose-script.yaml`

Second, the `docker-compose-script.yaml` is an executable python script that does the following:

1. Reads and parses the yaml files
2. Gets a list of your local Docker images, sorts them, then groups them
3. Iterates through the docker compose yaml tag where services live, then dynamically sets a) image b) database url c) database password

In short, the script programatically sets the latest Docker images to their respective place in the file so when you run `docker compose` you're testing the latest services.

> Note: Know that both the `docker-compose.yaml` and `docker-compose-debug.yaml` are added to the `.gitignore` file so that the database passwords don't persist in git.

## Prometheus / Grafana

[Prometheus](https://prometheus.io/) is a monitoring solution used to drill down into many aspects of a project. This project utilizes prometheus mainly for response time metrics, however it can be used in many other ways.

[Grafana](https://grafana.com/) is a tool that is used for visualization of metrics, and integrates with many different datasources, including prometheus. This project essentially takes the metrics that prometheus captures, then visualizes them in a dashboard.

Prometheus and grafana are configured within docker compose. You can see the configurations in `docker-compose-template.yaml` and `docker-compose-debug-template.yaml`. The files that are used to configure different aspects of each are in their respective directories, `grafana/` and `prometheus/`.

The following folders and files are copied into the grafana image file structure. You can access grafana at `localhost:3000`:

* grafana/dashboards - The actual dashboard seen when accessing grafana
* grafana/provisioning/dashboards - Used to configure the provider which is necessary for dashboard usage
* grafana/provisioning/datasources - The datasource used to source any data used in visualization
* grafana/grafana.ini - General configuration file for grafana application

The following file is copied into the prometheus image file structure. You can access prometheus at `localhost:9090`:

* prometheus/prometheus.yaml - Configures prometheus, including endpoint needed for capture, and targets where the endpoints live

## Usage

Prior to running docker compose you need to build all the dependent services so their images are available, and if you've made any changes to the dependent services, you need to build those again with `mvn clean install`. Then you need to run `mvn clean install -PdockerCompose` in this project, which will pick up the latest image.

In order to run the project, all you have to do is call:

```bash
docker compose up
```

If you want to debug, all you need to do is call the following:

```bash
docker compose -f docker-compose-debug.yaml up
```

Then you need to create a remote debugger to attach to the process. Once you run the debugger, all you need to do is set a breakpoint.

> Note: If you've made any changes to the root service, you will need to rebuild the Docker image before running `docker compose` again.
