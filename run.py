from app import app, re
from services import get_google_contacts, authenticate_google


@app.route('/')
def home():
    return "Hello, World!"

@app.route('/contacts')
def contacts():
    return get_google_contacts()

@app.route('/authenticate')
def authenticate():
    return authenticate_google()

@app.route('/oauthconectasuite48')
def oauth2callback():
    code = re.args.get('code')
    return f"Authorization code: {code}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)