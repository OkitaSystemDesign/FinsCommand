from finscom import fins

def test_create():
    f = fins("127.0.0.1")
    assert f is not None
    