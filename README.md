# 📬 Local LLM Email Assistant

A Streamlit web app that generates emails in your personal style by training on your past emails stored locally. This project uses a local Large Language Model (LLM) server (e.g., Mistral) for on-device AI-powered email generation.

---

## 🚀 Features

* Load and parse your historical emails from a structured `user_emails.txt` file.
* Browse emails filtered by customizable tags.
* Generate new emails styled after your writing, using prompts sent to a local LLM.
* Modular architecture separating UI, email loading, and LLM communication.

---

## 🗂️ Project Structure

```
/
├── app.py               # Main Streamlit application
├── email_loader.py      # Loads and parses user_emails.txt
├── llm_client.py        # API client for local LLM server
├── user_emails.txt      # Your email samples with subjects, bodies, tags
├── tests/               # Unit tests for email loader, LLM client, etc.
└── requirements.txt     # Python dependencies
```

---

## 📋 How It Works

1. **Email Loading (`email_loader.py`):**
   Parses `user_emails.txt` containing multiple emails. Each email has a defined format:

   ```
   ===EMAIL===
   Subject: ...
   Body:
   ...
   Tags: tag1, tag2, ...
   ```

   The loader converts this into a list of dictionaries for easy filtering and display.

2. **User Interface (`app.py`):**

   * Displays the loaded emails with an option to filter by tags.
   * Provides inputs for a new email subject and context description.
   * When you click "Generate," it compiles a prompt including examples of your writing style and sends it to the local LLM server.

3. **Local LLM API Client (`llm_client.py`):**
   Encapsulates HTTP calls to your local LLM server (default URL: `http://localhost:11434/api/generate`).

   * Sends the prompt and model choice.
   * Receives the generated email text.
   * Handles error reporting if the server is unreachable.

4. **Email Generation Workflow:**
   The app builds a prompt combining:

   * Your recent email bodies as style examples.
   * The new email's subject and a plain language description of what you want the email about.
     This prompt is sent to the local LLM, which replies with a stylistically consistent email.

---

## 🛠️ Setup Instructions

1. **Prepare your environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   .\venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

2. **Fill `user_emails.txt` with your past emails** following the provided format.

3. **Run your local LLM server** (e.g., Mistral) and ensure it listens on `http://localhost:11434/api/generate`.

4. **Start the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

5. **Access the web UI** in your browser at `http://localhost:8501`.

---

## 📦 Dependencies

* [Streamlit](https://streamlit.io/) — Web UI framework
* [Requests](https://requests.readthedocs.io/) — HTTP client for LLM API calls
* A local LLM server (self-hosted Mistral, LLaMA, etc.)

---

## 🧪 Testing

Unit tests for the email loader and LLM client are in the `tests/` directory. To run them:

```bash
pytest tests/
```

---

## 🔧 Extending or Customizing

* **Change LLM model:** Modify the model parameter in `llm_client.py` or the call in `app.py`.
* **Improve prompt engineering:** Edit the prompt construction in `app.py` to tailor output style or constraints.
* **Add authentication:** Enhance `llm_client.py` to support API keys or tokens if your local LLM requires them.
* **Advanced UI:** Add features like live streaming responses, email templates, or exporting generated emails.

---

## 🤝 Contribution

Feel free to fork, file issues, or submit pull requests to improve this assistant or adapt it to your workflow.

---

## ⚠️ Disclaimer

This tool uses local AI models and sample emails for style mimicry. Generated content should be reviewed before sending.