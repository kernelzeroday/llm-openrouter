import llm
import pytest
from click.testing import CliRunner
from llm.cli import cli


@pytest.mark.vcr
def test_web_plugin():
    """Test the web plugin functionality."""
    model = llm.get_model("openrouter/openai/gpt-4o")
    # Try to use the online option which should trigger the web plugin
    response = model.prompt("Get the latest news from Hacker News", options={"online": True})
    assert response is not None