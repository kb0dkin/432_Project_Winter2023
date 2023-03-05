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


## Chicago Database Integration with Google SQL and Looker

This repository contains the source code and configuration files required to integrate data from the Chicago Database into Google SQL and display it through Looker. The project is written in Go and SQL.

### How it Works

Data Extraction: The Go program extracts data from the Chicago Database and formats it to match the schema of our Google SQL database.

Google SQL: The formatted data is then uploaded to Google SQL and stored in our Bronze database instance.

Data Transformation: The data is then transformed and loaded into the Silver database instance, which is optimized for querying.

Data Visualization: Finally, Looker is used to create visualizations and dashboards for our users to access the data.


