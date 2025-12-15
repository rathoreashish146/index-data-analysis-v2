"""
Layout functions for the Index Data Analysis app.
Contains navbar, home, single index, cross index, and documentation layouts.
"""

from dash import html, dcc
from components import (
    PageContainer, Card, Field, RadioGroup, CheckboxGroup,
    DateRangePicker, FileDropzone, Button, feature_card
)
from config import STORE_RAW, STORE_META, STORE_A, STORE_B, MONTH_OPTIONS


def navbar():
    # Always dark theme
    bg_color = "#0a0a0a"
    text_color = "white"
    border_color = "rgba(255,255,255,0.1)"
    
    return html.Div(
        [
            # Left side: Logo
            html.Div([
                html.Img(
                    src="https://starlab-public.s3.us-east-1.amazonaws.com/starlab_images/transparent-slc-rgb.png",
                    style={
                        "height": "36px",
                        "marginRight": "20px",
                        "objectFit": "contain"
                    }
                ),
            ], style={"display": "flex", "alignItems": "center", "flex": 1}),
            
            # Right side: Navigation elements
            html.Div([
                dcc.Link("Home", href="/", style={
                    "marginRight": "20px", "textDecoration": "none",
                    "color": text_color, "fontSize": "14px", "fontWeight": 500,
                    "padding": "6px 12px", "borderRadius": "4px",
                    "transition": "all 0.2s"
                }),
                dcc.Link("Single Index", href="/single", style={
                    "marginRight": "20px", "textDecoration": "none",
                    "color": text_color, "fontSize": "14px", "fontWeight": 500,
                    "padding": "6px 12px", "borderRadius": "4px",
                    "transition": "all 0.2s"
                }),
                dcc.Link("Cross Index", href="/cross", style={
                    "marginRight": "20px", "textDecoration": "none",
                    "color": text_color, "fontSize": "14px", "fontWeight": 500,
                    "padding": "6px 12px", "borderRadius": "4px",
                    "transition": "all 0.2s"
                }),
                dcc.Link([
                    html.Span("📖 ", style={"marginRight": "4px"}),
                    "Documentation"
                ], href="/docs", style={
                    "textDecoration": "none",
                    "color": text_color, "fontSize": "14px", "fontWeight": 600,
                    "padding": "8px 16px", "borderRadius": "6px",
                    "transition": "all 0.2s",
                    "background": "linear-gradient(135deg, rgba(102,126,234,0.3) 0%, rgba(118,75,162,0.3) 100%)",
                    "border": "1px solid rgba(102,126,234,0.4)"
                }),
            ], style={"display": "flex", "alignItems": "center"})
        ],
        style={
            "padding": "14px 32px",
            "background": bg_color,
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-between",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
            "marginBottom": "0",
            "borderBottom": f"1px solid {border_color}",
            "transition": "background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease"
        }
    )

def home_layout():
    return html.Div(
        [
            html.Div([
                html.H1("Index Data Analysis", style={
                    "fontSize":"48px", "fontWeight":700, "marginBottom":"16px",
                    "background":"linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "WebkitBackgroundClip":"text", "WebkitTextFillColor":"transparent",
                    "backgroundClip":"text"
                }),
                html.P("Powerful financial data analysis made simple - no expertise required!", style={
                    "fontSize":"20px", "color":"rgba(255,255,255,0.7)", "marginBottom":"12px"
                }),
                html.P([
                    "📊 Upload your CSV data • 🔍 Get instant insights • 📈 Visualize trends"
                ], style={
                    "fontSize":"16px", "color":"rgba(255,255,255,0.6)", "marginBottom":"40px"
                }),
            ], style={"textAlign":"center", "marginBottom":"48px"}),
            
            # Feature cards container
            html.Div(
                [
                    feature_card(
                        icon="📊",
                        title="Single Index Analysis",
                        description="Perfect for analyzing one market index in depth",
                        features=[
                            "Find drop & gain events",
                            "Technical indicators",
                            "Statistical analysis"
                        ],
                        gradient_bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        href="/single"
                    ),
                    feature_card(
                        icon="🔀",
                        title="Cross Index Comparison",
                        description="Compare two indexes to understand their relationship",
                        features=[
                            "Correlation analysis",
                            "Relative performance",
                            "Side-by-side visualization"
                        ],
                        gradient_bg="linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                        href="/cross"
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "stretch",
                    "flexWrap": "wrap",
                    "gap": "32px",
                    "marginTop": "12px",
                    "marginBottom": "64px"
                }
            ),
            
            # Quick start guide
            html.Div([
                Card([
                    html.H3("🚀 Quick Start Guide", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"16px"}),
                    html.Div([
                        html.Div([
                            html.Strong("1. ", style={"color":"#667eea", "fontSize":"18px"}),
                            html.Strong("Prepare Your Data", style={"color":"rgba(255,255,255,0.95)"}),
                            html.P("CSV file with 2 columns: Date and Index Value", style={"fontSize":"14px", "color":"rgba(255,255,255,0.7)", "marginTop":"4px", "marginLeft":"24px"})
                        ], style={"marginBottom":"16px"}),
                        html.Div([
                            html.Strong("2. ", style={"color":"#667eea", "fontSize":"18px"}),
                            html.Strong("Choose Analysis Type", style={"color":"rgba(255,255,255,0.95)"}),
                            html.P("Single index for detailed analysis or Cross index for comparison", style={"fontSize":"14px", "color":"rgba(255,255,255,0.7)", "marginTop":"4px", "marginLeft":"24px"})
                        ], style={"marginBottom":"16px"}),
                        html.Div([
                            html.Strong("3. ", style={"color":"#667eea", "fontSize":"18px"}),
                            html.Strong("Upload & Analyze", style={"color":"rgba(255,255,255,0.95)"}),
                            html.P("Upload your file, configure settings, and click Analyze", style={"fontSize":"14px", "color":"rgba(255,255,255,0.7)", "marginTop":"4px", "marginLeft":"24px"})
                        ], style={"marginBottom":"16px"}),
                        html.Div([
                            html.Strong("4. ", style={"color":"#667eea", "fontSize":"18px"}),
                            html.Strong("Explore Results", style={"color":"rgba(255,255,255,0.95)"}),
                            html.P("View charts, statistics, and insights", style={"fontSize":"14px", "color":"rgba(255,255,255,0.7)", "marginTop":"4px", "marginLeft":"24px"})
                        ]),
                    ]),
                    html.Div([
                        html.A([
                            html.Span("📖 ", style={"marginRight":"6px"}),
                            "View Full Documentation"
                        ], href="/docs", style={
                            "display":"inline-block",
                            "marginTop":"24px",
                            "padding":"12px 24px",
                            "background":"linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%)",
                            "border":"1px solid rgba(102,126,234,0.4)",
                            "color":"#667eea",
                            "textDecoration":"none",
                            "borderRadius":"8px",
                            "fontWeight":"600",
                            "fontSize":"14px",
                            "transition":"all 0.3s"
                        })
                    ], style={"textAlign":"center"})
                ], style={"maxWidth":"600px", "margin":"48px auto 0"})
            ])
        ],
        style={"maxWidth":"1200px","margin":"0 auto","padding":"48px 24px", "marginTop":"0"}
    )

# ---------- Single Index (FULL) ----------
def single_layout():
    return PageContainer([
        # Header
        html.Div([
            html.H1("📊 Single Index Analysis", style={
                "fontSize":"36px", "fontWeight":700, "marginBottom":"12px",
                "color":"rgba(255,255,255,0.95)"
            }),
            html.P([
                "Analyze market movements, find significant drops and gains, and understand trends with technical indicators."
            ], style={
                "fontSize":"17px", "color":"rgba(255,255,255,0.8)", "marginBottom":"8px"
            }),
            html.P([
                "💡 ", html.Strong("Required Data Format:", style={"color":"#00c896"}), 
                " CSV file with 2 columns - a date column and a numeric index value column (column names can be anything). ",
                html.A("See examples in docs →", href="/docs#data-format", style={"color":"#667eea", "textDecoration":"underline"})
            ], style={
                "fontSize":"14px", "color":"rgba(255,255,255,0.6)", "marginBottom":"32px",
                "padding":"12px 16px", "background":"rgba(0,200,150,0.08)", 
                "borderRadius":"8px", "border":"1px solid rgba(0,200,150,0.2)"
            }),
        ], style={"marginBottom": "32px"}),

        # File Upload with Loading
        dcc.Loading(
            id="upload-loading",
            type="circle",
            children=html.Div([
                FileDropzone(
                    id="uploader",
                    label="Upload CSV File"
                ),
                html.Div(id="file-msg", style={"marginBottom": "8px", "fontSize": "14px"}),
                html.Div(id="warn-msg", style={"marginBottom": "8px", "fontSize": "14px"}),
            ])
        ),

        # Analysis Types
        Card([
            html.Div([
                html.H3("🎯 What do you want to analyze?", style={
                    "fontSize":"20px", "fontWeight":600, "color":"rgba(255,255,255,0.95)", "marginBottom":"12px"
                }),
                html.P("Select one or both types of analysis to run on your data:", style={
                    "fontSize":"14px", "color":"rgba(255,255,255,0.7)", "marginBottom":"16px"
                }),
            ]),
            CheckboxGroup(
                id="analysis-types",
                label="Analysis Type(s)",
                options=[
                    {"label": " 📉 Drop Analysis - Find periods where the index decreased", "value": "drop"},
                    {"label": " 📈 Gain Analysis - Find periods where the index increased", "value": "gain"}
                ],
                value=["drop", "gain"],
                inline=False
            ),
            html.P([
                "💡 ", html.Strong("Tip:", style={"color":"#00c896"}),
                " Analyzing both helps you understand the full picture of market volatility and opportunities."
            ], style={
                "fontSize":"13px", "color":"rgba(255,255,255,0.6)", "marginTop":"12px",
                "padding":"8px 12px", "background":"rgba(255,255,255,0.03)",
                "borderRadius":"6px"
            })
        ], style={"marginBottom": "24px"}),

        # Controls row: Drop (left) & Gain (right) - 2 column grid
        html.Div([
            # DROP CONTROLS
            Card([
                html.H3("📉 Drop Analysis Options", style={
                    "marginBottom": "8px", "fontSize":"22px",
                    "fontWeight":600, "color":"#ef4444"
                }),
                html.P("Configure settings to identify when the index decreased significantly", style={
                    "fontSize":"13px", "color":"rgba(255,255,255,0.6)", "marginBottom":"20px"
                }),
                DateRangePicker(
                        id="date-range-drop",
                    label="Date Range",
                    preset_id="preset-drop",
                    preset_value="all",
                    snap_id="snap-month-drop",
                    snap_value=["snap"]
                ),
                html.Div([
                    html.Label("Navigate to Date", style={
                        "display": "block",
                        "fontSize": "14px",
                        "fontWeight": "600",
                        "color": "rgba(255,255,255,0.9)",
                        "marginBottom": "8px"
                    }),
                    html.Div([
                    dcc.Dropdown(id="jump-year-drop", options=[], placeholder="Year",
                                     style={"width":"100px","display":"inline-block","marginRight":"8px"}),
                    dcc.Dropdown(id="jump-month-drop", options=MONTH_OPTIONS, placeholder="Month",
                                 style={"width":"120px","display":"inline-block"}),
                    ], style={"display": "flex", "alignItems": "center"})
                ], style={"marginBottom": "20px"}),
                RadioGroup(
                            id="window-size-drop",
                    label="Analysis Period (days)",
                    options=[{"label": "3", "value": 3}, {"label": "5", "value": 5},
                             {"label": "7", "value": 7}, {"label": "10", "value": 10}],
                    value=5,
                    inline=True,
                    accent_color="rgba(239,68,68,0.8)"
                ),
                Field(
                    label="Custom Period (days)",
                    input_component=dcc.Input(
                            id="window-size-input-drop", type="number", min=1, step=1,
                        placeholder="Enter custom days",
                        style={
                            "width": "100%",
                            "height": "40px",
                            "padding": "8px 12px",
                            "fontSize": "14px",
                            "background": "rgba(255,255,255,0.1)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "borderRadius": "6px",
                            "color": "rgba(255,255,255,0.9)"
                        }
                    ),
                    helper_text="Optional: Enter a custom analysis period in days"
                ),
                RadioGroup(
                            id="min-threshold-drop",
                    label="Minimum Change Threshold (%)",
                    options=[{"label":"1%","value":1},{"label":"3%","value":3},
                             {"label":"5%","value":5},{"label":"10%","value":10}],
                    value=3,
                    inline=True,
                    accent_color="rgba(239,68,68,0.8)"
                ),
                Field(
                    label="Custom Threshold (%)",
                    input_component=dcc.Input(
                            id="min-threshold-input-drop", type="number", min=0, max=100, step=0.01,
                            placeholder="e.g. 2.7", 
                        style={
                            "width": "100%",
                            "height": "40px",
                            "padding": "8px 12px",
                            "fontSize": "14px",
                            "background": "rgba(255,255,255,0.1)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "borderRadius": "6px",
                            "color": "rgba(255,255,255,0.9)"
                        }
                    ),
                    helper_text="Optional: Enter a custom threshold (0-100%)"
                ),
            ], style={
                "background": "rgba(239,68,68,0.08)",
                "border": "1px solid rgba(239,68,68,0.3)"
            }),

            # GAIN CONTROLS
            Card([
                html.H3("📈 Gain Analysis Options", style={
                    "marginBottom": "8px", "fontSize":"22px",
                    "fontWeight":600, "color":"#22c55e"
                }),
                html.P("Configure settings to identify when the index increased significantly", style={
                    "fontSize":"13px", "color":"rgba(255,255,255,0.6)", "marginBottom":"20px"
                }),
                DateRangePicker(
                        id="date-range-gain",
                    label="Date Range",
                    preset_id="preset-gain",
                    preset_value="all",
                    snap_id="snap-month-gain",
                    snap_value=["snap"]
                ),
                html.Div([
                    html.Label("Navigate to Date", style={
                        "display": "block",
                        "fontSize": "14px",
                        "fontWeight": "600",
                        "color": "rgba(255,255,255,0.9)",
                        "marginBottom": "8px"
                    }),
                    html.Div([
                    dcc.Dropdown(id="jump-year-gain", options=[], placeholder="Year",
                                     style={"width":"100px","display":"inline-block","marginRight":"8px"}),
                    dcc.Dropdown(id="jump-month-gain", options=MONTH_OPTIONS, placeholder="Month",
                                 style={"width":"120px","display":"inline-block"}),
                    ], style={"display": "flex", "alignItems": "center"})
                ], style={"marginBottom": "20px"}),
                RadioGroup(
                            id="window-size-gain",
                    label="Analysis Period (days)",
                    options=[{"label": "3", "value": 3}, {"label": "5", "value": 5},
                             {"label": "7", "value": 7}, {"label": "10", "value": 10}],
                    value=5,
                    inline=True,
                    accent_color="rgba(34,197,94,0.8)"
                ),
                Field(
                    label="Custom Period (days)",
                    input_component=dcc.Input(
                            id="window-size-input-gain", type="number", min=1, step=1,
                        placeholder="Enter custom days",
                        style={
                            "width": "100%",
                            "height": "40px",
                            "padding": "8px 12px",
                            "fontSize": "14px",
                            "background": "rgba(255,255,255,0.1)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "borderRadius": "6px",
                            "color": "rgba(255,255,255,0.9)"
                        }
                    ),
                    helper_text="Optional: Enter a custom analysis period in days"
                ),
                RadioGroup(
                            id="min-threshold-gain",
                    label="Minimum Change Threshold (%)",
                    options=[{"label":"1%","value":1},{"label":"3%","value":3},
                             {"label":"5%","value":5},{"label":"10%","value":10}],
                    value=3,
                    inline=True,
                    accent_color="rgba(34,197,94,0.8)"
                ),
                Field(
                    label="Custom Threshold (%)",
                    input_component=dcc.Input(
                            id="min-threshold-input-gain", type="number", min=0, max=100, step=0.01,
                            placeholder="e.g. 2.7", 
                        style={
                            "width": "100%",
                            "height": "40px",
                            "padding": "8px 12px",
                            "fontSize": "14px",
                            "background": "rgba(255,255,255,0.1)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "borderRadius": "6px",
                            "color": "rgba(255,255,255,0.9)"
                        }
                    ),
                    helper_text="Optional: Enter a custom threshold (0-100%)"
                ),
            ], style={
                "background": "rgba(34,197,94,0.08)",
                "border": "1px solid rgba(34,197,94,0.3)"
            }),
        ], style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(400px, 1fr))",
            "gap": "24px",
            "marginBottom": "24px"
        }),

        # INDICATORS - Collapsible card with multi-column layout
        Card([
        html.Div([
            html.H3("Indicators", style={
                "marginBottom":"16px", "fontSize":"22px",
                    "fontWeight":600, "color":"rgba(255,255,255,0.95)",
                    "display": "inline-block",
                    "marginRight": "16px"
                }),
                html.Button(
                    "Select All", id="indicators-select-all", n_clicks=0,
                    style={
                        "padding": "6px 16px",
                        "marginRight": "8px",
                        "borderRadius": "6px",
                        "border": "1px solid rgba(0,200,150,0.3)",
                        "background": "rgba(0,200,150,0.1)",
                        "color": "rgba(255,255,255,0.9)",
                        "cursor": "pointer",
                        "fontSize": "13px",
                        "fontWeight": "500",
                        "transition": "all 0.2s"
                    }
                ),
                html.Button(
                    "Clear All", id="indicators-clear-all", n_clicks=0,
                    style={
                        "padding": "6px 16px",
                        "borderRadius": "6px",
                        "border": "1px solid rgba(255,255,255,0.2)",
                        "background": "rgba(255,255,255,0.1)",
                        "color": "rgba(255,255,255,0.9)",
                        "cursor": "pointer",
                        "fontSize": "13px",
                        "fontWeight": "500",
                        "transition": "all 0.2s"
                    }
                )
            ], style={
                "marginBottom": "16px",
                "display": "flex",
                "alignItems": "center",
                "flexWrap": "wrap",
                "gap": "8px"
            }),
            html.Div([
                CheckboxGroup(
                id="indicators-select",
                    label="",
                options=[
                    {"label":" SMA (5 & 20)", "value":"sma"},
                    {"label":" EMA (12 & 26)", "value":"ema"},
                    {"label":" Bollinger Bands (20,2)", "value":"bb"},
                    {"label":" RSI (14)", "value":"rsi"},
                    {"label":" MACD (12,26,9)", "value":"macd"},
                    {"label":" Volatility (20/60)", "value":"vol"},
                    {"label":" Drawdown", "value":"dd"},
                ],
                value=["sma","ema","bb","rsi","macd","vol","dd"],
                    inline=True
                )
        ], style={
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "8px"
            })
        ], footer=html.Div([
            dcc.Loading(
                id="analyze-loading",
                type="circle",
                children=html.Div([
                    Button(
                        id="analyze",
                        label="Analyze",
                        variant="primary",
                        full_width=False,
                        style={"float": "right"}
                    )
                ], style={
                    "textAlign": "right",
                    "width": "100%"
                }, className="card-footer")
            )
        ], style={
            "textAlign": "right",
            "width": "100%"
        }, className="card-footer"), style={
            "marginBottom": "24px",
            "position": "relative",
            "display": "flex",
            "flexDirection": "column"
        }),

        # ---------- Results (Drop / Gain) ----------
        dcc.Loading(
            id="results-loading",
            type="circle",
            style={
                "position": "fixed",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "zIndex": "9999"
            },
            children=html.Div(id="results-container", style={"display": "none"}, children=[
                html.Div([
                html.H2("Drop Analysis", style={
                    "fontSize":"28px", "fontWeight":700, "color":"#ef4444",
                    "marginBottom":"20px"
                }),
                html.Div(id="analysis-output-drop", style={
                    "border": "1px solid rgba(239,68,68,0.3)", "borderRadius": "16px",
                    "padding": "20px", "margin": "10px 0",
                    "background": "rgba(239,68,68,0.08)",
                    "boxShadow": "0 4px 12px rgba(0,0,0,0.3)"
                }),
                html.Div(id="return-chart-drop-container"),
                html.Div(id="bar-chart-drop-container"),
                html.Div(id="stats-drop", style={"margin": "24px 0"}),
                html.Div(id="trade-windows-drop-container"),
            ], style={"flex": 1, "minWidth": "420px"}),

            html.Div([
                html.H2("Gain Analysis", style={
                    "fontSize":"28px", "fontWeight":700, "color":"#22c55e",
                    "marginBottom":"20px"
                }),
                html.Div(id="analysis-output-gain", style={
                    "border": "1px solid rgba(34,197,94,0.3)", "borderRadius": "16px",
                    "padding": "20px", "margin": "10px 0",
                    "background": "rgba(34,197,94,0.08)",
                    "boxShadow": "0 4px 12px rgba(0,0,0,0.3)"
                }),
                html.Div(id="return-chart-gain-container"),
                html.Div(id="bar-chart-gain-container"),
                html.Div(id="stats-gain", style={"margin": "24px 0"}),
                html.Div(id="trade-windows-gain-container"),
            ], style={"flex": 1, "minWidth": "420px"}),
            ])
        ),

        # ---------- Indicators figure ----------
        html.Div(id="indicators-container"),

        # ---------- Drawdown Recovery Analysis ----------
        Card([
            html.Div([
                html.H3("📉 Drawdown & Recovery Analysis", style={
                    "marginBottom":"12px", "fontSize":"24px",
                    "fontWeight":600, "color":"rgba(255,255,255,0.95)"
                }),
                html.P([
                    "Identify all major drawdown episodes from peak to trough to recovery. ",
                    "Filter by minimum drawdown percentage to focus on significant market corrections."
                ], style={
                    "fontSize":"15px", "color":"rgba(255,255,255,0.7)", "marginBottom":"24px",
                    "lineHeight":"1.6"
                }),
            ]),
            
            # Filter controls
            html.Div([
                html.Div([
                    html.Label("Minimum Drawdown Filter (%)", style={
                        "display":"block", "fontSize":"14px", "fontWeight":"600",
                        "color":"rgba(255,255,255,0.9)", "marginBottom":"8px"
                    }),
                    dcc.RadioItems(
                        id="drawdown-filter",
                        options=[
                            {"label": " Show All", "value": 0},
                            {"label": " ≥5%", "value": 5},
                            {"label": " ≥10%", "value": 10},
                            {"label": " ≥15%", "value": 15},
                            {"label": " ≥20%", "value": 20},
                            {"label": " Custom", "value": -1},
                        ],
                        value=10,
                        inline=True,
                        inputStyle={"marginRight":"6px", "cursor":"pointer"},
                        labelStyle={"marginRight":"16px", "cursor":"pointer", "fontSize":"14px",
                                  "color":"rgba(255,255,255,0.9)"}
                    ),
                    html.Div([
                        dcc.Input(
                            id="drawdown-custom-input",
                            type="number",
                            placeholder="Enter custom %",
                            min=0,
                            max=100,
                            step=0.1,
                            style={
                                "padding":"8px 12px", "borderRadius":"6px",
                                "border":"1px solid rgba(255,255,255,0.3)",
                                "background":"rgba(255,255,255,0.05)", "color":"white",
                                "fontSize":"13px", "width":"150px",
                                "marginTop":"8px"
                            },
                            disabled=True
                        ),
                        html.Span("% (e.g., 7.5, 12.3)", style={
                            "fontSize":"12px", "color":"rgba(255,255,255,0.5)",
                            "marginLeft":"8px"
                        })
                    ], id="custom-input-container", style={"marginTop":"8px"}),
                    html.P("Only show drawdowns equal to or greater than this percentage", style={
                        "fontSize":"12px", "color":"rgba(255,255,255,0.6)", "marginTop":"8px"
                    })
                ], style={"flex": "1", "minWidth": "300px"}),
                
                html.Div([
                    html.Button([
                        html.Span("📊 ", style={"marginRight":"6px"}),
                        "Analyze Drawdowns"
                    ], id="drawdown-analyze-btn", n_clicks=0, style={
                        "padding":"12px 28px", "borderRadius":"8px", "border":"none",
                        "background":"linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                        "color":"white", "cursor":"pointer", "fontSize":"15px",
                        "fontWeight":"600", "boxShadow":"0 4px 12px rgba(239,68,68,0.4)",
                        "transition":"all 0.3s", "marginBottom":"8px"
                    }),
                    html.Div([
                        html.Button([
                            html.Span("📥 ", style={"marginRight":"6px"}),
                            "Download CSV"
                        ], id="drawdown-download-btn", style={
                            "padding":"10px 20px", "borderRadius":"6px",
                            "border":"1px solid rgba(255,255,255,0.2)",
                            "background":"rgba(255,255,255,0.1)", "color":"rgba(255,255,255,0.9)",
                            "cursor":"pointer", "fontSize":"13px", "fontWeight":"500",
                            "transition":"all 0.3s", "marginRight":"8px"
                        }),
                        dcc.Download(id="drawdown-download")
                    ])
                ], style={"display":"flex", "flexDirection":"column", "alignItems":"flex-end",
                        "justifyContent":"center"})
            ], style={
                "display":"flex", "alignItems":"center", "justifyContent":"space-between",
                "flexWrap":"wrap", "gap":"20px", "marginBottom":"24px"
            }),
            
            # Results container with loading spinner
            dcc.Loading(
                id="drawdown-loading",
                type="circle",
                color="#ef4444",
                fullscreen=False,
                style={
                    "position": "fixed",
                    "top": "50%",
                    "left": "50%",
                    "transform": "translate(-50%, -50%)",
                    "zIndex": "9999"
                },
                children=html.Div(id="drawdown-results-container", style={"marginTop":"24px"}),
                parent_style={"position": "relative", "minHeight": "200px"}
            ),
        ], style={"marginBottom":"32px", "marginTop":"32px"}),

        html.Hr(),
        html.Div(id="preview", style={
            "marginTop":"40px", "padding":"24px",
            "background":"rgba(255,255,255,0.05)", "borderRadius":"16px",
            "boxShadow":"0 4px 12px rgba(0,0,0,0.3)",
            "border":"1px solid rgba(255,255,255,0.1)"
        }),  # <<< Data Preview lives here (first 10 rows)

        dcc.Store(id=STORE_RAW),
        dcc.Store(id=STORE_META),
    ])

# ---------- Cross Index ----------
def cross_layout():
    return PageContainer([
        # Header
            html.Div([
                html.H1("🔀 Cross Index Analysis", style={
                    "fontSize":"36px", "fontWeight":700, "marginBottom":"12px",
                "color":"rgba(255,255,255,0.95)"
                }),
                html.P([
                    "Compare two different indexes to understand their relationship, correlation, and relative performance over time."
                ], style={
                    "fontSize":"17px", "color":"rgba(255,255,255,0.8)", "marginBottom":"8px"
                }),
                html.P([
                    "💡 ", html.Strong("How it works:", style={"color":"#00c896"}), 
                    " Upload two CSV files (same format as Single Index), set a date range, and see how they move together. ",
                    html.A("Learn more in docs →", href="/docs#cross-index", style={"color":"#f5576c", "textDecoration":"underline"})
                ], style={
                    "fontSize":"14px", "color":"rgba(255,255,255,0.6)", "marginBottom":"32px",
                    "padding":"12px 16px", "background":"rgba(245,87,108,0.08)", 
                    "borderRadius":"8px", "border":"1px solid rgba(245,87,108,0.2)"
                }),
        ], style={"marginBottom": "32px"}),

        # Upload Index A/B - 2 column grid
            html.Div([
            Card([
                dcc.Loading(
                    id="upload-loading-a",
                    type="circle",
                        children=html.Div([
                        FileDropzone(
                            id="uploader-a",
                            label="Upload Index A (CSV)"
                        ),
                        html.Div(id="file-msg-a", style={"marginBottom": "8px", "fontSize": "14px"}),
                        html.Div(id="warn-msg-a", style={"marginBottom": "8px", "fontSize": "14px"}),
                        html.Div(id="preview-a")
                    ])
                )
            ], style={"minHeight": "200px"}),

            Card([
                dcc.Loading(
                    id="upload-loading-b",
                    type="circle",
                        children=html.Div([
                        FileDropzone(
                            id="uploader-b",
                            label="Upload Index B (CSV)"
                        ),
                        html.Div(id="file-msg-b", style={"marginBottom": "8px", "fontSize": "14px"}),
                        html.Div(id="warn-msg-b", style={"marginBottom": "8px", "fontSize": "14px"}),
                        html.Div(id="preview-b")
                    ])
                )
            ], style={"minHeight": "200px"}),
                ], style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(400px, 1fr))",
            "gap": "24px",
            "marginBottom": "32px"
        }),

        # Analysis Settings Card
        Card([
                html.H3("⚙️ Analysis Settings", style={
                    "fontSize":"24px", "fontWeight":600, "color":"rgba(255,255,255,0.95)",
                    "marginBottom":"8px"
                }),
                html.P("Configure the time range and calculation period for comparing both indexes", style={
                    "fontSize":"14px", "color":"rgba(255,255,255,0.7)", "marginBottom":"20px"
                }),
            # Row 1: Date Range + Snap to month
                html.Div([
                html.Div([
                    DateRangePicker(
                        id="date-range-cross",
                        label="Date Range",
                        preset_id="preset-cross",
                        preset_value="all",
                        snap_id="snap-month-cross",
                        snap_value=["snap"]
                    )
                ], style={"flex": 1, "minWidth": "300px"})
            ], style={
                "display": "flex",
                "alignItems": "flex-end",
                "gap": "16px",
                "marginBottom": "20px"
            }),
            # Row 2: Navigate to Date
                html.Div([
                html.Label("Navigate to Date", style={
                    "display": "block",
                    "fontSize": "14px",
                    "fontWeight": "600",
                    "color": "rgba(255,255,255,0.9)",
                    "marginBottom": "8px"
                }),
                html.Div([
                    dcc.Dropdown(id="jump-year-cross", options=[], placeholder="Year",
                                 style={"width":"100px","display":"inline-block","marginRight":"8px"}),
                    dcc.Dropdown(id="jump-month-cross", options=MONTH_OPTIONS, placeholder="Month",
                                 style={"width":"120px","display":"inline-block"}),
                ], style={"display": "flex", "alignItems": "center"})
            ], style={"marginBottom": "20px"}),
            # Row 3: Return Calculation Period
            Field(
                label="Return Calculation Period (days)",
                input_component=dcc.Input(
                    id="x-window",
                    type="number",
                    min=1,
                    step=1,
                    value=5,
                    placeholder="e.g., 5",
                        style={
                        "width": "100%",
                        "height": "40px",
                        "padding": "8px 12px",
                        "fontSize": "14px",
                        "background": "rgba(255,255,255,0.1)",
                        "border": "1px solid rgba(255,255,255,0.2)",
                        "borderRadius": "6px",
                        "color": "rgba(255,255,255,0.9)"
                    }
                ),
                helper_text="How many days to use when calculating returns (e.g., 5 days = weekly returns). This measures price change over X-day periods for both indexes."
            ),
        ], footer=html.Div([
            dcc.Loading(
                id="x-analyze-loading",
                type="circle",
                children=html.Div([
                    Button(
                        id="x-analyze",
                        label="Analyze",
                        variant="primary",
                        full_width=False,
                        style={"float": "right"}
                    )
                ], style={
                    "textAlign": "right",
                    "width": "100%"
                }, className="card-footer")
            )
        ], style={
            "textAlign": "right",
            "width": "100%"
        }, className="card-footer"), style={"marginBottom": "32px"}),

        # Results
        dcc.Loading(
            id="x-results-loading",
            type="circle",
            style={
                "position": "fixed",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "zIndex": "9999"
            },
            children=html.Div(id="x-results-container", children=[
                html.Div(id="x-line-levels-container"),
                html.Div(id="x-scatter-returns-container"),
                html.Div(id="x-line-returns-container"),
                html.Div(id="x-stats", style={"margin":"24px 0"}),
                html.Div(id="x-trade-windows-container"),
            ], style={"marginTop":"32px"})
        ),

            dcc.Store(id=STORE_A),
            dcc.Store(id=STORE_B),
    ])

# ---------- Documentation Page ----------
def docs_layout():
    return PageContainer([
        # Header
        html.Div([
            html.H1("📖 Documentation", style={
                "fontSize":"42px", "fontWeight":700, "marginBottom":"16px",
                "background":"linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "WebkitBackgroundClip":"text", "WebkitTextFillColor":"transparent",
                "backgroundClip":"text"
            }),
            html.P("Complete guide to using the Index Data Analysis application", style={
                "fontSize":"18px", "color":"rgba(255,255,255,0.7)", "marginBottom":"48px"
            }),
        ], style={"textAlign":"center"}),

        # Table of Contents
        Card([
            html.H2("📑 Table of Contents", style={"marginBottom":"20px", "fontSize":"26px", "fontWeight":600, "color":"rgba(255,255,255,0.95)"}),
            html.Ul([
                html.Li(html.A("1. What is this app?", href="#what-is", style={"color":"#667eea", "textDecoration":"none"})),
                html.Li(html.A("2. Data Format Requirements", href="#data-format", style={"color":"#667eea", "textDecoration":"none"})),
                html.Li(html.A("3. Single Index Analysis", href="#single-index", style={"color":"#667eea", "textDecoration":"none"})),
                html.Li(html.A("4. Cross Index Analysis", href="#cross-index", style={"color":"#667eea", "textDecoration":"none"})),
                html.Li(html.A("5. Understanding Key Concepts", href="#concepts", style={"color":"#667eea", "textDecoration":"none"})),
                html.Li(html.A("6. Drawdown & Recovery Analysis", href="#drawdown", style={"color":"#667eea", "textDecoration":"none"})),
                html.Li(html.A("7. Technical Indicators Explained", href="#indicators", style={"color":"#667eea", "textDecoration":"none"})),
                html.Li(html.A("8. Examples & Use Cases", href="#examples", style={"color":"#667eea", "textDecoration":"none"})),
            ], style={"fontSize":"16px", "lineHeight":"2", "color":"rgba(255,255,255,0.9)"})
        ], style={"marginBottom":"32px"}),

        # Section 1: What is this app?
        html.Div(id="what-is"),
        Card([
            html.H2("1️⃣ What is this app?", style={"marginBottom":"20px", "fontSize":"28px", "fontWeight":600, "color":"#667eea"}),
            html.P([
                "The Index Data Analysis app is a powerful tool designed to analyze financial index data. ",
                "It helps you understand market movements by analyzing price changes over time and identifying ",
                "significant events like drops and gains."
            ], style={"fontSize":"16px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginBottom":"16px"}),
            html.P([
                html.Strong("Two Main Features:", style={"color":"#667eea"}),
            ], style={"fontSize":"16px", "marginBottom":"12px"}),
            html.Ul([
                html.Li([html.Strong("Single Index Analysis:"), " Analyze one market index in depth, finding drop and gain events with detailed statistics and visualizations."]),
                html.Li([html.Strong("Cross Index Analysis:"), " Compare two different indexes to see how they move together, their correlation, and relative performance."]),
            ], style={"fontSize":"15px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginLeft":"20px"})
        ], style={"marginBottom":"32px"}),

        # Section 2: Data Format
        html.Div(id="data-format"),
        Card([
            html.H2("2️⃣ Data Format Requirements", style={"marginBottom":"20px", "fontSize":"28px", "fontWeight":600, "color":"#667eea"}),
            html.P([
                "Your CSV file must contain ", html.Strong("exactly two columns", style={"color":"#00c896"}), ":"
            ], style={"fontSize":"16px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginBottom":"16px"}),
            html.Ul([
                html.Li([html.Strong("Column 1:"), " A date or datetime column (any reasonable date format works)"]),
                html.Li([html.Strong("Column 2:"), " A numeric column representing the index value (price, level, etc.)"]),
            ], style={"fontSize":"15px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginLeft":"20px", "marginBottom":"20px"}),
            
            html.H3("✅ Example of Valid Data:", style={"fontSize":"20px", "fontWeight":600, "color":"#22c55e", "marginBottom":"12px"}),
            html.Pre([
                "Date,Index\n",
                "2024-01-01,1000.5\n",
                "2024-01-02,1005.2\n",
                "2024-01-03,998.7\n",
                "2024-01-04,1012.3"
            ], style={
                "background":"rgba(34,197,94,0.1)", "padding":"16px", "borderRadius":"8px",
                "border":"1px solid rgba(34,197,94,0.3)", "fontSize":"14px",
                "color":"rgba(255,255,255,0.95)", "overflowX":"auto"
            }),
            
            html.Div([
                html.Strong("💡 Important Notes:", style={"color":"#00c896", "display":"block", "marginBottom":"8px"}),
                html.Ul([
                    html.Li("Column headers can have any name - the app automatically detects which is the date and which is numeric"),
                    html.Li("The app handles common date formats automatically (YYYY-MM-DD, MM/DD/YYYY, etc.)"),
                    html.Li("Rows with missing or invalid data will be automatically removed"),
                    html.Li("Data will be automatically sorted by date"),
                ], style={"fontSize":"14px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.8)", "marginLeft":"20px"})
            ], style={"marginTop":"20px", "padding":"16px", "background":"rgba(0,200,150,0.08)", "borderRadius":"8px", "border":"1px solid rgba(0,200,150,0.3)"})
        ], style={"marginBottom":"32px"}),

        # Section 3: Single Index Analysis
        html.Div(id="single-index"),
        Card([
            html.H2("3️⃣ Single Index Analysis", style={"marginBottom":"20px", "fontSize":"28px", "fontWeight":600, "color":"#667eea"}),
            html.P("This mode analyzes a single market index to identify significant price movements.", style={
                "fontSize":"16px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginBottom":"24px"
            }),
            
            html.H3("📤 Step 1: Upload Your Data", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
            html.P("Click or drag & drop your CSV file into the upload area. You'll see a preview of your data once it's loaded.", style={
                "fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"20px"
            }),
            
            html.H3("🎯 Step 2: Choose Analysis Type", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
            html.Ul([
                html.Li([html.Strong("Drop Analysis (Red):", style={"color":"#ef4444"}), " Identifies periods where the index fell by a specified percentage"]),
                html.Li([html.Strong("Gain Analysis (Green):", style={"color":"#22c55e"}), " Identifies periods where the index rose by a specified percentage"]),
                html.Li("You can analyze both simultaneously!")
            ], style={"fontSize":"15px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginLeft":"20px", "marginBottom":"20px"}),
            
            html.H3("⚙️ Step 3: Configure Parameters", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
            html.Div([
                html.Strong("📅 Date Range:", style={"display":"block", "marginBottom":"8px", "color":"#667eea"}),
                html.P("Select the time period to analyze. Options include All time, Year-to-Date (YTD), Last 1 Year, Last 3 Years, Last 6 Months, or Custom range.", style={
                    "fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"16px"
                }),
                
                html.Strong("📍 Navigate to Date:", style={"display":"block", "marginBottom":"8px", "color":"#667eea"}),
                html.P("Jump directly to a specific year/month in your data for quick analysis of a particular time period.", style={
                    "fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"16px"
                }),
                
                html.Strong("📊 Analysis Period (days):", style={"display":"block", "marginBottom":"8px", "color":"#667eea"}),
                html.P([
                    "The time window to measure price changes. For example, a 5-day period means 'from day X to day X+5'. ",
                    "Common choices: 3 days (short-term), 5 days (weekly), 7 days (weekly), 10 days (two weeks). ",
                    "You can also enter a custom period."
                ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"16px"}),
                
                html.Strong("📉 Minimum Change Threshold:", style={"display":"block", "marginBottom":"8px", "color":"#667eea"}),
                html.P([
                    "The minimum percentage change to count as a significant event. ",
                    "For example, 3% means only drops/gains of 3% or more are counted. ",
                    "Lower thresholds = more events found, Higher thresholds = only major events."
                ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"16px"}),
                
                html.Strong("📅 Snap to Month:", style={"display":"block", "marginBottom":"8px", "color":"#667eea"}),
                html.P("When enabled, the analysis period starts at the beginning of the month and ends at month-end. Useful for clean monthly reporting.", style={
                    "fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"16px"
                }),
            ], style={"marginLeft":"20px", "marginBottom":"20px"}),
            
            html.H3("📊 Step 4: View Results", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
            html.P("After clicking 'Analyze', you'll see:", style={"fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"12px"}),
            html.Ul([
                html.Li([html.Strong("Event Statistics:"), " Total number of drop/gain events found and their probability"]),
                html.Li([html.Strong("Return Distribution Chart:"), " Visual distribution of all returns during the analysis period"]),
                html.Li([html.Strong("Bar Chart:"), " Count of events that crossed your threshold"]),
                html.Li([html.Strong("Statistical Summary:"), " Mean, median, standard deviation, and other key metrics"]),
                html.Li([html.Strong("Trade Windows Table:"), " Detailed table showing start/end dates for each analysis window"]),
                html.Li([html.Strong("Technical Indicators:"), " RSI, MACD, Bollinger Bands, and more (see section 6)"]),
            ], style={"fontSize":"15px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginLeft":"20px"}),
        ], style={"marginBottom":"32px"}),

        # Section 4: Cross Index Analysis
        html.Div(id="cross-index"),
        Card([
            html.H2("4️⃣ Cross Index Analysis", style={"marginBottom":"20px", "fontSize":"28px", "fontWeight":600, "color":"#f5576c"}),
            html.P("This mode compares two different indexes to understand their relationship and relative performance.", style={
                "fontSize":"16px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginBottom":"24px"
            }),
            
            html.H3("📤 Step 1: Upload Both Indexes", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
            html.P("Upload two separate CSV files - one for Index A and one for Index B. Both must follow the same data format (see Section 2).", style={
                "fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"20px"
            }),
            
            html.H3("⚙️ Step 2: Configure Analysis Settings", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
            html.Ul([
                html.Li([html.Strong("Date Range:"), " The time period to compare. The app will only analyze dates where both indexes have data."]),
                html.Li([html.Strong("Return Calculation Period:"), " Number of days to use when calculating returns for both indexes (typically 5 days)."]),
            ], style={"fontSize":"15px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginLeft":"20px", "marginBottom":"20px"}),
            
            html.H3("📊 Step 3: Understanding the Results", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
            html.Div([
                html.Strong("📈 Price Levels Over Time:", style={"display":"block", "marginBottom":"8px", "color":"#667eea"}),
                html.P("Shows both indexes plotted together so you can see their overall trends and movements.", style={
                    "fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"16px"
                }),
                
                html.Strong("🎯 Scatter Plot:", style={"display":"block", "marginBottom":"8px", "color":"#667eea"}),
                html.P("Each point represents the returns of both indexes on the same day. If points cluster along a line, the indexes move together (correlated). Scattered points mean independent movement.", style={
                    "fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"16px"
                }),
                
                html.Strong("📊 Returns Over Time:", style={"display":"block", "marginBottom":"8px", "color":"#667eea"}),
                html.P("Compares the percentage returns of both indexes over time, making it easy to see which performed better during specific periods.", style={
                    "fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"16px"
                }),
                
                html.Strong("📐 Correlation Coefficient:", style={"display":"block", "marginBottom":"8px", "color":"#667eea"}),
                html.Ul([
                    html.Li([html.Strong("+1.0:"), " Perfect positive correlation (always move together)"]),
                    html.Li([html.Strong("0.0:"), " No correlation (independent movement)"]),
                    html.Li([html.Strong("-1.0:"), " Perfect negative correlation (always move opposite)"]),
                    html.Li([html.Strong("0.7 to 1.0:"), " Strong positive correlation"]),
                    html.Li([html.Strong("0.3 to 0.7:"), " Moderate positive correlation"]),
                ], style={"fontSize":"14px", "lineHeight":"1.6", "color":"rgba(255,255,255,0.85)", "marginLeft":"20px"}),
            ], style={"marginLeft":"20px"}),
        ], style={"marginBottom":"32px"}),

        # Section 5: Key Concepts
        html.Div(id="concepts"),
        Card([
            html.H2("5️⃣ Understanding Key Concepts", style={"marginBottom":"20px", "fontSize":"28px", "fontWeight":600, "color":"#667eea"}),
            
            html.Div([
                html.H3("📊 Returns", style={"fontSize":"20px", "fontWeight":600, "color":"#00c896", "marginBottom":"8px"}),
                html.P([
                    "A return is the percentage change in index value over a period. ",
                    html.Strong("Formula:"), " ((End Value - Start Value) / Start Value) × 100"
                ], style={"fontSize":"15px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginBottom":"16px"}),
                html.P([
                    html.Strong("Example:"), " If an index goes from 1000 to 1050 over 5 days, the 5-day return is ((1050-1000)/1000) × 100 = 5%"
                ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.8)", "marginBottom":"24px", "fontStyle":"italic"}),
            ]),
            
            html.Div([
                html.H3("📅 Weekend-Aware Calculations", style={"fontSize":"20px", "fontWeight":600, "color":"#00c896", "marginBottom":"8px"}),
                html.P([
                    "Financial markets are closed on weekends. This app intelligently handles weekends by: ",
                    html.Ul([
                        html.Li("If an analysis period ends on Saturday, it uses Friday's data"),
                        html.Li("If it ends on Sunday, it uses Monday's data"),
                        html.Li("This ensures accurate calendar-based analysis without gaps")
                    ], style={"marginTop":"8px", "lineHeight":"1.6"})
                ], style={"fontSize":"15px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginBottom":"24px"}),
            ]),
            
            html.Div([
                html.H3("📈 Probability", style={"fontSize":"20px", "fontWeight":600, "color":"#00c896", "marginBottom":"8px"}),
                html.P([
                    "The probability shown is: (Number of Events / Total Analysis Windows) × 100"
                ], style={"fontSize":"15px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginBottom":"12px"}),
                html.P([
                    html.Strong("Example:"), " If you find 45 drop events out of 500 analysis windows, the probability is 45/500 = 9%"
                ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.8)", "fontStyle":"italic"}),
            ]),
        ], style={"marginBottom":"32px"}),

        # Section 6: Drawdown & Recovery Analysis
        html.Div(id="drawdown"),
        Card([
            html.H2("6️⃣ Drawdown & Recovery Analysis", style={"marginBottom":"20px", "fontSize":"28px", "fontWeight":600, "color":"#ef4444"}),
            html.P("A powerful tool to identify and analyze market corrections and their recovery patterns.", style={
                "fontSize":"16px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginBottom":"24px"
            }),
            
            html.Div([
                html.H3("📉 What is a Drawdown?", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
                html.P([
                    "A ", html.Strong("drawdown"), " is a decline from a historical peak to a subsequent trough in an investment. ",
                    "It measures how much value was lost from the highest point before recovery."
                ], style={"fontSize":"15px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginBottom":"16px"}),
                
                html.Div([
                    html.Strong("📊 Key Components:", style={"display":"block", "marginBottom":"12px", "fontSize":"16px"}),
                    html.Ul([
                        html.Li([html.Strong("Peak:"), " The highest price point before a decline begins"]),
                        html.Li([html.Strong("Trough:"), " The lowest price point during the decline"]),
                        html.Li([html.Strong("Recovery:"), " When the price returns to the previous peak level"]),
                        html.Li([html.Strong("Drawdown %:"), " (Trough - Peak) / Peak × 100 (negative number)"]),
                    ], style={"lineHeight":"1.8", "marginLeft":"20px"})
                ], style={"marginBottom":"20px"}),
                
                html.Div([
                    html.Strong("💡 Example:", style={"display":"block", "marginBottom":"8px", "color":"#00c896"}),
                    html.P([
                        "• Peak: $1000 on Jan 1st\n",
                        html.Br(),
                        "• Trough: $800 on Feb 15th\n",
                        html.Br(),
                        "• Recovery: $1000 on April 10th\n",
                        html.Br(),
                        "• Drawdown: -20% (lost 20% of value)\n",
                        html.Br(),
                        "• Days to Trough: 45 days\n",
                        html.Br(),
                        "• Days to Recovery: 99 days (full recovery took ~3 months)"
                    ], style={"fontSize":"14px", "lineHeight":"2", "fontFamily":"monospace",
                             "padding":"16px", "background":"rgba(239,68,68,0.1)", 
                             "borderRadius":"8px", "border":"1px solid rgba(239,68,68,0.3)"})
                ], style={"marginBottom":"24px"}),
            ]),
            
            html.Div([
                html.H3("🎯 How to Use This Feature", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
                html.Ol([
                    html.Li([html.Strong("Upload your data"), " to Single Index Analysis page"]),
                    html.Li([html.Strong("Scroll to Drawdown & Recovery Analysis"), " section"]),
                    html.Li([html.Strong("Set filter:"), " Choose minimum drawdown threshold (5%, 10%, 15%, 20%)"]),
                    html.Li([html.Strong("Click 'Analyze Drawdowns':"), " View all episodes and statistics"]),
                    html.Li([html.Strong("Download results:"), " Export as CSV for further analysis"]),
                ], style={"lineHeight":"2", "marginLeft":"20px", "marginBottom":"20px"}),
            ]),
            
            html.Div([
                html.H3("📊 Understanding the Results", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
                
                html.Div([
                    html.Strong("Summary Statistics:", style={"display":"block", "marginBottom":"8px", "fontSize":"16px", "color":"#ef4444"}),
                    html.Ul([
                        html.Li([html.Strong("Total Episodes:"), " How many drawdown events occurred"]),
                        html.Li([html.Strong("Avg Drawdown:"), " Mean decline percentage across all episodes"]),
                        html.Li([html.Strong("Max Drawdown:"), " Worst decline in your data (most severe)"]),
                        html.Li([html.Strong("Avg Recovery Days:"), " Average time to recover to previous peak"]),
                    ], style={"lineHeight":"1.8", "marginLeft":"20px", "marginBottom":"20px"})
                ]),
                
                html.Div([
                    html.Strong("Episode Table Columns:", style={"display":"block", "marginBottom":"8px", "fontSize":"16px", "color":"#3b82f6"}),
                    html.Ul([
                        html.Li([html.Strong("Peak Date & Value:"), " When and where the decline started"]),
                        html.Li([html.Strong("Trough Date & Value:"), " When and where it hit bottom"]),
                        html.Li([html.Strong("Recovery Date & Value:"), " When price returned to peak (N/A if still in drawdown)"]),
                        html.Li([html.Strong("Drawdown %:"), " Severity of the decline (color-coded in red)"]),
                        html.Li([html.Strong("Days to Trough:"), " How long the decline lasted"]),
                        html.Li([html.Strong("Days to Recovery:"), " Total recovery time (color-coded in blue)"]),
                    ], style={"lineHeight":"1.8", "marginLeft":"20px"})
                ]),
            ]),
            
            html.Div([
                html.H3("🔍 Filtering Drawdowns", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
                html.P("Use filters to focus on drawdowns that matter to you:", style={
                    "fontSize":"15px", "marginBottom":"12px", "color":"rgba(255,255,255,0.9)"
                }),
                html.Ul([
                    html.Li([html.Strong("Show All:"), " Every single drawdown episode (noisy, includes minor dips)"]),
                    html.Li([html.Strong("≥5%:"), " Small corrections - normal market volatility"]),
                    html.Li([html.Strong("≥10%:"), " Significant corrections - worth monitoring (default)"]),
                    html.Li([html.Strong("≥15%:"), " Major corrections - serious market stress"]),
                    html.Li([html.Strong("≥20%:"), " Bear market territory - severe crashes only"]),
                ], style={"lineHeight":"1.8", "marginLeft":"20px", "marginBottom":"20px"}),
                
                html.Div([
                    html.Strong("💡 Pro Tip:", style={"color":"#00c896", "marginRight":"8px"}),
                    html.Span("Start with ≥10% to see significant events, then adjust based on your risk tolerance and analysis needs.")
                ], style={
                    "padding":"12px 16px", "background":"rgba(0,200,150,0.08)", 
                    "borderRadius":"8px", "border":"1px solid rgba(0,200,150,0.3)",
                    "fontSize":"14px"
                }),
            ]),
            
            html.Div([
                html.H3("💼 Real-World Applications", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px", "marginTop":"24px"}),
                
                html.Div([
                    html.Strong("📉 Risk Assessment:", style={"display":"block", "marginBottom":"8px", "color":"#ef4444"}),
                    html.P("Understand how often severe declines happen and how long they typically last. Use historical patterns to set realistic expectations.", 
                          style={"fontSize":"14px", "lineHeight":"1.8", "marginBottom":"16px", "opacity":"0.9"}),
                ]),
                
                html.Div([
                    html.Strong("⏱️ Recovery Planning:", style={"display":"block", "marginBottom":"8px", "color":"#3b82f6"}),
                    html.P("Know typical recovery timeframes. If average recovery is 90 days, don't panic after 30 days in a drawdown.", 
                          style={"fontSize":"14px", "lineHeight":"1.8", "marginBottom":"16px", "opacity":"0.9"}),
                ]),
                
                html.Div([
                    html.Strong("📊 Comparing Periods:", style={"display":"block", "marginBottom":"8px", "color":"#f97316"}),
                    html.P("Identify if recent drawdowns are normal or unprecedented. Compare 2020's COVID crash to historical market behavior.", 
                          style={"fontSize":"14px", "lineHeight":"1.8", "marginBottom":"16px", "opacity":"0.9"}),
                ]),
                
                html.Div([
                    html.Strong("🎯 Investment Decisions:", style={"display":"block", "marginBottom":"8px", "color":"#22c55e"}),
                    html.P("Make informed choices about when to hold, buy more, or exit. Historical data removes emotion from decisions.", 
                          style={"fontSize":"14px", "lineHeight":"1.8", "opacity":"0.9"}),
                ]),
            ]),
            
            html.Div([
                html.H3("⚠️ Important Notes", style={"fontSize":"22px", "fontWeight":600, "color":"#f97316", "marginBottom":"12px", "marginTop":"24px"}),
                html.Ul([
                    html.Li("Historical drawdowns don't predict future events, but show possible scenarios"),
                    html.Li("Open drawdowns (no recovery yet) show N/A for recovery date and days"),
                    html.Li("Recovery time can vary greatly based on market conditions"),
                    html.Li("Filters are inclusive: ≥10% includes 10%, 15%, 20%, etc."),
                    html.Li("The app automatically detects your date and value columns"),
                ], style={"lineHeight":"1.8", "marginLeft":"20px", "fontSize":"14px", "opacity":"0.85"})
            ], style={
                "padding":"20px", "background":"rgba(249,115,22,0.08)", 
                "borderRadius":"12px", "border":"1px solid rgba(249,115,22,0.3)",
                "marginTop":"24px"
            }),
        ], style={"marginBottom":"32px"}),

        # Section 7: Technical Indicators
        html.Div(id="indicators"),
        Card([
            html.H2("7️⃣ Technical Indicators Explained", style={"marginBottom":"20px", "fontSize":"28px", "fontWeight":600, "color":"#667eea"}),
            html.P("When you analyze a single index, the app calculates various technical indicators used by traders and analysts:", style={
                "fontSize":"16px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginBottom":"24px"
            }),
            
            html.Div([
                html.H3("📊 Moving Averages (SMA, EMA)", style={"fontSize":"20px", "fontWeight":600, "color":"#00c896", "marginBottom":"8px"}),
                html.P([
                    html.Strong("What it is:"), " Average of prices over a period. SMA = simple average, EMA = gives more weight to recent prices."
                ], style={"fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"8px"}),
                html.P([
                    html.Strong("How to use it:"), " When price crosses above MA = potential uptrend. When price crosses below MA = potential downtrend."
                ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"20px"}),
            ]),
            
            html.Div([
                html.H3("📉 MACD (Moving Average Convergence Divergence)", style={"fontSize":"20px", "fontWeight":600, "color":"#00c896", "marginBottom":"8px"}),
                html.P([
                    html.Strong("What it is:"), " Shows the relationship between two moving averages (12-day EMA - 26-day EMA)."
                ], style={"fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"8px"}),
                html.P([
                    html.Strong("How to use it:"), " When MACD crosses above signal line = bullish signal. When MACD crosses below signal line = bearish signal."
                ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"20px"}),
            ]),
            
            html.Div([
                html.H3("💪 RSI (Relative Strength Index)", style={"fontSize":"20px", "fontWeight":600, "color":"#00c896", "marginBottom":"8px"}),
                html.P([
                    html.Strong("What it is:"), " Measures momentum on a scale of 0-100."
                ], style={"fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"8px"}),
                html.P([
                    html.Strong("How to use it:"),
                    html.Ul([
                        html.Li("RSI > 70: Potentially overbought (may drop soon)"),
                        html.Li("RSI < 30: Potentially oversold (may rise soon)"),
                        html.Li("RSI around 50: Neutral momentum")
                    ], style={"marginTop":"8px", "lineHeight":"1.6"})
                ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"20px"}),
            ]),
            
            html.Div([
                html.H3("📊 Bollinger Bands", style={"fontSize":"20px", "fontWeight":600, "color":"#00c896", "marginBottom":"8px"}),
                html.P([
                    html.Strong("What it is:"), " Shows a middle line (20-day average) with upper and lower bands (±2 standard deviations)."
                ], style={"fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"8px"}),
                html.P([
                    html.Strong("How to use it:"), " Price near upper band = potentially overbought. Price near lower band = potentially oversold. Narrowing bands = low volatility (potential breakout coming)."
                ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"20px"}),
            ]),
            
            html.Div([
                html.H3("📉 Volatility", style={"fontSize":"20px", "fontWeight":600, "color":"#00c896", "marginBottom":"8px"}),
                html.P([
                    html.Strong("What it is:"), " Measures how much prices fluctuate (standard deviation of returns)."
                ], style={"fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"8px"}),
                html.P([
                    html.Strong("How to use it:"), " High volatility = larger price swings (higher risk/opportunity). Low volatility = stable prices (lower risk/opportunity)."
                ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginBottom":"20px"}),
            ]),
            
            html.Div([
                html.H3("📉 Drawdown", style={"fontSize":"20px", "fontWeight":600, "color":"#00c896", "marginBottom":"8px"}),
                html.P([
                    html.Strong("What it is:"), " How far the price has fallen from its recent peak."
                ], style={"fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"8px"}),
                html.P([
                    html.Strong("How to use it:"), " Large drawdowns indicate significant losses from recent highs. Recovery from drawdown shows resilience."
                ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.85)"}),
            ]),
        ], style={"marginBottom":"32px"}),

        # Section 8: Examples
        html.Div(id="examples"),
        Card([
            html.H2("8️⃣ Examples & Use Cases", style={"marginBottom":"20px", "fontSize":"28px", "fontWeight":600, "color":"#667eea"}),
            
            html.Div([
                html.H3("💼 Use Case 1: Risk Assessment", style={"fontSize":"22px", "fontWeight":600, "color":"#f5576c", "marginBottom":"12px"}),
                html.P([
                    html.Strong("Scenario:"), " You want to understand how often the S&P 500 drops by 5% or more in a week."
                ], style={"fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"12px"}),
                html.Div([
                    html.Strong("Steps:", style={"display":"block", "marginBottom":"8px"}),
                    html.Ol([
                        html.Li("Upload your S&P 500 CSV data"),
                        html.Li("Select 'Drop' analysis"),
                        html.Li("Set Analysis Period to 7 days"),
                        html.Li("Set Minimum Threshold to 5%"),
                        html.Li("Click Analyze"),
                    ], style={"lineHeight":"1.8", "marginLeft":"20px"}),
                    html.P([
                        html.Strong("Result:"), " You'll see the probability (e.g., '8%') meaning that 7-day drops of 5%+ occur in 8% of all 7-day periods."
                    ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginTop":"12px"})
                ], style={"marginLeft":"20px", "marginBottom":"24px"}),
            ]),
            
            html.Div([
                html.H3("📈 Use Case 2: Growth Opportunities", style={"fontSize":"22px", "fontWeight":600, "color":"#22c55e", "marginBottom":"12px"}),
                html.P([
                    html.Strong("Scenario:"), " You want to find periods when a stock gained 10% or more in 10 days."
                ], style={"fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"12px"}),
                html.Div([
                    html.Strong("Steps:", style={"display":"block", "marginBottom":"8px"}),
                    html.Ol([
                        html.Li("Upload your stock index data"),
                        html.Li("Select 'Gain' analysis"),
                        html.Li("Set Analysis Period to 10 days"),
                        html.Li("Set Minimum Threshold to 10%"),
                        html.Li("Check the Trade Windows table to see exact dates of these events"),
                    ], style={"lineHeight":"1.8", "marginLeft":"20px"}),
                    html.P([
                        html.Strong("Result:"), " You'll see all periods where this occurred, helping you understand growth patterns."
                    ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginTop":"12px"})
                ], style={"marginLeft":"20px", "marginBottom":"24px"}),
            ]),
            
            html.Div([
                html.H3("🔀 Use Case 3: Comparing Indexes", style={"fontSize":"22px", "fontWeight":600, "color":"#667eea", "marginBottom":"12px"}),
                html.P([
                    html.Strong("Scenario:"), " You want to see if technology stocks move with the overall market."
                ], style={"fontSize":"15px", "color":"rgba(255,255,255,0.9)", "marginBottom":"12px"}),
                html.Div([
                    html.Strong("Steps:", style={"display":"block", "marginBottom":"8px"}),
                    html.Ol([
                        html.Li("Go to Cross Index Analysis"),
                        html.Li("Upload S&P 500 data as Index A"),
                        html.Li("Upload NASDAQ data as Index B"),
                        html.Li("Set a 5-day return period"),
                        html.Li("Click Analyze"),
                    ], style={"lineHeight":"1.8", "marginLeft":"20px"}),
                    html.P([
                        html.Strong("Result:"), " A correlation of 0.85 or higher means they move together strongly. Lower correlation means more independent movement."
                    ], style={"fontSize":"14px", "color":"rgba(255,255,255,0.85)", "marginTop":"12px"})
                ], style={"marginLeft":"20px", "marginBottom":"24px"}),
            ]),
            
            html.Div([
                html.H3("💡 Pro Tips", style={"fontSize":"22px", "fontWeight":600, "color":"#00c896", "marginBottom":"12px"}),
                html.Ul([
                    html.Li([html.Strong("Start with common settings:"), " 5-day period, 3% threshold"]),
                    html.Li([html.Strong("Use YTD:"), " To analyze current year performance"]),
                    html.Li([html.Strong("Compare different thresholds:"), " Run analysis with 3%, 5%, and 10% to see different risk levels"]),
                    html.Li([html.Strong("Check weekend behavior:"), " The app handles weekends automatically - no manual adjustments needed"]),
                    html.Li([html.Strong("Look at indicators together:"), " RSI + MACD + Bollinger Bands give a complete picture"]),
                ], style={"fontSize":"15px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)", "marginLeft":"20px"})
            ], style={"padding":"20px", "background":"rgba(0,200,150,0.08)", "borderRadius":"12px", "border":"1px solid rgba(0,200,150,0.3)"}),
        ], style={"marginBottom":"32px"}),

        # Footer
        Card([
            html.H3("❓ Need More Help?", style={"fontSize":"22px", "fontWeight":600, "color":"#667eea", "marginBottom":"12px"}),
            html.P([
                "This documentation covers all the main features and concepts. ",
                "If you're still unsure about something, start with the examples above and experiment with your data. ",
                "The app is designed to be intuitive - just upload your CSV and try the preset options first!"
            ], style={"fontSize":"15px", "lineHeight":"1.8", "color":"rgba(255,255,255,0.9)"}),
            html.Div([
                html.A("← Back to Home", href="/", style={
                    "display":"inline-block", "marginTop":"20px", "padding":"12px 24px",
                    "background":"linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "color":"white", "textDecoration":"none", "borderRadius":"8px",
                    "fontWeight":"600", "fontSize":"15px"
                })
            ])
        ], style={"marginTop":"32px", "textAlign":"center"})
    ], style={"maxWidth":"900px", "margin":"0 auto"})
