
import cv2
import pytesseract
#подключение камер
cap = cv2.VideoCapture(0)

# запуск цикла
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.putText(frame, "камера 1", (40, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
    # контур
    contours, h = cv2.findContours(thresh, 1, 2)
    largest_rectangle = [0, 0]
    for cnt in contours:
        lenght = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, lenght, True)
        if len(approx) == 4:
            area = cv2.contourArea(cnt)
            if area > largest_rectangle[0]:
                largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
    x, y, w, h = cv2.boundingRect(largest_rectangle[1])

    image = frame[y:y + h, x:x + w]
    cv2.drawContours(frame, [largest_rectangle[1]], 0, (0, 255, 0), 3)
    cropped = frame[y:y + h, x:x + w]
    cv2.putText(frame, 'kontyr', (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 255))
    cv2.imshow('detect', frame)
    cv2.drawContours(frame, [largest_rectangle[1]], 0, (255, 255, 255), 18)
    # считывание текста

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    invert = 255 - opening
    cv2.imshow('negativ', image)

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    data = pytesseract.image_to_string(blur, lang="rus+eng")


    s = data
    print(s.upper())
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()



