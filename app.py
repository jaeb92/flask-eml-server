from flask import Flask
from flask_restx import Api
from eml.eml_route import eml_api, eml_bp

app = Flask(
    __name__,
    static_url_path='',
    static_folder='',
    template_folder=''
)

app.register_blueprint(eml_bp, url_prefix="/ocr")
api = Api(
    app,
    version='0.0.1',
    title='flask api test',
    description='flask api test version',
    terms_url='/',
    license='cslee'
)

api.add_namespace(eml_api, '/ocr')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8888)