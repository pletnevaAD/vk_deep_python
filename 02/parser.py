import json
from inspect import signature


def parse_json(json_str: str, required_fields=None, keywords=None, keyword_callback=None):
    if not json_str:
        raise ValueError("Empty JSON string")
    if required_fields and keywords and keyword_callback:
        if len(signature(keyword_callback).parameters) > 2:
            raise TypeError("Wrong number of arguments in keyword_callback")
        json_doc = json.loads(json_str)
        for key, value in json_doc.items():
            if key in required_fields:
                for word in value.split():
                    if word in keywords:
                        keyword_callback(key, word)
                    else:
                        continue
            else:
                continue
    else:
        raise ValueError("Pass not none arguments")
