import cv2
import numpy as np

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Görüntü yüklenemedi.")
    return image

def preprocess_image(image):
    # Görüntüyü gri tonlamaya çevir
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def resize_image(image, width, height):
    return cv2.resize(image, (width, height))

def normalize_image(image):
    return image / 255.0

def convert_color_space(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def blur_image(image, kernel_size=(5, 5)):
    return cv2.GaussianBlur(image, kernel_size, 0)

def edge_detection(image):
    return cv2.Canny(image, 100, 200)

def histogram_equalization(image):
    return cv2.equalizeHist(image)

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h))

def flip_image(image):
    return cv2.flip(image, 1)  # 1, yatay ayna

