"""Tests for the cas protocol-related code"""
from __future__ import absolute_import

import sys

import cas
import pytest
from pytest import fixture


#general tests, apply to all protocols
#
# get_login_url tests
#
def test_login_url_helper():
    client = cas.CASClientBase(
                        renew=False,
                        extra_login_params=False,
                        server_url='http://www.example.com/cas/',
                        service_url='http://testserver/'
                    )
    actual = client.get_login_url()
    expected = 'http://www.example.com/cas/login?service=http%3A%2F%2Ftestserver%2F'

    assert actual == expected


def test_login_url_helper_with_extra_params():
    client = cas.CASClientBase(
                        renew=False,
                        extra_login_params={'test': '1234'},
                        server_url='http://www.example.com/cas/',
                        service_url='http://testserver/'
                    )
    actual = client.get_login_url()
    # since the dictionary of parameters is unordered, we dont know which
    # parameter will be first, so just check that both are in the url.

    assert 'service=http%3A%2F%2Ftestserver%2F' in actual
    assert 'test=1234' in actual


def test_login_url_helper_with_renew():
    client = cas.CASClientBase(
                        renew=True,
                        extra_login_params=None,
                        server_url='http://www.example.com/cas/',
                        service_url='http://testserver/'
                    )
    actual = client.get_login_url()
    # since the dictionary of parameters is unordered, we dont know which
    # parameter will be first, so just check that both are in the url.

    assert 'service=http%3A%2F%2Ftestserver%2F' in actual
    assert 'renew=true' in actual

#
# get_logout_url tests
#
@fixture
def logout_client_v1():
    return cas.CASClient(
        version='1',
        server_url='http://www.example.com/cas/'
    )


@fixture
def logout_client_v2():
    return cas.CASClient(
        version='2',
        server_url='http://www.example.com/cas/'
    )


@fixture
def logout_client_v3():
    return cas.CASClient(
        version='3',
        server_url='http://www.example.com/cas/'
    )


def test_logout_url(logout_client_v3):
    actual = logout_client_v3.get_logout_url()
    expected = 'http://www.example.com/cas/logout'

    assert actual == expected

def test_v1_logout_url_with_redirect(logout_client_v1):
    actual = logout_client_v1.get_logout_url(
                redirect_url='http://testserver/landing-page/'
            )
    expected = 'http://www.example.com/cas/logout?url=http%3A%2F%2Ftestserver%2Flanding-page%2F'

    assert actual == expected


def test_v2_logout_url_with_redirect(logout_client_v2):
    actual = logout_client_v2.get_logout_url(
                redirect_url='http://testserver/landing-page/'
            )
    expected = 'http://www.example.com/cas/logout?url=http%3A%2F%2Ftestserver%2Flanding-page%2F'

    assert actual == expected


def test_v3_logout_url_with_redirect(logout_client_v3):
    actual = logout_client_v3.get_logout_url(
                redirect_url='http://testserver/landing-page/'
            )
    expected = 'http://www.example.com/cas/logout?service=http%3A%2F%2Ftestserver%2Flanding-page%2F'

    assert actual == expected


def test_v3_logout_url_without_redirect(logout_client_v3):
    actual = logout_client_v3.get_logout_url()
    expected = 'http://www.example.com/cas/logout'

    assert actual == expected


#cas3 responses
@fixture
def client_v3():
    return cas.CASClient(
        version='3',
        server_url='https://cas.example.com/cas/',
        service_url='https://example.com/login')

SUCCESS_RESPONSE = """<?xml version=\'1.0\' encoding=\'UTF-8\'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>user@example.com</cas:user></cas:authenticationSuccess></cas:serviceResponse>
"""
def test_cas3_basic_successful_response_verification(client_v3):
    user, attributes, pgtiou = client_v3.verify_response(SUCCESS_RESPONSE)

    assert user == 'user@example.com'
    assert not attributes
    assert not pgtiou


SUCCESS_RESPONSE_WITH_ATTRIBUTES = """<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>user@example.com</cas:user><cas:attributes><cas:foo>bar</cas:foo><cas:baz>1234</cas:baz></cas:attributes></cas:authenticationSuccess></cas:serviceResponse>
"""
def test_cas3_successful_response_verification_with_attributes(client_v3):
    user, attributes, pgtiou = client_v3.verify_response(SUCCESS_RESPONSE_WITH_ATTRIBUTES)

    assert user == 'user@example.com'
    assert not pgtiou
    assert attributes['foo'] == 'bar'
    assert attributes['baz'] == '1234'


SUCCESS_RESPONSE_WITH_PGTIOU = """<?xml version=\'1.0\' encoding=\'UTF-8\'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>user@example.com</cas:user><cas:proxyGrantingTicket>PGTIOU-84678-8a9d</cas:proxyGrantingTicket></cas:authenticationSuccess></cas:serviceResponse>
"""
def test_successful_response_verification_with_pgtiou(client_v3):
    user, attributes, pgtiou = client_v3.verify_response(SUCCESS_RESPONSE_WITH_PGTIOU)

    assert user == 'user@example.com'
    assert pgtiou == 'PGTIOU-84678-8a9d'


FAILURE_RESPONSE = """<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationFailure code="INVALID_TICKET">service ticket ST-1415306486-qs5TfUWlwge23u013h8fivR21RklkeWI has already been used</cas:authenticationFailure></cas:serviceResponse>
"""
def test_unsuccessful_response(client_v3):
    user, attributes, pgtiou = client_v3.verify_response(FAILURE_RESPONSE)
    assert user is None
    assert not pgtiou
    assert not attributes

def test_proxy_url(client_v3):
    tgt = 'tgt-1234'
    proxy_url_string = client_v3.get_proxy_url(tgt)
    assert proxy_url_string == 'https://cas.example.com/cas//proxy?pgt=tgt-1234&targetService=https%3A%2F%2Fexample.com%2Flogin' or proxy_url_string == 'https://cas.example.com/cas//proxy?targetService=https%3A%2F%2Fexample.com%2Flogin&pgt=tgt-1234'

#test CAS+SAML protocol
def test_can_saml_assertion_is_encoded():
    ticket = 'test-ticket'

    client = cas.CASClient(version='CAS_2_SAML_1_0')
    saml = client.get_saml_assertion(ticket)

    if sys.version_info > (3, 0):
        assert type(saml) is bytes
        assert ticket.encode('utf-8') in saml
    else:
        assert ticket in saml


@fixture
def client_v2():
    return cas.CASClientV2()


SUCCESS_RESPONSE_WITH_JASIG_ATTRIBUTES = """<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>someuser</cas:user><cas:attributes><cas:attraStyle>Jasig</cas:attraStyle><cas:nombroj>unu</cas:nombroj><cas:nombroj>du</cas:nombroj><cas:nombroj>tri</cas:nombroj><cas:nombroj>kvar</cas:nombroj><cas:email>someuser@example.com</cas:email></cas:attributes></cas:authenticationSuccess></cas:serviceResponse>
"""
def test_cas2_jasig_attributes(client_v2):
    user, attributes, pgtiou = client_v2.verify_response(SUCCESS_RESPONSE_WITH_JASIG_ATTRIBUTES)
    assert user == 'someuser'
    expected_attributes = {
        'email': 'someuser@example.com',
        'nombroj': ['unu', 'du', 'tri', 'kvar'],
    }
    assert attributes == expected_attributes

SUCCESS_RESPONSE_WITH_NON_STANDARD_USER_NODE = """<?xml version="1.0" encoding="UTF-8"?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:utilisateur><cas:displayName>John Doe</cas:displayName><cas:user>someuser</cas:user><cas:uid>someuser</cas:uid></cas:utilisateur></cas:authenticationSuccess></cas:serviceResponse>
"""
def test_cas2_non_standard_user_node(client_v2):
    user, attributes, pgtiou = client_v2.verify_response(SUCCESS_RESPONSE_WITH_NON_STANDARD_USER_NODE)
    assert user == 'someuser'


def test_unsupported_protocol_version():
    with pytest.raises(ValueError):
        cas.CASClient(version='unknown')

def test_verify_logout_request_invalid_parameters():
    client = cas.CASClientWithSAMLV1()
    assert not client.verify_logout_request('', '')

def test_verify_logout_request_success():
    client = cas.CASClientWithSAMLV1()
    logout_request = '''
<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
   ID="[RANDOM ID]" Version="2.0" IssueInstant="[CURRENT DATE/TIME]">
  <saml:NameID xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
    @NOT_USED@
  </saml:NameID>
  <samlp:SessionIndex>st-1234</samlp:SessionIndex>
</samlp:LogoutRequest>
    '''
    ticket = 'st-1234'
    assert client.verify_logout_request(logout_request, ticket)

def test_verify_logout_request_invalid_st():
    client = cas.CASClientWithSAMLV1()
    logout_request = '''
<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
   ID="[RANDOM ID]" Version="2.0" IssueInstant="[CURRENT DATE/TIME]">
  <saml:NameID xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
    @NOT_USED@
  </saml:NameID>
  <samlp:SessionIndex>st-1234</samlp:SessionIndex>
</samlp:LogoutRequest>
    '''
    ticket = 'st-not-match'
    assert not client.verify_logout_request(logout_request, ticket)
