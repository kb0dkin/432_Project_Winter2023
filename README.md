# 432_Project_Winter2023
Repository for shared code for MSDS432 project. Working with A Ellingson and N Goodrich

## Project Overview
This is an EDA portal to look through different covid and taxi/ride-sharing datasets from the City of Chicago.

The system is set up as a series of Docker hosted microservices using a combination of Go, Python, PostGIS and JavaScript. 


### Data pipeline
1. Data is extracted from the city's [data portal](https://data.cityofchicago.org) using Socrata's Go API.
1. Data is loaded into a PostGIS database
1. Geographic associations and predictive analytics are performed with Python
1. Results are presented to User using JavaScript and HTML


### Cluster organization


