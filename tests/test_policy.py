from egasub.ega.entities.policy import Policy

policy = Policy('an alias',123,'Title of DAC','Text about the policy','http://www.example.com')

def test_dac_id():
    assert policy.dac_id == 123

def test_title():
    assert policy.title == "Title of DAC"
    
def test_policy_text():
    assert policy.policy_text == "Text about the policy"
    
def test_url():
    assert policy.url == "http://www.example.com"
    
def test_to_dict():
    assert cmp({'dacId':123,'title':'Title of DAC','policyText':'Text about the policy','url':'http://www.example.com','alias':'an alias'}, policy.to_dict()) == 0
    
def test_alias():
    assert 'an alias' == policy.alias