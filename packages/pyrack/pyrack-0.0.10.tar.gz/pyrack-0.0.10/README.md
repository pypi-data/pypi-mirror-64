This is a python package to analyze detections conducted across different types of documents. In the current version, it supports only objects detected in images.

This version is compatible with object detection performed by [ImageAI](https://github.com/OlafenwaMoses/ImageAI) using the pre-trained weights of [ResNet50](https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/resnet50_coco_best_v2.0.1.h5).

Download and place the aforementioned pre-trained weights in your local folder.

All the implementations and testing were performed using random samples from the [MS COCO 2017](http://cocodataset.org/#download) dataset. Do look into the notebooks in the [Demo](https://github.com/sidvenkat1988/pyrack/tree/master/Demo) folder to conduct some experiments on your custom data. 

# Installation
Install this package with the following command:
```
pip install --upgrade pyrack
```
In order to detect objects and perform some analysis on them, import the package with the following command:
```
from pyrack import object as obj
```

# Functionalities
The following functions can be implemented with the current version\
1) ## Reading an image

This function reads and stores an image in the RGB color-space in the form of numpy arrays.
```
img = obj.img(image_path)
```

2) ## Displaying the image

This loads the image that was read in the previous step.

```
obj.display_original_image(img)
```

<img width="176" alt="original_image" src="https://user-images.githubusercontent.com/49531274/78113256-bfcd9f00-73ff-11ea-91da-35103c331c3f.png">

3) ## Defining the model path

Here we need to mention the path where we have stored the pre-trained model weights meant for object detection.

```
model_path = obj.model_weights(os.path.join(path, 'resnet50_coco_best_v2.0.1.h5'))
```

4) ## Detecting objects in the image

With the help of the pre-trained weights loaded above, we perform object detections on the image loaded in step 1.

```
detections = obj.detections(img)
```

5) ## Get all detected objects

Here we print a list of all the objects that were detected in the previous step.

```
detected_objects = obj.detected_objects(img, detections)
print(detected_objects)
```

6) ## Getting the bounding-box(bbox) coordinates for all the detected objects

Here we extract the bbox co-ordinates for each detected object.

```
bbox = obj.bbox(detections)
```

7) ## Getting the regions of interest(roi)

From the bbox extracted above, we can draw roi's around the detected images on which we can perform further actions.

```
roi = obj.roi(img, detections)
```

8) ## Resizing the roi's

Here we resize each roi to a dimension of (100,100,3). Objects that are too small will be padded with black pixels before being resized.

```
resized_roi = obj.resized_roi(img, roi)
```

9) ## Number of detections

Here we print the total number of detections performed on the loaded image.

```
obj.number_of_detections(img, detections)
```

10) ## Unique items detected

This function returns all the unique items detected in the image.

```
obj.unique_items_detected(img, detected_objects)
```

11) ## Count of each unique object

Here we get to see the count per unique object detected in the image.

```
obj.count_per_unique_item(img, detected_objects)
```

<img width="423" alt="count_of_each_object" src="https://user-images.githubusercontent.com/49531274/78113235-ba705480-73ff-11ea-90f9-fd21c26f6122.png">

12) ## Shape of each detected object

Here we get to see the 3-dimensional shape of each detected object.

```
obj.detected_objects_shape(img, detected_objects, roi)
```

13) ## Display all detected objects

Here we display each detected object from the image individually.

```
obj.display_all_objects(img, detected_objects, roi)
```

<img width="343" alt="display_all_objects" src="https://user-images.githubusercontent.com/49531274/78113236-bb08eb00-73ff-11ea-93fa-631373267fa6.png">

14) ## Display specific objects

Here we give an option to display only specific objects detected in the image.

```
obj.display_specific_image(img, detected_objects, roi)
```

<img width="320" alt="display_specific_objects" src="https://user-images.githubusercontent.com/49531274/78113252-be03db80-73ff-11ea-9bbc-3b9cab0c4c06.png">

15) ## Display all resized objects

Here, all the resized roi's will be concatenated and displayed as one image of all the detected objects.

```
obj.display_all_resized_objects(img, detected_objects, resized_roi)
```

<img width="448" alt="display_resized_objects" src="https://user-images.githubusercontent.com/49531274/78113247-bcd2ae80-73ff-11ea-8378-8327bfe8cbaa.png">

16) ## Grouping objects by class

Here we display all detected objects grouped by their respective classes.

```
obj.group_objects_by_class(img, detected_objects, resized_roi)
```

<img width="348" alt="group_objects_by_class" src="https://user-images.githubusercontent.com/49531274/78113255-bf350880-73ff-11ea-869e-198241bed30b.png">




 