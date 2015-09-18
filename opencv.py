import cv2, subprocess

imagepath = "image.jpg"
cascPath = "haar.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

while True:
  subprocess.call(["fswebcam", "-S", "5", "image.jpg"])
  image = cv2.imread(imagepath)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  faces = faceCascade.detectMultiScale(
    gray, scaleFactor=1.1, minNeighbors = 5, minSize=(30,30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE
  )

  if len(faces)>0:
    print "Found face"
    #for (x,y,w,h) in faces:
    #  cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0),2)
    #cv2.imshow("Faces found", image)
  else:
    print "Face not found"
  #cv2.waitKey(0)
  raw_input()
