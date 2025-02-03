"""Main place to adjust pytest settings and creating global fixtures."""

MARKER = """\
unit: Mark unit test
integration: Mark integration test
high: High priority
medium: Medium priority
low: Low priority
"""


def pytest_configure(config):
    map(
        lambda line: config.addinivalue_line("markers", line),
        MARKER.split("\n"),
    )
