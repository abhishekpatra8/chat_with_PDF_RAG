import streamlit as st, requests, base64, time

st.set_page_config(page_title="QnA Application", layout="wide", page_icon="💬", initial_sidebar_state="collapsed")

st.header('RAG Based - QnA Application!!', divider='rainbow')

try:
    response = requests.get("http://localhost:8000/")

    if "uploader_key" not in st.session_state: st.session_state["uploader_key"] = 1

    updaload_file, view_all_file  = st.tabs(["Upload PDF File", "View All PDFs"])

    with updaload_file:
        upload_file = st.file_uploader("Upload the PDF", type="pdf", key=st.session_state["uploader_key"])

        if upload_file is not None:
            filename = (upload_file.name)
            file_bs64 = base64.b64encode(upload_file.read()).decode('utf-8')

            response = requests.post("http://localhost:8000/upload_file", json={"filename": filename, "base64": file_bs64})

            if response.status_code == 200:
                st.success(response.json()['message'], icon="✅")
                st.write("Click on `View All PDFs` tab, then select the PDF to start asking question....!!")

                time.sleep(3)

                st.session_state["uploader_key"] += 1
                st.rerun()

    with view_all_file:
        clicked = None
        response = requests.get("http://localhost:8000/get_all_files")

        if response.json()['details']:
            option_values = [i['filename'].replace("_", " ").split(".")[0] for i in response.json()['details']]

            with st.container():
                st.write("")
                st.write("Below are the list of PDFs present in DB. Select one to start QnA.")
                
                clicked = st.pills(label="abc", label_visibility="hidden", options=option_values, selection_mode="single")
                
                st.write("")

                if clicked:
                    st.write(f"Selected PDF to process - {clicked}")
                    st.write("")
                    st.write("")

                    data = [i for i in response.json()['details'] if i['filename'] == clicked.replace(" ", "_") + ".pdf"][0]

                    st.write("Enter the question - ")
                    
                    prompt = st.text_input("abc", label_visibility="collapsed")
                    btn = st.button("Submit", type="secondary")
                    
                    if btn:
                            
                        st.write(f"Question - {prompt}")

                        data.update({"prompt": prompt})
                        # st.write(f"Data - {data}")
                        response = requests.post("http://localhost:8000/ask_question", json=data)
                        
                        st.write(f"Answer - {response.json()['response']}")                    
        else:
            st.write("There are no PDFs saved in Database.")

except requests.ConnectionError as e:
    st.warning(body="Failed to establish a connection. Please start the FastAPI server; then refresh the page.", icon="⚠️")