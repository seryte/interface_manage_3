import pytest


# def test_main():
#     """
#     6666
#     :return:
#     """
#     assert 5 == 5


@pytest.mark.parametrize(("name", "password"), [
    ["user1", "psd1"],
    ["user2", "psd2"],
])
def test_login(name, password):
    assert "user1" == name

# if __name__ == "__main__":
#     pytest.main(["test-demo2.py"])
