import streamlit as st
import requests
import streamlit.components.v1 as components

# Define the URL for the FastAPI backend
API_URL = "http://127.0.0.1:8000"

# Function to call FastAPI backend
def call_backend(endpoint, payload):
    try:
        response = requests.post(f"{API_URL}/{endpoint}/", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")

# Function to display text with both download and copy options
def display_text_with_options(text, label="Text"):
    st.markdown(f"**{label}:**")
    
    # Display the text
    st.markdown(f"<pre id='text-to-copy'>{text}</pre>", unsafe_allow_html=True)
    
    # Download button
    st.download_button(
        label="Download Text",
        data=text,
        file_name="text.txt",
        mime="text/plain"
    )
    
    # JavaScript for copy to clipboard
    components.html(
        """
        <script>
        function copyText() {
            var text = document.getElementById("text-to-copy").innerText;
            navigator.clipboard.writeText(text).then(function() {
                alert("Text copied to clipboard!");
            }, function(err) {
                alert("Failed to copy text: " + err);
            });
        }
        </script>
        <button onclick="copyText()">Copy Text</button>
        """,
        height=100,
        width=150
    )

# Streamlit UI
st.title("NotesBuddy")

# Feature selection
st.sidebar.title("Features")
feature = st.sidebar.selectbox(
    "Choose a feature:",
    ["Summarize Your Points", "Write a Mail", "Correct Grammar", "Info About Any Topic"]
)

if feature == "Summarize Your Points":
    st.header("Summarize Your Points")
    text_to_summarize = st.text_area("Enter text to summarize")
    if st.button("Summarize"):
        if text_to_summarize:
            summary = call_backend("summarize", {"text": text_to_summarize, "topic": "", "text_to_be_improved": ""})
            if summary:
                display_text_with_options(summary.get("summary"), "Summary")
        else:
            st.warning("Please enter some text to summarize.")

elif feature == "Write a Mail":
    st.header("Write a Mail")
    recipient = st.text_input("Recipient's Email")
    subject = st.text_input("Subject")
    body = st.text_area("Email Body")
    if st.button("Generate Mail"):
        if recipient and subject and body:
            mail_content = call_backend("generate_mail", {
                "recipient": recipient,
                "subject": subject,
                "body": body,
                "text": "",
                "topic": "",
                "text_to_be_improved": ""
            })
            if mail_content:
                display_text_with_options(mail_content.get("mail_content"), "Generated Mail")
        else:
            st.warning("Please fill in all fields to generate the mail.")

elif feature == "Correct Grammar":
    st.header("Correct Grammar")
    text_to_improve = st.text_area("Enter text to correct grammar")
    if st.button("Improve"):
        if text_to_improve:
            improved_text = call_backend("grammar", {"text": "", "topic": "", "text_to_be_improved": text_to_improve})
            if improved_text:
                display_text_with_options(improved_text.get("text_to_be_improved"), "Improved Text")
        else:
            st.warning("Please enter text to correct grammar.")

elif feature == "Info About Any Topic":
    st.header("Info About Any Topic")
    topic_to_search = st.text_input("Enter topic to get information")
    if st.button("Get Information"):
        if topic_to_search:
            information = call_backend("information", {"text": "", "topic": topic_to_search, "text_to_be_improved": ""})
            if information:
                display_text_with_options(information.get("information"), "Information")
        else:
            st.warning("Please enter a topic to search.")
