import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_cop32_master_dataset():
    """
    Programmatically generates a comprehensive synthetic master dataset 
    for all 5 countries over the full 2015-2026 timeline.
    """
    dates = pd.date_range(start="2015-01-01", end="2026-12-31", freq="D")
    countries = ["Ethiopia", "Kenya", "Tanzania", "Sudan", "Nigeria"]
    
    master_records = []
    
    # Maintain reproducibility across data deployments
    np.random.seed(42)
    
    for country in countries:
        # Base environmental parameter anchors mimicking real-world baselines
        if country == "Ethiopia":
            t_base, p_base, h_base = 22.4, 5.92, 55.0
        elif country == "Sudan":
            t_base, p_base, h_base = 28.3, 1.12, 25.0
        elif country == "Nigeria":
            t_base, p_base, h_base = 26.8, 8.42, 75.0
        elif country == "Tanzania":
            t_base, p_base, h_base = 25.1, 6.85, 65.0
        else: # Kenya
            t_base, p_base, h_base = 23.5, 4.15, 60.0
            
        for d in dates:
            # Create rhythmic seasonal sine vectors mapping regional cycles
            seasonal_factor = np.sin(d.month * (np.pi / 6))
            
            # Programmatically construct individual environmental sensors
            t2m = t_base + (seasonal_factor * 3.5) + np.random.normal(0, 0.7)
            
            # Precipitation logic (highly skewed / zero-inflated modeling)
            rain_trigger = np.random.rand()
            if country == "Sudan":
                prectotcorr = np.random.gamma(shape=1.2, scale=12) if (rain_trigger > 0.90 and d.month in) else 0.0
            else:
                prectotcorr = np.random.gamma(shape=2.0, scale=8) if (rain_trigger > 0.65 and d.month in) else 0.0
                
            # Humidity tracking (inversely correlated with temperature ranges)
            rh2m = np.clip(h_base - (seasonal_factor * 15) + (prectotcorr * 0.5) + np.random.normal(0, 3), 5.0, 100.0)
            
            master_records.append({
                "Date": d,
                "YEAR": d.year,
                "Country": country,
                "T2M": t2m,
                "PRECTOTCORR": prectotcorr,
                "RH2M": rh2m
            })
            
    return pd.DataFrame(master_records)

def render_interactive_timeline(df, countries, year_range, active_variable):
    """
    Generates the interactive time-series chart based on sidebar slider inputs.
    """
    # Filter datasets by multi-select and year range sliders
    filtered_df = df[
        (df["Country"].isin(countries)) & 
        (df["YEAR"] >= year_range[0]) & 
        (df["YEAR"] <= year_range[1])
    ]
    
    # Resample daily data to monthly averages/totals to optimize readability
    if active_variable == "PRECTOTCORR":
        df_monthly = filtered_df.groupby(["Country", filtered_df["Date"].dt.to_period("M")]).agg({active_variable: "sum"}).reset_index()
        ylabel_text = "Total Monthly Precipitation (mm)"
        title_prefix = "Precipitation Accumulation Timeline"
    else:
        df_monthly = filtered_df.groupby(["Country", filtered_df["Date"].dt.to_period("M")]).agg({active_variable: "mean"}).reset_index()
        ylabel_text = "Mean Temperature (°C)" if active_variable == "T2M" else "Relative Humidity (%)"
        title_prefix = f"Historical Monthly Mean {active_variable} Trend"
        
    df_monthly["PlotDate"] = df_monthly["Date"].dt.to_timestamp()
    
    # Chart creation
    fig, ax = plt.subplots(figsize=(13, 5.5), dpi=100)
    
    country_colors = {
        "Ethiopia": "#2ca02c",
        "Kenya": "#1f77b4",
        "Tanzania": "#9467bd",
        "Sudan": "#d62728",
        "Nigeria": "#ff7f0e"
    }
    
    for country in df_monthly["Country"].unique():
        c_data = df_monthly[df_monthly["Country"] == country].sort_values("PlotDate")
        ax.plot(
            c_data["PlotDate"], 
            c_data[active_variable], 
            label=country, 
            color=country_colors.get(country, "#7f7f7f"),
            linewidth=2.5 if country == "Ethiopia" else 1.5,
            alpha=1.0 if country == "Ethiopia" else 0.75
        )
        
    ax.set_title(f"{title_prefix} | {year_range[0]}–{year_range[1]}", fontsize=12, weight="bold", pad=10)
    ax.set_xlabel("Timeline (Years)")
    ax.set_ylabel(ylabel_text)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(title="Countries", loc="upper left")
    
    plt.tight_layout()
    return fig
