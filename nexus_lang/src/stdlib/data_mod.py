"""
Sapphire Data Processing & Formatting Standard Library
"""
import json
import csv
import io
import hashlib
import base64

class DataModule:
    @staticmethod
    def parse_json(str_data: str) -> any:
        return json.loads(str_data)

    @staticmethod
    def to_json(val: any, indent: int = 2) -> str:
        return json.dumps(val, indent=indent, default=str)

    @staticmethod
    def parse_csv(csv_str: str) -> list[dict]:
        reader = csv.DictReader(io.StringIO(csv_str.strip()))
        return list(reader)

    @staticmethod
    def to_csv(records: list[dict]) -> str:
        if not records:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)
        return output.getvalue()

    @staticmethod
    def sha256(text: str) -> str:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    @staticmethod
    def base64_encode(text: str) -> str:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    @staticmethod
    def base64_decode(encoded: str) -> str:
        return base64.b64decode(encoded.encode('utf-8')).decode('utf-8')
