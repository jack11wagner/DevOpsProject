from simple_app import app


def test_basic():
    app.config['TESTING'] = True
    client = app.test_client()

    result = client.get('/')

    assert 'Currency' in str(result.data)
