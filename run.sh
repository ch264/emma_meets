# keep at run file and run bash shell. Keep this values secred and do not check them into source control!

# redirect to URI you set up earlier
export FN_AUTH_REDIRECT_URI=http://localhost:5000/google/auth
export FN_BASE_URI=http://localhost:5000
# client ID you saved earlier
export FN_CLIENT_ID=T110906266153-gq3b4tr0daql4h79p4eh9nkegcff3831.apps.googleusercontent.com
# client Secret you saved earlier
export FN_CLIENT_SECRET=T4B7YUAggeupJC36DVbghtach

export FLASK_APP=google_auth.py
export FLASK_DEBUG=1
# random value which will be used for encrypting the cookie in the Flask session
export FN_FLASK_SECRET_KEY=pickles


python -m flask run -p 5000