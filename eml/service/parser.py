import os
import base64
from datetime import datetime
from eml_parser.eml_parser import EmlParser
from bs4 import BeautifulSoup


class FileReader():
    def __init__(self) -> None:
        print('FileReader Initialized')

    def is_valid_file(self, path) -> int:
        if not os.path.exists(path):
            return -1

        return 1

    def check_extension(self, path) -> None:
        filename, ext = path.split('.')
        return ext

    def file_open(self, path) -> None:
        if self.is_valid_file(path) == 1:
            with open(path, 'rb') as f:
                return f.read()

        elif self.is_valid_file(path) == -1:
            print(f"{path} doesn't exists.")
            raise FileNotFoundError

        else:
            raise Exception


class Parser(FileReader):
    IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'raw']

    def __init__(self) -> None:
        self.parser = EmlParser(
            include_attachment_data=True,
            include_raw_body=True,
        )

    def parse(self, bytes_text: bytes):
        result = self.parser.decode_email_bytes(bytes_text)
        return result

    def get_header(self, parsed_eml: dict) -> dict:
        email_headers = parsed_eml['header']
        email_title = self.get_email_title(email_headers)
        email_date = self.get_email_date(email_headers)
        email_from = self.get_email_from(email_headers)
        email_to = self.get_email_to(email_headers)
        email_cc = self.get_email_cc(email_headers)
        email_bcc = self.get_email_bcc(email_headers)

        header = dict(
            email_title=email_title,
            email_from=email_from,
            email_to=email_to,
            emil_date=email_date,
            email_cc=email_cc,
            email_bcc=email_bcc
        )
        return header

    def get_body(self, parsed_eml: dict) -> dict:
        email_body = parsed_eml['body'][-1]
        email_contents = self.get_email_body_contents(email_body)
        body = dict(
            email_contents=email_contents
        )

        return body

    def get_attachment(self, parsed_eml: dict):
        if 'attachment' not in parsed_eml:
            return 'No Attachment'

        attach = parsed_eml['attachment']
        email_attachment = self.get_email_attachment(attach)

        attachment = dict(
            email_attachment=email_attachment
        )

        return attachment

    def get_email_title(self, header_dict: dict) -> str:
        if 'subject' not in header_dict:
            return 'No Title'

        return header_dict['subject']

    def get_email_from(self, header_dict: dict):
        return header_dict['from']

    def get_email_to(self, header_dict: dict):
        return header_dict['to']

    def get_email_cc(self, header_dict: dict):
        if 'cc' not in header_dict:
            return []

        return header_dict['cc']

    def get_email_bcc(self, header_dict: dict):
        if 'bcc' not in header_dict:
            return []

        return header_dict['bcc']

    def get_email_date(self, header_dict: dict):
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
        return header_dict['date'].strftime(DATETIME_FORMAT)

    def get_email_body_contents(self, body_dict: dict):
        return BeautifulSoup(body_dict['content'], 'html.parser').get_text(strip=True)

    def get_email_attachment(self, attachment_list: list):
        attachments = {'body_image': [], 'attachment_image_raw': [], 'attachment_file_raw': []}

        for attach in attachment_list:
            attach_ext = self.check_attachment_extension(attach)
            disposition = attach['content_header']['content-disposition']
            b64_raw = attach['raw']

            if 'inline' in disposition[-1]:  # 본문 이미지
                if attach_ext in self.IMAGE_EXTENSIONS:
                    attachments['body_image'].append(b64_raw)

            elif 'attachment' in disposition[-1]:  # 첨부 파일(이미지, 문서 등)
                if attach_ext in self.IMAGE_EXTENSIONS:
                    attachments['attachment_image_raw'].append(b64_raw)
                else:
                    attachments['attachment_file_raw'].append(b64_raw)

        return attachments

    def check_attachment_extension(self, attachment_dict: dict):
        return attachment_dict['extension']
        # print(attachment_dict['extension'])
