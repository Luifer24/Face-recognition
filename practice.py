

import cv2


eyes = input('Do yo want to detect the eyes too? ')

def detect(gray, image, eyes=eyes):

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 8)

        if eyes=='yes':
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
            
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2) 

    return image

def capture(channel, save):


    if channel == 0:
        capture = cv2.VideoCapture(channel)
    else:
        capture =  cv2.VideoCapture(channel)  
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # save video
    if save == 'yes':
        code = cv2.VideoWriter_fourcc(*'DIVX')
        record = cv2.VideoWriter('video.mp4', code, 20, (width, height))

    while True:

        _, video = capture.read()
        gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
        results = detect(gray, video)
        cv2.imshow('Detectar cara en video', results)

        if save == 'yes':
            record.write(video)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    
    channel = input('Do you want to detect your own video: ')
    if channel == 'yes':
        channel = input('Put the video: ')
    else:
        channel = 0

    save = input('Do yo want to save the video? ')
    
    capture(channel, save)