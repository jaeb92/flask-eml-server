import os

from flask import request, Blueprint
from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage
from .service.eml_service import EmlParsingService
from .utils.common import file_save

UPLOAD_FILE_PATH = f"{os.path.abspath(os.path.dirname(os.path.dirname(__file__)))}/static/upload/img"

eml_bp = Blueprint('eml', __name__)
eml_api = Namespace('eml_api', '/eml')


upload_parser = eml_api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


@eml_api.route('')
@eml_api.response(404, "Not Found")
@eml_api.response(201, "Found")
class OcrRequest(Resource):
    ALLOWED_EXTENSION = ['jpg', 'jpeg', 'gif', 'png']
    SUCCESS_CODE = [200, 201]

    eml_service = EmlParsingService()

    @eml_api.expect(upload_parser)
    def post(self):
        try:
            file = upload_parser.parse_args()['file']
            filename = file.filename

            # file save
            save_path = os.path.join(UPLOAD_FILE_PATH, filename)
            file_save(file, save_path)

            # eml parsing
            header, body, attachment = self.eml_service.get_eml_contents(save_path)
            print(header)
            print(body)

        except FileNotFoundError as fe:
            print(f"{fe}")

        # if result_code not in self.SUCCESS_CODE:
        #     return {'message': result_msg}, result_code
        #
        # print('===========================result===========================')
        # print(result_msg, result_code)
        # print('===========================================================')
        # if result_code in self.SUCCESS_CODE:
        #     ocr_result_msg, ocr_result_code = ocr_text(save_path)
        #
        # return {'message': ocr_result_msg}, ocr_result_code
