# Streamlit Dashboard Development Process and Usage Instructions

This module encapsulates the source interface files for deploying the interactive interactive climate platform built for the COP32 Delegation.

## 1. Development Process and Architecture

The dashboard architecture is intentionally separated from data tracking to maintain clean production boundaries:

- **Local Ingestion Layer:** `app/main.py` directly executes an optimized file ingest loop reading from the internal `data/` directory. It checks for file survival across all five target countries, structures chronological datetime vectors, and merges them inside short-term cache loops via `@st.cache_data`.
- **State Management Layout:** Widgets operate as structural control inputs. Modifying checkboxes or range intervals forces Streamlit to rebuild relevant matrices reactively without forcing cold full-script re-executions.

## 2. Setting Up Environment Dependencies

Before launching the application interface, ensure required modeling libraries are present within your sandbox environment:

```bash
pip install streamlit pandas matplotlib seaborn
```

## 3. Local Execution Guide

Launch the application shell using the standard framework runner from your project root folder:

```bash
streamlit run app/main.py
```

## 4. Interactive Widget Instructions

- **Country Filter Selection Panel:** Use the multi-select dropdown menu within the sidebar to insert or drop candidate nations dynamically. Plots adapt layouts in real-time to match subset rows.
- **Temporal Horizon Boundaries:** Adjust the twin slider thumbs to crop data spans (2015–2026). Charts automatically scale axes configurations to fit targeted years.
