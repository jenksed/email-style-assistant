# email_loader.py

def load_user_emails(file_path='user_emails.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = content.strip().split("===EMAIL===")
    emails = []

    for entry in entries:
        if not entry.strip():
            continue
        lines = entry.strip().split('\n')
        subject = ""
        body_lines = []
        tags = []
        in_body = False

        for line in lines:
            if line.startswith("Subject:"):
                subject = line[len("Subject:"):].strip()
            elif line.startswith("Body:"):
                in_body = True
                continue
            elif line.startswith("Tags:"):
                tags = [t.strip() for t in line[len("Tags:"):].split(',')]
                in_body = False
            elif in_body:
                body_lines.append(line)

        email = {
            "subject": subject,
            "body": "\n".join(body_lines).strip(),
            "tags": tags
        }
        emails.append(email)

    return emails
