# app.py
import streamlit as st
from email_loader import load_user_emails
from llm_client import call_local_llm


emails = load_user_emails()

st.title("📬 Local LLM Email Assistant")
st.write("Trained on your past 25 emails (user_emails.txt)")

# Dropdown for email tags
all_tags = sorted(set(tag for email in emails for tag in email['tags']))
selected_tags = st.multiselect("Filter by tags", all_tags)

# Filter by tag
filtered = [e for e in emails if any(tag in e['tags'] for tag in selected_tags)] if selected_tags else emails

# Display matching emails
for i, email in enumerate(filtered):
    with st.expander(f"{i+1}. {email['subject']}"):
        st.code(email["body"], language="markdown")
        st.text(f"Tags: {', '.join(email['tags'])}")

st.divider()

# Generate new email
st.subheader("✉️ Generate an Email in Your Voice")

subject_input = st.text_input("Email Subject")
body_prompt = st.text_area("What’s the email about? (Plain description, not the final message)", height=200)

if st.button("Generate"):
    combined_samples = "\n\n".join([email["body"] for email in emails[:15]])

    prompt = f"""You are an assistant trained to write emails in the style of the following examples:\n\n{combined_samples}\n\nNow, write a new email with the subject: {subject_input}\nContext: {body_prompt}\n\nEmail:"""
    
    with st.spinner("Calling local LLM..."):
        response = call_local_llm(prompt)

    st.text_area("📝 Styled Email Output", response, height=300)
    st.success("Email generated successfully!")
