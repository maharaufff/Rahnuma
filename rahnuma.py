import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# ──────────────────────── PAGE CONFIG ────────────────────────
st.set_page_config(
    page_title="Raahnuma - University Guide",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────── CUSTOM CSS ────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem; border-radius: 10px;
        color: white; text-align: center; margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem; border-radius: 10px;
        color: white; text-align: center; margin: 0.5rem 0;
    }
    .program-card {
        background: white; color: black;
        padding: 1.5rem; border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea; margin: 1rem 0;
    }
    .fee-badge {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        color: white; padding: 0.25rem 0.75rem;
        border-radius: 20px; font-size: 0.8rem; font-weight: bold;
    }
    .university-tag {
        background: linear-gradient(45deg, #43e97b 0%, #38f9d7 100%);
        color: white; padding: 0.25rem 0.5rem;
        border-radius: 15px; font-size: 0.7rem; font-weight: bold;
        margin: 0.25rem; display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────── LOAD DATA ────────────────────────
@st.cache_data
def load_data():
    conn = sqlite3.connect("raahnuma.db")
    universities = pd.read_sql_query("SELECT * FROM universities", conn)
    programs = pd.read_sql_query("SELECT * FROM programs", conn)
    fees = pd.read_sql_query("SELECT * FROM fees", conn)
    eligibility = pd.read_sql_query("SELECT * FROM eligibility", conn)
    conn.close()

    merged = programs.merge(universities, on="UniversityID") \
                     .merge(fees, on="ProgramID") \
                     .merge(eligibility, on="ProgramID")
    return universities, programs, merged

universities_df, programs_df, program_details = load_data()

# ──────────────────────── SESSION STATE ────────────────────────
if 'saved_programs' not in st.session_state:
    st.session_state.saved_programs = []
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# ──────────────────────── SIDEBAR ────────────────────────
st.sidebar.header("🔍 Filters")

page = st.sidebar.selectbox("Navigate to", ["🏠 Dashboard", "🔍 Search Programs", "💰 Fee Calculator", "💾 Saved", "📊 Analytics"])

selected_city = st.sidebar.selectbox("City", ["All"] + universities_df['City'].unique().tolist())
selected_degree = st.sidebar.selectbox("Degree Type", ["All"] + programs_df['DegreeType'].unique().tolist())
fee_limit = st.sidebar.slider("Max Tuition Fee", 0, 300000, 200000, step=10000)
min_percentage = st.sidebar.slider("Your Percentage", 0, 100, 80)

filtered_data = program_details.copy()
if selected_city != "All":
    filtered_data = filtered_data[filtered_data['City'] == selected_city]
if selected_degree != "All":
    filtered_data = filtered_data[filtered_data['DegreeType'] == selected_degree]
filtered_data = filtered_data[
    (filtered_data['TuitionFee'] <= fee_limit) &
    (filtered_data['MinPercentage'] <= min_percentage)
]

# ──────────────────────── MAIN PAGES ────────────────────────
if page == "🏠 Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Raahnuma - Your University Guide</h1>
        <p>Explore top university programs with fee and eligibility info</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="metric-card"><h3>{len(universities_df)}</h3><p>Universities</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card"><h3>{len(programs_df)}</h3><p>Programs</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card"><h3>{len(filtered_data)}</h3><p>Matches</p></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔥 Featured Programs")
    for _, row in filtered_data.head(3).iterrows():
        st.markdown(f"""
        <div class="program-card">
            <h4>{row['Name_x']}</h4>
            <p><strong>{row['Name_y']}</strong> • {row['City']} • {row['DegreeType']} • {row['Duration']} years</p>
            <span class="fee-badge">PKR {row['TuitionFee']:,}</span>
            <span class="university-tag">{row['MinPercentage']}% required</span>
        </div>
        """, unsafe_allow_html=True)

elif page == "🔍 Search Programs":
    st.header("🔍 Search University Programs")
    search_query = st.text_input("Search for a program...")
    if search_query:
        filtered_data = filtered_data[filtered_data['Name_x'].str.contains(search_query, case=False)]

    st.markdown(f"### Found {len(filtered_data)} results")
    for _, row in filtered_data.iterrows():
        st.markdown(f"""
        <div class="program-card">
            <h4>{row['Name_x']} at {row['Name_y']}</h4>
            <p>City: {row['City']} | Type: {row['DegreeType']} | Duration: {row['Duration']} years</p>
            <p>Tuition: PKR {row['TuitionFee']:,} | Required: {row['MinPercentage']}%</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "💰 Fee Calculator":
    st.header("💰 Estimate Your Program Cost")
    selected = st.selectbox("Choose Program", filtered_data['Name_x'].unique())
    if selected:
        prog = filtered_data[filtered_data['Name_x'] == selected].iloc[0]
        books = st.slider("Books & Supplies/year", 0, 50000, 10000)
        transport = st.slider("Transport/year", 0, 50000, 15000)
        misc = st.slider("Miscellaneous/year", 0, 50000, 5000)

        yearly = prog['TuitionFee'] + prog['HostelFee'] + books + transport + misc
        total = yearly * prog['Duration'] + prog['AdmissionFee']

        st.success(f"🎓 Total Cost: PKR {total:,} for {prog['Duration']} years")
        st.info(f"📅 Per Year Estimate: PKR {yearly:,}")

elif page == "💾 Saved":
    st.header("💾 Saved Programs")
    if st.session_state.saved_programs:
        saved = program_details[program_details['ProgramID'].isin(st.session_state.saved_programs)]
        for _, row in saved.iterrows():
            st.markdown(f"""
            <div class="program-card">
                <h4>{row['Name_x']} at {row['Name_y']}</h4>
                <p>Tuition: PKR {row['TuitionFee']:,} | Required: {row['MinPercentage']}%</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No programs saved yet!")

elif page == "📊 Analytics":
    st.header("📊 Program Analytics")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Programs by City")
        city_counts = program_details['City'].value_counts()
        fig = px.bar(x=city_counts.index, y=city_counts.values, title="Program Count by City")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Fee Distribution")
        fig2 = px.histogram(program_details, x='TuitionFee', nbins=10)
        st.plotly_chart(fig2, use_container_width=True)

# ──────────────────────── FOOTER ────────────────────────
st.markdown("""
<hr>
<div style='text-align: center; color: #999'>
Raahnuma © 2025 | Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
