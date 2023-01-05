import requests
import cv2
import numpy 
task_1b = __import__('task_1b')

  
# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = "http://192.168.152.71:8080/shot.jpg"
  
# While loop to continuously fetching data from the Url
while True:
    img_resp = requests.get(url)
    img_arr = numpy.array(bytearray(img_resp.content), dtype=numpy.uint8)
    img = cv2.imdecode(img_arr, -1)
    img=cv2.resize(img, (800, 500))
    try:
        a,b =task_1b.detect_ArUco_details(img)
        img=task_1b.mark_ArUco_image(img,a,b)
    except:
        pass
    cv2.imshow("Android_cam", img)
  
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
  
cv2.destroyAllWindows()