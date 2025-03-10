import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array # type: ignore
import time

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
        return None

    image_resized = cv2.resize(image, (150, 150))
    image_array = img_to_array(image_resized) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # Make predictions
    predictions = model.predict(image_array)
    predicted_class_index = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_index] * 100

    return class_labels[predicted_class_index], confidence

def process_video(return_result=False, duration=15):
    """
    Process video from webcam for disease detection.
    If return_result is True, returns the prediction with highest confidence.
    Otherwise displays video feed with predictions.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access the camera")
        return None

    # For tracking the best prediction
    best_prediction = None
    highest_confidence = 0
    start_time = time.time()
    
    # For averaging predictions
    predictions_history = []
    
    while True:
        # Check if duration has elapsed (when in return_result mode)
        if return_result and (time.time() - start_time > duration):
            break
            
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

        # If significant green is detected and confidence is high
        if green_percentage > 0.1 and confidence > 50:
            # Store current prediction
            predictions_history.append((class_labels[predicted_class_index], confidence))
            
            # Keep only the most recent predictions
            if len(predictions_history) > 10:
                predictions_history.pop(0)
            
            # Update best prediction if this one is better
            if confidence > highest_confidence:
                highest_confidence = confidence
                best_prediction = (class_labels[predicted_class_index], confidence)
            
            cv2.putText(frame, f"{class_labels[predicted_class_index]}: {confidence:.2f}%", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No plant detected or low confidence", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the remaining time in return_result mode
        if return_result:
            remaining = duration - (time.time() - start_time)
            cv2.putText(frame, f"Time remaining: {int(remaining)}s", 
                        (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (255, 255, 255), 2)

        # Display the video feed
        cv2.imshow('Video Feed', frame)

        # Exit if 'q' is pressed or duration is over
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    # If we need to return a result rather than just display the video
    if return_result:
        # If we have enough predictions, find the most common one
        if len(predictions_history) > 5:
            # Count occurrences of each disease
            disease_counts = {}
            for disease, _ in predictions_history:
                if disease in disease_counts:
                    disease_counts[disease] += 1
                else:
                    disease_counts[disease] = 1
            
            # Find the most common disease
            most_common_disease = max(disease_counts.items(), key=lambda x: x[1])[0]
            
            # Get the average confidence for this disease
            confidences = [conf for disease, conf in predictions_history if disease == most_common_disease]
            avg_confidence = sum(confidences) / len(confidences)
            
            return most_common_disease, avg_confidence
        
        return best_prediction
    
    return None

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
            result = predict_image(image_path)
            if result:
                disease, confidence = result
                print(f"Detected: {disease} with {confidence:.2f}% confidence")
        elif user_input.lower() == 'q':
            print("Quitting...")
            break
        else:
            print("Invalid input. Please choose '0', '1', or 'q'.")

if __name__ == "__main__":
    main()