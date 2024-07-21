import os
from edsl import Model


def test_application_with_custom_env(set_env_vars):
    # use the fixture to set  new env vars
    # - SOME_KEY was not previously set
    # - OPENAI_API_KEY was previously set to "a_fake_key" by pytest.ini
    set_env_vars(OPENAI_API_KEY="a_very_fake_key", SOME_KEY="SOME_VALUE")
    assert os.getenv("SOME_KEY") == "SOME_VALUE"
    assert os.getenv("OPENAI_API_KEY") == "a_very_fake_key"
    m = Model()
    assert m.has_valid_api_key()


def test_make_sure_env_vars_were_reset():
    # now notice that in the next test the env has been reset to its original state
    assert os.getenv("SOME_KEY") is None
    assert os.getenv("OPENAI_API_KEY") == "a_fake_key"
    m = Model()
    assert m.has_valid_api_key()


# def test_model_with_missing_key(set_env_vars):
#     # you can also use the fixture to delete an env var for the duration of the test
#     set_env_vars(OPENAI_API_KEY=None)
#     assert os.getenv("OPENAI_API_KEY") is None
#     from edsl.exceptions import MissingAPIKeyError
#     import pytest
#     with pytest.raises(MissingAPIKeyError):
#         m = Model()
