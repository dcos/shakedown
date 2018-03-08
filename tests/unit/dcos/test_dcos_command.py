from shakedown.dcos import command

class MockConnection:

    def __init__(self, h, u, k, failure=False):
        self.h = h
        self.u = u
        self.k = k
        self.failure = failure

    def open_session(self):
        if not self.failure:
            return self.h, self.u, self.k
        return None

def test_hostsession_enter(monkeypatch):
    """Test that `get_session` calls `_get_connection` for a 
    connection and then opens a new session.
    """
    def mockreturn(h, u, k):
        return MockConnection(h, u, k)
    # replace _get_connection with mockreturn
    monkeypatch.setattr(command, '_get_connection', mockreturn)

    hs = command.HostSession('local', 'me', 'key', True)
    v = hs.__enter__()
    assert v is not None
    assert hs.host == 'local'
    assert hs.session[0] == 'local'

def test_hostsession_enter_fail(monkeypatch):
    """Test that `get_session` calls `_get_connection` for a 
    connection and then opens a new session.
    """
    def mockreturn(h, u, k):
        return MockConnection(h, u, k, True)
    # replace _get_connection with mockreturn
    monkeypatch.setattr(command, '_get_connection', mockreturn)

    hs = command.HostSession('local', 'me', 'key', True)
    v = hs.__enter__()
    assert v is not None
    assert hs.host == 'local'
    assert hs.session is None
