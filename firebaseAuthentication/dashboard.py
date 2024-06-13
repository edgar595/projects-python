import pandas as pd
import plotly.graph_objs as go

def generate_dashboard(user_email):
    # Read the CSV file
    cema = pd.read_csv("C:/Users/USER/Downloads/cema_internship_task_2023.csv")

    # Sort values by period
    cema.sort_values(by='period', inplace=True)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cema['period'], y=cema['Total Dewormed'], mode='lines+markers'))
    fig.update_layout(
        title='Total Dewormed Over Period',
        xaxis=dict(tickangle=45),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    # Convert Plotly figure to HTML string
    plot_html = fig.to_html(full_html=False)

    # Generate the HTML content of the dashboard dynamically
    dashboard_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <script>
            function logout() {{
                window.location.href = "/login";
            }}
        </script>
        <link rel="stylesheet" href="assets/styles.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/remixicon/fonts/remixicon.css"> 
    <body>
        <div class="header-container">
            <div class="user-email">
                <i class="ri-user-line"></i>
                <span id="userEmail">{user_email}</span>!
                <button id="logoutButton" onclick="logout()">Logout</button>
            </div>
            
            <h3>Health Analysis</h3>
        </div>

        <h1>Welcome to A health aanalysis report</h1>
  
        <!-- Plot -->
        <div class="container">
        <div class="hello-container">
            <h2>Report</h2>
            <img src="assets\img\children.jpg" alt="img">
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
        </div>
        <div class="plot-container">
            {plot_html}
        </div>
        </div>


    </body>
    </html>
    """

    return dashboard_content
