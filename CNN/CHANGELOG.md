# CHANGELOG
This changelog is used to track the how the model changes through experimentation and intuition change. Links to reasoning should be included where relevant.
Comments should also be included.
----

[1.0.3] 10-23-23
- https://www.sciencedirect.com/science/article/pii/S0925231219313803 -> Impact of fully connected layer dimensionality on performance
- A regression based CNN is a *wide* dataset because it has fewer datapoints per class (continous value, thus infinite). Wide datasets tend to perform better with more fully connected
        layers and **more** neurons (pg 8)
- Could not find a specific paper to cite, but Adam optimizer tends to have better performance / faster convergence than RMSprop for most problems.
- Set conv2 output layers to be of size 4x4 by adjusting the fully connected layer dimensions. Note that performance on 5 epochs is essentially the same as on 20 epochs and that
        the network guesses around the mean for most values. Look into ways to make sure the network is sensitive to outliers. This could be done by externally examining the outliers
        and trying to decipher whether there is a feature that the model can be trained to look for.
- TODO: Clean input data of mostly black tiles.

[1.0.2] 10-22-23
- Added hook into the second layer of convolutions and some code to visualize it after training.
- Visualized different interpolations of CNN inputs and intermediate feature maps.
- Experimented with reducing the batch-size to 32 and saw similar performance in NRMSE. Not conclusive though that this is a major improvement, so it'll have to be examined again later.
- Noticed that 2x2 features layer outputs of the final convolution were likely too small to be capturing the relevant features of the input image. Consider restructuring the CNN to
        preserve the general context of our inputs and recognize features of 4x4 or larger. This would likely mean holding off pooling or using kernels of smaller sizes (to achieve more convolutions without loss of feature size). Our final layer should probably have more output layers of higher dimension instead of 32 x 2 x 2.


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
