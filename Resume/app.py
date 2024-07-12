import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, ALL
import os
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import base64
import io
import json  # Import JSON module

# Function to extract text from PDFs
def extract_pdf_text(directory):
    pdf_resumes = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'rb') as file:
                reader = PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() or ""
                pdf_resumes.append((filename, text))
    return pdf_resumes

# Directory containing PDF resumes
directory = 'Resume/data/data/ICT'

# Extract PDF text
pdf_resumes = extract_pdf_text(directory)

def extract_text_from_pdf(file_content):
    pdf_content = io.BytesIO(file_content)
    reader = PdfReader(pdf_content)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dash layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Top Ranked CVs Based on Job Description", 
                            className="text-center my-4",
                            style={'color': '#0056b3'}))),
    dbc.Row(
        dbc.Col(
            dcc.Dropdown(
                id='category-dropdown',
                options=[
                    {'label': 'ICT', 'value': 'ICT'},
                    {'label': 'HR', 'value': 'HR'},
                    {'label': 'Sales', 'value': 'Sales'}
                ],
                value='ICT',
                style={'width': '50%', 'color': 'black', 'margin': '0 auto'}
            ),
            width=12, style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'padding': '20px'}
        ),
        justify='center'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Total Documents", style={'background-color': '#0056b3', 'color': 'black'}),
                dbc.CardBody(html.H5(id='total-documents', className='card-text', style={'color': 'black'})),
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Total Departments", style={'background-color': '#0056b3', 'color': 'black'}),
                dbc.CardBody(html.H5(id='total-departments', className='card-text', style={'color': 'black'})),
            ])
        ], width=6)
    ], className='mb-4'),
    dbc.Row([
        # Job Description Card (75% width)
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Enter Job Description", 
                               style={'background-color': '#0056b3', 'color': 'white'}),
                dbc.CardBody([
                    dcc.Textarea(
                        id="job-description",
                        placeholder="Paste your job description here...",
                        style={"width": "100%", "height": "150px", "border": "1px solid #ced4da", "borderRadius": "0.25rem"}
                    ),
                    dbc.Button("Submit", id="submit-button", color="primary", className="mt-3")
                ])
            ], className="mb-4"),
            dbc.Card([
                dbc.CardHeader("Or Upload Job Description PDF", 
                               style={'background-color': '#0056b3', 'color': 'white'}),
                dbc.CardBody([
                    dcc.Upload(
                        id="upload-job-description",
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%', 'height': '60px',
                            'lineHeight': '60px', 'borderWidth': '1px',
                            'borderStyle': 'dashed', 'borderRadius': '5px',
                            'textAlign': 'center', 'margin': '10px'
                        },
                        multiple=False
                    ),
                    html.Div(id="upload-status")
                ])
            ])
        ], width=9),  # 75% width
        
        # Ranked Resumes (25% width)
        dbc.Col([
            html.H4("Top Ranked Resumes", className="mb-3"),
            html.Div(id="ranked-resumes"),
        ], width=3)  # 25% width
    ]),
    # Modal for displaying PDF
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("PDF Viewer")),
        dbc.ModalBody(dcc.Loading(dbc.Container(id="pdf-viewer", fluid=True)))
    ], id="pdf-modal", size="lg", is_open=False)
], fluid=True)

@app.callback(
    Output("total-documents", "children"),
    Input("category-dropdown", "value")
)
def update_total_documents(selected_category):
    directory = f'data/data/{selected_category}'
    pdf_resumes = extract_pdf_text(directory)
    return f"{len(pdf_resumes)} documents"

@app.callback(
    Output("total-departments", "children"),
    Input("category-dropdown", "value")
)
def update_total_departments(selected_category):
    total_departments = len([{'label': 'ICT', 'value': 'ICT'},
                             {'label': 'HR', 'value': 'HR'},
                             {'label': 'Sales', 'value': 'Sales'}])
    return f"{total_departments} departments"

# Callback to update ranked resumes based on job description or uploaded PDF
@app.callback(
    Output("ranked-resumes", "children"),
    Output("upload-status", "children"),
    Output("pdf-viewer", "children"),
    Output("pdf-modal", "is_open"),
    Input("submit-button", "n_clicks"),
    Input("upload-job-description", "contents"),
    Input({"type": "resume-link", "index": ALL}, "n_clicks"),
    State("upload-job-description", "filename"),
    State("upload-job-description", "last_modified"),
    State("job-description", "value"),
    State("category-dropdown", "value")
)
def update_ranked_resumes(submit_n_clicks, uploaded_file_content, resume_link_n_clicks, uploaded_file_name, uploaded_file_date, job_description, selected_category):
    ctx = dash.callback_context

    directory = f'data/data/{selected_category}'
    pdf_resumes = extract_pdf_text(directory)

    if not job_description and not uploaded_file_content:
        return html.P("Please enter a job description or upload a PDF file."), "", "", False

    # Extract text from the uploaded PDF
    if uploaded_file_content is not None:
        _, content_string = uploaded_file_content.split(",")
        decoded = base64.b64decode(content_string)
        job_description = extract_text_from_pdf(decoded)

    # Compute similarity scores
    def compute_similarity(pdf_resumes, job_description):
        resume_texts = [text for _, text in pdf_resumes]
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(resume_texts)
        job_vector = vectorizer.transform([job_description])
        similarities = cosine_similarity(job_vector, tfidf_matrix).flatten()
        return [(filename, similarity) for filename, similarity in zip([filename for filename, _ in pdf_resumes], similarities)]

    ranked_resumes = sorted(compute_similarity(pdf_resumes, job_description), key=lambda x: x[1], reverse=True)

    # Create table for top ranked resumes
    table_header = [
        html.Thead(html.Tr([html.Th("Rank"), html.Th("File"), html.Th("Score")]))
    ]
    table_rows = [
        html.Tr(
            [
                html.Td(f"{i + 1}"),
                html.Td(
                    html.A(
                        filename,
                        href="#",
                        id={"type": "resume-link", "index": i},
                        className="resume-link",
                    )
                ),
                html.Td(f"{similarity:.2%}"),
            ]
        )
        for i, (filename, similarity) in enumerate(ranked_resumes[:10])  
    ]
    table_body = [html.Tbody(table_rows)]
    ranked_table = dbc.Table(
        table_header + table_body,
        bordered=True,
        striped=True,
        hover=True,
        className="table",
    )

    upload_status = ""
    if uploaded_file_content is not None:
        upload_status = f"Uploaded: {uploaded_file_name}"

    # Handle PDF viewing
    pdf_viewer_content = ""
    pdf_modal_open = False
    if resume_link_n_clicks:
        clicked_index = ctx.triggered[0]["prop_id"].split(".")[0]
        index = int(json.loads(clicked_index)["index"])
        filename = ranked_resumes[index][0]
        filepath = os.path.join(directory, filename)
        with open(filepath, "rb") as file:
            encoded_pdf = base64.b64encode(file.read()).decode("utf-8")
            pdf_viewer_content = html.Embed(
                src=f"data:application/pdf;base64,{encoded_pdf}",
                type="application/pdf",
                width="100%",
                height="800px",
            )
        pdf_modal_open = True

    return ranked_table, upload_status, pdf_viewer_content, pdf_modal_open

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
