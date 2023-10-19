# CHANGELOG
This changelog is used to track the how the model changes through experimentation and intuition change. Links to reasoning should be included where relevant.
Comments should also be included.
----

[1.0.0] 10-19-23
- Ported current state of the CNN from local Jupyter Notebook into GitHub Repository.
- Added better folder structure for GitHub than previous local working environment.
- Opted to erase all the local revision history (not well documented anyways) for a clean history. 
- Current approach: Increased batch size for the train_loader and more output layers per convolution should improve RMSE (it has showed promise, but this definitely increases computation resources and time. Be weary of overfitting with the limited dataset too.)
