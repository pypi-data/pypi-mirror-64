import pytest
from unittest.mock import patch, Mock

TENANT_NAME = 'pycarol'
APP_NAME = 'my_app'
USERNAME = 'pycarol@totvs.com.br'
PASSWORD = 'foo123'


def test_password_login():
    from pycarol import PwdAuth, Carol
    login = Carol(domain=TENANT_NAME, app_name=APP_NAME, auth=PwdAuth(user=USERNAME, password=PASSWORD))
    assert login.auth._token.access_token is not None
    assert login.auth._token.refresh_token is not None
    assert login.auth._token.expiration is not None


def test_APIKEY_create_and_revoke():
    from pycarol import ApiKeyAuth, Carol, PwdAuth
    login = Carol(domain=TENANT_NAME, app_name=APP_NAME, auth=PwdAuth(user=USERNAME, password=PASSWORD))

    api_key = login.issue_api_key()

    assert api_key['X-Auth-Key']
    assert api_key['X-Auth-ConnectorId']

    X_Auth_Key = api_key['X-Auth-Key']
    X_Auth_ConnectorId = api_key['X-Auth-ConnectorId']

    print(f"This is a API key {api_key['X-Auth-Key']}")
    print(f"This is the connector Id {api_key['X-Auth-ConnectorId']}")

    revoke = login.api_key_revoke(connector_id=X_Auth_ConnectorId)

    assert revoke['success']




def test_mock_password_login():
    from pycarol import PwdAuth, Carol

    mock_tenant = patch('pycarol.tenant.Tenant.get_tenant_by_domain')
    mock_get_tenant = mock_tenant.start()
    mock_get_tenant.return_value = Mock(status_code=200)
    mock_get_tenant.return_value.json.return_value = {}

    """Mocking a whole function"""
    mock_get_patcher = patch('pycarol.carol.Carol.call_api')
    response = {
        "access_token": "213133213231321231",
        "refresh_token": "asdasdasdads23123",
        "timeIssuedInMillis": 123456,
        "expires_in": 3600
    }

    mock_get = mock_get_patcher.start()
    mock_get.return_value = response

    login = Carol(domain=TENANT_NAME, app_name=APP_NAME, auth=PwdAuth(user=USERNAME, password=PASSWORD))

    assert login.auth._token.access_token is not None
    assert login.auth._token.refresh_token is not None
    assert login.auth._token.expiration is not None

    mock_get_patcher.stop()
    mock_tenant.stop()










