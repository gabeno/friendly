from unittest.mock import patch
from friendly.tasks import set_user_metadata


@patch("friendly.tasks.set_user_metadata.run")
def test_mock_task(mock_run):
    assert set_user_metadata.run(1, "0.0.0.0")
    set_user_metadata.run.assert_called_once_with(1, "0.0.0.0")

    set_user_metadata.run(2, "1.1.1.1")
    assert set_user_metadata.run.call_count == 2
