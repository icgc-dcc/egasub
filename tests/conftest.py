import pytest
import httpretty
import logging

class test_ctx(object):
    def __init__(self):
        self.obj = {}
        self.obj['SETTINGS'] = {}
        self.obj['SETTINGS']['apiUrl'] = 'http://example.com/'
        self.obj['SUBMISSION'] = {}
        
        logger = logging.getLogger('ega_submission')
        self.obj['LOGGER'] = logger
        
test_ctx = test_ctx()



@pytest.fixture(scope="session")
def ctx():
    return test_ctx

@pytest.fixture(scope="session")
def mock_server(ctx):
    httpretty.enable()
    
    httpretty.register_uri(httpretty.POST,"%slogin" % (ctx.obj['SETTINGS']['apiUrl']),
                       body='{"header":{"code" : "200"},"response" : {"result" : [ { "session" : { "sessionToken":"abcdefg" }}]}}',
                       content_type="application/json")
    
    httpretty.register_uri(httpretty.POST,"%ssubmissions" % (ctx.obj['SETTINGS']['apiUrl']),
                       body='{"header" : {"code" : "200"}, "response" : {"result" : [{ "id":"12345" }]}}',
                       content_type="application/json")
    
    httpretty.register_uri(httpretty.DELETE, "%slogout" % (ctx.obj['SETTINGS']['apiUrl']),
                       content_type="application/json")
    
    httpretty.register_uri(httpretty.POST, "%ssubmissions/12345/studies" % (ctx.obj['SETTINGS']['apiUrl']),
                           body='{"header" : {"code" : "200"}, "response" : {"result" : [{ "id":"6789" }]}}',
                   content_type="application/json")
    
    httpretty.register_uri(httpretty.PUT, "%sstudies/6789?action=VALIDATE" % (ctx.obj['SETTINGS']['apiUrl']),
                           body='{"header" : {"code" : "200"}, "response" : {"result" : [{ "id":"12345" }]}}',
                   content_type="application/json")
    
    httpretty.register_uri(httpretty.GET, "%sstudies/test_alias?idType=ALIAS" % (ctx.obj['SETTINGS']['apiUrl']),
                           body='{"header" : {"code" : "200"}, "response" : {"result" : [{ "id":"12345" }]}}',
                   content_type="application/json")
    
