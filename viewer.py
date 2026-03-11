import cv2
import os

image_folder = "images"

images = [os.path.join(image_folder, img) for img in os.listdir(image_folder)]

index = 0
zoom = 1.0

while True:

    img = cv2.imread(images[index])
    h, w = img.shape[:2]

    resized = cv2.resize(img, (int(w*zoom), int(h*zoom)))

    cv2.imshow("Medical Viewer", resized)

    key = cv2.waitKey(100)

    if key == ord('q'):
        break

    elif key == 81:   # left arrow
        index = (index - 1) % len(images)

    elif key == 83:   # right arrow
        index = (index + 1) % len(images)

    elif key == ord('+'):
        zoom += 0.1

    elif key == ord('-'):
        zoom -= 0.1

cv2.destroyAllWindows()