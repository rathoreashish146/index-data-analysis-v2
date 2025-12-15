"""
Main application file for Index Data Analysis.
Initializes the Dash app, sets up routing, and registers callbacks.
"""

import os
from dash import Dash, html, dcc

from config import APP_INDEX_STRING
from callbacks import register_callbacks

# -----------------------------
# App Setup
# -----------------------------
app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Index Data Analysis"
app.index_string = APP_INDEX_STRING

# Expose the underlying Flask server for Gunicorn
server = app.server

# -----------------------------
# Top-level app layout with router
# -----------------------------
app.layout = html.Div(
    [
        html.Div(id="navbar-container"),
        dcc.Location(id="url"),
        html.Div(id="page-content"),
    ],
    id="app-container",
    style={
        "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif",
        "minHeight": "100vh",
        "padding": "0",
        "margin": "0",
        "background": "#0a0a0a",
        "color": "white",
        "transition": "background-color 0.3s ease, color 0.3s ease"
    }
)

# Register all callbacks
register_callbacks(app)

# -----------------------------
# Local run (useful for dev & Render health checks)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=False)
