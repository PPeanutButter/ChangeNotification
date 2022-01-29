class HCYRequest:

    def __init__(self, url: str = "", method: str = "", base_headers=None, **super_headers):
        """Constructs and sends a :class:`Request <Request>`.

            :param base_headers: 提供一个通用的，适合所有请求的headers缺省值，如: User-Agent.
            :param super_headers: 提供一个通用的，适合所有请求的headers替换值，如: Cookie.
        """
        self.url = url
        self.method = method
        self.headers = None
        self.base_headers = base_headers
        self.super_headers = super_headers
        self.params = None
        self.json = None
        self.data = None

    def set_headers(self, headers):
        self.headers = headers

    def set_params(self, params):
        self.params = params

    def set_json(self, _json):
        if not _json:
            return
        if self.method.upper() != 'POST':
            raise AssertionError("Only 'POST' support json data")
        if _json and not isinstance(_json, dict):
            raise AssertionError("Please use 'set_data' instead")
        self.json = _json

    def set_data(self, data):
        if not data:
            return
        if self.method.upper() != 'POST':
            raise AssertionError("Only 'POST' support 'data' data")
        self.data = data

    def values(self):
        return self.method, self.url, self.headers, self.params, self.json, self.data

    def build_from_hcy(self, hcy: str, **super_headers):
        """Constructs and sends a :class:`Request <Request>`.

            :param hcy: 非通用的hcy文件路径，通常只有两行， 如：
                GET /?a=b h2
                HOST: Baidu.com
            :param super_headers: 提供特定请求的一次性的headers替换值，如: Token.
        """
        method, url, headers, params, json, data = build_request_from_hcy(hcy, False).values()
        self.method = method
        self.url = url
        self.headers = load_base_headers(super_headers, headers)
        self.params = params
        self.json = json
        self.data = data
        return self

    def request(self):
        import requests
        if self.base_headers:
            self.headers = load_base_headers(super_headers=self.headers, base_headers=self.base_headers)
        if self.super_headers:
            self.headers = load_base_headers(super_headers=self.super_headers, base_headers=self.headers)
        # json to kv
        form_data = None
        if isinstance(self.data, dict):
            form_data = '&'.join([f'{k}={v}' for k, v in self.data.items()])
        return requests.request(method=self.method,
                                url=self.url,
                                headers=self.headers,
                                params=self.params,
                                data=self.data if not form_data else form_data,
                                json=self.json)


def build_request_from_hcy(hcy: str, override_headers=True) -> HCYRequest:
    import json
    import os
    method = ""
    url = ""
    http_schema = ""
    headers = {}
    params = {}
    json_data = None
    form_data = None
    with open(hcy, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.isspace():
                continue
            line = line.strip('\n')
            if str(line).startswith("GET ") or str(line).startswith("POST "):
                protocal = line.split(" ")
                method = protocal[0].upper()
                http_schema = "http://" if protocal[2] == "HTTP/1.0" else "https://"
                url = protocal[1]
                param = url.split("?")
                url = param[0]
                if len(param) > 1:
                    param = param[1].split("&")
                    for p in param:
                        key_value = p.split("=")
                        key, value = (key_value[0], key_value[1]) if len(key_value) > 1 else (key_value[0], "")
                        params[key] = value
            else:
                key_value = line.split(": ")
                if line.strip().startswith("{"):
                    # json body
                    json_data = json.loads(line)
                elif line.find(":") == -1:
                    # form body
                    if line.find("="):
                        # kv to json
                        form_data = {}
                        param = line.split("&")
                        for p in param:
                            key_value = p.split("=")
                            key, value = (key_value[0], key_value[1]) if len(key_value) > 1 else (key_value[0], "")
                            form_data[key] = value
                else:
                    # headers
                    key, value = (key_value[0], key_value[1]) if len(key_value) > 1 else (key_value[0], "")
                    if (key.lower() == 'cookie') and 'cookie' in headers:
                        headers['cookie'] = headers['cookie'] + ";" + value
                    else:
                        headers[key] = value
    if url and 'Host' in headers:
        url = http_schema + headers['Host'] + url
    if os.path.exists(hcy[:hcy.rfind('/') + 1] + "super.hcy") and override_headers:
        # overrides headers
        with open(hcy[:hcy.rfind('/') + 1] + "super.hcy", 'r', encoding='utf-8') as f:
            for line in f.readlines():
                key_value = line.split(": ")
                key, value = (key_value[0], key_value[1]) if len(key_value) > 1 else (key_value[0], "")
                headers[key] = value.strip('\n')
    if not params:
        params = None
    hcy = HCYRequest(method=method, url=url)
    hcy.set_headers(headers)
    hcy.set_params(params)
    hcy.set_json(json_data)
    hcy.set_data(form_data if form_data else None)
    return hcy


def load_base_headers(super_headers, base_headers):
    if isinstance(super_headers, str):
        _, _, default_headers, _, _, _ = build_request_from_hcy(base_headers, override_headers=False).values()
        super_headers = default_headers
    if isinstance(base_headers, str):
        _, _, default_headers, _, _, _ = build_request_from_hcy(base_headers, override_headers=False).values()
        base_headers = default_headers
    if not super_headers:
        return base_headers
    for k, v in super_headers.items():
        base_headers[k] = v
    return base_headers
