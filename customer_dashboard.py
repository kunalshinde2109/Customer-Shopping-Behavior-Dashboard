import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from pathlib import Path

# =========================================================
# GLOBAL UNIQUE PLOTLY CHART ID FIX
# =========================================================

_original_plotly_chart = st.plotly_chart
_chart_counter = 0

def _unique_plotly_chart(*args, **kwargs):

    global _chart_counter
    _chart_counter += 1

    kwargs["key"] = f"shopping_dashboard_chart_{_chart_counter}"

    return _original_plotly_chart(*args, **kwargs)

st.plotly_chart = _unique_plotly_chart

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Customer Shopping Analytics",
    page_icon="🛍️",
    layout="wide"
)

# =========================================================
# COLORS
# =========================================================
COLORS = [
    "#56E3CD", "#F5A623", "#FFD166", "#00B4D8",
    "#9B5DE5", "#F15BB5", "#FF6B35", "#90BE6D"
]

COLOR_MAP = {
    "Accessories": "#F5A623",
    "Clothing": "#56E3CD",
    "Footwear": "#00B4D8",
    "Outerwear": "#9B5DE5",
    "Female": "#F15BB5",
    "Male": "#56E3CD",
    "Fall": "#F5A623",
    "Spring": "#56E3CD",
    "Summer": "#FFD166",
    "Winter": "#00B4D8",
    "Yes": "#56E3CD",
    "No": "#F5A623"
}

# =========================================================
# CUSTOM CSS + SHARP BACKGROUND IMAGE
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
BG_IMAGE = BASE_DIR / "assets" / "dashboard_background.png"

if BG_IMAGE.exists():
    with open(BG_IMAGE, "rb") as img_file:
        bg_base64 = base64.b64encode(img_file.read()).decode()

    background_css = f"""
    background-image:
        linear-gradient(rgba(8,14,25,0.78), rgba(8,14,25,0.82)),
        url("data:image/png;base64,{bg_base64}");
    """
else:
    background_css = "background: #080e19;"

st.markdown(f"""
<style>

.stApp {{
    {background_css}
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #f1f5f9;
}}

[data-testid="stSidebar"] {{
    background: rgba(17, 28, 45, 0.96);
}}

.block-container {{
    padding-top: 2rem;
}}

div[data-testid="stMetric"] {{
    background: linear-gradient(135deg, rgba(23,42,64,0.94), rgba(16,29,45,0.94));
    border: 1px solid #285166;
    border-radius: 22px;
    padding: 23px;
    min-height: 140px;
    transition: all 0.3s ease;
}}

div[data-testid="stMetric"]:hover {{
    border: 1px solid #36e0c1;
    transform: translateY(-3px);
    box-shadow: 0px 0px 18px rgba(54, 224, 193, 0.15);
}}

div[data-testid="stMetricLabel"] {{
    color: #9eb0c5;
    font-size: 16px;
}}

div[data-testid="stMetricValue"] {{
    color: #56e3cd;
    font-size: 32px;
    font-weight: 800;
}}

h1, h2, h3 {{
    color: #f8fafc;
}}

[data-testid="stPlotlyChart"] {{
    background: rgba(17,28,45,0.94);
    border: 1px solid #263b50;
    border-radius: 16px;
    padding: 8px;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid #263b50;
    border-radius: 12px;
}}

.stDownloadButton button {{
    background: #172a40;
    color: #56e3cd;
    border: 1px solid #36e0c1;
    border-radius: 10px;
}}

.stDownloadButton button:hover {{
    background: #36e0c1;
    color: #080e19;
}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    data = pd.read_csv("shopping_trends_updated.csv")
    return data

df = load_data()

# =========================================================
# DATA PREPARATION
# =========================================================
amount_col = "Purchase Amount (USD)"
category_col = "Category"
item_col = "Item Purchased"
gender_col = "Gender"
season_col = "Season"
payment_col = "Payment Method"
age_col = "Age"
rating_col = "Review Rating"
subscription_col = "Subscription Status"
frequency_col = "Frequency of Purchases"
previous_col = "Previous Purchases"

# =========================================================
# UNIQUE PLOTLY CHART KEY FIX
# =========================================================
_chart_counter = 0

def plotly_chart(fig, use_container_width=True):

    global _chart_counter
    _chart_counter += 1

    st.plotly_chart(
        fig,
        use_container_width=use_container_width,
        key=f"unique_chart_{_chart_counter}"
    )
# =========================================================
# CHART STYLING
# =========================================================
def style_chart(fig):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111c2d",
        plot_bgcolor="#111c2d",
        font=dict(color="#E5E7EB"),
        margin=dict(l=30, r=30, t=50, b=30),
        hoverlabel=dict(
            bgcolor="#172a40",
            font_color="white"
        )
    )

    fig.update_xaxes(
        gridcolor="#263b50",
        zerolinecolor="#263b50"
    )

    fig.update_yaxes(
        gridcolor="#263b50",
        zerolinecolor="#263b50"
    )

    return fig

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def bar_chart(data, x, y, color=None, title=None):

    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color if color else x,
        color_discrete_sequence=COLORS,
        color_discrete_map=COLOR_MAP,
        text_auto=True
    )

    if title:
        fig.update_layout(title=title)

    fig.update_traces(
        textposition="outside",
        marker_line_width=0
    )

    return style_chart(fig)


def pie_chart(data, names, values):

    fig = px.pie(
        data,
        names=names,
        values=values,
        hole=0.45,
        color_discrete_sequence=COLORS,
        color_discrete_map=COLOR_MAP
    )

    fig.update_traces(
        textinfo="label+percent",
        hovertemplate="%{label}<br>%{value}<br>%{percent}<extra></extra>"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111c2d",
        plot_bgcolor="#111c2d",
        font=dict(color="#E5E7EB"),
        margin=dict(l=30, r=30, t=50, b=30),
        hoverlabel=dict(
            bgcolor="#172a40",
            font_color="white"
        )
    )

    return fig


def metric_row(labels, values):

    cols = st.columns(len(labels))

    for col, label, value in zip(cols, labels, values):
        col.metric(label, value)


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("🛍️ Shopping Analytics")
st.sidebar.caption("Customer Behavior Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Dataset Overview",
        "Exploratory Data Analysis",
        "Feature Engineering",
        "Executive Overview",
        "Shopping Behavior Analytics",
        "Purchase Explorer",
        "Shopping Insights",
        "Project Information"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Customer Shopping Behavior Analysis")

# =========================================================
# HOME
# =========================================================
if page == "Home":

    st.title("🛍️ Customer Shopping Behavior Analytics")
    st.subheader("Interactive Analytics Dashboard")

    st.write(
        "Analyze customer shopping trends, product preferences, "
        "purchasing patterns and business insights."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", f"{len(df):,}")
    col2.metric("Total Features", df.shape[1])
    col3.metric("Product Categories", df[category_col].nunique())
    col4.metric("Product Types", df[item_col].nunique())

    st.divider()

    # CATEGORY + GENDER
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🛒 Purchases by Category")

        cat = df[category_col].value_counts().reset_index()
        cat.columns = ["Category", "Count"]

        fig = px.bar(
            cat,
            x="Category",
            y="Count",
            color="Category",
            color_discrete_map=COLOR_MAP,
            text="Count"
        )

        fig.update_traces(textposition="outside")

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with col2:

        st.subheader("👥 Gender Distribution")

        gender = df[gender_col].value_counts().reset_index()
        gender.columns = ["Gender", "Count"]

        st.plotly_chart(
            pie_chart(gender, "Gender", "Count"),
            use_container_width=True
        )

    st.divider()

    # SEASON + PAYMENT
    col3, col4 = st.columns(2)

    with col3:

        st.subheader("🌦️ Seasonal Shopping")

        season = df[season_col].value_counts().reset_index()
        season.columns = ["Season", "Count"]

        fig = px.bar(
            season,
            x="Season",
            y="Count",
            color="Season",
            color_discrete_map=COLOR_MAP,
            text="Count"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with col4:

        st.subheader("💳 Payment Methods")

        payment = df[payment_col].value_counts().reset_index()
        payment.columns = ["Payment Method", "Count"]

        fig = px.bar(
            payment,
            x="Payment Method",
            y="Count",
            color="Payment Method",
            color_discrete_sequence=COLORS,
            text="Count"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.divider()

    st.subheader("📋 Dataset Preview")

    st.dataframe(df.head(10), use_container_width=True)

# =========================================================
# DATASET OVERVIEW
# =========================================================
elif page == "Dataset Overview":

    st.title("📊 Project Dataset")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", f"{len(df):,}")
    col2.metric("Total Features", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))
    col4.metric("Duplicate Rows", int(df.duplicated().sum()))

    st.divider()

    st.subheader("📁 Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Rows:** {df.shape[0]:,}")
        st.write(f"**Columns:** {df.shape[1]}")

    with col2:
        memory = df.memory_usage(deep=True).sum() / 1024
        st.write(f"**Memory Usage:** {memory:.2f} KB")
        st.write(f"**Dataset Cells:** {df.shape[0] * df.shape[1]:,}")

    st.divider()

    st.subheader("🔍 Column Information")

    info = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(info, use_container_width=True)

    st.divider()

    st.subheader("⚠️ Missing Values")

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": df.isnull().sum().values,
        "Missing Percentage": (
            df.isnull().sum().values / len(df) * 100
        ).round(2)
    })

    missing = missing.sort_values(
        "Missing Count",
        ascending=False
    )

    st.dataframe(missing, use_container_width=True)

    st.divider()

    st.subheader("📈 Statistical Summary")

    st.dataframe(
        df.describe(include="all").transpose(),
        use_container_width=True
    )

    st.divider()

    st.subheader("🔎 Dataset Search")

    search_column = st.selectbox("Select Column", df.columns)

    search_text = st.text_input("Enter search value")

    search_df = df.copy()

    if search_text:

        search_df = df[
            df[search_column].astype(str).str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    st.write(f"Matching Records: {len(search_df):,}")

    st.dataframe(search_df, use_container_width=True)

    st.download_button(
        "⬇️ Download Dataset",
        search_df.to_csv(index=False).encode("utf-8"),
        "shopping_dataset.csv",
        "text/csv"
    )

# =========================================================
# EDA
# =========================================================
elif page == "Exploratory Data Analysis":

    st.title("📊 Exploratory Data Analysis")

    st.write("Explore purchasing patterns and customer behavior.")

    st.divider()

    # CATEGORY ANALYSIS
    st.subheader("🛍️ Category Analysis")

    col1, col2 = st.columns(2)

    with col1:

        cat_count = df[category_col].value_counts().reset_index()
        cat_count.columns = ["Category", "Count"]

        fig = px.bar(
            cat_count,
            x="Category",
            y="Count",
            color="Category",
            color_discrete_map=COLOR_MAP,
            text="Count"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with col2:

        cat_amount = (
            df.groupby(category_col)[amount_col]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            cat_amount,
            x=category_col,
            y=amount_col,
            color=category_col,
            color_discrete_map=COLOR_MAP,
            text_auto=".2f"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.divider()

    # PRODUCT ANALYSIS
    st.subheader("📦 Top 10 Products")

    top_items = df[item_col].value_counts().head(10).reset_index()
    top_items.columns = ["Item", "Count"]

    fig = px.bar(
        top_items,
        x="Item",
        y="Count",
        color="Item",
        color_discrete_sequence=COLORS,
        text="Count"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

    st.divider()

    # GENDER AND AGE
    st.subheader("👥 Customer Analysis")

    col1, col2 = st.columns(2)

    with col1:

        gender_data = df[gender_col].value_counts().reset_index()
        gender_data.columns = ["Gender", "Count"]

        st.plotly_chart(
            pie_chart(gender_data, "Gender", "Count"),
            use_container_width=True
        )

    with col2:

        age_data = df[age_col].value_counts().sort_index().reset_index()
        age_data.columns = ["Age", "Count"]

        fig = px.line(
            age_data,
            x="Age",
            y="Count",
            markers=True
        )

        fig.update_traces(
            line=dict(color="#F5A623", width=3),
            marker=dict(color="#56E3CD", size=7)
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.divider()

    # SEASON
    st.subheader("🌦️ Seasonal Purchase Amount")

    seasonal_amount = (
        df.groupby(season_col)[amount_col]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        seasonal_amount,
        x=season_col,
        y=amount_col,
        color=season_col,
        color_discrete_map=COLOR_MAP,
        text_auto=".2f"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

    st.divider()

    # PAYMENT
    st.subheader("💳 Payment Method")

    payment_data = df[payment_col].value_counts().reset_index()
    payment_data.columns = ["Payment Method", "Count"]

    fig = px.bar(
        payment_data,
        x="Payment Method",
        y="Count",
        color="Payment Method",
        color_discrete_sequence=COLORS,
        text="Count"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

    st.divider()

    # FREQUENCY
    st.subheader("🔄 Purchase Frequency")

    frequency_data = df[frequency_col].value_counts().reset_index()
    frequency_data.columns = ["Frequency", "Count"]

    fig = px.bar(
        frequency_data,
        x="Frequency",
        y="Count",
        color="Frequency",
        color_discrete_sequence=COLORS,
        text="Count"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

    st.divider()

    # RATINGS
    st.subheader("⭐ Ratings by Category")

    ratings = (
        df.groupby(category_col)[rating_col]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        ratings,
        x=category_col,
        y=rating_col,
        color=category_col,
        color_discrete_map=COLOR_MAP,
        text_auto=".2f"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

    st.divider()

    # SUBSCRIPTION
    st.subheader("🔔 Subscription Distribution")

    subscription_data = df[subscription_col].value_counts().reset_index()
    subscription_data.columns = ["Subscription", "Count"]

    st.plotly_chart(
        pie_chart(subscription_data, "Subscription", "Count"),
        use_container_width=True
    )

# =========================================================
# FEATURE ENGINEERING
# =========================================================
elif page == "Feature Engineering":

    st.title("⚙️ Feature Engineering")

    fe = df.copy()

    # AGE GROUP
    fe["Age Group"] = pd.cut(
        fe[age_col],
        bins=[0, 25, 35, 45, 60, 100],
        labels=["18-25", "26-35", "36-45", "46-60", "60+"],
        include_lowest=True
    )

    # PURCHASE SEGMENT
    fe["Purchase Segment"] = pd.cut(
        fe[amount_col],
        bins=[0, 50, 100, 150, float("inf")],
        labels=["Low", "Medium", "High", "Very High"],
        include_lowest=True
    )

    # CUSTOMER EXPERIENCE
    fe["Customer Experience"] = pd.cut(
        fe[previous_col],
        bins=[-1, 10, 30, 50, float("inf")],
        labels=[
            "New/Less Experienced",
            "Regular",
            "Experienced",
            "Highly Experienced"
        ]
    )

    # DISCOUNT FEATURE
    fe["Discount Customer"] = fe["Discount Applied"].astype(str)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Created Features", 4)
    col2.metric("Age Segments", fe["Age Group"].nunique())
    col3.metric("Purchase Segments", fe["Purchase Segment"].nunique())
    col4.metric("Experience Segments", fe["Customer Experience"].nunique())

    st.divider()

    # AGE
    st.subheader("👥 Age Segmentation")

    age_segment = fe["Age Group"].value_counts().sort_index().reset_index()
    age_segment.columns = ["Age Group", "Customers"]

    fig = px.bar(
        age_segment,
        x="Age Group",
        y="Customers",
        color="Age Group",
        color_discrete_sequence=COLORS,
        text="Customers"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

    st.divider()

    # PURCHASE SEGMENT
    st.subheader("💰 Purchase Amount Segmentation")

    purchase_segment = fe["Purchase Segment"].value_counts().sort_index().reset_index()
    purchase_segment.columns = ["Segment", "Customers"]

    st.plotly_chart(
        pie_chart(purchase_segment, "Segment", "Customers"),
        use_container_width=True
    )

    st.divider()

    # EXPERIENCE
    st.subheader("🛒 Previous Purchase Experience")

    experience = (
        fe["Customer Experience"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    experience.columns = ["Experience", "Customers"]

    fig = px.bar(
        experience,
        x="Experience",
        y="Customers",
        color="Experience",
        color_discrete_sequence=COLORS,
        text="Customers"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

    st.divider()

    # DISCOUNT
    st.subheader("🏷️ Discount Customers")

    discount_data = fe["Discount Customer"].value_counts().reset_index()
    discount_data.columns = ["Discount", "Customers"]

    st.plotly_chart(
        pie_chart(discount_data, "Discount", "Customers"),
        use_container_width=True
    )

    st.divider()

    st.subheader("📋 Engineered Dataset Preview")

    st.dataframe(fe, use_container_width=True)

    st.download_button(
        "⬇️ Download Engineered Dataset",
        fe.to_csv(index=False).encode("utf-8"),
        "customer_shopping_engineered.csv",
        "text/csv"
    )

# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================
elif page == "Executive Overview":

    st.title("📈 Executive Overview")
    st.caption("High-level business performance and customer metrics")

    total_customers = len(df)
    total_amount = df[amount_col].sum()
    avg_amount = df[amount_col].mean()
    avg_rating = df[rating_col].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", f"{total_customers:,}")
    col2.metric("Total Purchase Amount", f"${total_amount:,.0f}")
    col3.metric("Average Purchase", f"${avg_amount:,.2f}")
    col4.metric("Average Rating", f"{avg_rating:.2f} / 5")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📦 Category Purchase Amount")

        category_sales = (
            df.groupby(category_col)[amount_col]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            category_sales,
            x=category_col,
            y=amount_col,
            color=category_col,
            color_discrete_map=COLOR_MAP,
            text_auto=".2f"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with col2:

        st.subheader("📊 Average Purchase by Season")

        season_avg = (
            df.groupby(season_col)[amount_col]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            season_avg,
            x=season_col,
            y=amount_col,
            color=season_col,
            color_discrete_map=COLOR_MAP,
            text_auto=".2f"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.divider()

    col3, col4 = st.columns(2)

    with col3:

        st.subheader("⭐ Category Rating")

        category_rating = (
            df.groupby(category_col)[rating_col]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            category_rating,
            x=category_col,
            y=rating_col,
            color=category_col,
            color_discrete_map=COLOR_MAP,
            text_auto=".2f"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with col4:

        st.subheader("💳 Payment Distribution")

        pay = df[payment_col].value_counts().reset_index()
        pay.columns = ["Payment", "Count"]

        st.plotly_chart(
            pie_chart(pay, "Payment", "Count"),
            use_container_width=True
        )

    st.divider()

    st.subheader("📌 Executive Summary")

    top_category = df[category_col].value_counts().idxmax()
    top_item = df[item_col].value_counts().idxmax()
    top_season = df[season_col].value_counts().idxmax()
    top_payment = df[payment_col].value_counts().idxmax()

    st.markdown(f"""
    - **Most purchased category:** {top_category}
    - **Most frequently purchased product:** {top_item}
    - **Most represented season:** {top_season}
    - **Most commonly used payment method:** {top_payment}
    - **Average purchase amount:** ${avg_amount:,.2f}
    - **Average customer rating:** {avg_rating:.2f}
    """)

# =========================================================
# SHOPPING BEHAVIOR ANALYTICS
# =========================================================
elif page == "Shopping Behavior Analytics":

    st.title("🛒 Shopping Behavior Analytics")

    st.write(
        "Analyze customer preferences across product, "
        "season, payment, subscription and shopping frequency."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🛍️ Category Preferences")

        category_behavior = df[category_col].value_counts().reset_index()
        category_behavior.columns = ["Category", "Customers"]

        st.plotly_chart(
            pie_chart(category_behavior, "Category", "Customers"),
            use_container_width=True
        )

    with col2:

        st.subheader("🎨 Product Color Preferences")

        color_data = df["Color"].value_counts().head(10).reset_index()
        color_data.columns = ["Color", "Count"]

        fig = px.bar(
            color_data,
            x="Color",
            y="Count",
            color="Color",
            color_discrete_sequence=COLORS,
            text="Count"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.divider()

    col3, col4 = st.columns(2)

    with col3:

        st.subheader("📏 Size Preferences")

        size_data = df["Size"].value_counts().reset_index()
        size_data.columns = ["Size", "Count"]

        fig = px.bar(
            size_data,
            x="Size",
            y="Count",
            color="Size",
            color_discrete_sequence=COLORS,
            text="Count"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with col4:

        st.subheader("🚚 Shipping Type")

        shipping_data = df["Shipping Type"].value_counts().reset_index()
        shipping_data.columns = ["Shipping", "Count"]

        st.plotly_chart(
            pie_chart(shipping_data, "Shipping", "Count"),
            use_container_width=True
        )

    st.divider()

    col5, col6 = st.columns(2)

    with col5:

        st.subheader("🔔 Subscription Status")

        subscription = df[subscription_col].value_counts().reset_index()
        subscription.columns = ["Subscription", "Count"]

        st.plotly_chart(
            pie_chart(subscription, "Subscription", "Count"),
            use_container_width=True
        )

    with col6:

        st.subheader("🔄 Purchase Frequency")

        freq = df[frequency_col].value_counts().reset_index()
        freq.columns = ["Frequency", "Count"]

        fig = px.bar(
            freq,
            x="Frequency",
            y="Count",
            color="Frequency",
            color_discrete_sequence=COLORS,
            text="Count"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.divider()

    st.subheader("🏷️ Discount and Promo Code Analysis")

    col7, col8 = st.columns(2)

    with col7:

        discount = df["Discount Applied"].value_counts().reset_index()
        discount.columns = ["Discount", "Count"]

        st.plotly_chart(
            pie_chart(discount, "Discount", "Count"),
            use_container_width=True
        )

    with col8:

        promo = df["Promo Code Used"].value_counts().reset_index()
        promo.columns = ["Promo Code", "Count"]

        st.plotly_chart(
            pie_chart(promo, "Promo Code", "Count"),
            use_container_width=True
        )

# =========================================================
# PURCHASE EXPLORER
# =========================================================
elif page == "Purchase Explorer":

    st.title("🔎 Purchase Explorer")

    st.write("Filter, explore and download customer purchase records.")

    st.divider()

    # FILTERS
    col1, col2, col3 = st.columns(3)

    with col1:

        selected_category = st.multiselect(
            "Category",
            options=sorted(df[category_col].dropna().unique()),
            default=list(df[category_col].dropna().unique())
        )

    with col2:

        selected_gender = st.multiselect(
            "Gender",
            options=sorted(df[gender_col].dropna().unique()),
            default=list(df[gender_col].dropna().unique())
        )

    with col3:

        selected_season = st.multiselect(
            "Season",
            options=sorted(df[season_col].dropna().unique()),
            default=list(df[season_col].dropna().unique())
        )

    col4, col5, col6 = st.columns(3)

    with col4:

        selected_payment = st.multiselect(
            "Payment Method",
            options=sorted(df[payment_col].dropna().unique()),
            default=list(df[payment_col].dropna().unique())
        )

    with col5:

        selected_subscription = st.multiselect(
            "Subscription Status",
            options=sorted(df[subscription_col].dropna().unique()),
            default=list(df[subscription_col].dropna().unique())
        )

    with col6:

        selected_shipping = st.multiselect(
            "Shipping Type",
            options=sorted(df["Shipping Type"].dropna().unique()),
            default=list(df["Shipping Type"].dropna().unique())
        )

    min_amount = float(df[amount_col].min())
    max_amount = float(df[amount_col].max())

    amount_range = st.slider(
        "Purchase Amount Range",
        min_value=min_amount,
        max_value=max_amount,
        value=(min_amount, max_amount)
    )

    # APPLY FILTERS
    filtered = df[
        df[category_col].isin(selected_category)
        & df[gender_col].isin(selected_gender)
        & df[season_col].isin(selected_season)
        & df[payment_col].isin(selected_payment)
        & df[subscription_col].isin(selected_subscription)
        & df["Shipping Type"].isin(selected_shipping)
        & df[amount_col].between(amount_range[0], amount_range[1])
    ]

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Filtered Records", f"{len(filtered):,}")
    col2.metric("Average Purchase", f"${filtered[amount_col].mean():,.2f}" if not filtered.empty else "$0")
    col3.metric("Total Amount", f"${filtered[amount_col].sum():,.2f}")

    st.divider()

    st.subheader("📋 Filtered Purchases")

    st.dataframe(
        filtered,
        use_container_width=True
    )

    st.download_button(
        "⬇️ Download Filtered Data",
        filtered.to_csv(index=False).encode("utf-8"),
        "filtered_shopping_data.csv",
        "text/csv"
    )

    st.divider()

    if not filtered.empty:

        st.subheader("📊 Filtered Category Summary")

        summary = filtered[category_col].value_counts().reset_index()
        summary.columns = ["Category", "Count"]

        fig = px.bar(
            summary,
            x="Category",
            y="Count",
            color="Category",
            color_discrete_map=COLOR_MAP,
            text="Count"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    else:

        st.warning("No records match the selected filters.")

# =========================================================
# SHOPPING INSIGHTS
# =========================================================
elif page == "Shopping Insights":

    st.title("💡 Shopping Insights")

    st.write("Data-driven observations derived from this dataset.")

    st.divider()

    # CATEGORY INSIGHTS
    category_counts = df[category_col].value_counts()
    top_category = category_counts.idxmax()
    top_category_count = category_counts.max()

    # ITEM INSIGHTS
    item_counts = df[item_col].value_counts()
    top_product = item_counts.idxmax()
    top_product_count = item_counts.max()

    # SEASON INSIGHTS
    season_counts = df[season_col].value_counts()
    top_season = season_counts.idxmax()

    # PAYMENT INSIGHTS
    payment_counts = df[payment_col].value_counts()
    top_payment = payment_counts.idxmax()

    # GENDER INSIGHTS
    gender_counts = df[gender_col].value_counts()
    top_gender = gender_counts.idxmax()

    # RATINGS
    top_rated_category = (
        df.groupby(category_col)[rating_col]
        .mean()
        .idxmax()
    )

    top_rating = (
        df.groupby(category_col)[rating_col]
        .mean()
        .max()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Leading Category", top_category)
    col2.metric("Top Product", top_product)
    col3.metric("Most Represented Season", top_season)
    col4.metric("Leading Payment", top_payment)

    st.divider()

    st.subheader("📌 Key Observations")

    st.markdown(f"""
    - **Category:** {top_category} has the highest number of records ({top_category_count:,}).
    - **Product:** {top_product} is the most frequently recorded product ({top_product_count:,}).
    - **Season:** {top_season} is the most represented season in the dataset.
    - **Payment:** {top_payment} is the most frequently recorded payment method.
    - **Gender:** {top_gender} is the most represented gender group.
    - **Customer Rating:** {top_rated_category} has the highest average category rating ({top_rating:.2f}).
    """)

    st.divider()

    st.subheader("📊 Customer and Purchase Distribution")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Gender")

        gender_insights = df[gender_col].value_counts().reset_index()
        gender_insights.columns = ["Gender", "Count"]

        st.plotly_chart(
            pie_chart(gender_insights, "Gender", "Count"),
            use_container_width=True
        )

    with col2:

        st.subheader("Category")

        category_insights = df[category_col].value_counts().reset_index()
        category_insights.columns = ["Category", "Count"]

        fig = px.bar(
            category_insights,
            x="Category",
            y="Count",
            color="Category",
            color_discrete_map=COLOR_MAP,
            text="Count"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.divider()

    st.subheader("💼 Suggested Business Actions")

    st.markdown("""
    - Review inventory allocation using category-level purchase counts.
    - Compare seasonal demand before planning seasonal promotions.
    - Monitor customer ratings across product categories.
    - Compare payment preferences when planning checkout options.
    - Explore purchase frequency when designing customer engagement campaigns.
    - Evaluate discount and promotional usage alongside purchasing patterns.
    """)

# =========================================================
# PROJECT INFORMATION
# =========================================================
elif page == "Project Information":

    st.title("ℹ️ Project Information")

    st.subheader("Customer Shopping Behavior Analytics")

    st.write("""
    This project explores customer shopping behavior using an interactive
    data analytics dashboard. It provides an overview of customer records,
    product preferences, purchasing patterns, payment methods,
    seasonal trends and customer ratings.
    """)

    st.divider()

    st.subheader("🎯 Project Objectives")

    st.markdown("""
    - Explore customer shopping data.
    - Analyze product categories and purchasing patterns.
    - Understand seasonal and payment preferences.
    - Explore customer ratings and subscription behavior.
    - Create derived customer segments.
    - Build an interactive analytics dashboard.
    """)

    st.divider()

    st.subheader("🛠️ Tools & Technologies")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Language", "Python")
    col2.metric("Data Analysis", "Pandas")
    col3.metric("Visualization", "Plotly")
    col4.metric("Dashboard", "Streamlit")

    st.divider()

    st.subheader("📂 Dataset Details")

    st.write(f"**Dataset Records:** {len(df):,}")
    st.write(f"**Dataset Features:** {df.shape[1]}")
    st.write(f"**Product Categories:** {df[category_col].nunique()}")
    st.write(f"**Products:** {df[item_col].nunique()}")

    st.divider()

    st.subheader("📚 Analysis Modules")

    st.markdown("""
    1. Home Dashboard
    2. Dataset Overview
    3. Exploratory Data Analysis
    4. Feature Engineering
    5. Executive Overview
    6. Shopping Behavior Analytics
    7. Purchase Explorer
    8. Shopping Insights
    9. Project Information
    """)

    st.divider()

    st.subheader("👨‍💻 Portfolio Project")

    st.write("Customer Shopping Behavior Analysis | Interactive Portfolio Dashboard")

    st.caption("Built with Python, Pandas, Plotly and Streamlit.")

# =========================================================
# FOOTER
# =========================================================
st.sidebar.markdown("---")
st.sidebar.caption("🛍️ Customer Shopping Analytics")
st.sidebar.caption("Portfolio Dashboard")