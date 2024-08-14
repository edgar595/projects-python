# Breast Cancer Prediction Project

## Project Overview
This project is a machine learning-based application designed to assist in the diagnosis of breast cancer. It uses cell nuclei measurements to predict whether a breast mass is benign or malignant. The application provides an interactive interface built with Streamlit, allowing users to adjust various cell measurements and receive real-time predictions.

## Key Features
- **Interactive Data Input:** Sidebar sliders for adjusting 30 different cell nuclei measurements.
- **Data Visualization:** Radar chart displaying mean, standard error, and worst values for various cell characteristics.
- **Machine Learning Prediction:** Utilizes a pre-trained model to predict cancer diagnosis.
- **Probability Scores:** Displays the probability of the mass being benign or malignant.
- **Responsive Design:** Custom CSS styling for an enhanced user experience.

## Data Processing

### Data Cleaning
- **Libraries Used:** Pandas is employed for data manipulation and cleaning.
- **Methodology:** Removes unnecessary columns, maps diagnosis labels to binary values (0 for Benign, 1 for Malignant).

### Feature Scaling
- **Purpose:** To normalize the input features for consistent model performance.
- **Technique:** Uses a pre-trained scaler (likely StandardScaler or MinMaxScaler) to scale input values.

## Modeling

### Machine Learning Model
- **Model Type:** The specific model type is Logistic Regression
- **Model Loading:** The trained model is loaded from a pickle file (`model.pkl`).
- **Prediction:** The model predicts the probability of benign and malignant outcomes based on the input features.

## Application Features

### Streamlit Interface
- **Sidebar Input:** Sliders for 30 different cell nuclei measurements, allowing users to adjust values interactively.
- **Main Display:** 
  - Radar chart visualization of input data.
  - Prediction output showing benign or malignant diagnosis.
  - Probability scores for both outcomes.

### Data Visualization
- **Radar Chart:** Uses Plotly to create an interactive radar chart displaying mean, standard error, and worst values for various cell characteristics.
- **Dynamic Updates:** The chart updates in real-time as users adjust the input sliders.

### Prediction Display
- **Color-Coded Output:** Displays the prediction (Benign or Malignant) with appropriate color coding (green for Benign, red for Malignant).
- **Probability Scores:** Shows the probability of the mass being benign or malignant.

## Getting Started

## Usage
1. Launch the Streamlit app.
2. Use the sidebar sliders to input or adjust cell nuclei measurements.
3. Observe the radar chart updating in real-time.
4. View the prediction and probability scores in the main panel.

## Important Note
The README includes a disclaimer stating that while the app can be used to assist in professional medical diagnosis, it should not be considered a substitute for a proper medical diagnosis.

## Future Improvements
- Integration with actual lab equipment for direct data input.
- Incorporation of additional diagnostic features or imaging data.
- Expansion of the model to predict more specific cancer types or stages.

## Demonstration
**[Project Demonstration](https://predictingcancer.streamlit.app/):** A detailed walkthrough of the project and how various features a affect the output 