import json
import time

import ujson
import cjson

if __name__ == "__main__":
    with open('generated.json', 'r', encoding='utf-8') as f:
        data = f.read()
        data_replace = data.replace('}{', '},{')
        data_loads = json.loads(data_replace)
        json_data = [json.dumps(val) for val in data_loads]
        start_time = time.time()
        dict_json = []
        for json_str in json_data:
            dict_json.append(json.loads(json_str))
        end_time = time.time()
        print(f"json load: {(end_time - start_time) * 1000} ms")
        start_time = time.time()
        for js in dict_json:
            str_json = json.dumps(js)
        end_time = time.time()
        print(f"json dump: {(end_time - start_time) * 1000} ms")
        start_time = time.time()
        dict_ujson = []
        for json_str in json_data:
            dict_ujson.append(ujson.loads(json_str))
        end_time = time.time()
        print(f"ujson load: {(end_time - start_time) * 1000} ms")
        start_time = time.time()
        for js in dict_ujson:
            str_ujson = ujson.dumps(js)
        end_time = time.time()
        print(f"ujson dump: {(end_time - start_time) * 1000} ms")
        start_time = time.time()
        dict_cjson = []
        for json_str in json_data:
            dict_cjson.append(cjson.loads(json_str))
        end_time = time.time()
        print(f"cjson load: {(end_time - start_time) * 1000} ms")
        start_time = time.time()
        for js in dict_cjson:
            str_cjson = cjson.dumps(js)
        end_time = time.time()
        print(f"cjson dump: {(end_time - start_time) * 1000} ms")
