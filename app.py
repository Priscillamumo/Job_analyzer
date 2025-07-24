import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="💰 Tech Job Salary Explorer", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("ds_salaries.csv")
    
    # Check and standardize column names (common variations)
    column_mapping = {
        'company': 'company_name',
        'company_name': 'company_name',
        'employer_name': 'company_name',
        'company_location': 'location'
    }
    
    for old_name, new_name in column_mapping.items():
        if old_name in df.columns:
            df.rename(columns={old_name: new_name}, inplace=True)
    
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
selected_job = st.sidebar.selectbox(
    "Select Job Title", 
    df["job_title"].unique()
)

# Check if we have location data
location_col = 'company_location' if 'company_location' in df.columns else 'location'
location_options = ["All"] + list(df[location_col].unique())

selected_country = st.sidebar.selectbox(
    "Select Country", 
    location_options
)

salary_range = st.sidebar.slider(
    "Salary Range (USD)",
    min_value=int(df["salary_in_usd"].min()),
    max_value=int(df["salary_in_usd"].max()),
    value=(int(df["salary_in_usd"].quantile(0.25)), int(df["salary_in_usd"].quantile(0.75)))
)

# Filter data
filtered_df = df[df["job_title"] == selected_job]
if selected_country != "All":
    filtered_df = filtered_df[filtered_df[location_col] == selected_country]
filtered_df = filtered_df[(filtered_df["salary_in_usd"] >= salary_range[0]) & 
                         (filtered_df["salary_in_usd"] <= salary_range[1])]

# --- Main Content ---
st.title("💰 Tech Job Salary Explorer")

# Metrics
st.subheader(f"📊 Stats for {selected_job}")
col1, col2, col3 = st.columns(3)
with col1:
    avg_salary = filtered_df["salary_in_usd"].mean()
    st.metric("Average Salary", f"${avg_salary:,.0f}")

with col2:
    st.metric("Median Salary", f"${filtered_df['salary_in_usd'].median():,.0f}")

with col3:
    st.metric("Jobs Found", len(filtered_df))

# Charts - Two columns layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Salary Distribution")
    fig1 = px.histogram(
        filtered_df, 
        x="salary_in_usd",
        nbins=20,
        color="experience_level",
        hover_data=["job_title", location_col],
        labels={"salary_in_usd": "Salary (USD)"},
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📊 Salary by Experience Level")
    fig2 = px.box(
        filtered_df, 
        x="experience_level", 
        y="salary_in_usd",
        color="experience_level",
        hover_data=["job_title", location_col],
        points="all",
        labels={
            "experience_level": "Experience Level",
            "salary_in_usd": "Salary (USD)"
        },
        template="plotly_white"
    )
    fig2.update_traces(boxmean=True)
    st.plotly_chart(fig2, use_container_width=True)

# New Features - Only show if data exists
st.subheader("✨ Additional Insights")

# 1. Top Paying Companies (only if column exists)
if 'company_name' in filtered_df.columns:
    st.markdown("### 🏢 Top Paying Companies")
    top_companies = filtered_df.groupby('company_name')['salary_in_usd'].mean().nlargest(5).reset_index()
    st.dataframe(top_companies.style.format({"salary_in_usd": "${:,.0f}"}))
else:
    st.warning("Company name data not available in this dataset")

# 2. Salary Trend Over Years (if column exists)
if 'work_year' in df.columns:
    st.markdown("### 📅 Salary Trend Over Years")
    yearly_data = filtered_df.groupby('work_year')['salary_in_usd'].mean().reset_index()
    fig3 = px.line(
        yearly_data,
        x="work_year",
        y="salary_in_usd",
        markers=True,
        labels={"work_year": "Year", "salary_in_usd": "Average Salary (USD)"}
    )
    st.plotly_chart(fig3, use_container_width=True)

# 3. Interactive Data Table
st.markdown("### 🔍 Detailed Job Listings")
display_columns = ['job_title', location_col, 'experience_level', 'salary_in_usd']
if 'company_name' in filtered_df.columns:
    display_columns.insert(1, 'company_name')
    
st.dataframe(filtered_df[display_columns]
            .sort_values('salary_in_usd', ascending=False)
            .style.format({"salary_in_usd": "${:,.0f}"}))