# Russian Troll Tweet Prediction

The files in this directory contain the research paper, presentation, and code for this project.  Code files are named as follows:

* **NB01_w266Proj_PreProcess_Part1.ipynb**:  Fetches the data and performs initial joins.
* **NB02_w266Proj_PreProcess_Part2.ipynb**:  Tokenizes and canonicalizes tweets, and loads GloVe embeddings.  For use with the small, partial data set.
* **NB02b_w266Proj_PreProcess_Part2a_FullData.ipynb**:  Similar to previous file, but does not load GloVe embeddings, allowing them to be utilized on-the-fly for streaming with the full data set in `NB03b_w266Proj_LSTM_Plus_Meta_FullData.ipynb`.
* **NB03_w266Proj_LSTM_Plus_Meta.ipynb**:  Creates and executes TensorFlow model, along with results analysis. For use with the small, partial data set.
* **NB03a_w266Proj_LSTM_Metadata_Exploration.ipynb**:  Explores the partial data set, including data visualizations.
* **NB03b_w266Proj_LSTM_Plus_Meta_FullData.ipynb**:  Creates and executes TensorFlow model, along with results analysis.  Streams full data in batches, loading GloVe embeddings at run time to allow much larger data to be processed.  For use on the full data set produced in `NB02b_w266Proj_PreProcess_Part2a_FullData.ipynb`.
