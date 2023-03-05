# 432_Project_Winter2023
Repository for shared code for MSDS432 project. 
Group2: Kevin Bodkin, Nikolas Goodrich, Alissa Ellingson

## Project Overview
This is an EDA portal to look through different covid and taxi/ride-sharing datasets from the City of Chicago.

The system is set up as a series of Docker hosted microservices using a combination of Go, Python, PostGIS and JavaScript. 

### Data retrieval and processing microservices implemented in Golang:
1. build-permit
1. covid-19-daily-cases
1. covid-19-zip
1. health-ind
1. taxi-trips
1. tnp-trips

### Database engine microservices implemented with PostgreSQL having PostGIS extension:
Bronze database tables:
1. build-permit
1. covid-19-daily-cases
1. covid-19-zip
1. health-ind
1. taxi-trips
1. tnp-trips

Silver database tables:
1. ccvi-taxi
1. midway-taxi-covid
1. ohare-taxi-covid
1. permit-neighborhood
1. permit-zip
1. taxi-count
1. taxi-covid

### Data pipeline:
1. Data is extracted from the city's [data portal](https://data.cityofchicago.org) using Socrata's Go API.
1. Data is loaded into a PostGIS database in Google Cloud SQL
1. Google Cloud Run is used to manage microservices
1. Geographic associations and predictive analytics are performed with Python
1. Results are presented to User using Google Looker Studio dashboard


### Cluster organization


