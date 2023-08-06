<h2> fewsver 0.1.0 </h2>

This package is part of the prototype forecast verification system that was developed at Deltares for an in-house use only, and it aims to monitor the quality of GLOFFIS forecasts over time. 

Running the main function of the package, triggers the download of forecasts and observations via the FEWS PI REST Web Service and the verification by calling the Ensemble Verification System (EVS). Verification information (Brier Skill Score) is stored both locally and online and can be further disseminated via Plotly's API.

The .txt file that serves as input-argument to the main function, should contain:

* path to csv file with the IDs of point locations
* path to folder where observations will be stored
* path to folder where forecasts will be stored
* path to EVS template
* path to folder where the EVS project will be stored
* path to EVS jar file
* path to folder where results will be stored
* path to csv file of monthly BSS values
* username for Plotly's API
* api_key for Plotly's API

<em> For a Jupyter Notebook with the fully commented code, contact me via e-mail at boumis.georgios@gmail.com
