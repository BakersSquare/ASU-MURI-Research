# CHANGELOG
This changelog is used to track the how the model changes through experimentation and intuition change. Links to reasoning should be included where relevant.
Comments should also be included.
----

[1.0.6] 1-22-24
- ***No model changes***
- Scripts are changed to accept the delivered SLEA data.
- TODO: Redevelop the tiled images and include the [0-255] scaling in the gdal.translate() method. Right now the CNN is previewing them as miscolored and it's likely because the pixel values
        are not valid grayscale
- Reconsidered the previous comments - It's likely the model highly biased the mean because each pixel was the running 50m average height, and each new tile only varied by 1 column of pixels. Thus 
        the majority of the model was made through averages and their slight variations. The new data should be an improvement from this because of it's high resolution and ability to capture the
        discrete ICESAT2 footprint.

[1.0.5] 1-14-24
- ***No model changes***
- Git Repo has been updated in anticipation for SLEA ICEYE data delivery (15km x 15km, 1m resolution SLEA imaging).
- Consideration: The model as it stands has a problem where it overfits by guessing near the mean. This could be happening because the majority of the training data has overlap with the corresponding neighboring tiles (due to stubbing the SAR imaging with 50m resolution Sentinel 1 imaging). This frequent overlapping could bias the moddel into essentially tripling the likelihood that it see's a remarkably average tile. Moving forward with the ICEYE 1m resolution data, investigate whether this distribution holds true even when tiles have 6-10px buffers from overlapping. This can be done inherently, or the new data can be tiled into explicitly distinct tiles (15000 / 17m distinct tiles)

[1.0.4] 11-12-23
- Manually cleaned input data and removed all tiles containing an edge of the SAR. Removing 130 tiles, leaving 3,675 tiles. Essentially 3.4165% of our data was bad.
- Plotted the distributions of the input vs output data, suggesting there's an overfitting happen (which I'd assume is because of the fully connected layers or our RMSE optimization function). 
        According to "ASU-MURI-Research/personal-research/Image Processing/CNN Research/fc layer suggestions.pdf" a shallow network requires more FC layers. But because we have the RMSE optimizer as our
        activation function, it could be forcing these dense layers to optimize towards the mean. It makes sense that the distribution of guesses is slightly above the input mean because the distribution is not normal
        and actually has a slight right tail. Or it could be because there are only so many combinations of our final feature space that each matrix gets mapped down to near the mean. Maybe our convolution steps should
        take more steps to shrink in fewer dimensions.
        Knowing that feature maps representing less *abstract* data, which is ours because our feature map begins in small dimension as it is and we perform few convolutions, need more FC layers, we should first work on increasing
        the output size of our 2nd convolution. Switching to an L1 Loss function appeared to help the spread of the output data, but it's comparable to the spread achieved using regular RMSE. This means our problem will likely
        need to be addressed elsewhere.
- Network Changes:
       - Assumed normalization was not happening correctly -> Immediately spread out the final distribution of guesses
       - Removed pooling and tested the effects of a single fully connected layer
- TODO: Make sure the transforms object is doing what we expect it to do, or consider developing without the normalizing. It could be that our target values were all normalized values and that we were supposed to unnormalize them before
        testing.
        https://stackoverflow.com/questions/49444262/normalize-data-before-or-after-split-of-training-and-testing-data
- CONSIDER: Modifying the CNN to output a regression value of distributions (https://medium.com/hal24k-techblog/a-guide-to-generating-probability-distributions-with-neural-networks-ffc4efacd6a4)

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
