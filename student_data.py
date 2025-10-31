import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the Dataset
st.title("🎓 Student Performance Dashboard")
df = pd.read_csv("students_data.csv")

st.header("📘 Dataset Preview")
st.dataframe(df)

# 2. Sidebar Filters
st.sidebar.header("🔍 Filters")

course_filter = st.sidebar.selectbox("Select Course", options=["All"] + list(df["Course"].unique()))
city_filter = st.sidebar.multiselect("Select City", options=df["City"].unique(), default=list(df["City"].unique()))
min_marks = st.sidebar.slider("Minimum Marks", 0, 100, 0)
gender_filter = st.sidebar.radio("Select Gender", options=["All", "Male", "Female"])

# Apply filters
filtered_df = df.copy()

if course_filter != "All":
    filtered_df = filtered_df[filtered_df["Course"] == course_filter]

filtered_df = filtered_df[filtered_df["City"].isin(city_filter)]
filtered_df = filtered_df[filtered_df["Marks"] >= min_marks]

if gender_filter != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender_filter]

# 3. Display Filtered Data
st.header("📊 Filtered Student Data")
st.dataframe(filtered_df)

# 4. Display Key Metrics
st.subheader("📈 Summary Statistics")

if not filtered_df.empty:
    avg_marks = filtered_df["Marks"].mean()
    if "Attendance" in filtered_df.columns:
        avg_attendance = filtered_df["Attendance"].mean()
    else:
        avg_attendance = None
else:
    avg_marks = 0
    avg_attendance = None

total_students = len(filtered_df)

col1, col2, col3 = st.columns(3)
col1.metric("Average Marks", f"{avg_marks:.2f}")
if avg_attendance is not None:
    col2.metric("Average Attendance", f"{avg_attendance:.2f}%")
else:
    col2.metric("Average Attendance", "N/A")
col3.metric("Total Students", total_students)

# 5. Search by Student Name
st.subheader("🔎 Search Student by Name")
search_name = st.text_input("Enter student name:")
if search_name:
    search_result = df[df["Name"].str.contains(search_name, case=False, na=False)]
    if not search_result.empty:
        st.table(search_result)
    else:
        st.error("No student found with that name.")

# 6. Buttons
colA, colB = st.columns(2)
if colA.button("Show Top Performers"):
    top_students = df[df["Marks"] > 90]
    st.success("Top Performers (Marks > 90)")
    st.dataframe(top_students)

if colB.button("Show All Data"):
    st.info("Full Dataset:")
    st.dataframe(df)

# 7. Charts
st.subheader("📉 Charts & Visuals")

if not filtered_df.empty:
    st.bar_chart(filtered_df.set_index("Name")["Marks"])

    # Only show attendance chart if available
    if "Attendance" in filtered_df.columns:
        st.line_chart(filtered_df.set_index("Name")["Attendance"])
    else:
        st.info("Attendance data not available for line chart.")

    # Matplotlib chart
    plt.figure(figsize=(8, 4))
    plt.hist(filtered_df["Marks"], bins=10, edgecolor='black')
    plt.title("Distribution of Marks")
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    st.pyplot(plt)

# 8. Display Performance Messages
if avg_marks > 85:
    st.success("Excellent performance! 🌟")
elif 70 <= avg_marks <= 85:
    st.info("Good performance. 👍")
else:
    st.warning("Needs improvement. 📘")

# 9. Add Image
try:
    st.image("streamlit.png", caption="Streamlit App", use_column_width=True)
except:
    st.info("Add an image named 'streamlit.png' in your project folder to display it here.")

st.markdown("---")
st.write("Made with ❤️ using Streamlit")
