
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="CO2 Dashboard", page_icon="🌱", layout="wide")

# ── Data ──────────────────────────────────────────────────────────────────────
# @st.cache_data: Streamlit reruns the entire script on every widget interaction.
# Without caching, the CSV is read from disk on every interaction — slow and wasteful.
# cache_data stores the result after the first run and reuses it until the file changes.
@st.cache_data
def load_data():
    path = Path(__file__).parent.parent / 'data' / 'co2_emissions.csv'
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-01-01')
    return df

df = load_data()

st.title("🌱 CO2 Emissions Explorer")
st.caption("Source: Our World in Data — ourworldindata.org/co2-emissions")

# ── TASK 1: Sidebar with 5 widgets ────────────────────────────────────────────
#   a) st.selectbox for Region (with 'All')
#   b) st.multiselect for Countries (updates based on region — chained)
#   c) st.date_input for date range (two-handle; convert years to Jan-1 dates)
#   d) st.radio for Metric: "Total CO2 (Mt)" vs "CO2 per capita"
#   e) st.checkbox labelled "Show only top emitter highlighted"
#
# Guards:
#   - empty countries → st.warning + st.stop()
#   - incomplete date_input → st.warning + st.stop()
# Convert date_input result to pd.Timestamp before filtering.
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    
    regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
    selected_region = st.selectbox("Region", options=regions)
    
    if selected_region == "All":
        country_options = sorted(df["Country"].unique().tolist())
    else:
        country_options = sorted(df[df["Region"] == selected_region]["Country"].unique().tolist())
        
    selected_countries = st.multiselect("Countries", options=country_options, default=country_options)
    
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    
    date_range = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    
    metric_map = {
        "Total CO2 (Mt)": "CO2_Mt",
        "CO2 per capita": "CO2_per_capita"
    }
    selected_metric_label = st.radio("Metric", options=list(metric_map.keys()))
    selected_metric = metric_map[selected_metric_label]
    
    highlight_top = st.checkbox("Show only top emitter highlighted")

if not selected_countries:
    st.warning("Please select at least one country.")
    st.stop()

if len(date_range) != 2:
    st.warning("Please select a complete date range.")
    st.stop()

start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

filtered = df[
    (df['Country'].isin(selected_countries)) &
    (df['Date'] >= start_date) &
    (df['Date'] <= end_date)
]


# ── TASK 2: Filter summary caption ────────────────────────────────────────────
# Show: "X countries | Region | Date range | Metric"
# BBD rule: always show users how many records match current filters
# ─────────────────────────────────────────────────────────────────────────────
st.caption(f"{len(selected_countries)} countries | {selected_region} | {start_date.year} - {end_date.year} | {selected_metric_label}")


# ── TASK 3: Two charts reacting to ALL filters ────────────────────────────────
#   Left: line chart — selected metric over time, one line per country
#         If "Show only top emitter highlighted" checkbox is on:
#           - grey all lines except the highest emitter in the date range
#           - label that country at the end of its line (SWD grey-and-highlight)
#   Right: bar chart — ranking for the last year in selected date range
#
# BBD colour requirement: name the colour type in a comment next to each chart
# SWD requirements: white background, insight title, use_container_width=True
# ─────────────────────────────────────────────────────────────────────────────
# ── EXTENSION: KPI row above the charts ───────────────────────────────────────
if not filtered.empty:
    first_year_data = filtered[filtered['Date'] == filtered['Date'].min()]
    last_year_data = filtered[filtered['Date'] == filtered['Date'].max()]
    
    total_last = last_year_data['CO2_Mt'].sum()
    total_first = first_year_data['CO2_Mt'].sum()
    pct_change = ((total_last - total_first) / total_first * 100) if total_first else 0
    
    if not last_year_data.empty:
        top_country = last_year_data.loc[last_year_data['CO2_Mt'].idxmax()]['Country']
    else:
        top_country = "N/A"
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total CO2 (Mt) in last year", f"{total_last:,.1f}")
    kpi2.metric("Change from first year", f"{pct_change:+.1f}%")
    kpi3.metric("Top Emitter (last year)", top_country)
    st.markdown("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # Line chart
    # Identify highest emitter in the selected date range
    if not filtered.empty:
        total_emissions = filtered.groupby('Country')[selected_metric].sum()
        top_emitter = total_emissions.idxmax() if not total_emissions.empty else None
    else:
        top_emitter = None

    if highlight_top and top_emitter:
        # Categorical colour highlighting (SWD) - BBD colour requirement
        color_discrete_map = {c: 'lightgrey' for c in selected_countries}
        color_discrete_map[top_emitter] = '#d62728'
        
        fig_line = px.line(
            filtered, x='Date', y=selected_metric, color='Country',
            color_discrete_map=color_discrete_map,
            title=f"Trend of {selected_metric_label} over time"
        )
        
        # Label that country at the end of its line
        end_data = filtered[filtered['Country'] == top_emitter]
        if not end_data.empty:
            end_point = end_data.iloc[-1]
            fig_line.add_annotation(
                x=end_point['Date'],
                y=end_point[selected_metric],
                text=top_emitter,
                showarrow=False,
                xanchor='left',
                xshift=5,
                font=dict(color='#d62728', size=12)
            )
        fig_line.update_layout(showlegend=False)
    else:
        # Categorical colours - BBD colour requirement
        fig_line = px.line(
            filtered, x='Date', y=selected_metric, color='Country',
            title=f"Trend of {selected_metric_label} over time"
        )
    
    # SWD requirements: white background, insight title, use_container_width
    fig_line.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='lightgrey')
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col_right:
    # Bar chart
    if not filtered.empty:
        # Ranking for the last year in selected date range
        last_year_data = filtered[filtered['Date'] == filtered['Date'].max()]
        bar_data = last_year_data.sort_values(selected_metric, ascending=True)
        
        # Single colour - BBD colour requirement
        fig_bar = px.bar(
            bar_data, x=selected_metric, y='Country', orientation='h',
            title=f"Ranking in {end_date.year}",
            color_discrete_sequence=['#1f77b4'] 
        )
        # SWD requirements: white background
        fig_bar.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='lightgrey'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig_bar, use_container_width=True)