import sys
import cv2


#file below must be in same directory dont dum pls
cascPath = "haarcascade_frontalface_default.xml"

#create haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

#capture video feed
video_capture = cv2.VideoCapture(0)
dog = cv2.imread('dog_filter.png')
mst = cv2.imread('moustache.png')
hat = cv2.imread('cowboy_hat.png')

def put_dog_filter(dog,fc,x,y,w,h):
    face_width = w
    face_height = h
    
    dog = cv2.resize(dog,(int(face_width*1.5),int(face_height*1.75)))
    for i in range(int(face_height*1.75)):
        for j in range(int(face_width*1.5)):
            for k in range(3):
                if dog[i][j][k]<235:
                    fc[y+i-int(0.375*h)-1][x+j-int(0.25*w)][k] = dog[i][j][k]
    return fc
def put_moustache(mst,fc,x,y,w,h):
    
    face_width = w
    face_height = h

    mst_width = int(face_width*0.4166666)+1
    mst_height = int(face_height*0.142857)+1



    mst = cv2.resize(mst,(mst_width,mst_height))

    for i in range(int(0.62857142857*face_height),int(0.62857142857*face_height)+mst_height):
        for j in range(int(0.29166666666*face_width),int(0.29166666666*face_width)+mst_width):
            for k in range(3):
                if mst[i-int(0.62857142857*face_height)][j-int(0.29166666666*face_width)][k] <235:
                    fc[y+i][x+j][k] = mst[i-int(0.62857142857*face_height)][j-int(0.29166666666*face_width)][k]
    return fc

def put_hat(hat,fc,x,y,w,h):
    
    face_width = w
    face_height = h
    
    hat_width = face_width+1
    hat_height = int(0.35*face_height)+1
    
    hat = cv2.resize(hat,(hat_width,hat_height))
    
    for i in range(hat_height):
        for j in range(hat_width):
            for k in range(3):
                if hat[i][j][k]<235:
                    fc[y+i-int(0.25*face_height)][x+j][k] = hat[i][j][k]
    return fc

while True:
    
    #capture frame by frame
    ret, frame = video_capture.read()
    #convert to GrayScale 
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors=5,
        minSize=(30,30)
    )
    #use String.format to show num faces found 
    print("Found {} faces!".format(len(faces)))

    #make rectangle around faces
    for (x,y,w,h) in faces:
        #cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)
        frame = put_moustache(mst,frame,x,y,w,h)
    #after img is processed and rectangle is rendered, frame is pushed to screen
    cv2.imshow("Video",frame)
    #basically kills if q is pressed 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#cleaning up
video_capture.release()
cv2.destroyAllWindows()



