import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array # type: ignore

model = tf.keras.models.load_model('model.h5')

class_labels = [
    'Anthracnose',
    'Bacterial Canker',
    'Cutting Weevil',
    'Die Back',
    'Gall Midge',
    'Healthy',
    'Powdery Mildew',
    'Sooty Mould'
]

def predict_image(image_path):
    """Load an image, preprocess it, and predict the disease."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not open image at {image_path}")
        return

    image_resized = cv2.resize(image, (150, 150))
    image_array = img_to_array(image_resized) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # Make predictions
    predictions = model.predict(image_array)
    predicted_class_index = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_index] * 100

    print(f"Predicted Disease: {class_labels[predicted_class_index]} with confidence {confidence:.2f}%")

def process_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access the camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Resize the frame for model input
        frame_resized = cv2.resize(frame, (150, 150))
        frame_array = img_to_array(frame_resized) / 255.0
        frame_array = np.expand_dims(frame_array, axis=0)

        # Make predictions
        predictions = model.predict(frame_array)
        predicted_class_index = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class_index] * 100

        # Check if there is enough "green" in the frame (indicating leaves)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([36, 25, 25])
        upper_green = np.array([86, 255, 255])
        green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
        green_percentage = np.sum(green_mask) / (green_mask.shape[0] * green_mask.shape[1])

        if green_percentage > 0.1:
            cv2.putText(frame, f"{class_labels[predicted_class_index]}: {confidence:.2f}%", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No tree detected", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the video feed
        cv2.imshow('Video Feed', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def process_photo(image_path):
    print("Starting Photo Mode...")
    predict_image(image_path)

def main():
    while True:
        print("\nChoose an option:")
        print("0: Video Mode")
        print("1: Photo Mode")
        print("q: Quit")
        
        user_input = input("Enter your choice: ")

        if user_input == '0':
            print("Starting Video Mode...")
            process_video()
        elif user_input == '1':
            image_path = input("Enter the full path to the image file: ")
            process_photo(image_path)
        elif user_input.lower() == 'q':
            print("Quitting...")
            break
        else:
            print("Invalid input. Please choose '0', '1', or 'q'.")

if __name__ == "__main__":
    main()