# CHANGELOG
This changelog is used to track the how the model changes through experimentation and intuition change. Links to reasoning should be included where relevant.
Comments should also be included.
----

[1.0.1] 10-20-23
- Added a hook into the CNN which allows the capturing of intermediate convolution outputs. This will aid in our CNN development by helping us understand what is being abstracted by the SAR images.
- Added annotations to understand how the CNN is performing (ex: OUTPUT shape is num_training_iterations x batch_size x image_res=(1 channel, 17px, 17px))
- Next steps: Add hooks into other relevant layers of our CNN. Possibly increase robustness of our dictionaries to guarantee accurate mapping of pics when visualizing.
- IDEAS: Consider pooling (max or averaging) at the initial stages of the network. Consider methods of convolution that are better at extracting ***texture***. Because
          we're dealing with low resolution imaging of an icy/snowy surface of variable radiowave permeability, texture is primarily what we're going off of. Consider
          visualizing our intermediate layers with different interpolation methods such that we can see area/gradients that the CNN is focusing on, and move away from
          individual pixel values


[1.0.0] 10-19-23
- Ported current state of the CNN from local Jupyter Notebook into GitHub Repository.
- Added better folder structure for GitHub than previous local working environment.
- Opted to erase all the local revision history (not well documented anyways) for a clean history. 
- Current approach: Increased batch size for the train_loader and more output layers per convolution should improve RMSE (it has showed promise, but this definitely increases computation resources and time. Be weary of overfitting with the limited dataset too.)
