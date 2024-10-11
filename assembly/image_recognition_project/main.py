import cv2
import numpy as np
from model import load_data, create_model
from image_processing import (
    load_image,
    preprocess_image,
    resize_image,
    normalize_image,
    edge_detection,
    convert_to_gray,
    show_images
)

# Görüntü dosyasını yükleyip gri tonlamaya çevir
def process_image(image_path):
    image = load_image(image_path)
    gray_image = convert_to_gray(image)
    
    # Pikselleri düzleştir ve ikili dosyaya yaz
    pixels = gray_image.flatten()
    with open("pixels.bin", "wb") as f:
        f.write(pixels)

    show_images(image, gray_image)  # Orijinal ve gri görüntüyü göster
    return gray_image

# BMP dosyası oluşturma
def create_bmp(filename):
    width = 2
    height = 2
    padding = (4 - (width * 3) % 4) % 4

    with open(filename, "wb") as f:
        # BMP Header
        f.write(b'BM')  # Signature
        f.write((54 + (width * height * 3) + (height * padding)).to_bytes(4, 'little'))  # File size
        f.write(b'\x00\x00')  # Reserved 1
        f.write(b'\x00\x00')  # Reserved 2
        f.write(b'\x36\x00\x00\x00')  # Offset to pixel data
        f.write(b'\x28\x00\x00\x00')  # Header size
        f.write(width.to_bytes(4, 'little'))  # Width
        f.write(height.to_bytes(4, 'little'))  # Height
        f.write(b'\x01\x00')  # Planes
        f.write(b'\x18\x00')  # Bits per pixel
        f.write(b'\x00\x00\x00\x00')  # Compression
        f.write((width * height * 3).to_bytes(4, 'little'))  # Image size
        f.write(b'\x13\x0B\x00\x00')  # X pixels per meter
        f.write(b'\x13\x0B\x00\x00')  # Y pixels per meter
        f.write(b'\x00\x00\x00\x00')  # Total colors
        f.write(b'\x00\x00\x00\x00')  # Important colors

        # Pixel Data (RGB format)
        f.write(b'\x00\x00\xFF')  # Blue
        f.write(b'\x00\xFF\x00')  # Green
        f.write(b'\xFF\x00\x00')  # Red
        f.write(b'\xFF\xFF\xFF')  # White

        # Padding
        f.write(b'\x00' * padding)


def main():
    image_path = 'kedi.webp'  
    gray_image = process_image(image_path)  
    create_bmp("input.bmp")  

    (x_train, y_train), (x_test, y_test) = load_data()
    model = create_model()
    model.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.2)

    test_loss, test_acc = model.evaluate(x_test, y_test)
    print(f"Test kaybı: {test_loss}, Test doğruluğu: {test_acc}")

    resized_image = resize_image(gray_image, 224, 224)
    normalized_image = normalize_image(resized_image)
    edges = edge_detection(normalized_image)
    cv2.imwrite('output_edges.jpg', edges)

    print("Görüntü işleme tamamlandı.")

if __name__ == "__main__":
    main()


