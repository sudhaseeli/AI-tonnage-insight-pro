import pathlib

import pandas as pd
import streamlit as st

from tonnage.rules_engine import load_rule_config, apply_rules
from tonnage.anomaly_detector import detect_anomalies
from tonnage.report_generator import annotate_dataframe, summarize_issues

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]


def load_sample_data() -> pd.DataFrame:
    sample_path = BASE_DIR / "data" / "sample_tonnage_data.csv"
    return pd.read_csv(sample_path)


def main():
    st.set_page_config(page_title="AI Tonnage Insight Pro", layout="wide")
    st.title("AI Tonnage Insight Pro")
    st.caption("Validate tonnage data, detect anomalies, and generate compliance-friendly insights.")

    st.sidebar.header("Configuration")
    rules_path = BASE_DIR / "config" / "rules.yml"
    st.sidebar.write(f"Using rules from: `{rules_path}`")

    uploaded_file = st.file_uploader("Upload tonnage CSV file", type=["csv"])
    use_sample = st.checkbox("Use sample data (demo)", value=not bool(uploaded_file))

    if use_sample:
        df = load_sample_data()
        st.info("Using included sample data.")
    else:
        if uploaded_file is None:
            st.warning("Please upload a CSV file or enable sample data.")
            st.stop()
        df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    if st.button("Run AI + Rules Checks"):
        config = load_rule_config(rules_path)
        df_rules = apply_rules(df, config)
        df_anom = detect_anomalies(df_rules)
        df_final = annotate_dataframe(df_anom)

        summary = summarize_issues(df_final)

        st.subheader("Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Rows", summary["total_rows"])
        col2.metric("Rows with Rule Issues", summary["rows_with_rule_issues"])
        col3.metric("Rows with Anomalies", summary["rows_with_anomalies"])
        col4.metric("Rows with Any Issue", summary["rows_with_any_issue"])

        st.subheader("Flagged Rows")
        flagged = df_final[df_final["has_any_issue"]]
        if flagged.empty:
            st.success("No issues detected in this dataset.")
        else:
            st.dataframe(flagged, use_container_width=True)

        st.subheader("All Data with Annotations")
        st.dataframe(df_final, use_container_width=True)

        # Download
        csv_bytes = df_final.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Annotated CSV",
            data=csv_bytes,
            file_name="tonnage_validated_annotated.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
