# Causal Impact of Labeling Opinion Articles on Reader Perceptions

The files in this directory contain the research paper, presentation, code, and supporting material for this project.  Code files are named as follows:

* **data/rawSurveyData.csv**: Contains the data from the survey responses. It is included in the `data` folder, along with pilot data in csv files.
* **DataPrep.Rmd**: R file that reads the data from rawSurveyData.csv and wrangles it into a data tables for both visual and statistical analysis. Relies on other files in this directory (included in the `data` directory) that join survey outputs to article covariates. Outputs
the `POSurveyData.rds` file.
* **ResultsEDA.Rmd**: Reads the POSurveyData.rds file and conducts exploratory data analysis, including numerous visualizations not shown in the final report.
* **StatAnalysis.Rmd**: Reads the POSurveyData.rds file and conducts statistical analysis, largely using polr models, and provides stargazer table output.
* **PowerCalcs/PowerCalcs.Rmd**: A standalone file located in the PowerCalcs directory that contains code to calculate statistical power of various effect sizes given various number of responses. A thorough knitting of this file is also included in the `PowerCalcs.pdf` file.