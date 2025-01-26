from collections import defaultdict
import google_auth_oauthlib.flow
import googleapiclient.discovery
from flask import jsonify
from config import Config
import time

cached_credentials = None
last_auth_time = None
CACHE_EXPIRATION = 2 * 60 

def authenticate_google():
    global cached_credentials, last_auth_time

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", Config.SCOPES
    )

    credentials = flow.run_local_server(
        host="localhost",
        authorization_prompt_message="Please visit this URL to authorize this application: {url}",
        success_message="Authorization complete. You can close this tab.",
        open_browser=True
    )

    cached_credentials = credentials
    last_auth_time = time.time()

    return credentials


def get_google_contacts():
    global cached_credentials, last_auth_time

    if not cached_credentials or (time.time() - last_auth_time) > CACHE_EXPIRATION:
        print("Reautenticando no Google...")
        authenticate_google()

    service = googleapiclient.discovery.build(
        Config.API_SERVICE_NAME,
        Config.API_VERSION,
        credentials=cached_credentials
    )

    results = service.people().connections().list(
        resourceName="people/me",
        personFields="names,emailAddresses,phoneNumbers",
        pageSize=173
    ).execute()

    connections = results.get("connections", [])

    if not connections:
        return jsonify({"message": "No contacts found"}), 404

    domain_emails = defaultdict(list)

    for person in connections:
        email_addresses = person.get("emailAddresses", [])
        if email_addresses: 
            for email_obj in email_addresses:
                email = email_obj.get("value")
                if email:
                    domain = email.split("@")[-1]
                    domain_emails[domain].append(email)

    result = [{"domain": domain, "emails": emails} for domain, emails in domain_emails.items()]

    return jsonify(result)
