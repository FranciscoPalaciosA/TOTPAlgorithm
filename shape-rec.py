import cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX

img = cv2.imread("./shape/square-1.png", cv2.IMREAD_GRAYSCALE)
_, threshold = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    cv2.drawContours(img, [approx], 0, (0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    shape="undefined"
    if len(approx) == 3:
        shape="triangle"
        cv2.putText(img, "Triangle", (x, y), font, 1, (0))
    elif len(approx) == 4:
        shape="Rectangle"
        cv2.putText(img, "Rectangle", (x, y), font, 1, (0))
    elif len(approx) == 5:
        shape="Pentagon"
        cv2.putText(img, "Pentagon", (x, y), font, 1, (0))
    elif 6 < len(approx) < 15:
        shape="Ellipse"
        cv2.putText(img, "Ellipse", (x, y), font, 1, (0))
    else:
        shape="Circle"
        cv2.putText(img, "Circle", (x, y), font, 1, (0))
    print("Shape = ", shape)
    print("Length = ", len(approx))

cv2.imshow("shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()