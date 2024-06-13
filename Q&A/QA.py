from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
from transformers import ViltProcessor, ViltForQuestionAnswering
from io import BytesIO

load_dotenv()

@st.cache_resource(show_spinner="Loading model...")
def load_model():
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    return model, processor

def process_query(image, query):
    model, processor = load_model()
    encoding = processor(image, query, return_tensors="pt")
    outputs = model(**encoding)
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    return model.config.id2label[idx]

def convert_png_to_jpg(image):
    rgb_image = image.convert('RGB')
    byte_arr = BytesIO()
    rgb_image.save(byte_arr, format='JPEG')
    byte_arr.seek(0)
    return Image.open(byte_arr)


def app():
    st.title("Visual Question and Answering based on IMAGE")
    # Sidebar contents
    with st.sidebar:
        st.title('About')
        st.markdown('''
        This app is built using:
        - [Streamlit](https://streamlit.io/)
        - [ViLT](https://huggingface.co/dandelin/vilt-b32-finetuned-vqa)
        ''')
        st.write('Made by [eddy](https://edgaresume.netlify.app/)')
        st.write('Repository [Github](https://github.com/edgar595)')

    uploaded_file = st.file_uploader('Upload your IMAGE', type=['png', 'jpeg', 'jpg'], key="imageUploader")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # ViLT model only supports JPG images
        if image.format == 'PNG':
            image = convert_png_to_jpg(image)

        st.image(image, caption='Uploaded Image.', width=300)
        
        cancel_button = st.button('Cancel')
        query = st.text_input('Ask a question to the IMAGE')

        if query:
            with st.spinner('Processing...'):
                answer = process_query(image, query)
                st.write("Answer:", answer)
          
        if cancel_button:
            st.stop()
            

app()
