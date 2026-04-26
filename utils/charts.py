"""
Plotly Chart Builders — all charts for the results dashboard.
"""
import plotly.graph_objects as go
import config


def radar_chart(skills, required, claimed, assessed) -> go.Figure:
    """Radar: required vs claimed vs assessed."""
    cats = skills + [skills[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=required + [required[0]], theta=cats,
        fill="toself", name="Required",
        line=dict(color=config.COLOR_REQUIRED, width=2),
        fillcolor="rgba(99,102,241,0.1)"
    ))
    fig.add_trace(go.Scatterpolar(
        r=claimed + [claimed[0]], theta=cats,
        fill="toself", name="Claimed",
        line=dict(color=config.COLOR_CLAIMED, width=2),
        fillcolor="rgba(16,185,129,0.1)"
    ))
    fig.add_trace(go.Scatterpolar(
        r=assessed + [assessed[0]], theta=cats,
        fill="toself", name="Assessed",
        line=dict(color=config.COLOR_ASSESSED, width=2),
        fillcolor="rgba(245,158,11,0.15)"
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1],
                            gridcolor="#1E1E35", color="#94A3B8"),
            angularaxis=dict(gridcolor="#1E1E35"),
            bgcolor="#12121E",
        ),
        paper_bgcolor="#0A0A0F",
        plot_bgcolor="#0A0A0F",
        font=dict(color="#E2E8F0"),
        legend=dict(bgcolor="#12121E", bordercolor="#1E1E35"),
        showlegend=True,
        height=420,
        margin=dict(t=40, b=40),
    )
    return fig


def gap_bar(skills, gaps) -> go.Figure:
    """Horizontal bar: skill gap (positive = needs work)."""
    colors = [config.COLOR_GAP if g > 0 else config.COLOR_CLAIMED for g in gaps]
    labels = [f"{g:+.0%}" for g in gaps]

    fig = go.Figure(go.Bar(
        x=gaps, y=skills, orientation="h",
        marker_color=colors,
        text=labels, textposition="auto",
        textfont=dict(color="#E2E8F0"),
    ))
    fig.update_layout(
        title=dict(text="Skill Gap (Required − Assessed)", font=dict(color="#E2E8F0")),
        xaxis=dict(title="Gap", gridcolor="#1E1E35", color="#94A3B8"),
        yaxis=dict(gridcolor="#1E1E35", color="#E2E8F0"),
        paper_bgcolor="#0A0A0F",
        plot_bgcolor="#12121E",
        font=dict(color="#E2E8F0"),
        height=max(300, len(skills) * 55),
        margin=dict(t=50, b=30, l=10, r=10),
    )
    return fig


def claimed_vs_assessed(skills, claimed, assessed) -> go.Figure:
    """Grouped bar: claim accuracy per skill."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Claimed (Resume)", x=skills, y=claimed,
        marker_color=config.COLOR_CLAIMED,
        text=[f"{v:.0%}" for v in claimed],
        textposition="auto",
    ))
    fig.add_trace(go.Bar(
        name="Assessed (Verified)", x=skills, y=assessed,
        marker_color=config.COLOR_ASSESSED,
        text=[f"{v:.0%}" for v in assessed],
        textposition="auto",
    ))
    fig.update_layout(
        barmode="group",
        title=dict(text="Claim Accuracy: Resume vs Reality", font=dict(color="#E2E8F0")),
        yaxis=dict(range=[0, 1], title="Proficiency", gridcolor="#1E1E35", color="#94A3B8"),
        xaxis=dict(gridcolor="#1E1E35", color="#E2E8F0"),
        paper_bgcolor="#0A0A0F",
        plot_bgcolor="#12121E",
        font=dict(color="#E2E8F0"),
        legend=dict(bgcolor="#12121E", bordercolor="#1E1E35"),
        height=380,
        margin=dict(t=50, b=30),
    )
    return fig


def readiness_gauge(score: float) -> go.Figure:
    """Gauge chart for overall readiness."""
    pct = round(score * 100, 1)
    if score >= 0.75:
        bar_color = config.COLOR_CLAIMED
    elif score >= 0.50:
        bar_color = "#F59E0B"
    else:
        bar_color = config.COLOR_GAP

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={"suffix": "%", "font": {"size": 48, "color": bar_color}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#94A3B8",
                     "tickfont": {"color": "#94A3B8"}},
            "bar": {"color": bar_color, "thickness": 0.25},
            "bgcolor": "#12121E",
            "bordercolor": "#1E1E35",
            "steps": [
                {"range": [0,  40], "color": "rgba(239,68,68,0.15)"},
                {"range": [40, 70], "color": "rgba(245,158,11,0.15)"},
                {"range": [70, 100], "color": "rgba(16,185,129,0.15)"},
            ],
            "threshold": {
                "line": {"color": "#6366F1", "width": 3},
                "thickness": 0.75,
                "value": 70,
            },
        },
    ))
    fig.update_layout(
        paper_bgcolor="#0A0A0F",
        font=dict(color="#E2E8F0"),
        height=280,
        margin=dict(t=20, b=20, l=30, r=30),
    )
    return fig