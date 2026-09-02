import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pypdf import PdfReader
from ddgs import DDGS

def read_resume(filepath: str) -> str:
    """Reads a PDF resume and returns its text content.
    
    Args:
        filepath: The path to the PDF resume.
    """
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading resume: {e}"

def search_jobs(query: str, max_results: int = 10) -> str:
    """Searches the web for jobs based on a query.
    
    Args:
        query: The search query (e.g., 'remote AI engineer jobs').
        max_results: The maximum number of results to return.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"Title: {r.get('title', '')}\nLink: {r.get('href', '')}\nSnippet: {r.get('body', '')}\n")
        return "\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Error searching jobs: {e}"

def send_email_report(subject: str, body: str) -> str:
    """Sends an email report to the user with the found opportunities.
    
    Args:
        subject: The subject of the email.
        body: The body content of the email report.
    """
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    
    if not sender_email or not sender_password or not receiver_email:
        return "Error: Email credentials (SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL) are not set in environment variables."
        
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Assuming Gmail SMTP. For other providers, change the host and port.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {e}"
