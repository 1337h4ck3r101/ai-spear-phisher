import openai
import requests
import json

# Set up your OpenAI API key
openai.api_key = ''  # Replace with your actual API key

# PHP file URL for sending emails
php_email_url = ''  # Replace with your actual PHP file URL

# Load email logs from JSON file
email_logs_file = "email_logs.json"  # Ensure this matches your file name
try:
    with open(email_logs_file, 'r') as file:
        email_logs = json.load(file)
except FileNotFoundError:
    print(f"Error: The file '{email_logs_file}' was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not parse the JSON file '{email_logs_file}'.")
    exit(1)

# Generate a phishing email using OpenAI
def generate_phishing_email(recipient_name, department, subject, body):
    try:
        prompt = (
            f"You are an email content generator. Create a phishing email targeting {recipient_name} "
            f"from the {department} department. Use the following context from their email logs:\n\n"
            f"Subject: {subject}\nBody: {body}\n\n"
            f"Make the email persuasive and relevant to their department."
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an email generator for cybersecurity training."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating phishing email for {recipient_name}: {e}")
        return None

# Send the email via PHP file
def send_email_via_php(to_email, subject, body):
    payload = {
        'to': to_email,
        'subject': subject,
        'body': body
    }
    try:
        response = requests.post(php_email_url, data=payload)
        if response.status_code == 200:
            print(f"Email sent successfully to {to_email}.")
        else:
            print(f"Error sending email to {to_email}: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")

# Main logic to process email logs and send phishing emails
for log in email_logs:
    recipient_email = log['To'].split('<')[-1].replace('>', '').strip()  # Extract the email address
    recipient_name = log['To'].split('<')[0].strip()  # Extract the recipient's name
    department = log['Department']
    subject = log['Subject']
    body = log['Body']

    # Generate phishing email content
    phishing_email_content = generate_phishing_email(recipient_name, department, subject, body)

    if phishing_email_content:
        # Send the phishing email using PHP file
        send_email_via_php(recipient_email, f"Re: {subject}", phishing_email_content)
    else:
        print(f"Skipping email to {recipient_email} due to content generation failure.")
