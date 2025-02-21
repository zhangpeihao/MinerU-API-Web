import streamlit as st
import os
from dotenv import load_dotenv
from api_client import MineruClient
import time

# Load environment variables
load_dotenv()

# Initialize Mineru client
client = MineruClient(token=os.getenv("MINERU_TOKEN"))

def main():
    st.title("Mineru File Parser")
    
    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["Single File Processing", "Batch Processing"])
    
    with tab1:
        st.header("Single File Processing")
        process_single_file()
        
    with tab2:
        st.header("Batch Processing")
        process_batch_files()

def process_single_file():
    # File URL input
    url = st.text_input("Enter file URL")
    
    # Advanced options
    with st.expander("Advanced Options"):
        is_ocr = st.checkbox("Enable OCR", value=False)
        enable_formula = st.checkbox("Enable Formula Recognition", value=True)
        enable_table = st.checkbox("Enable Table Recognition", value=True)
        layout_model = st.selectbox("Layout Model", 
                                  ["doclayout_yolo", "layoutlmv3"],
                                  index=0)
        language = st.text_input("Language", value="ch")
        data_id = st.text_input("Data ID (optional)")
    
    if st.button("Process File"):
        if url:
            with st.spinner("Creating task..."):
                try:
                    result = client.create_single_task(
                        url=url,
                        is_ocr=is_ocr,
                        enable_formula=enable_formula,
                        enable_table=enable_table,
                        layout_model=layout_model,
                        language=language,
                        data_id=data_id if data_id else None
                    )
                    
                    if result.get("code") == 200:
                        task_id = result["data"]["task_id"]
                        st.success(f"Task created successfully! Task ID: {task_id}")
                        
                        # Add task monitoring
                        monitor_task(task_id)
                    else:
                        st.error(f"Error creating task: {result.get('msg')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a file URL")

def process_batch_files():
    st.write("Upload multiple files or provide multiple URLs")
    
    # Advanced options for batch processing
    with st.expander("Advanced Options"):
        enable_formula = st.checkbox("Enable Formula Recognition (Batch)", value=True)
        enable_table = st.checkbox("Enable Table Recognition (Batch)", value=True)
        layout_model = st.selectbox("Layout Model (Batch)", 
                                  ["doclayout_yolo", "layoutlmv3"],
                                  index=0)
        language = st.text_input("Language (Batch)", value="ch")
    
    # File upload option
    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
    
    if uploaded_files and st.button("Process Batch"):
        with st.spinner("Processing batch..."):
            try:
                files = [{"name": file.name, "is_ocr": False} for file in uploaded_files]
                result = client.create_batch_upload_urls(
                    files=files,
                    enable_formula=enable_formula,
                    enable_table=enable_table,
                    layout_model=layout_model,
                    language=language
                )
                
                if result.get("code") == 200:
                    batch_id = result["data"]["batch_id"]
                    urls = result["data"]["file_urls"]
                    
                    # Upload files
                    for file, url in zip(uploaded_files, urls):
                        if client.upload_file(url, file.read()):
                            st.success(f"Uploaded: {file.name}")
                        else:
                            st.error(f"Failed to upload: {file.name}")
                    
                    st.success(f"Batch created successfully! Batch ID: {batch_id}")
                    
                    # Monitor batch progress
                    monitor_batch(batch_id)
                else:
                    st.error(f"Error creating batch: {result.get('msg')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def monitor_task(task_id):
    progress_placeholder = st.empty()
    result_placeholder = st.empty()
    
    while True:
        result = client.get_task_result(task_id)
        if result.get("code") == 200:
            state = result["data"]["state"]
            
            if state == "done":
                progress_placeholder.success("Processing completed!")
                result_placeholder.json(result["data"])
                break
            elif state == "failed":
                progress_placeholder.error(f"Processing failed: {result['data'].get('err_msg', 'Unknown error')}")
                break
            elif state == "running":
                progress = result["data"].get("extract_progress", {})
                extracted = progress.get("extracted_pages", 0)
                total = progress.get("total_pages", 0)
                if total > 0:
                    progress_placeholder.progress(extracted / total)
                    progress_placeholder.text(f"Processing: {extracted}/{total} pages")
            
            time.sleep(2)
        else:
            progress_placeholder.error(f"Error checking status: {result.get('msg')}")
            break

def monitor_batch(batch_id):
    progress_placeholder = st.empty()
    result_placeholder = st.empty()
    
    while True:
        result = client.get_batch_results(batch_id)
        if result.get("code") == 200:
            extract_results = result["data"]["extract_result"]
            all_done = True
            
            # Display status for each file
            status_text = ""
            for file_result in extract_results:
                status = file_result["state"]
                filename = file_result["file_name"]
                
                if status == "running":
                    all_done = False
                    progress = file_result.get("extract_progress", {})
                    extracted = progress.get("extracted_pages", 0)
                    total = progress.get("total_pages", 0)
                    status_text += f"{filename}: {extracted}/{total} pages\n"
                elif status == "pending":
                    all_done = False
                    status_text += f"{filename}: Pending\n"
                elif status == "failed":
                    status_text += f"{filename}: Failed - {file_result.get('err_msg', 'Unknown error')}\n"
                else:
                    status_text += f"{filename}: Complete\n"
            
            progress_placeholder.text(status_text)
            
            if all_done:
                result_placeholder.json(result["data"])
                break
            
            time.sleep(2)
        else:
            progress_placeholder.error(f"Error checking batch status: {result.get('msg')}")
            break

if __name__ == "__main__":
    main()