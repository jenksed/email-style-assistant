# app.py
import streamlit as st
from email_loader import load_user_emails
from llm_client import call_local_llm, MAX_PROMPT_CHARS

def filter_emails_by_tags(emails, selected_tags):
    if not selected_tags:
        return emails
    return [e for e in emails if any(tag in e['tags'] for tag in selected_tags)]

def main():
    emails = load_user_emails()

    st.title("📬 Local LLM Email Assistant")
    st.write("Trained on your past 25 emails (user_emails.txt)")

    # Dropdown for email tags
    all_tags = sorted(set(tag for email in emails for tag in email['tags']))
    selected_tags = st.multiselect("Filter by tags", all_tags)

    # Filter by tag
    filtered = filter_emails_by_tags(emails, selected_tags)

    for i, email in enumerate(filtered):
        with st.expander(f"{i+1}. {email['subject']}"):
            st.code(email["body"], language="markdown")
            st.text(f"Tags: {', '.join(email['tags'])}")

    st.divider()

    st.subheader("✉️ Generate an Email in Your Voice")

    subject_input = st.text_input("Email Subject")
    body_prompt = st.text_area("What's the email about?", height=200)

if st.button("Generate"):
    if len(prompt) > MAX_PROMPT_CHARS:
        st.error("⚠️ Prompt is too long. Please shorten it.")
    else:
        with st.spinner("Generating…"):
            response = call_local_llm(prompt, model="mistral:latest")
        st.text_area("📝 Output", response, height=300)

if __name__ == "__main__":
    main()