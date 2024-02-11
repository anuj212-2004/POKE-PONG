import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pygame

pygame.init()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread("collection/background.png")
imgGameover = cv2.imread("collection/Gameover.png")
imgBall = cv2.imread("collection/pokeball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("collection/pikachu.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("collection/charmander.png", cv2.IMREAD_UNCHANGED)

# hand detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Sound sfx
pygame.mixer.music.load("collection/bg music.mp3")
pikachu_sfx = pygame.mixer.Sound("pikachu.mp3")
charmander_sfx = pygame.mixer.Sound("charmander.mp3")

# Variables
ballpos = [150, 140]
speedX = 15
speedY = 15
gameOver = False
score = [0, 0]

# Start playing background music
pygame.mixer.music.play(-1)  # -1 to loop indefinitely

while True:
    _, img = cap.read()

    img = cv2.flip(img, 1)  # 0 for vertical  & 1 for Horizontal flipping
    imgRaw = img.copy()
    # find hands and its landmarks
    hands, img = detector.findHands(img, flipType=False)

    # overlaying
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)  # for transparency of bg

    # Check for Hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 20, 415)

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1160, y1))
                if 1160 - 50 < ballpos[0] < 1160 and y1 < ballpos[1] < y1 + h1:
                    speedX = -speedX
                    ballpos[0] -= 40
                    score[1] += 1
                    charmander_sfx.play()

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 62 < ballpos[0] < 62 + w1 and y1 < ballpos[1] < y1 + h1:
                    speedX = -speedX
                    ballpos[0] += 30
                    score[0] += 1
                    pikachu_sfx.play()

    # Game Over
    if ballpos[0] < 40 or ballpos[0] > 1200:
        gameOver = True
    if gameOver:
        img = imgGameover
        cv2.putText(img, str("Press R->Restart or Q->Exit"), (180, 80), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
        cv2.putText(img, str(score[0] ).zfill(2), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 225, 225), 5)
        cv2.putText(img, str(score[1]).zfill(2), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 127, 225), 5)
        cv2.putText(img, str("PIKACHU"), (300, 560), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 204, 204), 2)
        cv2.putText(img, str("CHARMANDER"), (750, 560), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 127, 225), 2)
        img = cvzone.overlayPNG(imgGameover, imgBat2, (1050,560 ))
        img = cvzone.overlayPNG(imgGameover, imgBat1, (450, 560))
        #cv2.putText(img, str(score[0] + score[1]).zfill(2),(560, 650) , cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200),5)
    # If Game not Over Move the Ball
    else:
        # Move the Ball
        if ballpos[1] >= 500 or ballpos[1] <= 10:  # Bouncing of Ball
            speedY = -speedY

        ballpos[0] += speedX
        ballpos[1] += speedY

        # Draw the Ball
        img = cvzone.overlayPNG(img, imgBall, ballpos)

        # Below Score Display
        cv2.putText(img, str("Score"), (500, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 0), 5)
        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 127, 255), 5)

    img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        ballpos = [150, 140]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameover = cv2.imread("collection/Gameover.png")

    if key == ord('q'):
        break  # Exit the loop if 'q' is pressed

# Release resources
cap.release()
cv2.destroyAllWindows()