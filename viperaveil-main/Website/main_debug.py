import logging
import os
os.environ.setdefault('DEBUG_MODE', 'True')
from website import create_app

app = create_app()
logging.basicConfig(filename='waitress.log',encoding='utf-8',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    # serve(app, host="0.0.0.0", port=5000, threads=100, url_scheme='http')
    app.run(debug=True, host='0.0.0.0', port=5000)
