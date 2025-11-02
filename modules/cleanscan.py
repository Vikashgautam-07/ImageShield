import cv2
import numpy as np
from PIL import Image
import logging

# Load the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def remove_sensitive_content(image):
    """
    Detects faces in the image and applies blur to anonymize them.
    Input: PIL image
    Output: PIL image with blurred faces
    """
    try:
        # Convert PIL image to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        logging.info(f"Detected {len(faces)} faces")
        
        # Blur each face region
        for (x, y, w, h) in faces:
            face_region = cv_image[y:y+h, x:x+w]
            blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
            cv_image[y:y+h, x:x+w] = blurred_face
        
        # Convert back to PIL format
        result_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        return result_image

    except Exception as e:
        logging.error(f"Error in remove_sensitive_content: {e}")
        return image
