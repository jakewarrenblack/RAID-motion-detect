# Multiple threads needed to display camera data and screenshot
import threading
import winsound # Will be removed, tutorial sounds an alarm, I'll take a screenshot
import cv2
import imutils

# Use default camera, index 0
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# The idea is to get one frame, and then another, and calculate the difference
# If the difference is high enough, trigger motion detection

# _, is unnamed return value, no return
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
# Converting to grayscale, this may be removed
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
# Smooth image with gaussian blur
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0


# TODO: Change to take screenshot
def alarm():
    global alarm
    # 5 consecutive 1 second beeps
    for _ in range(5):
        if not alarm_mode:
            # terminate alarm when alarm mode exits
            break
        print("ALARM")
        winsound.Beep(2500, 1000)
    # Always end by stopping
    alarm = False


# Main loop
while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    # if currently in alarm mode, calc distances to determine if alarm or not
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        # calc diff between start frame and this frame
        difference = cv2.absdiff(frame_bw, start_frame)
        # we have grayscale pixels with varying likeness between 255 and 0, above is 255, below is 0, only 2 values to worry about
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        # for the NEXT iteration, THIS frame will be the one to calc diff between
        start_frame = frame_bw

        # calc sum of threshold difference and define a value to look for
        # lower is more sensitive
        if threshold.sum() > 300:
            alarm_counter+= 1
        else:
            if alarm_counter > 0:
                # decrease alarm every time a threshold over 300 detected
                alarm_counter -= 1

        cv2.imshow("Cam", threshold)
    else:
        # if alarm not active, show normal cam
        cv2.imshow("Cam", frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=alarm).start()

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        # if t pressed (toggle), disable alarm, reset
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break

# When quit
cap.release()
cv2.destroyAllWindows()
