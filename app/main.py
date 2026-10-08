import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# 1. Page settings
st.set_page_config(
    page_title="COP32 Climate Dashboard",
    page_icon="🌍",
    layout="wide"
)

# 2. Direct Local Data Loader
@st.cache_data
def load_local_master_data():
    country_files = {
        "Ethiopia": "data/ethiopia_cleaned.csv",
        "Kenya": "data/kenya_cleaned.csv",
        "Tanzania": "data/tanzania_cleaned.csv",
        "Sudan": "data/sudan_cleaned.csv",
        "Nigeria": "data/nigeria_cleaned.csv"
    }
    
    dataframe_list = []
    for country, file_path in country_files.items():
        if os.path.exists(file_path):
            df_temp = pd.read_csv(file_path)
            df_temp["Country"] = country
            if "Date" in df_temp.columns:
                df_temp["Date"] = pd.to_datetime(df_temp["Date"])
            if "YEAR" not in df_temp.columns and "Date" in df_temp.columns:
                df_temp["YEAR"] = df_temp["Date"].dt.year
            dataframe_list.append(df_temp)
            
    if not dataframe_list:
        st.error("🚨 Could not find the files. Check that they are inside the 'data' folder.")
        return pd.DataFrame()
        
    return pd.concat(dataframe_list, axis=0, ignore_index=True)

df_master = load_local_master_data()

# 3. Sidebar UI Widgets
st.sidebar.title("Dashboard Controls")

# INTERACTIVE ELEMENT 1: Variable Selector Dropdown
active_variable = st.sidebar.selectbox(
    "Select Climate Variable",
    options=["T2M", "PRECTOTCORR", "RH2M"],
    format_func=lambda x: {
        "T2M": "Temperature (T2M)",
        "PRECTOTCORR": "Precipitation (PRECTOTCORR)",
        "RH2M": "Relative Humidity (RH2M)"
    }[x]
)

# INTERACTIVE ELEMENT 2: Country Multi-Select Widget
active_countries = st.sidebar.multiselect(
    "Select Target Countries",
    options=["Ethiopia", "Kenya", "Tanzania", "Sudan", "Nigeria"],
    default=["Ethiopia", "Kenya", "Tanzania", "Sudan", "Nigeria"]
)

# INTERACTIVE ELEMENT 3: Year Range Slider Control
selected_years = st.sidebar.slider(
    "Observation Timeline Window",
    min_value=2015,
    max_value=2026,
    value=(2015, 2026),
    step=1
)

# 4. Main Panel Layout
st.title("🌍 COP32 Climate Vulnerability Analytics Platform")
st.markdown("### National Strategic Synthesis Dashboard")

if df_master.empty:
    st.warning("Data load failed. Please make sure files exist in the data/ folder.")
elif not active_countries:
    st.warning("⚠️ Please select at least one country in the sidebar filter to draw plots.")
else:
    # Filter dataset globally by user selections
    df_filtered = df_master[
        (df_master["Country"].isin(active_countries)) & 
        (df_master["YEAR"] >= selected_years[0]) & 
        (df_master["YEAR"] <= selected_years[1])
    ]
    
    if df_filtered.empty:
        st.info("No records match the active filters.")
    else:
        # ADVANCED UPGRADE: Dynamic KPI Summary Card Bar
        st.markdown("---")
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            max_val = df_filtered[active_variable].max()
            max_country = df_filtered.loc[df_filtered[active_variable] == max_val, "Country"].iloc[0]
            unit = "°C" if active_variable == "T2M" else "mm" if active_variable == "PRECTOTCORR" else "%"
            st.metric(label=f"Maximum Observed {active_variable}", value=f"{max_val:.2f} {unit}", delta=max_country, delta_color="inverse")
            
        with metric_col2:
            mean_val = df_filtered[active_variable].mean()
            st.metric(label=f"Filtered Dataset Average", value=f"{mean_val:.2f} {unit}")
            
        with metric_col3:
            min_val = df_filtered[active_variable].min()
            min_country = df_filtered.loc[df_filtered[active_variable] == min_val, "Country"].iloc[0]
            st.metric(label=f"Minimum Observed {active_variable}", value=f"{min_val:.2f} {unit}", delta=min_country)
        st.markdown("---")

        # Build side-by-side plots columns
        col1, col2 = st.columns(2)
        
        # Configure names and metrics based on selected dropdown variable
        ylabel_line = "Total Monthly Volume (mm)" if active_variable == "PRECTOTCORR" else "Mean Value"
        ylabel_box = "Daily Volumetric Depth (mm/day)" if active_variable == "PRECTOTCORR" else "Daily Distribution"
        agg_func = "sum" if active_variable == "PRECTOTCORR" else "mean"
        
        with col1:
            st.subheader(f"📈 {active_variable} Trend Ingestion Timeline")
            df_filtered["YearMonth"] = df_filtered["Date"].dt.to_period("M")
            df_monthly = df_filtered.groupby(["Country", "YearMonth"]).agg({active_variable: agg_func}).reset_index()
            df_monthly["PlotDate"] = df_monthly["YearMonth"].dt.to_timestamp()
            
            fig1, ax1 = plt.subplots(figsize=(7, 4.5))
            country_colors = {"Ethiopia": "#2ca02c", "Kenya": "#1f77b4", "Tanzania": "#9467bd", "Sudan": "#d62728", "Nigeria": "#ff7f0e"}
            
            for country in df_monthly["Country"].unique():
                c_data = df_monthly[df_monthly["Country"] == country].sort_values("PlotDate")
                ax1.plot(c_data["PlotDate"], c_data[active_variable], label=country, color=country_colors.get(country), linewidth=2 if country == "Ethiopia" else 1.5)
                
            ax1.set_ylabel(ylabel_line)
            ax1.grid(True, linestyle="--", alpha=0.4)
            ax1.legend(loc="upper left", fontsize=8)
            st.pyplot(fig1)
            plt.close(fig1)
            
        with col2:
            st.subheader(f"📊 {active_variable} Distribution & Anomaly Matrix")
            fig2, ax2 = plt.subplots(figsize=(7, 4.5))
            sns.boxplot(
                data=df_filtered, 
                x="Country", 
                y=active_variable, 
                palette={"Ethiopia": "#2ca02c", "Kenya": "#1f77b4", "Tanzania": "#9467bd", "Sudan": "#d62728", "Nigeria": "#ff7f0e"},
                hue="Country",
                legend=False,
                fliersize=2,
                ax=ax2
            )
            ax2.set_ylabel(ylabel_box)
            ax2.grid(True, linestyle="--", alpha=0.3, axis="y")
            st.pyplot(fig2)
            plt.close(fig2)
