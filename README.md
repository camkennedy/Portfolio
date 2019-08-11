# Cameron's Data Science and Analytics Portfolio
This repository showcases some of the more interesting technical projects I've developed that can be shared publicly, highlighting data science and analytics solutions to business problems along with other notable work.

## About the Author
Cameron is a graduate student at the University of California, Berkeley, pursuing his Masters in Information and Data Science (MIDS) degree. With 20 years of experience in a wide variety of roles and industries including healthcare, financial services, management consulting, and mining, using analytics to solve business problems has been a central theme in his career.

For more information, please see my [resume](https://github.com/camkennedy/Portfolio/blob/master/Cameron_Kennedy_Resume.pdf), or visit my [LinkedIn profile](https://www.linkedin.com/in/cameron-kennedy-profile/).

# Projects

_Click project name for code, reports, and presentations._

| Project Description | Notable Outcomes | Key Technologies / Methods |
|:-|:-|:-|
|[**Opioid Risk Assessment Tool**](https://github.com/camkennedy/Portfolio/tree/master/Projects/OpioidRisk)<br>Web app that uses data science to impact the opioid crisis by enabling physicians to make more informed decisions about prescribing opioids.  Patients submit responses to ~25 demographic and health questions, which triggers the pipeline to produce a report that provides their personalized probability of opioid misuse, their percentile of misuse among all patients, and the impact that each of their responses has on their risk score.  A calibrated XG Boost model produces the risk score, with Shapley values generating the contributions of individualized risk factors.|<ul><li>Predicted probabilities within 7% of actual probabilities</li><li>[Website](https://opioidmisuserisk.github.io/)</li><li>[Direct link to tool](https://opioidrisk.herokuapp.com/polls/)</li></ul>|<ul><li>Python</li><li>XG Boost</li><li>Calibrated Classifiers</li><li>Calibration Curves</li><li>Brier Loss Score</li><li>Shapley Values</li><li>Django</li><li>Heroku</li><li>FusionCharts</li></ul>|
|[**Russian Troll Tweet Prediction**](https://github.com/camkennedy/Portfolio/tree/master/Projects/RussianTweetPrediction)<br>Natural language processing project to identify Russian political troll-bots on Twitter in the 2016 US election. The technical highlight was concatenating tweet metadata to the LSTM output, then piping the combined data through additional neural network layers.|<ul><li>99% accuracy</li><li>Increased accuracy from 96% baseline using LSTM alone</li><li>[Research report with complete findings](https://github.com/camkennedy/Portfolio/blob/master/Projects/RussianTweetPrediction/Project%20Final%20Paper.pdf)</li></ul>|<ul><li>LSTM Neural Network</li><li>TensorFlow</li><li>Python</li><li>SQL</li></ul>|
|[**Causal Impact of Labeling Opinion Articles on Reader Perceptions**](https://github.com/camkennedy/Portfolio/tree/master/Projects/OpinionArticleLabelingCausality)<br>Research project to determine if adding the label “Opinion:” before article titles on reddit’s politics blog causes a shift in reader perceptions about the underlying article’s factualness and political intensity (i.e., are liberal articles seen as more liberal / are conservative articles seen as more conservative).  The project surveyed 292 individuals who provided their perceptions on multiple article titles which were randomly assigned to be labeled or unlabeled.|<ul><li>Labeling _causes_ ~8% point shift in reader perceptions that articles are more opinionated / less factual</li><li>Important non-finding:  No change in perceptions of political intensity</li><li>Detailed outcomes in [summary presentation](https://github.com/camkennedy/Portfolio/blob/master/Projects/OpinionArticleLabelingCausality/OpinionProject_Presentation.pdf) or [full report](https://github.com/camkennedy/Portfolio/blob/master/Projects/OpinionArticleLabelingCausality/OpinionProject_FinalReport.pdf)</li></ul>|<ul><li>Causal Inference</li><li>Proportional Odds Logistic Regression (polr) given ordinal outcome data</li><li>Statistical Power</li><li>R</li><li>data.table library</li><li>Qualtrics Survey, incl. multi-level randomization</li></ul>|
|[**Large Scale Machine Learning Prediction**](https://github.com/camkennedy/Portfolio/tree/master/Projects/LargeScaleML)<br>Project that predicted advertising click-through rates using a large data set that contained 46 million records with an extremely sparse 33 million features.  Used PySpark and logistic regression techniques to develop a model that scaled nearly uniformly with data size and/or computing cycles.|<ul><li>Highly scalable solution</li><li>65% accuracy (beat 60% target)</li><li>Detailed outcomes in [full report](https://github.com/camkennedy/Portfolio/blob/master/Projects/LargeScaleML/LargeScaleML.pdf) and [code notebook](https://github.com/camkennedy/Portfolio/blob/master/Projects/LargeScaleML/LargeScaleML.ipynb)</li></ul>|<ul><li>PySpark</li><li>EDA and Feature Engineering</li><li>Logistic Regression (Log Loss)</li><li>Gradient Descent</li><li>Ridge and Lasso Regularization</li></ul>|
|[**Predicting Customer Churn for a Subscription Music Service**](https://github.com/camkennedy/Portfolio/tree/master/Projects/MusicServiceChurn)<br>This analysis uses machine learning to predict customer churn for a large music subscription serivce.|<ul><li>97% accuracy</li><li>78% recall</li><li>Economic model to optimze spending amount by customer to prevent churn</li></ul>|<ul><li>XGBoost (best results); also explored Random Forest, SVM, and other models</li><li>Scikit-Learn</li><li>Python</li><li>SQL</li></ul>|
|[**GPS Fitness Activity Tracker**](https://github.com/camkennedy/Portfolio/tree/master/Projects/GPSActivityTracker)<br>Command line software tool to analyze fitness events (e.g., cycling, running, or hiking activities) from a GPS activity tracker such as a Garmin device.  The tool loads and then clusters near-identical activites (e.g., the same cycling route on different days) using an unsupervized learning algorithm.  Clustered events can be compared to each other, providing event dates and best times.  Individual events can be analyzed to show distance and percent of activity at multiple steepness grades.|<ul><li>Software tool to track GPS events</li></ul>|<ul><li>Python</li><li>DBSCAN density-based spatial clustering</li><li>GPS data parsing</li><li>GPS data smoothing</li></ul>|
|[**Medicare Cost Analysis**](https://github.com/camkennedy/Portfolio/tree/master/Projects/MedicareAnalysis)<br>Exploratory data analysis of 2011 Medicare costs and payments, medical conditions, and demographic factors.|<ul><li>Low correlation (< \|0.3\|) between patient demographics and cost</li><li>Top and bottom providers by cost</li><li>Most and least frequently treated conditions</li><li>Distribution of hospital charges vs. Medicare payment amounts</li><li>Tool to search for lowest cost provider by zip code and medical condition</li></ul>|<ul><li>Python</li><li>Pandas</li><li>Visualization tools (Matplotlib, Seaborn)</li></ul>|
|[**R Data Aggregation and Feature Extraction Technique**](https://github.com/camkennedy/Portfolio/tree/master/Projects/R_FeatureExtraction)<br>This example creates multiple summaries of data from a large table using parameters from another (usually much smaller) table. It features a non-equi join, allowing summary data to be extracted efficiently from multiple, simultaneous conditions. This technique can then be used either to generate quick summaries of data, or in feature extraction as part of a larger machine learning exercise. It's not a project like the others on this list; instead, it's a code snippet I find very useful!|<ul><li>Efficient summarization of data without creating an interim table</li></ul><img width=4000/>|<ul><li>R</li><li>data.table library</li><li>Non-equi join</li></ul><img width=1500/>|
