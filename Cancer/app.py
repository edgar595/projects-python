import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pickle
import numpy as np

def get_clean_data():
    data = pd.read_csv('Cancer/dataset/data.csv')
    
    data = data.drop(['Unnamed: 32', 'id'], axis=1)

    data['diagnosis'] = data['diagnosis'].map({ 'M': 1, 'B':0})

    return data



def add_sidebar():
    st.sidebar.header("Cell Nucleui Info")

    data = get_clean_data()

    input_dict = {}

        # Define the labels
    slider_labels = [
        ("Radius (mean)", "radius_mean"),
        ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"),
        ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"),
        ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"),
        ("Concave points (mean)", "concave points_mean"),
        ("Symmetry (mean)", "symmetry_mean"),
        ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"),
        ("Texture (se)", "texture_se"),
        ("Perimeter (se)", "perimeter_se"),
        ("Area (se)", "area_se"),
        ("Smoothness (se)", "smoothness_se"),
        ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"),
        ("Concave points (se)", "concave points_se"),
        ("Symmetry (se)", "symmetry_se"),
        ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"),
        ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"),
        ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"),
        ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"),
        ("Concave points (worst)", "concave points_worst"),
        ("Symmetry (worst)", "symmetry_worst"),
        ("Fractal dimension (worst)", "fractal_dimension_worst"),
    ]

    input_dict = {}

    # Add the sliders
    for label, key in slider_labels:
        input_dict[key] = st.sidebar.slider(
            label,
            min_value=float(data[key].min()),
            max_value=float(data[key].max()),
            value=float(data[key].mean())
        )
    
    return input_dict


def get_scaled_values_dict(values_dict):
    data = get_clean_data()
    X = data.drop(['diagnosis'], axis=1)

    scaled_dict = {}

    for key, value in values_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        scaled_value = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_value

    return scaled_dict


def get_radar_chart(input_dict):

    input_dict = get_scaled_values_dict(input_dict)

    categories = ['Radius','Texture','Perimeter', 'Area',
                'Smoothness', 'Concavity', 'Concave points',
                'Symmetry', 'Fractal dimension'
                ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[input_dict['radius_mean'], input_dict['texture_mean'], input_dict['perimeter_mean'],
                input_dict['area_mean'], input_dict['smoothness_mean'], input_dict['compactness_mean'],
                input_dict['concavity_mean'], input_dict['concave points_mean'], input_dict['symmetry_mean'],
                input_dict['fractal_dimension_mean']],
        theta=categories,
        fill='toself',
        name='Mean Value'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[input_dict['radius_se'], input_dict['texture_se'], input_dict['perimeter_se'], input_dict['area_se'],
            input_dict['smoothness_se'], input_dict['compactness_se'], input_dict['concavity_se'],
            input_dict['concave points_se'], input_dict['symmetry_se'], input_dict['fractal_dimension_se']],
        theta=categories,
        fill='toself',
        name='Standard Error'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[input_dict['radius_worst'], input_dict['texture_worst'], input_dict['perimeter_worst'], input_dict['area_worst'],
            input_dict['smoothness_worst'], input_dict['compactness_worst'], input_dict['concavity_worst'],
            input_dict['concave points_worst'], input_dict['symmetry_worst'], input_dict['fractal_dimension_worst']],
        theta=categories,
        fill='toself',
        name='Worst'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 1]
        )),
    showlegend=True
    )

    return fig


def add_predictions(input_dict):
    model = pickle.load(open("Cancer/model/model.pkl", "rb"))
    scaler = pickle.load(open("Cancer/model/scaler.pkl", "rb"))

    input_array = np.array(list(input_dict.values())).reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)

    prediction = model.predict(input_array_scaled)

    st.subheader("Cell cluster Analyzer")
    st.write("The cell cluster is")

    if prediction[0] == 0:
        st.write("<span class='diagnosis bright-green'>Benign</span>",
                 unsafe_allow_html=True)
    else:
        st.write("<span class='diagnosis bright-red'>Malignant</span>",
                 unsafe_allow_html=True)

    
    st.write("Probability of being benign: ", model.predict_proba(input_array_scaled)[0][0])
    st.write("Probability of being malignan: ", model.predict_proba(input_array_scaled)[0][1])

    st.write("This app can be used to make a proffesional medical diagnosis but it shouldn't be a substitute for a diagnosis")



def main():
    st.set_page_config(
        page_title="Breast cancer prediction",
        page_icon=":female-doctor:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with open("Cancer/assets/styles.css") as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


    input_dict = add_sidebar()

    with st.container():
        st.title("Breast Cancer")
        st.write("Connect this app to your cancer lab to assist in diagnosing breast cancer from tissue samples. The app uses a machine learning model to predict whether a breast mass is benign or malignant based on data received from your lab. You can also manually adjust the measurements using the sliders provided in the sidebar.")

    col1, col2 = st.columns([4,1])

    with col1:
        radar_chart = get_radar_chart(input_dict)
        st.plotly_chart(radar_chart)
    with col2:
        add_predictions(input_dict)


if __name__ == "__main__":
    main()
