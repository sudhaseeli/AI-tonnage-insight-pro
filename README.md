# AI Tonnage Insight Pro

**AI Tonnage Insight Pro** is an end-to-end, portfolio-ready project that showcases how AI and automation can be used to streamline **regulatory tonnage reporting**.

It mimics a real-world workflow where companies need to track product tonnage (for example, by state, product, and reporting period), identify issues before filing, and generate clear, auditable summaries for compliance and business users.

This project is designed to be:
- **Realistic enough for recruiters and hiring managers**
- **Safe to share** (no confidential data or company-specific logic)
- **Easy to run locally** with sample data included

---

## 🎯 Project Goals

This project demonstrates how to:

- Ingest and validate tonnage data from CSV files.
- Apply rule-based checks to catch common data quality and compliance issues.
- Use an AI/ML model to flag **anomalies** in reported tonnage.
- Generate human-readable summaries and explanations for potential issues.
- Provide an interactive **Streamlit UI** for reviewing and exporting results.

It’s ideal to showcase skills in **Python, data validation, ML, automation, and regulatory-style workflows**.

---

## 🧱 High-Level Design

The project follows a simple but realistic architecture:

1. **Input Layer (Data)**
   - Reads tonnage data from CSV files.  
   - Example columns: `state`, `product_name`, `tonnage`, `reporting_year`.

2. **Rules Engine**
   - Applies configurable rules such as:
     - Missing or negative tonnage values  
     - Tonnage above configured thresholds  
     - Missing required states or products  
   - Rules are stored in `config/rules.yml` so they are easy to adjust.

3. **Anomaly Detection (AI/ML)**
   - Uses a lightweight **IsolationForest** model to detect unusual tonnage values by product/state.
   - Flags rows that look statistically abnormal.

4. **Insight & Reporting Layer**
   - Combines rule violations and anomaly scores.
   - Generates human-readable messages for each flagged record.
   - Summarizes counts of issues by type (data quality vs anomaly vs threshold).

5. **Interactive UI**
   - A **Streamlit app** lets users:
     - Upload a CSV file
     - Run validation + AI checks
     - Filter and review flagged rows
     - Download a cleaned and annotated CSV file for record-keeping

---

## 🧰 Tech Stack

- **Python 3.9+**
- **Pandas** for data wrangling
- **scikit-learn** (IsolationForest) for anomaly detection
- **PyYAML** for rule configuration
- **Streamlit** for the web-based review interface

---

## 📂 Project Structure

```bash
ai-tonnage-insight-pro/
│
├── README.md
├── requirements.txt
│
├── config/
│   └── rules.yml
│
├── data/
│   └── sample_tonnage_data.csv
│
├── tonnage/
│   ├── __init__.py
│   ├── rules_engine.py
│   ├── anomaly_detector.py
│   └── report_generator.py
│
└── app/
    ├── __init__.py
    └── streamlit_app.py
```

---

## ⚙️ Installation

1. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the App

From the project root:

```bash
streamlit run app/streamlit_app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`) in your browser.

You can use the **sample file** at:

```text
data/sample_tonnage_data.csv
```

Upload it in the UI to see how the checks and AI logic work.

---

## 🧪 Core Components

### 1. Rules Engine (`tonnage/rules_engine.py`)

- Loads rules from `config/rules.yml`.
- Applies:
  - value checks (negative / missing / zero)
  - threshold checks
  - allowed states and products (if configured)
- Returns a dataframe with an `issues` column listing rule violations.

### 2. Anomaly Detector (`tonnage/anomaly_detector.py`)

- Trains a simple **IsolationForest** on historical or current tonnage values.
- Outputs an `anomaly_score` and `is_anomaly` flag.

### 3. Report Generator (`tonnage/report_generator.py`)

- Combines rule issues and anomalies.
- Creates:
  - A summary table by issue type.
  - Row-level explanation strings (e.g., “Tonnage unusually high for this product in this state”).

### 4. Streamlit App (`app/streamlit_app.py`)

- File upload component.
- Buttons to run checks and show results.
- Tables for:
  - All data
  - Only flagged records
  - Summary view
- Option to **download results** as a CSV with annotations.

---

## 📊 Sample Data

The included `data/sample_tonnage_data.csv` contains **fake example data**, such as:

- Several US states  
- Multiple products  
- Varied tonnage values (including a few intentionally odd values to trigger anomalies)

This keeps the project realistic without exposing any proprietary or sensitive information.

---

## ✅ How to Talk About This Project on Your Resume

You can describe this project as:

> Built an AI-powered tonnage reporting assistant that validates regulatory-style tonnage data using configurable business rules, applies anomaly detection to flag unusual values, and generates human-readable compliance insights through a Streamlit interface.

---

## ✅ How to Talk About This Project in an Interview

Key points:

- You designed it to mirror **regulatory reporting workflows**.
- You separated:
  - configuration (YAML rules),
  - logic (rules engine + anomaly model),
  - and presentation (Streamlit UI).
- You used **ML as a helper**, not a replacement for rules.
- It demonstrates practical **DataOps-style structure**: modular code, configs, sample data, and a simple UI layer.

---

This repository is intentionally written in a clear, educational style so that recruiters, engineers, and hiring managers can quickly understand how you think about **data quality, automation, and AI in a compliance context**.
