import cv2
import mediapipe as mp
import pyautogui

webcam = cv2.VideoCapture(0)
webcam.set(3,240)
webcam.set(4,280)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
x1 = y1 = x2 = y2 = 0


while True:
    _ , image = webcam.read()
    image = cv2.flip(image,1)
    frame_height, frame_width, _ = image.shape
    rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks
    if hands:
      for hand in hands:
          drawing_utils.draw_landmarks(image,hand)
          landmarks = hand.landmark
          for id, landmark in enumerate(landmarks):
              x = int(landmark.x * frame_width)
              y = int(landmark.y * frame_height)
              if id == 8:
                  cv2.circle(img=image, center=(x,y),radius=8, color=(0,255,255),thickness=3)
                  x1 = x
                  y1 = y
              if id == 4:
                  cv2.circle(img=image, center=(x,y),radius=8, color=(0,0,255),thickness=3)
                  x2 = x
                  y2 = y
      dist = ((x2-x1)**2 + (y2-y1)**2) **(0.5) 
      cv2.line(image,(x1,y1),(x2,y2),(0,255,0),5)
      if dist > 30:
          pyautogui.press("volumeup")
          volume_status = "Volume Up"
      else: 
          pyautogui.press("volumedown")
          volume_status = "Volume Down"
      cv2.putText(image, volume_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 0, 0), 3, cv2.LINE_AA)    
                      
    cv2.imshow("Volume Hand Control",image)    
    key = cv2.waitKey(10)
    