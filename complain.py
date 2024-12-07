import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import os
# MongoDB setup
MONGO_URI = st.secrets["MONGO_DB_URL"]  # Replace with your MongoDB URI if needed
DATABASE_NAME = "complaints_db"
COLLECTION_NAME = "complaints"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Streamlit App
st.set_page_config(page_title="Complaints Manager", layout="wide")

# Tabs for adding/viewing complaints
tab1, tab2 = st.tabs(["Add Complaint", "View Complaints"])

# Tab 1: Add a complaint
with tab1:
    st.header("Submit a Complaint on G")
    user = st.text_input("Your Name", placeholder="Enter your name...")
    title = st.text_input("Title of Complaint", placeholder="Enter the title of your complaint here...")
    complaint = st.text_area("Complaint", placeholder="Describe your complaint in detail...")
    
    if st.button("Submit Complaint"):
        if title and complaint:
            new_complaint = {
                "user": user,
                "title": title,
                "complaint": complaint,
                "timestamp": datetime.now()
            }
            collection.insert_one(new_complaint)
            st.success("Your complaint has been submitted successfully!")
        else:
            st.error("Please provide both a title and the complaint.")

# Tab 2: View all complaints
with tab2:
    st.header("All Complaints")
    complaints = list(collection.find().sort("timestamp", -1))  # Fetch complaints sorted by latest
    
    if complaints:
        for complaint in complaints:
            with st.expander(complaint["title"], expanded=False):
                st.write(f"**Description:** {complaint['complaint']}")
                st.caption(f"Submitted by: {complaint['user']}")
                st.caption(f"Submitted on: {complaint['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.info("No complaints to display yet. Start by adding one!")