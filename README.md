# TRUSTY &mdash; System-to-human Trust Estimation

![inattentive_pedestrian](https://github.com/saadejazz/trusty/blob/main/examples/test3.gif)

For the scope of this repository, trust is defined as the degree to which a robotic system can rely on a specific human or agent in the environment to actively maintain safety. By incorporating trust-awareness, a robotic system can adopt more assertive policies towards trusted agents while taking extra safety considerations for untrustworthy agents. This approach enables the system to strike a balance between performance and safety in human-robot interactions, optimizing its behavior based on the level of trust established with individual agents.

Images contain rich information that can be extracted to estimate indicators of trust, referred to as behavior traits. For images of pedestrians in an autonomous driving system, indicators such as head pose, smartphone usage, age, and gait analysis can be appropriate traits for trust estimation. These behaviours all indicate distraction levels of pedestrians and the final trust at any time step can be formulated as a linear combination of one or more of these trait values at that time step. This work specifically provides an example for such a formulation of trust.

## Behaviour Traits

The following three behaviour traits are considered, with each of the behaviour trait resulting in a continuous confidence value bounded between 0 and 1. The final aggregated trust is just a linear combination of those values.
1. Smartphone usage - end-to-end model training and dataset sourcing described in [smato](https://github.com/saadejazz/smato)
2. Pose fluctuation - determined by change in pose (scaled with bounding boxes) between time frames - [openpifpaf](https://github.com/openpifpaf/openpifpaf) [[1]](1)
3. Eye contact/gaze direction - a deep learning model built on top of OpenPifPaf: [looking](https://github.com/vita-epfl/looking) [[2]](2)


## Dynamics of Trust

Since trust depends on the result of neural network prediction over images, the values can change erratically causing a major variations if the trust is considered as a time-varying signal. This would cause significant problems when used with a practical control system with input limits. Therefore, the ```tshufflenet2k30``` model of openpifpaf is used to track pedestrians between frames and changes in their behaviour attributes are smoothed out using recursive functions such as moving average. In this repository, the behaviour traits smartphonge usage and pose fluctuations are smoothed using moving averages (parameters can be modified in ```config.py```), while the confidence corresponding to eye contact detection is monotonically increasing (a small proportion is added to the previous value at each time step). This is logical as humans have memory and do not need to maintain eye contact wito be considered trustworthy.

## Usage
This code requires the installation of [openpifpaf](https://github.com/openpifpaf/openpifpaf), torch, keras, and matplotlib among other dependencies. Once the dependencies are installed, the code in ```test_trust.py``` can be modified to your own liking. Results will be stored in a folder named ```output```. You can find various example pictures in the ```exmples``` folder.

The simple python code to output imaegs with trust information and viualized bounding boxes is as follows
```python
from trusty import init_predictor

trust_estimator = init_predictor()
trust_estimator.predict(<list_of_image_paths>)
```

## Examples
The output images have a rather complex visualization scheme. There are four pieces of information to each detected pedestrian, that are as follows:
1. _The trust value:_ A value between 0 and 1, with 0 being the least trustworthy and vice versa. This value is the aggregate of the behaviour trait confidence values (after smoothing)
2. _The color of the bounding box:_ this can be either of red, orange, or green which correspond to high, moderate, and low value for trust, discussed in the previous point.
3. _The color of the skeleton mask:_ this can be either of red, orange, or green corresponding to a high, moderate, or low threshold of eye contact detection - directly adapted from [looking](https://github.com/vita-epfl/looking)
4. _The letter alognside the trust value:_ this can be either of ```N```, ```U```, and ```Y``` corresponding to a low, medium, and high confidence for detection of smartphone usage. The letters are short for ```No smartphone```, ```Unsure about smartphone```, and ```Yes smartphone```.

The categorical visualizations mentioned above are for the sake of simplicity. Internal calculations of trust are conducted using continuous variables.

Some examples for real-life scenarios are as follows:  

![smato_distracted](https://github.com/saadejazz/trusty/blob/main/examples/smato_distracted.gif)

![multiple_pedestrians](https://github.com/saadejazz/trusty/blob/main/examples/test2.gif)

As can be seen, the individual estimations are not perfect. There are times when the pose is estimated incorrectly, and the smartphone classifier predicts incorrectly. However, the aggregation and smoothing out allows for alleviating these problems. More work is being done to improve the misclassifications and error.

The algorithm also works decently on images of simulated pedestrians, which can be useful if combined with a driving simulator such as [CARLA](https://carla.org/)

![carla_example](https://github.com/saadejazz/trusty/blob/main/examples/simulated.gif)

## Attributions
The code is adapted from the work of [[1]](1) on eye contact detection, the work of [[2]](2) on pose estimation, and from [bounding-box](https://github.com/nalepae/bounding-box) for visualization of bounding boxes.

## References
<a id="1">[1]</a> Belkada, Y., Bertoni, L., Caristan, R., Mordan, T. and Alahi, A., 2021. Do pedestrians pay attention? eye contact detection in the wild. arXiv preprint arXiv:2112.04212.
<a id="2">[2]</a> Kreiss, S., Bertoni, L. and Alahi, A., 2021. Openpifpaf: Composite fields for semantic keypoint detection and spatio-temporal association. IEEE Transactions on Intelligent Transportation Systems, 23(8), pp.13498-13511.
