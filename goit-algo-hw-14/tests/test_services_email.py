import pytest
from unittest.mock import patch, AsyncMock
from src.services.email import send_email

@pytest.fixture
def email_details():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "host": "http://testhost.com"
    }

@pytest.fixture
def mock_auth_service():
    with patch("src.services.auth.Auth.create_email_token") as mock_create_email_token:
        mock_create_email_token.return_value = "fake_token"
        yield mock_create_email_token

@pytest.fixture
def mock_fastmail():
    with patch("src.services.email.FastMail") as mock_fastmail:
        mock_instance = mock_fastmail.return_value
        mock_instance.send_message = AsyncMock()
        yield mock_instance

@pytest.mark.asyncio
async def test_send_email_success(email_details, mock_auth_service, mock_fastmail):
    await send_email(email_details["email"], email_details["username"], email_details["host"])

    mock_auth_service.assert_called_once_with({"sub": email_details["email"]})
    mock_fastmail.send_message.assert_called_once()
    message = mock_fastmail.send_message.call_args[0][0]
    assert message.subject == "Confirm your email"
    assert message.recipients == [email_details["email"]]
    assert message.template_body["host"] == email_details["host"]
    assert message.template_body["username"] == email_details["username"]
    assert message.template_body["token"] == "fake_token"
    assert message.subtype == "html"

@pytest.mark.asyncio
async def test_send_email_connection_error(email_details, mock_auth_service, mock_fastmail):
    mock_fastmail.send_message.side_effect = Exception("Connection error")

    with patch("builtins.print") as mock_print:
        await send_email(email_details["email"], email_details["username"], email_details["host"])
        mock_print.assert_called_once_with("Connection error")
