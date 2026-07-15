import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Global CO2 Emissions | Analytical Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Google Fonts and inject Custom CSS for premium Dark Mode / Hybrid look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Roboto Mono', monospace;
        color: #f3f4f6;
    }
    
    /* Clean Robotic Black Page Background with Binary Font Pattern */
    .stApp {
        background-color: #000000;
        background-image: url("data:image/svg+xml,%3Csvg width='300' height='300' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='20' y='50' font-family='monospace' font-weight='bold' font-size='14' fill='rgba(16, 185, 129, 0.07)' letter-spacing='2'%3E01010110 1001%3C/text%3E%3Ctext x='120' y='150' font-family='monospace' font-weight='bold' font-size='14' fill='rgba(16, 185, 129, 0.07)' letter-spacing='2'%3E11001010 0110%3C/text%3E%3Ctext x='40' y='250' font-family='monospace' font-weight='bold' font-size='14' fill='rgba(16, 185, 129, 0.07)' letter-spacing='2'%3E00110011 1101%3C/text%3E%3C/svg%3E");
        border-top: 4px solid #10b981;
    }
    
    /* Main container spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Premium Dark Glassmorphic Title Header */
    .title-container {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(12px);
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid rgba(55, 65, 81, 0.4);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 2.75rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        background: linear-gradient(to right, #ffffff, #9ca3af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #9ca3af;
        font-weight: 300;
    }
    
    /* Dark Glassmorphic Card design for metrics */
    .metric-card {
        background: rgba(17, 24, 39, 0.85);
        backdrop-filter: blur(12px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(55, 65, 81, 0.4);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.5);
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #9ca3af;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 0.25rem;
    }
    .metric-delta {
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    .delta-up { color: #f87171; }
    .delta-down { color: #34d399; }

    /* Elegant Containers for Controls (Sidebars / Columns) in Dark Glass */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(17, 24, 39, 0.7) !important;
        backdrop-filter: blur(12px);
        border-radius: 12px !important;
        border: 1px solid rgba(55, 65, 81, 0.4) !important;
        padding: 1.5rem !important;
    }
    
    /* Fix text colors inside control panels for readability */
    label[data-testid="stWidgetLabel"] {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }
    .stMarkdown p, .stMarkdown h5 {
        color: #e5e7eb !important;
    }

    /* Wrap Plotly Charts in elegant white cards to ensure visual standard compliance */
    div[data-testid="stPlotlyChart"] {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
    }

    /* Custom styles for Streamlit Tabs (matching dark theme) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: rgba(17, 24, 39, 0.6);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(55, 65, 81, 0.4);
        border-radius: 8px 8px 0 0;
        color: #9ca3af;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background-color: rgba(31, 41, 55, 0.8);
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(17, 24, 39, 0.9) !important;
        border-bottom: 2px solid #ffffff !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('owid-co2-data.csv')
    return df

df = load_data()

# Styling Constants
FONT_FAMILY = "'Roboto Mono', monospace"
COLOR_PRIMARY = "#0f172a"      # Sleek Charcoal for text
COLOR_HIGHLIGHT = "#c2410c"    # Warm Amber/Copper (CVD-safe focus)
COLOR_MUTED = "#94a3b8"        # Slate grey for background
COLORS_SEQUENCE = ["#0284c7", "#c2410c", "#0d9488", "#7c3aed", "#db2777", "#ea580c"] # CVD-safe vibrant palette

def apply_plotly_theme(fig, title_text, yaxis_title=""):
    fig.update_layout(
        title={
            'text': title_text,
            'font': {'family': FONT_FAMILY, 'size': 18, 'weight': 600, 'color': '#0f172a'},
            'y': 0.95,
            'x': 0,
            'xanchor': 'left',
            'yanchor': 'top'
        },
        font=dict(family=FONT_FAMILY, color="#334155"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="left",
            x=0,
            font=dict(size=11)
        ),
        yaxis_title=yaxis_title,
        xaxis_title=""
    )
    fig.update_xaxes(showgrid=False, linecolor='#cbd5e1', tickfont=dict(size=11))
    fig.update_yaxes(showgrid=False, linecolor='#cbd5e1', tickfont=dict(size=11))
    return fig

# Title Block
st.markdown("""
<div class="title-container">
    <div class="main-title">Decarbonization Dynamics</div>
    <div class="subtitle">An analytical exploration of global greenhouse gas emissions, decoupling pathways, and energy transitions.</div>
</div>
""", unsafe_allow_html=True)

# Metric Summary Cards
latest_year = 2021 # Using 2021 for cleaner general data density
df_latest = df[df['year'] == latest_year]
global_co2_latest = df_latest[df_latest['country'] == 'World']['co2'].values[0] / 1000  # Gt
global_co2_prev = df[df['year'] == 2000][df['country'] == 'World']['co2'].values[0] / 1000

# Top Emitters
top_emitter = df_latest[df_latest['iso_code'].notnull()].nlargest(1, 'co2')
top_emitter_name = top_emitter['country'].values[0]
top_emitter_val = top_emitter['co2'].values[0]

# UK Decoupling stat
uk_2021 = df[(df['country'] == 'United Kingdom') & (df['year'] == 2021)]['co2_per_capita'].values[0]
uk_1990 = df[(df['country'] == 'United Kingdom') & (df['year'] == 1990)]['co2_per_capita'].values[0]
uk_decline = (uk_2021 - uk_1990) / uk_1990 * 100

m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Global Emissions ({latest_year})</div>
        <div class="metric-value">{global_co2_latest:.1f} Gt</div>
        <div class="metric-delta delta-up">▲ +{(global_co2_latest - global_co2_prev)/global_co2_prev*100:.1f}% change since 2000</div>
    </div>
    """, unsafe_allow_html=True)
with m_col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Top Emitter ({latest_year})</div>
        <div class="metric-value">{top_emitter_name}</div>
        <div class="metric-delta">{top_emitter_val/1000:.1f} Gt emitted</div>
    </div>
    """, unsafe_allow_html=True)
with m_col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">UK Carbon Reduction (since 1990)</div>
        <div class="metric-value">{abs(uk_decline):.1f}%</div>
        <div class="metric-delta delta-down">▼ Per capita emissions cut in half</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["Global Macro Trends", "Economic Decoupling Analysis", "Energy Source Breakdown"])

# --- TAB 1: Global Trends ---
with tab1:
    st.write("")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("##### Filter Timeframe & Regions")
        st.write("Examine the long-term shifts in emissions as developing economies industrialize.")
        
        year_range = st.slider(
            "Select Time Range", 
            min_value=1950, 
            max_value=2021, 
            value=(1970, 2021), 
            key="t1_slider"
        )
        
        regions = ['Asia', 'Europe', 'North America', 'South America', 'Africa', 'Oceania']
        selected_regions = st.multiselect(
            "Select Regions", 
            options=regions, 
            default=['Asia', 'Europe', 'North America', 'Africa'], 
            key="t1_multi"
        )
        
    with col2:
        df_regions = df[(df['country'].isin(selected_regions)) & (df['year'] >= year_range[0]) & (df['year'] <= year_range[1])].copy()
        if not df_regions.empty:
            fig = px.area(
                df_regions, 
                x='year', 
                y='co2', 
                color='country', 
                color_discrete_sequence=COLORS_SEQUENCE
            )
            apply_plotly_theme(
                fig, 
                title_text=f"Asia Dominates Modern Emissions while Western Regions Stabilize", 
                yaxis_title="CO2 Emissions (million tonnes)"
            )
            # Add direct annotation to show Asian rise
            fig.add_annotation(
                x=2015, y=17000,
                text="Asian emissions surge past rest of world combined",
                showarrow=True, arrowhead=2, arrowcolor="#334155",
                ax=-100, ay=-40,
                font=dict(size=11, color="#334155")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")

# --- TAB 2: Economic Decoupling ---
with tab2:
    st.write("")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("##### Is Decoupling Happening?")
        st.write("Decoupling occurs when GDP grows while CO2 emissions decline. Compare indexed trajectories.")
        
        base_year = st.selectbox("Select Index Base Year", [1990, 2000, 2010], index=1, key="t2_base")
        df_base = df[(df['year'] == base_year) & (df['gdp'].notnull()) & (df['co2_per_capita'].notnull())]
        available_countries = df_base['country'].unique().tolist()
        
        default_countries = ['United States', 'United Kingdom', 'Germany', 'China', 'India']
        default_selection = [c for c in default_countries if c in available_countries]
        
        selected_countries = st.multiselect(
            "Select Countries to Compare", 
            options=available_countries, 
            default=default_selection, 
            key="t2_countries"
        )
        
    with col2:
        if selected_countries:
            df_dec = df[(df['year'] >= base_year) & (df['gdp'].notnull()) & (df['co2_per_capita'].notnull()) & (df['country'].isin(selected_countries))].copy()
            df_dec['gdp_per_capita'] = df_dec['gdp'] / df_dec['population']
            
            for c in selected_countries:
                b_gdp = df_dec[(df_dec['country'] == c) & (df_dec['year'] == base_year)]['gdp_per_capita'].values[0]
                b_co2 = df_dec[(df_dec['country'] == c) & (df_dec['year'] == base_year)]['co2_per_capita'].values[0]
                df_dec.loc[df_dec['country'] == c, 'gdp_pc_index'] = df_dec['gdp_per_capita'] / b_gdp * 100
                df_dec.loc[df_dec['country'] == c, 'co2_pc_index'] = df_dec['co2_per_capita'] / b_co2 * 100
            
            fig2 = go.Figure()
            # Muted colors for baseline, bold colors for focus
            for i, c in enumerate(selected_countries):
                df_c = df_dec[df_dec['country'] == c]
                color = COLORS_SEQUENCE[i % len(COLORS_SEQUENCE)]
                # Add GDP line (dotted)
                fig2.add_trace(go.Scatter(
                    x=df_c['year'], y=df_c['gdp_pc_index'], 
                    mode='lines', name=f'{c} (GDP/Capita)', 
                    line=dict(color=color, width=1.5, dash='dot'),
                    hovertemplate="%{y:.1f}% of base year"
                ))
                # Add CO2 line (solid)
                fig2.add_trace(go.Scatter(
                    x=df_c['year'], y=df_c['co2_pc_index'], 
                    mode='lines', name=f'{c} (CO2/Capita)', 
                    line=dict(color=color, width=3),
                    hovertemplate="%{y:.1f}% of base year"
                ))
            
            apply_plotly_theme(
                fig2, 
                title_text="Western Countries Decouple (Solid CO2 Drops, Dotted GDP Rises), Developers Rise in Tandem",
                yaxis_title=f"Index ({base_year} = 100)"
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.caption("**SYSTEM GUIDANCE**: Solid lines designate CO2 per Capita. Dotted lines designate GDP per Capita. Dotted lines transcending solid lines signifies economic decoupling.")
        else:
            st.warning("SYSTEM ALERT: Target minimum one country for analysis.")

# --- TAB 3: Fuel Sources ---
with tab3:
    st.write("")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("##### Fuel Breakdown")
        st.write("Understand the primary sources of carbon emissions across the top global emitters.")
        
        recent_year = st.slider("Select Year", min_value=1990, max_value=2021, value=2021, key="t3_slider")
        num_countries = st.number_input("Number of Top Countries", min_value=3, max_value=15, value=8, key="t3_num")
        
    with col2:
        df_recent = df[(df['year'] == recent_year) & (df['iso_code'].notnull())].copy()
        top_emitters = df_recent.nlargest(num_countries, 'co2')['country'].tolist()
        df_top = df_recent[df_recent['country'].isin(top_emitters)]
        
        sources = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']
        df_melted = df_top.melt(id_vars='country', value_vars=sources, var_name='Source', value_name='Emissions')
        df_melted['Source'] = df_melted['Source'].str.replace('_co2', '').str.capitalize()
        
        # Consistent customized colors for specific sources
        source_colors = {
            'Coal': '#475569',    # Dark slate
            'Oil': '#c2410c',     # Warm copper/orange
            'Gas': '#0284c7',     # Deep blue
            'Cement': '#94a3b8',  # Light slate
            'Flaring': '#e2e8f0'  # Off white/grey
        }
        
        fig3 = px.bar(
            df_melted, 
            x='country', 
            y='Emissions', 
            color='Source',
            color_discrete_map=source_colors,
            category_orders={"Source": ["Coal", "Oil", "Gas", "Cement", "Flaring"]}
        )
        
        apply_plotly_theme(
            fig3, 
            title_text=f"Coal and Oil Remain Dominant Sources for the Largest Global Emitters in {recent_year}",
            yaxis_title="CO2 Emissions (million tonnes)"
        )
        fig3.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
        
        st.plotly_chart(fig3, use_container_width=True)
