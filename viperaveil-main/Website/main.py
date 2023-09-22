# from website import create_app
# from OpenSSL import SSL
# from waitress import serve

# app = create_app()

# if __name__ == '__main__':
#     serve(app, listen="0.0.0.0:5000",connection_limit=1000,threads=1000)
from waitress import serve
from website import create_app
import logging

logger = logging.getLogger('waitress')
#logger.setLevel(logging.INFO)
logging.basicConfig(filename='waitress.log',encoding='utf-8',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = create_app()

if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0',port=5000)
    serve(app, host="0.0.0.0", port=5000, threads=100, url_scheme='https')
