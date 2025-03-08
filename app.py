"import streamlit as st\nst.title('Hello, Streamlit!')" 
import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="Smart Data Transformer", layout="wide")


st.title("Smart Data Transformer")
st.write("Easily convert and clean your CSV and Excel files with interactive data processing!")
uploaded_files = st.file_uploader("Upload your data files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_extension = os.path.splitext(uploaded_file.name)[-1].lower()
        try:
            if file_extension == ".csv":
                df = pd.read_csv(uploaded_file)
            elif file_extension == ".xlsx":
                df = pd.read_excel(uploaded_file)
            else:
                st.error(f"Unsupported file type: {file_extension}")
                continue
        except Exception as e:
            st.error(f"Error reading file {uploaded_file.name}: {e}")
            continue
        
        
        st.write(f"### File: {uploaded_file.name}")
        st.write(f"Size: {uploaded_file.size / 1024:.2f} KB")
        st.write("Preview of the uploaded dataset:")
        st.write(df.head())

        
        st.subheader("🔧 Data Cleaning Options")
        col1, col2 = st.columns(2)
        if st.checkbox(f"Clean data for {uploaded_file.name}"):
            with col1:
                if st.checkbox("Remove duplicate rows", key=f"remove_dupes_{uploaded_file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✔ Duplicates removed")
            with col2:
                if st.checkbox("Fill missing numeric values with median", key=f"fill_missing_{uploaded_file.name}"):
                    numeric_cols = df.select_dtypes(include='number').columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
                    st.write("✔ Missing values filled with median")
        
        
        st.subheader("📌 Select Columns to Keep")
        selected_columns = st.multiselect(f"Choose columns for {uploaded_file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        
        
        st.subheader("📊 Data Visualization")
        if st.checkbox("Enable Visualization", key=f"viz_{uploaded_file.name}"):
            numeric_cols = df.select_dtypes(include='number').columns
            if numeric_cols.any():
                st.line_chart(df[numeric_cols].head())
            else:
                st.warning("No numeric data available for visualization.")
        
        
        st.subheader("📂 Convert and Download")
        conversion_choice = st.radio("Select output format:", ["CSV", "Excel"], key=f"convert_{uploaded_file.name}")
        
        if st.button("Download File", key=f"download_{uploaded_file.name}"):
            buffer = BytesIO()
            if conversion_choice == "CSV":
                df.to_csv(buffer, index=False)
                buffer.seek(0)
                st.download_button("Download CSV", buffer, file_name=f"{uploaded_file.name.replace(file_extension, '.csv')}", mime="text/csv")
            elif conversion_choice == "Excel":
                df.to_excel(buffer, index=False)
                buffer.seek(0)
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                st.download_button("Download Excel", buffer, file_name=f"{uploaded_file.name.replace(file_extension, '.xlsx')}", mime=mime_type)

st.success("All files processed successfully! 🚀")
