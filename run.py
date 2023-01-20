from dotenv import load_dotenv

import server


load_dotenv()
app = server.create_app()

if __name__ == '__main__':
    if server.CONFIG.DEBUG:
        app.run(debug=True, host='0.0.0.0')
