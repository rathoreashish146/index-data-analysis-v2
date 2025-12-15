"""
Reusable UI components for the Index Data Analysis app.
"""

from dash import html, dcc


def PageContainer(children, **kwargs):
    """Consistent page container with max-width and responsive padding"""
    return html.Div(
        children,
        style={
            "maxWidth": "1152px",  # max-w-6xl equivalent
            "width": "100%",
            "margin": "0 auto",
            "padding": "16px 16px",
            **kwargs.get("style", {})
        },
        **{k: v for k, v in kwargs.items() if k != "style"}
    )


def Card(children, header=None, footer=None, **kwargs):
    """Reusable card component with header, content, and footer slots"""
    card_children = []
    if header:
        card_children.append(html.Div(
            header,
            style={
                "padding": "0 0 16px 0",
                "borderBottom": "1px solid rgba(255,255,255,0.1)",
                "marginBottom": "16px"
            }
        ))
    card_children.append(html.Div(children, style={"flex": 1}))
    if footer:
        card_children.append(html.Div(
            footer,
            style={
                "padding": "16px 0 0 0",
                "borderTop": "1px solid rgba(255,255,255,0.1)",
                "marginTop": "16px",
                "position": "sticky",
                "bottom": 0,
                "background": "#121821",
                "zIndex": 5
            }
        ))
    
    card_style = {
        "padding": "24px",
        "background": "#121821",
        "borderRadius": "12px",
        "boxShadow": "0 4px 12px rgba(0,0,0,0.3)",
        "border": "1px solid rgba(255,255,255,0.1)",
        "display": "flex",
        "flexDirection": "column",
        "position": "relative"
    }
    card_style.update(kwargs.get("style", {}))
    
    return html.Div(
        card_children,
        style=card_style,
        **{k: v for k, v in kwargs.items() if k != "style"}
    )


def Field(label, input_component, helper_text=None, error_text=None, required=False, **kwargs):
    """Reusable field component with label, input, helper text, and error message"""
    label_style = {
        "display": "block",
        "fontSize": "14px",
        "fontWeight": "600",
        "color": "rgba(255,255,255,0.9)",
        "marginBottom": "8px",
        "lineHeight": "1.4"
    }
    if required:
        label_style["color"] = "rgba(255,255,255,0.95)"
    
    field_children = [
        html.Label(label, style=label_style),
        input_component
    ]
    
    if helper_text:
        field_children.append(html.Div(
            helper_text,
            style={
                "fontSize": "12px",
                "color": "rgba(255,255,255,0.6)",
                "marginTop": "4px"
            }
        ))
    
    if error_text:
        field_children.append(html.Div(
            error_text,
            style={
                "fontSize": "12px",
                "color": "#ef4444",
                "marginTop": "4px"
            }
        ))
    
    return html.Div(
        field_children,
        style={
            "marginBottom": "20px",
            **kwargs.get("style", {})
        },
        **{k: v for k, v in kwargs.items() if k != "style"}
    )


def RadioGroup(id, label, options, value=None, inline=True, accent_color=None, **kwargs):
    """Reusable radio group component"""
    input_style = {
        "marginRight": "4px",
        "cursor": "pointer",
        "accentColor": accent_color or "rgba(0,200,150,0.8)"
    }
    label_style = {
        "marginRight": "16px",
        "cursor": "pointer",
        "fontSize": "14px",
        "color": "rgba(255,255,255,0.9)",
        "display": "inline-block" if inline else "block"
    }
    
    return html.Div([
        html.Label(label, style={
            "display": "block",
            "fontSize": "14px",
            "fontWeight": "600",
            "color": "rgba(255,255,255,0.9)",
            "marginBottom": "8px"
        }),
        dcc.RadioItems(
            id=id,
            options=options,
            value=value,
            inline=inline,
            inputStyle=input_style,
            labelStyle=label_style,
            **kwargs
        )
    ], style={"marginBottom": "20px"})


def CheckboxGroup(id, label, options, value=None, inline=True, **kwargs):
    """Reusable checkbox group component"""
    input_style = {
        "marginRight": "8px",
        "cursor": "pointer"
    }
    label_style = {
        "marginRight": "16px",
        "cursor": "pointer",
        "fontSize": "14px",
        "color": "rgba(255,255,255,0.9)",
        "display": "inline-block" if inline else "block"
    }
    
    return html.Div([
        html.Label(label, style={
            "display": "block",
            "fontSize": "14px",
            "fontWeight": "600",
            "color": "rgba(255,255,255,0.9)",
            "marginBottom": "8px"
        }),
        dcc.Checklist(
            id=id,
            options=options,
            value=value or [],
            inline=inline,
            inputStyle=input_style,
            labelStyle=label_style,
            **kwargs
        )
    ], style={"marginBottom": "20px"})


def DateRangePicker(id, label, preset_id=None, preset_options=None, preset_value="all",
                    snap_id=None, snap_value=None, min_date=None, max_date=None,
                    start_date=None, end_date=None, helper_text=None, **kwargs):
    """Reusable date range picker with preset dropdown and snap to month"""
    return html.Div([
        html.Label(label, style={
            "display": "block",
            "fontSize": "14px",
            "fontWeight": "600",
            "color": "rgba(255,255,255,0.9)",
            "marginBottom": "8px"
        }),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id=preset_id,
                    options=preset_options or [
                        {"label":"All","value":"all"},
                        {"label":"YTD","value":"ytd"},
                        {"label":"Last 1Y","value":"1y"},
                        {"label":"Last 3Y","value":"3y"},
                        {"label":"Last 6M","value":"6m"},
                        {"label":"Custom","value":"custom"},
                    ],
                    value=preset_value,
                    clearable=False,
                    style={
                        "width": "100%"
                    }
                )
            ], style={
                "flex": "0 0 160px"
            }),
            html.Div([
                dcc.DatePickerRange(
                    id=id,
                    display_format="YYYY-MM-DD",
                    minimum_nights=0,
                    clearable=True,
                    persistence=True,
                    min_date_allowed=min_date,
                    max_date_allowed=max_date,
                    start_date=start_date,
                    end_date=end_date,
                    style={
                        "width": "100%"
                    },
                    **kwargs
                )
            ], style={
                "flex": "1 1 auto",
                "minWidth": "300px"
            }),
            html.Div([
                dcc.Checklist(
                    id=snap_id,
                    options=[{"label": " Snap to month", "value": "snap"}],
                    value=snap_value or ["snap"],
                    inline=True,
                    style={"display": "inline-block"}
                )
            ], style={
                "flex": "0 0 auto",
                "display": "flex",
                "alignItems": "center"
            })
        ], style={
            "display": "flex",
            "alignItems": "center",
            "flexWrap": "wrap",
            "gap": "12px"
        }),
        helper_text and html.Div(
            helper_text,
            style={
                "fontSize": "12px",
                "color": "rgba(255,255,255,0.6)",
                "marginTop": "4px"
            }
        )
    ], style={"marginBottom": "20px"})


def FileDropzone(id, label, accept=".csv", filename=None, on_replace_id=None, on_remove_id=None, **kwargs):
    """Reusable file dropzone component with drag/drop and click support"""
    if filename:
        # Show file info with replace/remove actions
        return html.Div([
            html.Label(label, style={
                "display": "block",
                "fontSize": "14px",
                "fontWeight": "600",
                "color": "rgba(255,255,255,0.9)",
                "marginBottom": "8px"
            }),
            html.Div([
                html.Div([
                    html.Span("📄", style={"fontSize": "20px", "marginRight": "8px"}),
                    html.Span(filename, style={
                        "fontSize": "14px",
                        "color": "rgba(255,255,255,0.9)",
                        "flex": 1
                    }),
                    html.Button(
                        "Replace",
                        id=on_replace_id,
                        n_clicks=0,
                        style={
                            "padding": "6px 12px",
                            "marginRight": "8px",
                            "borderRadius": "6px",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "background": "rgba(255,255,255,0.1)",
                            "color": "rgba(255,255,255,0.9)",
                            "cursor": "pointer",
                            "fontSize": "12px"
                        }
                    ) if on_replace_id else None,
                    html.Button(
                        "Remove",
                        id=on_remove_id,
                        n_clicks=0,
                        style={
                            "padding": "6px 12px",
                            "borderRadius": "6px",
                            "border": "1px solid rgba(239,68,68,0.3)",
                            "background": "rgba(239,68,68,0.1)",
                            "color": "#ef4444",
                            "cursor": "pointer",
                            "fontSize": "12px"
                        }
                    ) if on_remove_id else None
                ], style={
                    "display": "flex",
                    "alignItems": "center",
                    "padding": "12px 16px",
                    "background": "rgba(0,200,150,0.1)",
                    "borderRadius": "8px",
                    "border": "1px solid rgba(0,200,150,0.3)"
                })
            ])
        ], style={"marginBottom": "20px"})
    
    # Show upload zone
    return html.Div([
        html.Label(label, style={
            "display": "block",
            "fontSize": "14px",
            "fontWeight": "600",
            "color": "rgba(255,255,255,0.9)",
            "marginBottom": "8px"
        }),
        dcc.Upload(
            id=id,
            children=html.Div([
                html.Div([
                    html.Span("Drag and drop or ", style={
                        "fontSize": "15px",
                        "color": "rgba(255,255,255,0.7)"
                    }),
                    html.A("Select CSV File", style={
                        "fontSize": "15px",
                        "color": "#00c896",
                        "fontWeight": "600",
                        "textDecoration": "underline"
                    })
                ], style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "8px"
                }),
                html.Span("📁", style={
                    "fontSize": "24px",
                    "marginLeft": "12px",
                    "opacity": 0.8,
                    "transition": "all 0.3s"
                })
            ], style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center"
            }),
            style={
                "width": "100%",
                "height": "100px",
                "borderWidth": "2px",
                "borderStyle": "dashed",
                "borderColor": "rgba(0,200,150,0.3)",
                "borderRadius": "12px",
                "textAlign": "center",
                "background": "rgba(0,200,150,0.05)",
                "transition": "all 0.3s",
                "cursor": "pointer",
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "center",
                "alignItems": "center"
            },
            multiple=False,
            accept=accept,
            **kwargs
        )
    ], style={"marginBottom": "20px"})


def Button(id, label, variant="primary", disabled=False, loading=False, full_width=False, **kwargs):
    """Reusable button component with variants and states"""
    base_style = {
        "padding": "12px 24px",
        "borderRadius": "8px",
        "border": "none",
        "fontWeight": "600",
        "fontSize": "15px",
        "cursor": "pointer" if not disabled and not loading else "not-allowed",
        "transition": "all 0.3s",
        "opacity": "0.6" if disabled or loading else "1"
    }
    
    if variant == "primary":
        base_style.update({
            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "color": "white",
            "boxShadow": "0 4px 12px rgba(102, 126, 234, 0.4)"
        })
    elif variant == "secondary":
        base_style.update({
            "background": "rgba(255,255,255,0.1)",
            "color": "rgba(255,255,255,0.9)",
            "border": "1px solid rgba(255,255,255,0.2)"
        })
    
    if full_width:
        base_style["width"] = "100%"
    
    button_label = f"{'⏳ ' if loading else ''}{label}"
    
    return html.Button(
        button_label,
        id=id,
        disabled=disabled or loading,
        style={**base_style, **kwargs.get("style", {})},
        **{k: v for k, v in kwargs.items() if k != "style"}
    )


def feature_card(icon, title, description, features, gradient_bg, href):
    """Reusable feature card component with consistent styling and layout"""
    return dcc.Link(
        html.Div([
            # Icon container - fixed height for alignment
            html.Div(
                icon,
                style={
                    "fontSize": "56px",
                    "lineHeight": "1",
                    "marginBottom": "24px",
                    "height": "56px",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center"
                }
            ),
            # Title
            html.H3(
                title,
                style={
                    "margin": "0 0 16px 0",
                    "fontSize": "26px",
                    "fontWeight": 700,
                    "lineHeight": "1.2",
                    "letterSpacing": "-0.5px"
                }
            ),
            # Description
            html.P(
                description,
                style={
                    "margin": "0 0 24px 0",
                    "fontSize": "15px",
                    "lineHeight": "1.6",
                    "opacity": 0.95,
                    "minHeight": "48px"  # Ensures consistent height for 2 lines
                }
            ),
            # Feature list
            html.Div([
                html.Div([
                    html.Span("✓ ", style={"marginRight": "8px", "fontWeight": 600}),
                    html.Span(feature)
                ], style={
                    "fontSize": "14px",
                    "marginBottom": "10px" if i < len(features) - 1 else "0",
                    "opacity": 0.9,
                    "display": "flex",
                    "alignItems": "flex-start",
                    "lineHeight": "1.5"
                }) for i, feature in enumerate(features)
            ], style={
                "textAlign": "left",
                "width": "100%"
            })
        ], style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "padding": "36px 28px",
            "borderRadius": "20px",
            "background": gradient_bg,
            "color": "white",
            "width": "100%",
            "maxWidth": "380px",
            "minHeight": "360px",
            "boxShadow": "0 8px 24px rgba(0,0,0,0.2), 0 2px 8px rgba(0,0,0,0.1)",
            "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
            "cursor": "pointer",
            "boxSizing": "border-box",
            "position": "relative",
            "overflow": "hidden"
        }),
        href=href,
        style={"textDecoration": "none", "flex": "1 1 380px", "maxWidth": "380px"}
    )

