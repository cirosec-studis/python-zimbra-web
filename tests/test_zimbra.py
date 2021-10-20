from zimbra import ZimbraUser
import os
import pkg_resources


def test_failing_authentication():
    username = os.environ["ZIMBRA_USERNAME"]
    password = "INCORRECT123"
    user = ZimbraUser(url="https://studgate.dhbw-mannheim.de")
    assert not user.login(username, password)
    assert not user.authenticated


def test_send_email(zimbra_user: ZimbraUser, identifier: str):
    response = zimbra_user.send_mail(f"{zimbra_user.session_data.username}@student.dhbw-mannheim.de",
                                     "[PYTEST] Zimbra Mail", f"{identifier}Hello, world!")
    assert response.success
    assert response.message == "Ihre Mail wurde gesendet."


def test_send_utf8(zimbra_user: ZimbraUser, identifier: str):
    unicodes = pkg_resources.resource_stream(__name__, "templates/unicode.txt").read().decode("utf8")
    response = zimbra_user.send_mail(f"{zimbra_user.session_data.username}@student.dhbw-mannheim.de",
                                     "[PYTEST] Unicode Test", f"{identifier}Unicodes: {unicodes}")
    assert response.success
    assert response.message == "Ihre Mail wurde gesendet."
