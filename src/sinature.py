from keys import huobi_ak, huobi_sk
import hashlib, hmac
import base64
from urllib import quote
import urllib2

domain = "api.huobipro.com"


class Signature(object):
    @staticmethod
    def huobi_signature(params, method, path):
        def aggregate_params():
            sorted_parameters = sorted(params.items(), key=lambda p: p[0], reverse=False)

            c_query_str = ''
            first = True
            for (k, v) in sorted_parameters:
                if first:
                    c_query_str += quote(k) + '=' + quote(v)
                    first = False
                else:
                    c_query_str += "&" + quote(k) + '=' + quote(v)
            print c_query_str
            return c_query_str

        def aggregate_signature():
            signature_str = "%s\n%s\n%s\n%s\n" % (method, domain, path, aggregate_params())
            return base64.b64encode(
                hmac.new(huobi_sk.encode('utf-8'), signature_str.encode('utf-8'), hashlib.sha256).digest())

        return aggregate_signature()


import time

now = int(time.time()) - 8 * 3600
print time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now))
params = {"AccessKeyId": huobi_ak,
          "SignatureMethod": "HmacSHA256",
          "SignatureVersion": "2",
          "Timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now))}

Signature.huobi_signature(params, "GET", "/v1/account/accounts")

p = ""
for k, v in params.items():
    p += "%s=%s&" % (k, quote(v))
p += "Signature=%s" % Signature.huobi_signature(params, "GET", "/v1/account/accounts")
request = urllib2.Request("http://api.huobipro.com/v1/account/accounts?" + p)
request.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
response = urllib2.urlopen(request)
print response.read()
