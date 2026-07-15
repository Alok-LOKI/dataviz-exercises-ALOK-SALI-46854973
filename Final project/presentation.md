---
marp: true
theme: default
class: lead
backgroundColor: #fff
---

# Global CO2 Emissions: A Data Story
**Final Individual Project - Data Visualization**
*Summer 2026*

---

# Project Overview

- **Dataset**: Our World in Data (OWID) CO2 and Greenhouse Gas Emissions Dataset
- **Objective**: To tell a multi-dimensional story about how global carbon emissions have evolved and are shifting, using 10 key analytical questions.
- **Deliverables**:
  - Jupyter Notebook with EDA and 10 Plotly visualizations
  - Interactive Streamlit Dashboard
  - This presentation deck

---

# Key Insight 1: The Regional Shift

Historically, North America and Europe dominated global emissions. However, our analysis reveals a massive shift over the last 50 years.

- **Observation**: Asian emissions (driven heavily by rapid developers) have surged and now dwarf other continents.
- **Implication**: Climate change mitigation is now a truly global challenge that cannot be solved by Western nations alone.

---

# Key Insight 2: The Decoupling of Growth

*Is economic growth intrinsically tied to rising emissions?*

- **Finding**: We observed clear evidence of "decoupling" in major Western economies (e.g., UK, Germany, US). 
- **Data**: Since 2000, these countries have seen GDP per capita rise while CO2 per capita steadily declines.
- **Context**: Meanwhile, developing nations show steep positive correlations, as expected in early industrialization phases.

---

# Key Insight 3: Transitioning Fuel Sources

- **Global View**: The top 10 emitters still rely heavily on Coal and Oil.
- **Regional Success**: Analyzing Europe shows a concerted and successful phase-out of coal since 1990, mostly replaced by natural gas and, increasingly, renewables.
- **Consumption vs Production**: Wealthier nations often show higher consumption-based emissions than production-based, indicating some "offloading" of carbon-intensive manufacturing.

---

# The Interactive Dashboard

I built an interactive Streamlit app to let you explore these insights yourself!

**Features**:
1. **Global Trends Tab**: Filter by region and timeframe to see the shift in absolute emissions.
2. **Economic Decoupling Tab**: Pick a base year and any set of countries to see if their GDP and CO2 curves have diverged.
3. **Fuel Sources Tab**: See the exact breakdown of fossil fuel reliance for the top N emitters in any given year.

---

# Dashboard Snapshot

*(Placeholder for dashboard screenshot - refer to live app)*

- **Link to Live App**: `https://your-streamlit-app-url.streamlit.app`
- **Link to Source Repo**: `https://github.com/yourusername/data-viz-final-project`

---

# Conclusion

The data tells a story of two halves:
1. **The Developed World**: Historically responsible for the bulk of cumulative emissions, now successfully decoupling growth and reducing coal reliance.
2. **The Developing World**: Currently driving global emission growth due to rapid industrialization and population growth, but with opportunities to leapfrog dirty technologies.

Thank you!
