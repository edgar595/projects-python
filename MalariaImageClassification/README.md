## Malaria Image Classification

### Project Overview
This project focuses on classifying malaria images as infected or uninfected using deep learning techniques. Malaria is a life-threatening disease caused by parasites that are transmitted through mosquitoes. Early and accurate diagnosis of malaria is crucial for effective treatment and management. The project utilizes a dataset of malaria cell images and employs TensorFlow for building and training the classification model.

### Data Preprocessing
- **Image Loading and Augmentation:** Images were loaded and augmented to increase the diversity of the training set and improve the model's ability to generalize.
- **Normalization:** Pixel values of the images were normalized to ensure consistent input to the neural network.
- **Train-Test Split:** The dataset was split into training and testing sets to evaluate the model's performance.

### Model Architecture
- **Convolutional Neural Network (CNN):** A CNN architecture was chosen for its ability to effectively capture spatial hierarchies in images.
- **Layers:** The model consists of convolutional layers for feature extraction followed by pooling layers for dimensionality reduction and fully connected layers for classification.
- **Activation Functions:** ReLU activation was used in convolutional layers, and softmax activation in the output layer for multiclass classification.

### Training
- **Optimizer:** Adam optimizer was used to minimize the categorical cross-entropy loss function.
- **Hyperparameters:** Batch size, learning rate, and number of epochs were tuned to achieve optimal training performance.
- **Evaluation:** Model performance was evaluated using accuracy, precision, recall, and F1-score metrics on the test set.

### Model Evaluation
- **Confusion Matrix:** Visualized the confusion matrix to analyze the model's performance in classifying infected and uninfected malaria cells.
- **ROC Curve:** Plotted the Receiver Operating Characteristic (ROC) curve and calculated the Area Under the Curve (AUC) to assess the model's sensitivity and specificity.

### Dash Dashboard
A Dash application was developed to showcase the malaria image classification model:
- **Upload Interface:** Users can upload malaria cell images for classification.
- **Prediction:** The application predicts whether the uploaded cell images are infected or uninfected based on the trained model.
- **Visualization:** Results are displayed with predicted labels and confidence scores, enhancing user interaction and understanding.

