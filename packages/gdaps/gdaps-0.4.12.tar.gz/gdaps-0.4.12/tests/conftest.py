import os

import django
from django.core import management


def pytest_addoption(parser):
    """Add option for staticfiles. Used to test the distribution."""
    parser.addoption(
        "--staticfiles",
        action="store_true",
        default=False,
        help="Run tests with static files collection, using manifest "
        "staticfiles storage. Used for testing the distribution.",
    )


def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        SECRET_KEY="test",
        BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        INSTALLED_APPS=["gdaps.core", "tests.plugins.plugin1"],
        PLUGIN1={"OVERRIDE": 20},
    )

    django.setup()
    if config.getoption("--staticfiles"):
        management.call_command("collectstatic", verbosity=0, interactive=False)
