import Augmentor

img = Augmentor.Pipeline(r"E:\0610\seongnamfalse0125_flipping\dataset")

img.flip_left_right(probability=1.0)

img.sample(45)

