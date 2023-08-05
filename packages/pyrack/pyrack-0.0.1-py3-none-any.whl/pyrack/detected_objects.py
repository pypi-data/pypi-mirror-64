class objects:
  def __init__(self):
    pass
  #Total number of objects detected in the image
  def number(detected):
  	if len(detected) > 0:
  		if len(detected) == 1:
  			return '1 object detected'
  		else:
  			return '{} objects detected'.format(len(detected))
  	else:
  		return 'No objects detected'
  
  #Unique objects detected in the image
  def unique(detected):
    if len(detected) > 0:
      detected_object = []
      for i in range(len(detected)):
        detected_object.append(detected[i]['name'])
      unique_objects = list(set(detected_object))
      if len(unique_objects) > 1:
        return 'The following unique objects were detected : {}'.format(unique_objects)
      else:
        unique_objects = unique_objects[0]
        return 'Unique object detected - {}'.format(unique_objects)
    else:
      return 'No objects detected'

  #Count of each unique object detected in the image
  def unique_num(detected):
    if len(detected) > 0:
      detected_objects = []
      for i in range(len(detected)):
        detected_objects.append(detected[i]['name'])
      df = pd.DataFrame(columns = ['Unique Objects Detected'])
      df['Unique Objects Detected'] = detected_objects
      df['Count'] = df['Unique Objects Detected'].map(df['Unique Objects Detected'].value_counts(dropna = False))
      df = df.drop_duplicates(subset = ['Unique Objects Detected', 'Count'], keep = 'first')
      df = df.sort_values('Count', ascending = False)
      df = df.reset_index(drop = True)
      return df
    else:
      return 'No objects detected'


  #Displaying the image shape of the detected objects
  def object_shape(detected):
    if len(detected) > 0:
      bbox = []
      roi_shape = []
      detected_object = []
      for i in range(len(detected)):
        bbox.append(detected[i]['box_points'])
        detected_object.append(detected[i]['name'])
      for i in bbox:
        for (x,y,w,h) in [i]:
          cropped_img = img[y:y+h, x:x+w]
          roi_shape.append(cropped_img.shape)
      df = pd.DataFrame(columns = ['Detected Object', 'Image Dimensions'])
      df['Detected Object'] = detected_object
      df['Image Dimensions'] = roi_shape
      return df
    else:
      return 'No objects detected'

  #Displaying all original sized objects
  def display_all_original_objects(detected):
    if len(detected) > 0:
      bbox = []
      roi = []
      detected_object = []
      for i in range(len(detected)):
        bbox.append(detected[i]['box_points'])
        detected_object.append(detected[i]['name'])
      for i in bbox:
        for (x,y,w,h) in [i]:
          cropped_img = img[y:y+h, x:x+w]
          for (h, w, d) in [cropped_img.shape]:
            if h > 50 and w > 50:
              roi.append(cropped_img)
            elif h > 50 and w < 50:
              cropped_img = cv2.copyMakeBorder(cropped_img, 0, 0, (150 - w), (150 - w), cv2.BORDER_CONSTANT, value = (255,255,255))
              cropped_img = cv2.putText(cropped_img, 'Image too small to be displayed', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
              roi.append(cropped_img)
            elif h < 50 and w > 50:
              cropped_img = cv2.copyMakeBorder(cropped_img, (150 - h), (150 - h), 0, 0, cv2.BORDER_CONSTANT, value = (255,255,255))
              cropped_img = cv2.putText(cropped_img, 'Image too small to be displayed', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
              roi.append(cropped_img)
            else:
              cropped_img = cv2.copyMakeBorder(cropped_img, (150 - h), (150 - h), (150 - w), (150 - w), cv2.BORDER_CONSTANT, value = (255,255,255))
              cropped_img = cv2.putText(cropped_img, 'Image too small to be displayed', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
              roi.append(cropped_img)
      if len(detected_object) > 1:
        fig, ax = plt.subplots(1, len(detected_object))
        for i in range(len(detected_object)):
          a = ax[i].imshow(roi[i])
          a = ax[i].set_title(detected_object[i])
          a = ax[i].axis('off')
        a = fig.suptitle('All objects detected in the image', size = 20)
        #a = fig.title('Some images may be too small to be displayed')
        a = plt.show()
        return a
      else:
        roi = roi[0]
        detected_object = detected_object[0]
        a = plt.imshow(roi)
        a = plt.suptitle('The only detected object in the image', size = 20)
        a = plt.title(detected_object)
        a = plt.axis('off')
        a = plt.show()
        return a
    else:
      return 'No objects detected'

  #Display specific objects
  def display_specific_object(detected):
    if len(detected) > 0:
      bbox = []
      roi = []
      detected_object = []
      for i in range(len(detected)):
        bbox.append(detected[i]['box_points'])
        detected_object.append(detected[i]['name'])
      for i in bbox:
        for (x,y,w,h) in [i]:
          cropped_img = img[y:y+h, x:x+w]
          for (h, w, d) in [cropped_img.shape]:
            if h > 50 and w > 50:
              roi.append(cropped_img)
            elif h < 50 and w > 50:
              cropped_img = cv2.copyMakeBorder(cropped_img, (150 - h), (150 - h), 0, 0, cv2.BORDER_CONSTANT, value = (255, 255, 255))
              cropped_img = cv2.putText(cropped_img, 'Too small to be displayed', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
              roi.append(cropped_img)
            elif h >50 and w < 50:
              cropped_img = cv2.copyMakeBorder(cropped_img, 0, 0, (150 - w), (150 - w), cv2.BORDER_CONSTANT, value = (255, 255, 255))
              cropped_img = cv2.putText(cropped_img, 'Too small to be displayed', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
              roi.append(cropped_img)
            else:
              cropped_img = cv2.copyMakeBorder(cropped_img, (150 - h), (150 - h), (150 - w), (150 - w), cv2.BORDER_CONSTANT, value = (255, 255, 255))
              cropped_img = cv2.putText(cropped_img, 'Too small to be displayed', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
              roi.append(cropped_img)
          #roi.append(cropped_img)
      if len(detected_object) > 1:
        df = pd.DataFrame(columns = ['detected_object'])
        df['detected_object'] = detected_object
        #df_index = list(df.index)
        specific_object = input('Which of these do you wish to be displayed : {} '.format(df['detected_object'].unique()))
        if specific_object in detected_object:
          specific_detected_object = []
          specific_roi = []
          specific_index = [i for i,x in enumerate(detected_object) if x == specific_object]
          for i in specific_index:
            specific_detected_object.append(detected_object[i])
            specific_roi.append(roi[i])
          if len(specific_detected_object) > 1:
            fig, ax = plt.subplots(1, len(specific_detected_object))
            for i in range(len(specific_detected_object)):
              a = ax[i].imshow(specific_roi[i])
              a = ax[i].axis('off')
            a = fig.suptitle('All ' + specific_object + 's detected in the image', size = 20)
            a = plt.show()
            return a
          else:
            specific_roi = specific_roi[0]
            a = plt.imshow(specific_roi)
            a = plt.suptitle('The only ' + specific_object + ' detected in the image', size = 20)
            a = plt.axis('off')
            a = plt.show()
            return a
        else:
          return 'Incorrect value entered'
      else:
        detected_object = detected_object[0]
        roi = roi[0]
        a = plt.imshow(roi)
        a = plt.suptitle('The only object detected in the image - {}'.format(detected_object), size = 20)
        a = plt.axis('off')
        a = plt.show()
    else:
      return 'No objects detected'

  #Displaying all resized objects
  def display_all_resized_objects(detected):
    if len(detected) > 0:
      bbox = []
      detected_object = []
      roi = []
      for i in range(len(detected)):
        bbox.append(detected[i]['box_points'])
        detected_object.append(detected[i]['name'])
      for i in bbox:
        for (x,y,w,h) in [i]:
          cropped_img = img[y:y+h, x:x+w]
          roi.append(cropped_img)
      resized_roi = []
      for i in range(len(roi)):
        for (h,w,d) in [roi[i].shape]:
          if h > 100 and w > 100:
            resized_img = cv2.resize(roi[i], (100, 100))
            resized_img = cv2.rectangle(resized_img, (0,0), (100,100), (0,0,0), 3)
            resized_roi.append(resized_img)
          elif h > 100 and w < 100:
            resized_img = cv2.copyMakeBorder(roi[i], 0, 0, (150 - w), (150 - w), cv2.BORDER_CONSTANT, value = (255, 255, 255))
            resized_img = cv2.putText(resized_img, 'Too small to be displayed', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            resized_img = cv2.resize(resized_img, (100,100))
            resized_img = cv2.rectangle(resized_img, (0,0), (100,100), (0,0,0), 3)
            resized_roi.append(resized_img)
          elif h < 100 and w > 100:
            resized_img = cv2.copyMakeBorder(roi[i], (150 - h), (150 - h), 0, 0, cv2.BORDER_CONSTANT, value = (255, 255, 255))
            resized_img = cv2.putText(resized_img, 'Too small to be displayed', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            resized_img = cv2.resize(resized_img, (100, 100))
            resized_img = cv2.rectangle(resized_img, (0,0), (100,100), (0,0,0), 3)
            resized_roi.append(resized_img)
          else:
            resized_img = cv2.copyMakeBorder(roi[i], (150 - h), (150 - h), (150 - w), (150 - w), cv2.BORDER_CONSTANT, value = (255, 255, 255))
            resized_img = cv2.putText(resized_img, 'Too small to be displayed', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            resized_img = cv2.resize(resized_img, (100,100))
            resized_img = cv2.rectangle(resized_img, (0,0), (100,100), (0,0,0), 3)
            resized_roi.append(resized_img)
        
      if len(resized_roi) > 1:
        resized_roi = np.hstack(resized_roi)
        #for (x,y,z) in [roi[i].shape]:
          #if x < 100 and y < 100:
            #position = (30,30)
            #resized_roi = cv2.putText(resized_roi, 'Images in white are too small to be displayed', position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
          #elif x > 100 and y < 100:
            #position = (30,30)
            #resized_roi = cv2.putText(resized_roi, 'Images in white are too small to be displayed', position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
          #elif x < 100 and y > 100:
            #position = (0,0)
            #resized_roi = cv2.putText(resized_roi, 'Images in white are too small to be displayed', position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
          #else:
            #pass
        a = plt.imshow(resized_roi)
        a = plt.suptitle('All resized objects in the following order - {}'.format(detected_object), size = 15)
        a = plt.title('Some images may be too small to be displayed')
        a = plt.axis('off')
        a = plt.show()
      else:
        resized_roi = resized_roi[0]
        a = plt.imshow(resized_roi)
        a = plt.suptitle('The only detected {} in the image - resized'.format(detected_object[0]), size = 20)
        a = plt.axis('off')
        a = plt.show()
    else:
      return 'No objects detected'

  #Grouping objects by class
  def group_objects_by_class(detected):
    if len(detected) > 0:
      bbox = []
      detected_object = []
      roi = []
      for i in range(len(detected)):
        bbox.append(detected[i]['box_points'])
        detected_object.append(detected[i]['name'])
      for i in bbox:
        for (x,y,w,h) in [i]:
          cropped_img = img[y:y+h, x:x+w]
          roi.append(cropped_img)
      if len(bbox) > 1:
        resized_roi = []
        for i in range(len(roi)):
          for (h,w,d) in [roi[i].shape]:
            if h > 100 and w > 100:
              resized_img = cv2.resize(roi[i], (100,100))
              resized_img = cv2.rectangle(resized_img, (0,0), (100,100), (0,0,0), 3)
              resized_roi.append(resized_img)
            elif h > 100 and w < 100:
              resized_img = cv2.copyMakeBorder(roi[i], 0, 0, (100-w), (100-w), cv2.BORDER_CONSTANT, value = (255,255,255))
              #resized_img = cv2.putText(resized_img, 'Image \n too \n small \n to \n be \n displayed', (10,10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)
              resized_img = cv2.resize(resized_img, (100,100))
              resized_img = cv2.rectangle(resized_img, (0,0), (100,100), (0,0,0), 3)
              resized_roi.append(resized_img)
              detected_object[i] = detected_object[i] + ' - Image too small to be displayed'

            elif h < 100 and w > 100:
              resized_img = cv2.copyMakeBorder(roi[i], (100 - h), (100 - h), 0, 0, cv2.BORDER_CONSTANT, value = (255,255,255))
              resized_img = cv2.resize(resized_img, (100, 100))
              resized_img = cv2.rectangle(resized_img, (0,0), (100,100), (0,0,0), 3)
              resized_roi.append(resized_img)
              detected_object[i] = detected_object[i] + ' - Image too small to be displayed'

            else:
              resized_img = cv2.copyMakeBorder(roi[i], (100 - h), (100 - h), (100 - w), (100 - w), cv2.BORDER_CONSTANT, value = (255,255,255))
              resized_img = cv2.resize(resized_img, (100, 100))
              resized_img = cv2.rectangle(resized_img, (0,0), (100,100), (0,0,0), 3)
              resized_roi.append(resized_img)
              detected_object[i] = detected_object[i] + ' - Image too small to be displayed'
        df = pd.DataFrame(columns = ['detected_object'])
        df['detected_object'] = detected_object
        #df = df.sort_values('detected_object', ascending = False)
        #df = df.reset_index(drop = True)
        df_index = list(df.index)
        df['df_index'] = df_index
        df = df.groupby('detected_object')['df_index'].apply(list)
        df = pd.DataFrame(df)
        unique_objects = list(df.index)
        #len_unique_objects = []
        unique_roi = []
        for i in df['df_index']:
          grouped_index = []
          grouped_roi = []
          for j in i:
            grouped_index.append(j)
          for k in grouped_index:
            grouped_roi.append(resized_roi[k])
          if len(grouped_roi) > 1:
            grouped_roi = np.hstack(grouped_roi)
            unique_roi.append(grouped_roi)
          else:
            #grouped_roi = grouped_roi
            unique_roi.append(grouped_roi[0])
          #unique_roi.append(grouped_roi[0])
        fig, ax = plt.subplots(len(unique_roi), 1)
        for i in range(len(unique_roi)):
          a = ax[i].imshow(unique_roi[i])
          a = ax[i].set_title(unique_objects[i], size = 10)
          a = ax[i].axis('off')
        a = fig.suptitle('Objects grouped by classes', size = 20)
        a = plt.show()
        return a

      else:
        a = plt.imshow(roi[0])
        a = plt.suptitle('The only ' + detected_object[0] + ' detected in the image.', size = 20)
        a = plt.axis('off')
        a = plt.show()
        return a 
    else:
      return 'No objects detected'

