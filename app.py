from flask import Flask, request, render_template, send_from_directory, abort
import os

app = Flask(__name__)



# Your secret 20-digit PIN (example)
SECRET_PIN = "12345678901234567890"  # Replace with actual secret PIN

@app.before_request
def limit_remote_addr():
    client_ip = request.remote_addr
    if client_ip not in ALLOWED_IPS:
        return "Access Denied: Your IP is not allowed.", 403

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sounds')
def sounds_page():
    return render_template('sounds.html')

@app.route('/sounds/beep')
def music():
    music_dir = os.path.join(app.root_path, 'sounds')
    return send_from_directory(music_dir, 'beep.wav', as_attachment=True)

@app.route('/pin', methods=['GET', 'POST'])
def pin_auth():
    error = None
    flag_content = None

    if request.method == 'POST':
        user_pin = request.form.get('pin', '').strip()
        if user_pin == SECRET_PIN:
            flag_path = os.path.join(app.root_path, 'protected', 'flag.txt')
            try:
                with open(flag_path, 'r') as f:
                    flag_content = f.read()
            except FileNotFoundError:
                error = "Flag file not found."
        else:
            error = "Incorrect PIN. Access denied."

    return render_template('pin.html', error=error, flag=flag_content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
