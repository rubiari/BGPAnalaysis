# BGPAnalaysis
Analysis of BGP prefix churn rate vs traffic popularity

DAVID ARIAS RUBIO - MASTER'S THESIS (September 2018)

This code analyzes the UPDATE traces for a set of days for the years 2014 and 2015.
We correlate this data with the traffic popularity for these prefix obtained by a 
private provider for these years. 

The main program is BGPMAIN.py from which we call the other functions of this project

The steps of this code are:
- Download of Update traces
- Cleaning Data
- Clustering Data
- Analysis of Events/Updates per prefix
- Analysis of Traffic popularity per prefix
etc.
