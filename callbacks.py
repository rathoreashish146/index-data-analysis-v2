"""
Callback functions for the Index Data Analysis app.
Contains all Dash app callbacks for user interactions.
"""

import base64
import io
import numpy as np
import pandas as pd
from dash import html, dcc, dash_table, no_update
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils import (
    parse_csv_flexible, compute_range, compute_windowed_returns_calendar,
    build_indicators, drop_event_analysis, gain_event_analysis,
    compute_drawdown_recovery
)
from config import STORE_RAW, STORE_META, STORE_A, STORE_B, MONTH_OPTIONS
from layouts import navbar, home_layout, single_layout, cross_layout, docs_layout


def register_callbacks(app):
    """Register all callbacks with the Dash app"""
    
    # Navbar callback - always dark theme
    @app.callback(
        Output("navbar-container", "children"),
        Input("url", "pathname"),
        prevent_initial_call=False
    )
    def update_navbar(pathname):
        # Always return dark theme navbar
        return navbar()
    
    
    # Router
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname")
    )
    def render_page(pathname):
        if pathname == "/single":
            return single_layout()
        elif pathname == "/cross":
            return cross_layout()
        elif pathname == "/docs":
            return docs_layout()
        else:
            return home_layout()
    
    # -----------------------------
    # Indicators Select All / Clear All callback
    # -----------------------------
    @app.callback(
        Output("indicators-select", "value"),
        Input("indicators-select-all", "n_clicks"),
        Input("indicators-clear-all", "n_clicks"),
        State("indicators-select", "options"),
        prevent_initial_call=True,
    )
    def update_indicators_select_all(select_all_clicks, clear_all_clicks, options):
        ctx = dash.callback_context
        if not ctx.triggered:
            return no_update
        
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if trigger_id == "indicators-select-all":
            # Select all indicator values
            return [opt["value"] for opt in options]
        elif trigger_id == "indicators-clear-all":
            # Clear all (return empty list)
            return []
        
        return no_update
    
    # -----------------------------
    # Upload callback (Single page)
    # -----------------------------
    @app.callback(
        Output("file-msg", "children"),
        Output("warn-msg", "children"),
        Output("preview", "children"),          # <<< Data Preview here
        Output(STORE_RAW, "data"),
        Output(STORE_META, "data"),
        # Drop bounds
        Output("date-range-drop", "min_date_allowed"),
        Output("date-range-drop", "max_date_allowed"),
        Output("date-range-drop", "start_date"),
        Output("date-range-drop", "end_date"),
        # Gain bounds
        Output("date-range-gain", "min_date_allowed"),
        Output("date-range-gain", "max_date_allowed"),
        Output("date-range-gain", "start_date"),
        Output("date-range-gain", "end_date"),
        # Year options for jump controls
        Output("jump-year-drop", "options"),
        Output("jump-year-drop", "value"),
        Output("jump-month-drop", "value"),
        Output("jump-year-gain", "options"),
        Output("jump-year-gain", "value"),
        Output("jump-month-gain", "value"),
        Input("uploader", "contents"),
        State("uploader", "filename"),
        prevent_initial_call=True,
    )
    def on_upload_single(contents, filename):
        if contents is None:
            return (no_update,)*19
    
        df, warns, err = parse_csv_flexible(contents, filename)
        if err:
            return (html.Div(err, style={"color":"crimson"}), None, None, None, None,
                    no_update, no_update, no_update, no_update,
                    no_update, no_update, no_update, no_update,
                    [], None, None, [], None, None)
    
        info = html.Div([
            html.Strong("Uploaded:"), html.Span(f" {filename} "),
            html.Span(" · Detected columns: ['datetime','index']"),
            html.Span(f" · Rows: {len(df)}"),
        ])
        warn_block = (html.Div([html.Strong("Warnings:"),
                       html.Ul([html.Li(w) for w in warns])], style={"color":"#996800"}) if warns else None)
    
        # --- Data Preview (first 10 rows)
        table = dash_table.DataTable(
            data=df.head(10).to_dict("records"),
            columns=[{"name": c, "id": c} for c in df.columns],
            page_size=10, 
            style_table={"overflowX": "auto", "backgroundColor": "#1a1a1a"},
            style_cell={
                "textAlign": "left", 
                "minWidth": "120px",
                "backgroundColor": "#1a1a1a",
                "color": "rgba(255,255,255,0.9)",
                "border": "1px solid rgba(255,255,255,0.1)",
                "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
            },
            style_header={
                "backgroundColor": "#252525",
                "color": "rgba(255,255,255,0.95)",
                "fontWeight": "600",
                "border": "1px solid rgba(0,200,150,0.3)",
                "textAlign": "left"
            },
            style_data={
                "backgroundColor": "#1a1a1a",
                "color": "rgba(255,255,255,0.9)",
                "border": "1px solid rgba(255,255,255,0.1)"
            },
            style_data_conditional=[
                {
                    "if": {"row_index": "even"},
                    "backgroundColor": "#222222",
                },
                {
                    "if": {"state": "selected"},
                    "backgroundColor": "rgba(0,200,150,0.2)",
                    "border": "1px solid rgba(0,200,150,0.5)"
                }
            ],
        )
    
        raw_payload = {
            "filename": filename,
            "columns": list(df.columns),
            "rows": int(len(df)),
            "csv_b64": base64.b64encode(df.to_csv(index=False).encode()).decode(),
        }
        meta = {"summary": {"rows": int(len(df)), "columns": list(df.columns)}}
    
        min_d = df["datetime"].min().date()
        max_d = df["datetime"].max().date()
        years = list(range(min_d.year, max_d.year + 1))
        year_options = [{"label": str(y), "value": y} for y in years]
    
        return (
            info, warn_block, html.Div([html.H3("Preview (first 10 rows)"), table]),
            raw_payload, meta,
            min_d, max_d, min_d, max_d,
            min_d, max_d, min_d, max_d,
            year_options, min_d.year, 1,
            year_options, min_d.year, 1
        )
    
    # Preset → custom when dates edited (Single page)
    @app.callback(Output("preset-drop", "value"),
                  Input("date-range-drop", "start_date"),
                  Input("date-range-drop", "end_date"),
                  prevent_initial_call=True)
    def force_custom_drop(_s, _e):
        return "custom"
    
    @app.callback(Output("preset-gain", "value"),
                  Input("date-range-gain", "start_date"),
                  Input("date-range-gain", "end_date"),
                  prevent_initial_call=True)
    def force_custom_gain(_s, _e):
        return "custom"
    
    # Jump-to initial_visible_month (Single page)
    @app.callback(
        Output("date-range-drop", "initial_visible_month"),
        Input("jump-year-drop", "value"),
        Input("jump-month-drop", "value"),
        State("date-range-drop", "initial_visible_month"),
        prevent_initial_call=True
    )
    def jump_drop(year, month, _cur):
        if year and month:
            return pd.Timestamp(int(year), int(month), 1)
        return no_update
    
    @app.callback(
        Output("date-range-gain", "initial_visible_month"),
        Input("jump-year-gain", "value"),
        Input("jump-month-gain", "value"),
        State("date-range-gain", "initial_visible_month"),
        prevent_initial_call=True
    )
    def jump_gain(year, month, _cur):
        if year and month:
            return pd.Timestamp(int(year), int(month), 1)
        return no_update
    
    # -----------------------------
    # Analyze callback (Single page)
    # -----------------------------
    @app.callback(
        # DROP outputs
        Output("analysis-output-drop", "children"),
        Output("return-chart-drop-container", "children"),
        Output("bar-chart-drop-container", "children"),
        Output("stats-drop", "children"),
        Output("trade-windows-drop-container", "children"),
        # GAIN outputs
        Output("analysis-output-gain", "children"),
        Output("return-chart-gain-container", "children"),
        Output("bar-chart-gain-container", "children"),
        Output("stats-gain", "children"),
        Output("trade-windows-gain-container", "children"),
        # INDICATOR figure
        Output("indicators-container", "children"),
        # Results container visibility
        Output("results-container", "style"),
        Input("analyze", "n_clicks"),
        State(STORE_RAW, "data"),
        State("analysis-types", "value"),
        # Drop states
        State("preset-drop", "value"),
        State("date-range-drop", "start_date"),
        State("date-range-drop", "end_date"),
        State("snap-month-drop", "value"),
        State("window-size-drop", "value"),
        State("window-size-input-drop", "value"),
        State("min-threshold-drop", "value"),
        State("min-threshold-input-drop", "value"),
        # Gain states
        State("preset-gain", "value"),
        State("date-range-gain", "start_date"),
        State("date-range-gain", "end_date"),
        State("snap-month-gain", "value"),
        State("window-size-gain", "value"),
        State("window-size-input-gain", "value"),
        State("min-threshold-gain", "value"),
        State("min-threshold-input-gain", "value"),
        # Indicators toggles
        State("indicators-select", "value"),
        prevent_initial_call=True,
    )
    def run_analysis_single(n_clicks, raw_payload, analysis_types,
                     preset_drop, sd_drop, ed_drop, snap_drop, ws_drop, ws_in_drop, th_drop, th_in_drop,
                     preset_gain, sd_gain, ed_gain, snap_gain, ws_gain, ws_in_gain, th_gain, th_in_gain,
                     indicators_selected):
        if not n_clicks:
            return (no_update,) * 12
        if not raw_payload:
            # Hide all results when no data
            hidden_style = {"display": "none"}
            return (None, None, None, None, None, None, None, None, None, None, None, hidden_style)
    
        try:
            csv_bytes = base64.b64decode(raw_payload["csv_b64"].encode())
            df = pd.read_csv(io.BytesIO(csv_bytes))
        except Exception as e:
            # Hide all results on error
            hidden_style = {"display": "none"}
            return (None, None, None, None, None, None, None, None, None, None, None, hidden_style)
    
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
        df["index"] = pd.to_numeric(df["index"], errors="coerce")
        df = df.dropna(subset=["datetime", "index"]).sort_values("datetime").reset_index(drop=True)
    
        data_min, data_max = df["datetime"].min(), df["datetime"].max()
    
        def build_outputs(mode: str,
                          preset, sdate, edate, snap, ws_radio, ws_custom, th_radio, th_custom):
            snap_month = ("snap" in (snap or []))
            start, end = compute_range(preset, sdate, edate, data_min, data_max, snap_month)
            dff = df[(df["datetime"] >= start) & (df["datetime"] <= end)].reset_index(drop=True)
            if dff.empty:
                msg = html.Div(f"No data in selected date range ({start.date()} to {end.date()}).", style={"color": "crimson"})
                empty = go.Figure()
                return msg, empty, empty, None, None
    
            ws = int(ws_custom) if ws_custom else int(ws_radio)
            th_pct = float(th_custom) if th_custom is not None else float(th_radio)
            th_frac = th_pct / 100.0
    
            # Weekend-aware summary
            if mode == "gain":
                summary = gain_event_analysis(dff, minimum_per_gain=th_frac, windows_size=ws)
                title = "Gain Event Analysis"
                label = "Min Gain: "
                sign = +1
                color = "#22c55e"
            else:
                summary = drop_event_analysis(dff, minimum_per_drop=th_frac, windows_size=ws)
                title = "Drop Event Analysis"
                label = "Min Drop: "
                sign = -1
                color = "#ef4444"
    
            (k, v), = summary.items()
            bg_color = "rgba(34,197,94,0.08)" if mode == "gain" else "rgba(239,68,68,0.08)"
            border_color = "rgba(34,197,94,0.3)" if mode == "gain" else "rgba(239,68,68,0.3)"
            card = html.Div([
                html.H3(title, style={"marginTop": 0, "fontSize": "24px", "fontWeight": 700, "color": "inherit"}),
                html.P([
                    html.Strong("Change over: "), f"{ws} calendar days (weekend-aware) ",
                    html.Span(" · "),
                    html.Strong("Range: "), f"{start.date()} → {end.date()} ",
                    html.Span(" · "),
                    html.Strong(label), f"{th_pct:.2f}%",
                ], style={"fontSize": "14px", "color": "inherit", "opacity": 0.8, "marginBottom": "20px"}),
                html.Div([
                    html.Div([
                        html.Div("Events", style={"color": "rgba(255,255,255,0.7)", "fontSize": "13px", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
                        html.Div(str(v["events"]), style={"fontSize": "36px", "fontWeight": 700, "color": color, "marginTop": "8px"}),
                    ], style={"flex": 1, "textAlign": "center", "padding": "16px", "background": "rgba(255,255,255,0.05)", "borderRadius": "12px", "border": "1px solid rgba(255,255,255,0.1)"}),
                    html.Div([
                        html.Div("Probability", style={"color": "rgba(255,255,255,0.7)", "fontSize": "13px", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
                        html.Div(v["probability"], style={"fontSize": "36px", "fontWeight": 700, "color": color, "marginTop": "8px"}),
                    ], style={"flex": 1, "textAlign": "center", "padding": "16px", "background": "rgba(255,255,255,0.05)", "borderRadius": "12px", "border": "1px solid rgba(255,255,255,0.1)"}),
                ], style={"display": "flex", "gap": "16px", "marginTop": "12px"}),
            ], style={"border": f"1px solid {border_color}", "borderRadius": "16px", "padding": "24px", "background": bg_color, "boxShadow": "0 4px 12px rgba(0,0,0,0.3)"})
    
            # Weekend-aware returns for visuals
            ret = compute_windowed_returns_calendar(dff, ws)
            mask = ~ret.isna()
            x_time = dff.loc[mask, "datetime"]
            y_pct = ret.loc[mask].values * 100.0
    
            # Return chart
            line_fig = go.Figure()
            if len(y_pct) > 0:
                line_fig.add_trace(go.Scatter(x=x_time, y=y_pct, mode="lines", name=f"{ws}-day % change"))
                th_line = sign * th_frac * 100.0
                line_fig.add_trace(go.Scatter(x=x_time, y=[th_line]*len(x_time), mode="lines",
                                              name="Threshold", line=dict(dash="dash")))
                idx = np.arange(len(y_pct))
                z = np.polyfit(idx, y_pct, 1)
                trend = z[0]*idx + z[1]
                line_fig.add_trace(go.Scatter(x=x_time, y=trend, mode="lines", name="Trend", line=dict(dash="dot")))
            line_fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(26,26,26,0.8)",
                paper_bgcolor="rgba(10,10,10,0.8)",
                font=dict(color="rgba(255,255,255,0.9)"),
                margin=dict(t=100, r=10, l=40, b=40),  # Increased top margin for legend
                xaxis_title="Time", 
                yaxis_title="% change",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.01,  # Position just above the chart
                    xanchor="center",
                    x=0.5,
                    bgcolor="rgba(10,10,10,0.9)",
                    bordercolor="rgba(255,255,255,0.2)",
                    borderwidth=1,
                    itemwidth=30,
                    font=dict(size=10)
                ),
                xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
            )
    
            # Bar chart (counts & probabilities by threshold)
            ret_clean = ret.dropna()
            N = len(ret_clean)
            thresholds_pct = [i for i in range(1, 11)]
            labels = [f"{t}%" for t in thresholds_pct]
            if mode == "gain":
                counts = np.array([(ret_clean >= (t/100.0)).sum() for t in thresholds_pct], dtype=int)
                bar_title = f"{ws}-day gain events"
            else:
                counts = np.array([(ret_clean <= -(t/100.0)).sum() for t in thresholds_pct], dtype=int)
                bar_title = f"{ws}-day drop events"
            probs = (counts / N) * 100.0 if N > 0 else np.zeros_like(counts, dtype=float)
    
            bar_fig = make_subplots(specs=[[{"secondary_y": True}]])
            bar_fig.add_trace(
                go.Bar(
                    x=labels, y=counts, name="Count",
                    marker_color=color,
                    text=[f"{c:,}" for c in counts], textposition="outside",
                    cliponaxis=False,
                    customdata=np.round(probs, 2),
                    hovertemplate="<b>%{x}</b><br>Count: %{y:,}<br>Probability: %{customdata:.2f}%<extra></extra>",
                ),
                secondary_y=False,
            )
            max_prob = float(probs.max()) if len(probs) else 0.0
            y2_top = max(5.0, np.ceil(max_prob * 1.15 / 5.0) * 5.0)
            bar_fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(26,26,26,0.8)",
                paper_bgcolor="rgba(10,10,10,0.8)",
                font=dict(color="rgba(255,255,255,0.9)"),
                title=dict(
                    text=bar_title + (f"  · N={N}" if N else ""),
                    x=0.5,
                    xanchor="center",
                    y=0.98,
                    yanchor="top"
                ),
                margin=dict(t=100, r=10, l=40, b=40),  # Increased top margin for legend
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.01,  # Position just above the chart
                    xanchor="center",
                    x=0.5,
                    bgcolor="rgba(10,10,10,0.9)",
                    bordercolor="rgba(255,255,255,0.2)",
                    borderwidth=1,
                    itemwidth=30,
                    font=dict(size=10)
                ),
                xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
                bargap=0.2
            )
            bar_fig.update_yaxes(title_text="Count of events", secondary_y=False)
            bar_fig.update_yaxes(title_text="Probability (%)", range=[0, y2_top], secondary_y=True)
    
            # Stats
            if N > 0:
                desc = ret_clean.describe()
                stats_list = [
                    ("Data points", f"{int(desc['count'])}"),
                    ("Average change", f"{desc['mean']*100:.2f}%"),
                    ("Typical variability (stdev)", f"{desc['std']*100:.2f}%"),
                    ("Biggest drop", f"{desc['min']*100:.2f}%"),
                    ("25th percentile", f"{desc['25%']*100:.2f}%"),
                    ("Median (middle)", f"{desc['50%']*100:.2f}%"),
                    ("75th percentile", f"{desc['75%']*100:.2f}%"),
                    ("Biggest rise", f"{desc['max']*100:.2f}%"),
                ]
            else:
                stats_list = [("Data points", "0")]
            stats_view = html.Div([
                html.H4("Change summary", style={"margin": "0 0 16px 0", "fontSize": "20px", "fontWeight": 600, "color": "inherit"}),
                html.Ul([html.Li(html.Span([html.Strong(k + ": ", style={"color": "inherit"}), v]), style={
                    "marginBottom": "8px", "fontSize": "14px", "color": "inherit", "opacity": 0.9
                }) for k, v in stats_list], style={"listStyle": "none", "padding": 0})
            ], style={"background": "rgba(255,255,255,0.05)", "border": "1px solid rgba(255,255,255,0.1)",
                      "borderRadius": "16px", "padding": "24px", "boxShadow": "0 4px 12px rgba(0,0,0,0.3)"})
    
            # Trade windows list
            # trade_table = build_trade_window_table(dff[["datetime","index"]], ws, limit=200)
            
            # Wrap graphs and tables in containers with proper styling
            return_chart_container = html.Div([
                dcc.Graph(figure=line_fig, config={"displayModeBar": False}, style={"height": "320px"})
            ], style={
                "background":"rgba(255,255,255,0.05)", "borderRadius":"12px",
                "padding":"16px", "marginBottom":"16px",
                "boxShadow":"0 2px 8px rgba(0,0,0,0.3)",
                "border":"1px solid rgba(255,255,255,0.1)"
            })
            
            bar_chart_container = html.Div([
                dcc.Graph(figure=bar_fig, config={"displayModeBar": False}, style={"height": "320px"})
            ], style={
                "background":"rgba(255,255,255,0.05)", "borderRadius":"12px",
                "padding":"16px", "marginBottom":"16px",
                "boxShadow":"0 2px 8px rgba(0,0,0,0.3)",
                "border":"1px solid rgba(255,255,255,0.1)"
            })
            
            # COMMENTED OUT FOR DEBUGGING - Trade windows data hidden
            # trade_windows_container = html.Div([
            #     html.H4("Trade windows (first and last day)", style={
            #         "fontSize":"20px", "fontWeight":600, "color":"inherit",
            #         "marginTop":"32px", "marginBottom":"16px"
            #     }),
            #     trade_table
            # ], style={
            #     "background":"rgba(255,255,255,0.05)", "borderRadius":"12px",
            #     "padding":"20px", "boxShadow":"0 2px 8px rgba(0,0,0,0.3)",
            #     "border":"1px solid rgba(255,255,255,0.1)"
            # })
            trade_windows_container = html.Div()  # Empty placeholder
    
            return card, return_chart_container, bar_chart_container, stats_view, trade_windows_container, dff
    
        want_drop = "drop" in (analysis_types or [])
        want_gain = "gain" in (analysis_types or [])
    
        drop_out = build_outputs("drop",
                                 preset_drop, sd_drop, ed_drop, snap_drop, ws_drop, ws_in_drop, th_drop, th_in_drop) \
                   if want_drop else (html.Div("Drop disabled"), None, None, None, None, None)
    
        gain_out = build_outputs("gain",
                                 preset_gain, sd_gain, ed_gain, snap_gain, ws_gain, ws_in_gain, th_gain, th_in_gain) \
                   if want_gain else (html.Div("Gain disabled"), None, None, None, None, None)
    
        # Build indicators figure from the union of the filtered range (prefer gain range if both same; else use full df slice)
        # We'll use the DROP slice if available, else GAIN slice, else overall df.
        dff_for_indicators = None
        if drop_out[-1] is not None:
            dff_for_indicators = drop_out[-1]
        if gain_out[-1] is not None:
            # if both exist, take intersection of their date windows to keep consistent
            if dff_for_indicators is not None:
                s1, e1 = dff_for_indicators["datetime"].min(), dff_for_indicators["datetime"].max()
                s2, e2 = gain_out[-1]["datetime"].min(), gain_out[-1]["datetime"].max()
                s, e = max(s1, s2), min(e1, e2)
                dff_for_indicators = df[(df["datetime"]>=s) & (df["datetime"]<=e)].reset_index(drop=True)
            else:
                dff_for_indicators = gain_out[-1]
        if dff_for_indicators is None:
            dff_for_indicators = df.copy()
    
        # --- Build indicators and figure
        feats = build_indicators(dff_for_indicators[["datetime","index"]].copy())
        price = dff_for_indicators["index"].astype(float)
        time = dff_for_indicators["datetime"]
    
        show_sma  = "sma"  in (indicators_selected or [])
        show_ema  = "ema"  in (indicators_selected or [])
        show_bb   = "bb"   in (indicators_selected or [])
        show_rsi  = "rsi"  in (indicators_selected or [])
        show_macd = "macd" in (indicators_selected or [])
        show_vol  = "vol"  in (indicators_selected or [])
        show_dd   = "dd"   in (indicators_selected or [])
    
        # Determine which rows to show
        row1_needed = any([True, show_sma, show_ema, show_bb, show_vol, show_dd])  # price always shown
        row2_needed = show_rsi
        row3_needed = show_macd
    
        rows = (1 if row1_needed else 0) + (1 if row2_needed else 0) + (1 if row3_needed else 0)
        if rows == 0:
            rows = 1  # safety
    
        fig_ind = make_subplots(
            rows=rows, cols=1, shared_xaxes=True,
            row_heights=[0.5 if rows==3 else (0.65 if rows==2 else 1.0)] + ([0.25] if rows>=2 else []) + ([0.25] if rows==3 else []),
            vertical_spacing=0.06,
            specs=[[{"secondary_y": True}] for _ in range(rows)]
        )
    
        # helper to map logical row numbers
        cur_row = 1
        row_price = cur_row
        # Row 1: Price + overlays
        fig_ind.add_trace(go.Scatter(x=time, y=price, mode="lines", name="Price"), row=row_price, col=1, secondary_y=False)
    
        if show_sma:
            fig_ind.add_trace(go.Scatter(x=time, y=feats["sma_5"],  mode="lines", name="SMA 5"),  row=row_price, col=1, secondary_y=False)
            fig_ind.add_trace(go.Scatter(x=time, y=feats["sma_20"], mode="lines", name="SMA 20"), row=row_price, col=1, secondary_y=False)
        if show_ema:
            fig_ind.add_trace(go.Scatter(x=time, y=feats["ema_12"], mode="lines", name="EMA 12"), row=row_price, col=1, secondary_y=False)
            fig_ind.add_trace(go.Scatter(x=time, y=feats["ema_26"], mode="lines", name="EMA 26"), row=row_price, col=1, secondary_y=False)
        if show_bb:
            fig_ind.add_trace(go.Scatter(x=time, y=feats["bb_mid"], mode="lines", name="BB Mid"),   row=row_price, col=1, secondary_y=False)
            fig_ind.add_trace(go.Scatter(x=time, y=feats["bb_up"],  mode="lines", name="BB Upper"), row=row_price, col=1, secondary_y=False)
            fig_ind.add_trace(go.Scatter(x=time, y=feats["bb_lo"],  mode="lines", name="BB Lower"), row=row_price, col=1, secondary_y=False)
        if show_vol:
            # plot vol_20 on secondary y to keep scales tidy
            fig_ind.add_trace(go.Scatter(x=time, y=feats["vol_20"], mode="lines", name="Vol 20 (stdev)"),
                              row=row_price, col=1, secondary_y=True)
        if show_dd:
            fig_ind.add_trace(go.Scatter(x=time, y=feats["dd"], mode="lines", name="Drawdown"),
                              row=row_price, col=1, secondary_y=True)
    
        fig_ind.update_yaxes(title_text="Price", row=row_price, col=1, secondary_y=False)
        if show_vol or show_dd:
            fig_ind.update_yaxes(title_text="Vol / DD", row=row_price, col=1, secondary_y=True)
    
        # Row 2: RSI (if needed)
        if row2_needed:
            cur_row += 1
            fig_ind.add_trace(go.Scatter(x=time, y=feats["rsi_14"], mode="lines", name="RSI (14)"),
                              row=cur_row, col=1, secondary_y=False)
            fig_ind.add_hline(y=70, line=dict(dash="dash"), row=cur_row, col=1)
            fig_ind.add_hline(y=30, line=dict(dash="dash"), row=cur_row, col=1)
            fig_ind.update_yaxes(title_text="RSI", range=[0, 100], row=cur_row, col=1)
    
        # Row 3: MACD (if needed)
        if row3_needed:
            cur_row += 1
            fig_ind.add_trace(go.Bar(x=time, y=feats["macd_hist"], name="MACD Hist"),
                              row=cur_row, col=1, secondary_y=False)
            fig_ind.add_trace(go.Scatter(x=time, y=feats["macd"],     mode="lines", name="MACD"),
                              row=cur_row, col=1, secondary_y=False)
            fig_ind.add_trace(go.Scatter(x=time, y=feats["macd_sig"], mode="lines", name="MACD Signal"),
                              row=cur_row, col=1, secondary_y=False)
            fig_ind.update_yaxes(title_text="MACD", row=cur_row, col=1)
    
        # Calculate proper margins to accommodate legend outside plotting area
        # Legend will be positioned above the chart, so we need extra top margin
        legend_height = 60  # Estimated height for horizontal legend
        top_margin = 120 + legend_height  # Extra top margin for legend above chart
        bottom_margin = 80  # Base bottom margin
        
        fig_ind.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(26,26,26,0.8)",
            paper_bgcolor="rgba(10,10,10,0.8)",
            font=dict(color="rgba(255,255,255,0.9)"),
            margin=dict(t=top_margin, r=10, l=40, b=bottom_margin),  # Extra top margin for legend above
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.01,  # Position just above the chart (outside plotting area)
                xanchor="center",
                x=0.5,
                itemwidth=30,
                font=dict(size=10),
                bgcolor="rgba(10,10,10,0.9)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
                tracegroupgap=10,  # Space between legend items
                entrywidthmode="fraction",
                entrywidth=0.15  # Control width of legend items
            ),
            title=dict(
                text="Indicators (weekend-aware where applicable)",
                x=0.5,
                xanchor="center",
                font=dict(size=16),
                y=0.95,
                yanchor="top"
            ),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
        )
        
        # Update all subplot x-axes to have consistent styling and prevent overlap
        for i in range(1, cur_row + 1):
            fig_ind.update_xaxes(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.1)",
                row=i, col=1
        )
    
        # Unpack results for return
        drop_card, drop_line, drop_bar, drop_stats, drop_table, _dff_drop = drop_out
        gain_card, gain_line, gain_bar, gain_stats, gain_table, _dff_gain = gain_out
        
        # Wrap indicators figure in container
        indicators_container = html.Div([
            html.H3("Indicator Charts", style={
                "fontSize":"28px", "fontWeight":700, "color":"inherit",
                "marginTop":"40px", "marginBottom":"20px"
            }),
            dcc.Graph(figure=fig_ind, config={"displayModeBar": False}, style={"height":"540px"})
        ], style={
            "background":"rgba(255,255,255,0.05)", "borderRadius":"16px",
            "padding":"20px", "boxShadow":"0 4px 12px rgba(0,0,0,0.3)",
            "border":"1px solid rgba(255,255,255,0.1)"
        })
        
        # Show results container
        results_style = {"display": "flex", "gap": "20px", "flexWrap": "wrap"}
    
        return (drop_card, drop_line, drop_bar, drop_stats, drop_table,
                gain_card, gain_line, gain_bar, gain_stats, gain_table,
                indicators_container, results_style)
    
    # -----------------------------
    # Upload callback (CROSS page)
    # -----------------------------
    @app.callback(
        # A side
        Output("file-msg-a", "children"),
        Output("warn-msg-a", "children"),
        Output("preview-a", "children"),
        Output(STORE_A, "data"),
        # B side
        Output("file-msg-b", "children"),
        Output("warn-msg-b", "children"),
        Output("preview-b", "children"),
        Output(STORE_B, "data"),
        # Date range bounds (shared)
        Output("date-range-cross", "min_date_allowed"),
        Output("date-range-cross", "max_date_allowed"),
        Output("date-range-cross", "start_date"),
        Output("date-range-cross", "end_date"),
        # Year jump options
        Output("jump-year-cross", "options"),
        Output("jump-year-cross", "value"),
        Output("jump-month-cross", "value"),
    
        Input("uploader-a", "contents"),
        State("uploader-a", "filename"),
        Input("uploader-b", "contents"),
        State("uploader-b", "filename"),
        prevent_initial_call=True,
    )
    def upload_cross(contents_a, filename_a, contents_b, filename_b):
        out = [no_update]*15
    
        # Parse A
        dfA = warnsA = errA = None
        if contents_a is not None:
            dfA, warnsA, errA = parse_csv_flexible(contents_a, filename_a)
            if errA:
                out[0] = html.Div(errA, style={"color":"crimson"})
                out[1] = None
                out[2] = None
                out[3] = None
            else:
                out[0] = html.Div([html.Strong("A uploaded:"), f" {filename_a} · Rows: {len(dfA)}"])
                out[1] = (html.Div([html.Strong("Warnings:"), html.Ul([html.Li(w) for w in warnsA])],
                                   style={"color":"#996800"}) if warnsA else None)
                tableA = dash_table.DataTable(
                    data=dfA.head(10).to_dict("records"),
                    columns=[{"name": c, "id": c} for c in dfA.columns],
                    page_size=10, 
                    style_table={"overflowX":"auto", "backgroundColor": "#1a1a1a"},
                    style_cell={
                        "textAlign":"left",
                        "minWidth":"120px",
                        "backgroundColor": "#1a1a1a",
                        "color": "rgba(255,255,255,0.9)",
                        "border": "1px solid rgba(255,255,255,0.1)",
                        "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
                    },
                    style_header={
                        "backgroundColor": "#252525",
                        "color": "rgba(255,255,255,0.95)",
                        "fontWeight": "600",
                        "border": "1px solid rgba(0,200,150,0.3)",
                        "textAlign": "left"
                    },
                    style_data={
                        "backgroundColor": "#1a1a1a",
                        "color": "rgba(255,255,255,0.9)",
                        "border": "1px solid rgba(255,255,255,0.1)"
                    },
                    style_data_conditional=[
                        {
                            "if": {"row_index": "even"},
                            "backgroundColor": "#222222",
                        },
                        {
                            "if": {"state": "selected"},
                            "backgroundColor": "rgba(0,200,150,0.2)",
                            "border": "1px solid rgba(0,200,150,0.5)"
                        }
                    ],
                )
                out[2] = html.Div([html.H4("Preview A (first 10)"), tableA])
                out[3] = {
                    "filename": filename_a,
                    "csv_b64": base64.b64encode(dfA.to_csv(index=False).encode()).decode()
                }
    
        # Parse B
        dfB = warnsB = errB = None
        if contents_b is not None:
            dfB, warnsB, errB = parse_csv_flexible(contents_b, filename_b)
            if errB:
                out[4] = html.Div(errB, style={"color":"crimson"})
                out[5] = None
                out[6] = None
                out[7] = None
            else:
                out[4] = html.Div([html.Strong("B uploaded:"), f" {filename_b} · Rows: {len(dfB)}"])
                out[5] = (html.Div([html.Strong("Warnings:"), html.Ul([html.Li(w) for w in warnsB])],
                                   style={"color":"#996800"}) if warnsB else None)
                tableB = dash_table.DataTable(
                    data=dfB.head(10).to_dict("records"),
                    columns=[{"name": c, "id": c} for c in dfB.columns],
                    page_size=10, 
                    style_table={"overflowX":"auto", "backgroundColor": "#1a1a1a"},
                    style_cell={
                        "textAlign":"left",
                        "minWidth":"120px",
                        "backgroundColor": "#1a1a1a",
                        "color": "rgba(255,255,255,0.9)",
                        "border": "1px solid rgba(255,255,255,0.1)",
                        "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
                    },
                    style_header={
                        "backgroundColor": "#252525",
                        "color": "rgba(255,255,255,0.95)",
                        "fontWeight": "600",
                        "border": "1px solid rgba(0,200,150,0.3)",
                        "textAlign": "left"
                    },
                    style_data={
                        "backgroundColor": "#1a1a1a",
                        "color": "rgba(255,255,255,0.9)",
                        "border": "1px solid rgba(255,255,255,0.1)"
                    },
                    style_data_conditional=[
                        {
                            "if": {"row_index": "even"},
                            "backgroundColor": "#222222",
                        },
                        {
                            "if": {"state": "selected"},
                            "backgroundColor": "rgba(0,200,150,0.2)",
                            "border": "1px solid rgba(0,200,150,0.5)"
                        }
                    ],
                )
                out[6] = html.Div([html.H4("Preview B (first 10)"), tableB])
                out[7] = {
                    "filename": filename_b,
                    "csv_b64": base64.b64encode(dfB.to_csv(index=False).encode()).decode()
                }
    
        # Set date bounds based on whichever is loaded; if both, use intersection
        if dfA is None and dfB is None:
            return tuple(out)
    
        if dfA is not None and dfB is not None:
            min_d = max(dfA["datetime"].min().date(), dfB["datetime"].min().date())
            max_d = min(dfA["datetime"].max().date(), dfB["datetime"].max().date())
            if min_d > max_d:
                # No overlap
                out[8]  = None
                out[9]  = None
                out[10] = None
                out[11] = None
                out[12] = []
                out[13] = None
                out[14] = None
                return tuple(out)
        elif dfA is not None:
            min_d = dfA["datetime"].min().date()
            max_d = dfA["datetime"].max().date()
        else:
            min_d = dfB["datetime"].min().date()
            max_d = dfB["datetime"].max().date()
    
        years = list(range(min_d.year, max_d.year + 1))
        year_options = [{"label": str(y), "value": y} for y in years]
    
        out[8]  = min_d
        out[9]  = max_d
        out[10] = min_d
        out[11] = max_d
        out[12] = year_options
        out[13] = min_d.year
        out[14] = 1
        return tuple(out)
    
    # Preset → custom when dates edited (CROSS page)
    @app.callback(Output("preset-cross", "value"),
                  Input("date-range-cross", "start_date"),
                  Input("date-range-cross", "end_date"),
                  prevent_initial_call=True)
    def force_custom_cross(_s, _e):
        return "custom"
    
    # Jump-to initial_visible_month (CROSS page)
    @app.callback(
        Output("date-range-cross", "initial_visible_month"),
        Input("jump-year-cross", "value"),
        Input("jump-month-cross", "value"),
        State("date-range-cross", "initial_visible_month"),
        prevent_initial_call=True
    )
    def jump_cross(year, month, _cur):
        if year and month:
            return pd.Timestamp(int(year), int(month), 1)
        return no_update
    
    # -----------------------------
    # Analyze callback (CROSS page)
    # -----------------------------
    @app.callback(
        Output("x-line-levels-container", "children"),
        Output("x-scatter-returns-container", "children"),
        Output("x-line-returns-container", "children"),
        Output("x-stats", "children"),
        Output("x-trade-windows-container", "children"),
        Output("x-results-container", "style"),
        Input("x-analyze", "n_clicks"),
        State(STORE_A, "data"),
        State(STORE_B, "data"),
        State("preset-cross", "value"),
        State("date-range-cross", "start_date"),
        State("date-range-cross", "end_date"),
        State("snap-month-cross", "value"),
        State("x-window", "value"),
        prevent_initial_call=True,
    )
    def run_cross(n_clicks, rawA, rawB, preset, sd, ed, snap_val, win):
        if not n_clicks:
            return (no_update,) * 6
        if not rawA or not rawB:
            # Hide all results when no data
            hidden_style = {"display": "none"}
            return None, None, None, None, None, hidden_style
    
        # Load A & B
        try:
            dfA = pd.read_csv(io.BytesIO(base64.b64decode(rawA["csv_b64"].encode())))
            dfB = pd.read_csv(io.BytesIO(base64.b64decode(rawB["csv_b64"].encode())))
        except Exception as e:
            # Hide all results on error
            hidden_style = {"display": "none"}
            return None, None, None, None, None, hidden_style
    
        for df in (dfA, dfB):
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
            df["index"] = pd.to_numeric(df["index"], errors="coerce")
        dfA = dfA.dropna(subset=["datetime","index"]).sort_values("datetime").reset_index(drop=True)
        dfB = dfB.dropna(subset=["datetime","index"]).sort_values("datetime").reset_index(drop=True)
    
        # Determine overall range intersection
        data_min = max(dfA["datetime"].min(), dfB["datetime"].min())
        data_max = min(dfA["datetime"].max(), dfB["datetime"].max())
        if data_min >= data_max:
            # Hide all results when no overlap
            hidden_style = {"display": "none"}
            return None, None, None, None, None, hidden_style
    
        snap = ("snap" in (snap_val or []))
        start, end = compute_range(preset, sd, ed, data_min, data_max, snap)
    
        # Slice to range and inner-join on dates for level chart
        A_in = dfA[(dfA["datetime"]>=start) & (dfA["datetime"]<=end)][["datetime","index"]].rename(columns={"index":"A"})
        B_in = dfB[(dfB["datetime"]>=start) & (dfB["datetime"]<=end)][["datetime","index"]].rename(columns={"index":"B"})
        levels = pd.merge(A_in, B_in, on="datetime", how="inner")
        if levels.empty:
            # Hide all results when no data in range
            hidden_style = {"display": "none"}
            return None, None, None, None, None, hidden_style
    
        # -------- Chart 1: Dual Y-Axis - Index A (left) vs Index B (right) --------
        fig_levels = go.Figure()
        
        # Index A on left y-axis (primary)
        fig_levels.add_trace(go.Scatter(
            x=levels["datetime"], 
            y=levels["A"], 
            mode="lines", 
            name="Index A",
            line=dict(color="#00c896", width=2),
            yaxis="y"
        ))
        
        # Index B on right y-axis (secondary)
        fig_levels.add_trace(go.Scatter(
            x=levels["datetime"], 
            y=levels["B"], 
            mode="lines", 
            name="Index B",
            line=dict(color="#888888", width=1.5),
            yaxis="y2"
        ))
        
        fig_levels.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(26,26,26,0.8)",
            paper_bgcolor="rgba(10,10,10,0.8)",
            font=dict(color="rgba(255,255,255,0.9)"),
            title=f"Both Indexes (Dual Axis) · {start.date()} → {end.date()}",
            margin=dict(t=100, r=80, l=80, b=40),  # Increased margins for dual axes
            xaxis_title="Date",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.01,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(10,10,10,0.9)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
                itemwidth=30,
                font=dict(size=10)
            ),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(
                title=dict(text="Index A", font=dict(color="#00c896")),
                tickfont=dict(color="#00c896"),
                gridcolor="rgba(255,255,255,0.1)",
                side="left"
            ),
            yaxis2=dict(
                title=dict(text="Index B", font=dict(color="#888888")),
                tickfont=dict(color="#888888"),
                anchor="x",
                overlaying="y",
                side="right",
                showgrid=False
            )
        )
    
        # -------- Weekend-aware returns (window size in calendar days) --------
        win = max(int(win or 1), 1)
        retA_series = compute_windowed_returns_calendar(dfA, win)
        retB_series = compute_windowed_returns_calendar(dfB, win)
    
        tmpA = dfA.assign(retA=retA_series)
        tmpB = dfB.assign(retB=retB_series)
        tmpA = tmpA[(tmpA["datetime"]>=start) & (tmpA["datetime"]<=end)]
        tmpB = tmpB[(tmpB["datetime"]>=start) & (tmpB["datetime"]<=end)]
    
        rets = pd.merge(
            tmpA[["datetime","retA"]],
            tmpB[["datetime","retB"]],
            on="datetime",
            how="inner"
        ).dropna(subset=["retA","retB"])
    
        if rets.empty:
            # Hide all results when no returns data
            hidden_style = {"display": "none"}
            return None, None, None, None, None, hidden_style
    
        # -------- Chart 2: Correlation scatter (windowed returns) --------
        # Use standardized returns (z-scores) for better visualization when scales differ vastly
        # This preserves the Pearson correlation exactly while making the scatter interpretable
        x_raw = rets["retB"].values * 100.0
        y_raw = rets["retA"].values * 100.0
        
        if len(x_raw) >= 2:
            corr = float(np.corrcoef(x_raw, y_raw)[0,1])
            # Standardize to z-scores: (x - mean) / std
            x_mean, x_std = np.mean(x_raw), np.std(x_raw)
            y_mean, y_std = np.mean(y_raw), np.std(y_raw)
            # Avoid division by zero
            x_std = x_std if x_std > 0 else 1
            y_std = y_std if y_std > 0 else 1
            x = (x_raw - x_mean) / x_std
            y = (y_raw - y_mean) / y_std
        else:
            corr = float("nan")
            x, y = x_raw, y_raw
    
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(
            x=x, y=y, mode="markers", name=f"{win}-day returns",
            hovertemplate="B (z): %{x:.2f}<br>A (z): %{y:.2f}<extra></extra>"
        ))
        if len(x) >= 2:
            m, b = np.polyfit(x, y, 1)
            xfit = np.linspace(x.min(), x.max(), 100)
            yfit = m*xfit + b
            fig_scatter.add_trace(go.Scatter(x=xfit, y=yfit, mode="lines", name="Fit", line=dict(dash="dash")))
            # For standardized data, slope ≈ correlation (when both are z-scores)
            subtitle = f"Pearson corr = {corr:.2f} · β (standardized) ≈ {m:.2f}"
        else:
            subtitle = "Pearson corr = n/a"
        fig_scatter.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(26,26,26,0.8)",
            paper_bgcolor="rgba(10,10,10,0.8)",
            font=dict(color="rgba(255,255,255,0.9)"),
            title=dict(
                text=f"Correlation (standardized returns) — {subtitle}",
                x=0.5,
                xanchor="center",
                y=0.98,
                yanchor="top"
            ),
            margin=dict(t=100, r=10, l=50, b=50),  # Increased top margin for legend
            xaxis_title=f"Index B {win}-day return (z-score)",
            yaxis_title=f"Index A {win}-day return (z-score)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.01,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(10,10,10,0.9)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
                itemwidth=30,
                font=dict(size=10)
            ),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
        )
    
        # -------- Chart 3: Windowed returns through time (Dual Y-Axis) --------
        ret_time = rets.reset_index(drop=True)
        fig_returns = go.Figure()
        
        # Index A returns on left y-axis (primary)
        fig_returns.add_trace(go.Scatter(
            x=ret_time["datetime"], 
            y=ret_time["retA"]*100.0, 
            mode="lines", 
            name=f"A {win}-day %",
            line=dict(color="#00c896", width=2),
            yaxis="y"
        ))
        
        # Index B returns on right y-axis (secondary)
        fig_returns.add_trace(go.Scatter(
            x=ret_time["datetime"], 
            y=ret_time["retB"]*100.0, 
            mode="lines", 
            name=f"B {win}-day %",
            line=dict(color="#888888", width=1.5),
            yaxis="y2"
        ))
        
        fig_returns.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(26,26,26,0.8)",
            paper_bgcolor="rgba(10,10,10,0.8)",
            font=dict(color="rgba(255,255,255,0.9)"),
            title=f"{win}-day Returns Over Time (Dual Axis) · {start.date()} → {end.date()}",
            margin=dict(t=100, r=80, l=80, b=40),  # Increased margins for dual axes
            xaxis_title="Date",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.01,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(10,10,10,0.9)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
                itemwidth=30,
                font=dict(size=10)
            ),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(
                title=dict(text=f"Index A {win}-day return (%)", font=dict(color="#00c896")),
                tickfont=dict(color="#00c896"),
                gridcolor="rgba(255,255,255,0.1)",
                side="left"
            ),
            yaxis2=dict(
                title=dict(text=f"Index B {win}-day return (%)", font=dict(color="#888888")),
                tickfont=dict(color="#888888"),
                anchor="x",
                overlaying="y",
                side="right",
                showgrid=False
            )
        )
    
        # -------- Stats card --------
        def stats_block(name, s):
            desc = s.describe()
            items = [
                ("Data points", f"{int(desc['count'])}"),
                ("Average %",   f"{desc['mean']*100:.2f}%"),
                ("Std dev %",   f"{desc['std']*100:.2f}%"),
                ("Min %",       f"{desc['min']*100:.2f}%"),
                ("25% %",       f"{desc['25%']*100:.2f}%"),
                ("Median %",    f"{desc['50%']*100:.2f}%"),
                ("75% %",       f"{desc['75%']*100:.2f}%"),
                ("Max %",       f"{desc['max']*100:.2f}%"),
            ]
            return html.Div([
                html.H4(name, style={"margin":"0 0 16px 0", "fontSize":"18px", "fontWeight":600, "color":"inherit"}),
                html.Ul([html.Li(html.Span([html.Strong(k + ": ", style={"color":"inherit"}), v]), style={
                    "marginBottom":"8px", "fontSize":"14px", "color":"inherit", "opacity":0.9
                }) for k, v in items], style={"listStyle":"none", "padding":0})
            ], style={"flex":1, "background":"rgba(255,255,255,0.05)","border":"1px solid rgba(255,255,255,0.1)",
                      "borderRadius":"16px","padding":"24px", "boxShadow":"0 4px 12px rgba(0,0,0,0.3)"})
    
        corr_text = html.Div([
            html.H4("Relationship", style={"margin":"0 0 12px 0", "fontSize":"18px", "fontWeight":600, "color":"inherit"}),
            html.P(f"Pearson correlation (windowed returns): {corr:.2f}" if np.isfinite(corr) else
                   "Pearson correlation (windowed returns): n/a", style={
                       "fontSize":"16px", "color":"inherit", "opacity":0.9, "margin":0,
                       "fontWeight":500 if np.isfinite(corr) else 400
                   })
        ], style={"flex":1, "background":"rgba(0,200,150,0.08)","border":"1px solid rgba(0,200,150,0.3)",
                  "borderRadius":"16px","padding":"24px", "boxShadow":"0 4px 12px rgba(0,0,0,0.3)"})
    
        stats_view = html.Div([
            html.Div([
                stats_block("Index A — Stats", rets["retA"]),
                stats_block("Index B — Stats", rets["retB"]),
                corr_text
            ], style={"display":"flex","gap":"12px","flexWrap":"wrap"})
        ])
    
        twin = html.Div()  # Empty placeholder
        
        # Wrap graphs in containers
        levels_container = html.Div([
            dcc.Graph(figure=fig_levels, config={"displayModeBar": False}, style={"height":"360px"})
        ], style={
            "background":"rgba(255,255,255,0.05)", "borderRadius":"16px",
            "padding":"20px", "marginBottom":"24px",
            "boxShadow":"0 4px 12px rgba(0,0,0,0.3)",
            "border":"1px solid rgba(255,255,255,0.1)"
        })
        
        scatter_container = html.Div([
            dcc.Graph(figure=fig_scatter, config={"displayModeBar": False}, style={"height":"360px"})
        ], style={
            "background":"rgba(255,255,255,0.05)", "borderRadius":"16px",
            "padding":"20px", "marginBottom":"24px",
            "boxShadow":"0 4px 12px rgba(0,0,0,0.3)",
            "border":"1px solid rgba(255,255,255,0.1)"
        })
        
        returns_container = html.Div([
            dcc.Graph(figure=fig_returns, config={"displayModeBar": False}, style={"height":"360px"})
        ], style={
            "background":"rgba(255,255,255,0.05)", "borderRadius":"16px",
            "padding":"20px", "marginBottom":"24px",
            "boxShadow":"0 4px 12px rgba(0,0,0,0.3)",
            "border":"1px solid rgba(255,255,255,0.1)"
        })
        
        # Show results container
        results_style = {"marginTop": "32px"}
    
        return levels_container, scatter_container, returns_container, stats_view, twin, results_style
    
    
    # -----------------------------
    # Drawdown Custom Input Toggle
    # -----------------------------
    @app.callback(
        Output("drawdown-custom-input", "disabled"),
        Input("drawdown-filter", "value")
    )
    def toggle_custom_input(filter_value):
        return filter_value != -1
    
    # -----------------------------
    # Drawdown Recovery Analysis Callback
    # -----------------------------
    @app.callback(
        Output("drawdown-results-container", "children"),
        Input("drawdown-analyze-btn", "n_clicks"),
        State(STORE_RAW, "data"),
        State("drawdown-filter", "value"),
        State("drawdown-custom-input", "value"),
        prevent_initial_call=True
    )
    def analyze_drawdowns(n_clicks, stored_data, min_drawdown_pct, custom_value):
        if not stored_data or n_clicks == 0:
            return html.Div()
        
        try:
            # Check if stored_data is the metadata format (with csv_b64)
            if isinstance(stored_data, dict) and "csv_b64" in stored_data:
                # Decode base64 CSV data
                csv_bytes = base64.b64decode(stored_data["csv_b64"])
                df = pd.read_csv(io.BytesIO(csv_bytes))
            else:
                # Try as direct DataFrame
                df = pd.DataFrame(stored_data)
            
            if df.empty:
                return html.Div("No data available", style={"color":"rgba(255,255,255,0.7)"})
            
            # Auto-detect date and numeric columns
            date_col = None
            numeric_col = None
            
            # Find date column
            for col in df.columns:
                try:
                    pd.to_datetime(df[col], errors='coerce')
                    if pd.to_datetime(df[col], errors='coerce').notna().sum() > len(df) * 0.5:
                        date_col = col
                        break
                except:
                    continue
            
            # Find numeric column (excluding the date column)
            for col in df.columns:
                if col != date_col:
                    try:
                        pd.to_numeric(df[col], errors='coerce')
                        if pd.to_numeric(df[col], errors='coerce').notna().sum() > len(df) * 0.5:
                            numeric_col = col
                            break
                    except:
                        continue
            
            if not date_col or not numeric_col:
                available_cols = ", ".join(df.columns.tolist())
                return html.Div([
                    html.P("Could not automatically detect date and numeric columns in the data.", 
                          style={"marginBottom":"8px"}),
                    html.P(f"Available columns: {available_cols}", 
                          style={"fontSize":"13px", "opacity":"0.8"})
                ], style={"color":"#ef4444", "padding":"20px"})
            
            # Compute drawdown episodes
            events_df, annotated = compute_drawdown_recovery(df, date_col, numeric_col)
            
            if events_df.empty:
                return html.Div("No drawdown episodes found in the data", 
                              style={"color":"rgba(255,255,255,0.7)", "padding":"20px"})
            
            # Determine the actual filter value to use
            if min_drawdown_pct == -1:  # Custom option selected
                if custom_value is not None and custom_value >= 0:
                    filter_threshold = custom_value
                else:
                    return html.Div("Please enter a valid custom drawdown percentage (≥0)", 
                                  style={"color":"#ef4444", "padding":"20px"})
            else:
                filter_threshold = min_drawdown_pct
            
            # Filter by minimum drawdown percentage
            # drawdown_pct is negative, so we use abs
            if filter_threshold > 0:
                events_df = events_df[events_df["drawdown_pct"].abs() * 100 >= filter_threshold]
            
            if events_df.empty:
                return html.Div(f"No drawdowns found with magnitude ≥{filter_threshold}%", 
                              style={"color":"rgba(255,255,255,0.7)", "padding":"20px"})
            
            # Format the data for display
            display_df = events_df.copy()
            display_df["peak_date"] = pd.to_datetime(display_df["peak_date"]).dt.strftime("%Y-%m-%d")
            display_df["trough_date"] = pd.to_datetime(display_df["trough_date"]).dt.strftime("%Y-%m-%d")
            display_df["recovery_date"] = pd.to_datetime(display_df["recovery_date"]).dt.strftime("%Y-%m-%d")
            display_df["drawdown_pct"] = (display_df["drawdown_pct"] * 100).round(2)
            display_df = display_df.rename(columns={
                "peak_date": "Peak Date",
                "peak_value": "Peak Value",
                "trough_date": "Trough Date",
                "trough_value": "Trough Value",
                "recovery_date": "Recovery Date",
                "recovery_value": "Recovery Value",
                "drawdown_pct": "Drawdown %",
                "days_to_trough": "Days to Trough",
                "days_to_recovery": "Days to Recovery"
            })
            
            # Store for download
            dcc.Store(id="drawdown-data-store", data=display_df.to_dict("records"))
            
            # Summary statistics
            total_episodes = len(display_df)
            avg_drawdown = display_df["Drawdown %"].mean()
            max_drawdown = display_df["Drawdown %"].min()
            avg_recovery = display_df["Days to Recovery"].dropna().mean()
            
            # Info banner showing detected columns
            info_banner = html.Div([
                html.Span("✓ ", style={"marginRight":"6px", "fontSize":"16px"}),
                html.Span(f"Analyzed using: ", style={"fontWeight":"500"}),
                html.Span(f"Date column: '{date_col}' | Value column: '{numeric_col}'", 
                         style={"opacity":"0.8"})
            ], style={
                "padding":"12px 16px", "background":"rgba(0,200,150,0.1)", 
                "borderRadius":"8px", "border":"1px solid rgba(0,200,150,0.3)",
                "fontSize":"14px", "color":"rgba(255,255,255,0.9)", "marginBottom":"24px"
            })
            
            summary = html.Div([
                html.H4("📊 Summary Statistics", style={
                    "fontSize":"18px", "fontWeight":600, "color":"rgba(255,255,255,0.95)",
                    "marginBottom":"16px"
                }),
                html.Div([
                    html.Div([
                        html.Div("Total Episodes", style={"fontSize":"13px", "color":"rgba(255,255,255,0.6)", "marginBottom":"4px"}),
                        html.Div(str(total_episodes), style={"fontSize":"24px", "fontWeight":700, "color":"#ef4444"})
                    ], style={"flex":"1", "padding":"16px", "background":"rgba(239,68,68,0.1)", 
                             "borderRadius":"12px", "border":"1px solid rgba(239,68,68,0.2)"}),
                    
                    html.Div([
                        html.Div("Avg Drawdown", style={"fontSize":"13px", "color":"rgba(255,255,255,0.6)", "marginBottom":"4px"}),
                        html.Div(f"{avg_drawdown:.2f}%", style={"fontSize":"24px", "fontWeight":700, "color":"#f97316"})
                    ], style={"flex":"1", "padding":"16px", "background":"rgba(249,115,22,0.1)", 
                             "borderRadius":"12px", "border":"1px solid rgba(249,115,22,0.2)"}),
                    
                    html.Div([
                        html.Div("Max Drawdown", style={"fontSize":"13px", "color":"rgba(255,255,255,0.6)", "marginBottom":"4px"}),
                        html.Div(f"{max_drawdown:.2f}%", style={"fontSize":"24px", "fontWeight":700, "color":"#dc2626"})
                    ], style={"flex":"1", "padding":"16px", "background":"rgba(220,38,38,0.1)", 
                             "borderRadius":"12px", "border":"1px solid rgba(220,38,38,0.2)"}),
                    
                    html.Div([
                        html.Div("Avg Recovery Days", style={"fontSize":"13px", "color":"rgba(255,255,255,0.6)", "marginBottom":"4px"}),
                        html.Div(f"{avg_recovery:.0f}" if not pd.isna(avg_recovery) else "N/A", 
                               style={"fontSize":"24px", "fontWeight":700, "color":"#3b82f6"})
                    ], style={"flex":"1", "padding":"16px", "background":"rgba(59,130,246,0.1)", 
                             "borderRadius":"12px", "border":"1px solid rgba(59,130,246,0.2)"}),
                ], style={"display":"flex", "gap":"12px", "flexWrap":"wrap", "marginBottom":"32px"})
            ])
            
            # DataTable with better column widths
            table = dash_table.DataTable(
                data=display_df.to_dict("records"),
                columns=[{"name": c, "id": c} for c in display_df.columns],
                page_size=10,
                page_action="native",
                page_current=0,
                sort_action="native",
                style_table={
                    "overflowX": "auto",
                    "backgroundColor": "#1a1a1a",
                    "borderRadius": "12px",
                    "overflow": "hidden",
                    "minWidth": "100%"
                },
                style_cell={
                    "textAlign": "left",
                    "padding": "12px 16px",
                    "backgroundColor": "#1a1a1a",
                    "color": "rgba(255,255,255,0.9)",
                    "border": "1px solid rgba(255,255,255,0.1)",
                    "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
                    "fontSize": "14px",
                    "minWidth": "100px",
                    "maxWidth": "180px",
                    "whiteSpace": "normal"
                },
                style_cell_conditional=[
                    {"if": {"column_id": "Peak Date"}, "minWidth": "120px", "maxWidth": "140px"},
                    {"if": {"column_id": "Peak Value"}, "minWidth": "110px", "maxWidth": "130px"},
                    {"if": {"column_id": "Trough Date"}, "minWidth": "120px", "maxWidth": "140px"},
                    {"if": {"column_id": "Trough Value"}, "minWidth": "110px", "maxWidth": "130px"},
                    {"if": {"column_id": "Recovery Date"}, "minWidth": "120px", "maxWidth": "140px"},
                    {"if": {"column_id": "Recovery Value"}, "minWidth": "110px", "maxWidth": "130px"},
                    {"if": {"column_id": "Drawdown %"}, "minWidth": "120px", "maxWidth": "140px"},
                    {"if": {"column_id": "Days to Trough"}, "minWidth": "130px", "maxWidth": "150px"},
                    {"if": {"column_id": "Days to Recovery"}, "minWidth": "140px", "maxWidth": "160px"},
                ],
                style_header={
                    "backgroundColor": "#252525",
                    "color": "rgba(255,255,255,0.95)",
                    "fontWeight": "600",
                    "border": "1px solid rgba(255,255,255,0.2)",
                    "textAlign": "left",
                    "padding": "14px 16px"
                },
                style_data={
                    "backgroundColor": "#1a1a1a",
                    "color": "rgba(255,255,255,0.9)",
                    "border": "1px solid rgba(255,255,255,0.1)"
                },
                style_data_conditional=[
                    {
                        "if": {"row_index": "even"},
                        "backgroundColor": "#222222",
                    },
                    {
                        "if": {"state": "selected"},
                        "backgroundColor": "rgba(239,68,68,0.2)",
                        "border": "1px solid rgba(239,68,68,0.5)"
                    },
                    {
                        "if": {"column_id": "Drawdown %"},
                        "color": "#ef4444",
                        "fontWeight": "600"
                    },
                    {
                        "if": {"column_id": "Days to Recovery"},
                        "color": "#3b82f6",
                        "fontWeight": "500"
                    }
                ],
            )
            
            # Create drawdown visualization graph with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add price line (primary y-axis) - no markers
            fig.add_trace(go.Scatter(
                x=annotated[date_col],
                y=annotated[numeric_col],
                mode='lines',
                name='Price',
                line=dict(color='#667eea', width=2),
                marker=dict(size=0),  # Explicitly no markers
                hovertemplate='<b>Price:</b> %{y:.2f}<extra></extra>'
            ), secondary_y=False)
            
            # Add cumulative max line (peaks) - primary y-axis
            fig.add_trace(go.Scatter(
                x=annotated[date_col],
                y=annotated['cum_max'],
                mode='lines',
                name='Peak Level',
                line=dict(color='#00c896', width=1, dash='dash'),
                marker=dict(size=0),  # Explicitly no markers
                hovertemplate='<b>Peak:</b> %{y:.2f}<extra></extra>'
            ), secondary_y=False)
            
            # Add drawdown percentage line (secondary y-axis) - ONLY for filtered episodes
            # Create a masked version that only shows drawdowns meeting the threshold
            drawdown_pct_display = annotated['drawdown_pct'] * 100  # Convert to percentage
            # Mask: only show drawdown when it meets or exceeds the threshold
            drawdown_display_masked = drawdown_pct_display.copy()
            drawdown_display_masked[drawdown_pct_display.abs() < filter_threshold] = 0  # Set small drawdowns to 0
            
            fig.add_trace(go.Scatter(
                x=annotated[date_col],
                y=drawdown_display_masked,
                mode='lines',
                name='Drawdown %',
                line=dict(color='#ef4444', width=2, dash='dot'),
                fill='tozeroy',
                fillcolor='rgba(239,68,68,0.15)',
                marker=dict(size=0),  # Explicitly no markers
                hovertemplate='<b>Drawdown:</b> %{y:.2f}%<extra></extra>'
            ), secondary_y=True)
            
            # Add shaded regions for each filtered drawdown episode (primary y-axis)
            for _, episode in events_df.iterrows():
                # Get the data for this episode
                episode_mask = (annotated[date_col] >= pd.to_datetime(episode['peak_date'])) & \
                              (annotated[date_col] <= pd.to_datetime(episode['recovery_date'] if pd.notna(episode['recovery_date']) else annotated[date_col].max()))
                episode_data = annotated[episode_mask]
                
                if not episode_data.empty:
                    # Add shaded region
                    fig.add_trace(go.Scatter(
                        x=episode_data[date_col],
                        y=episode_data[numeric_col],
                        fill='tonexty',
                        fillcolor='rgba(239,68,68,0.25)',
                        line=dict(width=0),
                        showlegend=False,
                        hoverinfo='skip'
                    ), secondary_y=False)
            
            # Update layout
            fig.update_layout(
                title={
                    'text': f'📈 Price History with Drawdown Episodes (≥{filter_threshold}%)',
                    'font': {'size': 18, 'color': 'rgba(255,255,255,0.95)', 'family': 'system-ui'},
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis=dict(
                    title='Date',
                    gridcolor='rgba(255,255,255,0.1)',
                    color='rgba(255,255,255,0.9)',
                    showgrid=True
                ),
                plot_bgcolor='#1a1a1a',
                paper_bgcolor='#1a1a1a',
                font=dict(color='rgba(255,255,255,0.9)', family='system-ui'),
                hovermode='x unified',
                legend=dict(
                    bgcolor='rgba(37,37,37,0.9)',
                    bordercolor='rgba(255,255,255,0.2)',
                    borderwidth=1,
                    font=dict(size=12),
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='center',
                    x=0.5
                ),
                height=550,
                margin=dict(l=60, r=80, t=80, b=60)
            )
            
            # Set y-axes titles
            fig.update_yaxes(
                title_text=numeric_col.title(),
                gridcolor='rgba(255,255,255,0.1)',
                color='rgba(255,255,255,0.9)',
                showgrid=True,
                secondary_y=False
            )
            
            fig.update_yaxes(
                title_text="Drawdown %",
                gridcolor='rgba(239,68,68,0.1)',
                color='#ef4444',
                showgrid=False,
                zeroline=True,
                zerolinecolor='rgba(255,255,255,0.3)',
                zerolinewidth=1,
                secondary_y=True
            )
            
            graph_component = dcc.Graph(
                figure=fig,
                config={'displayModeBar': True, 'displaylogo': False},
                style={"borderRadius": "12px", "overflow": "hidden", "marginBottom": "32px"}
            )
            
            return html.Div([
                info_banner,
                summary,
                html.Div([
                    html.H4("📋 Drawdown Episodes Table", style={
                        "fontSize":"18px", "fontWeight":600, "color":"rgba(255,255,255,0.95)",
                        "marginBottom":"16px", "marginTop":"24px"
                    }),
                    html.P(f"Showing {len(display_df)} episode(s) with drawdown ≥{filter_threshold}%", style={
                        "fontSize":"14px", "color":"rgba(255,255,255,0.6)", "marginBottom":"16px"
                    }),
                    table,
                    # Store data for download
                    dcc.Store(id="drawdown-data-store", data=display_df.to_dict("records"))
                ])
            ])
            
        except Exception as e:
            return html.Div(f"Error analyzing drawdowns: {str(e)}", 
                           style={"color":"#ef4444", "padding":"20px"})
    
    
    # Drawdown Download Callback
    @app.callback(
        Output("drawdown-download", "data"),
        Input("drawdown-download-btn", "n_clicks"),
        State("drawdown-data-store", "data"),
        prevent_initial_call=True
    )
    def download_drawdowns(n_clicks, stored_data):
        if not stored_data or n_clicks == 0:
            return no_update
        
        df = pd.DataFrame(stored_data)
        return dcc.send_data_frame(df.to_csv, "drawdown_recoveries.csv", index=False)
    
    
    # Local run (useful for dev & Render health checks)
