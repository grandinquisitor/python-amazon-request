import base64
import hashlib
import hmac
import time
import urllib
 
def get_signed(url_params, access_key, secret):
    # Sort the URL parameters by key

    url_params['AWSAccessKeyId'] = access_key
    url_params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

    keys = url_params.keys()
    keys.sort()
    # Get the values in the same order of the sorted keys
    values = map(url_params.get, keys)
     
    # Reconstruct the URL paramters and encode them
    url_string = urllib.urlencode( zip(keys,values) )
    url_string = url_string.replace('+'," ") 
    url_string = url_string.replace(':',":") 
     
    #Construct the string to sign
    string_to_sign = "GET\necs.amazonaws.com\n/onca/xml\n%s" % url_string

    h = hmac.new(secret, string_to_sign, hashlib.sha256)
    signature = base64.b64encode(h.digest())
    base_url = "http://ecs.amazonaws.com/onca/xml"
    request = "%s?%s&Signature=%s" % (base_url,url_string,urllib.quote(signature))

    return request

if __name__ == '__main__':

    AWS_ACCESS_KEY_ID = "Your Access Key ID"
    AWS_SECRET_ACCESS_KEY = "Your Secret Key"
 
    url_params = {
        'Operation':"ItemSearch",
        'Service':"AWSECommerceService",
        'ItemPage':"1",
        'ResponseGroup':"Images,ItemAttributes",
        "SearchIndex":"Books",
        'Keywords':"Monkees"
    }
 
    print get_signed(url_params,AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
