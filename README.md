
# 🇵🇰 PakInsight — Pakistan City Data Intelligence

**Find the right city for your lifestyle with clear insights into weather, living costs and economic opportunities across Pakistan.**

<p align="center">
  <a href="https://pakinsight2026.streamlit.app/">🌐 Live Dashboard</a> |
  <a href="https://github.com/nawabanis10/pakinsight">💻 GitHub Repository</a>
</p>

## 📌 Project Overview

PakInsight is an end-to-end data analytics project focused on collecting, cleaning, analyzing, and visualizing public data about Pakistani cities.

It combines weather information, cost-of-living data, and economic indicators to uncover meaningful insights and help users compare cities through data-driven analysis.

The project demonstrates how Python, SQL, data visualization, and cloud technologies can be used to transform raw public data into an interactive analytical dashboard.

## 🎯 Key Features

- **Weather Analysis:** Explore temperature and rainfall patterns across cities.
- **Cost of Living Analysis:** Compare prices of essential consumer items.
- **Economic Analysis:** Explore available economic indicators.
- **City Comparison:** Analyze differences between cities using data.
- **Interactive Dashboard:** Explore insights through a Streamlit application.
- **Cloud Database:** Store and retrieve data using a hosted MySQL database.

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Plotly |
| Database | MySQL, SQL |
| Web Application | Streamlit |
| Data Collection | APIs, Web Scraping |
| Cloud & Deployment | Aiven, Streamlit Community Cloud |
| Version Control | Git, GitHub |

## 🏗️ Project Architecture

1. Collect public data from available sources.
2. Clean and prepare datasets using Python and Pandas.
3. Store structured data in MySQL.
4. Host the database using Aiven Cloud.
5. Retrieve and analyze data through Python and SQL.
6. Present results through an interactive Streamlit dashboard.

## 📂 Project Structure

```text
PakInsight/
├── app/
│   ├── assets/
│   ├── app.py
│   └── home_ui.py
├── data/
│   ├── Raw/
│   └── processed/
├── notebooks/
├── sql/
├── README.md
├── requirements.txt
└── .gitignore
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/nawabanis10/pakinsight.git
cd pakinsight
```

### 2. Create and activate the environment

```bash
conda create -n pakinsight python=3.11
conda activate pakinsight
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

- Install MySQL locally.
- Create a database named `pakinsight`.
- Configure your local database connection in `app/db_config.py`.
- Keep database credentials private and never commit them to GitHub.

### 5. Run the application

```bash
cd app
streamlit run app.py
```

## ☁️ Deployment

PakInsight is deployed using:

- **Streamlit Community Cloud** — for hosting the interactive dashboard.
- **Aiven Cloud** — for hosting the MySQL database.

Database credentials are configured securely through Streamlit Secrets.

## 📊 Project Status

**Live Prototype — Under Development**

The dashboard is deployed and currently includes weather, cost-of-living, and economic data analysis. Further improvements and features are planned.

## 👨‍💻 Author

**Muhammad Anis Nawab**

BS Computer Science Student | Aspiring Data Scientist | Python Developer

[GitHub](https://github.com/nawabanis10) · [LinkedIn](https://www.linkedin.com/in/muhammad-anis-nawab-501736390?utm_source=share_via&utm_content=profile&utm_medium=member_android)

---
*Built as a practical data analytics portfolio project focused on Pakistan.*
