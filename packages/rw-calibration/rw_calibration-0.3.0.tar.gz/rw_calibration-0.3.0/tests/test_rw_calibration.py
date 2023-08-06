#!/usr/bin/env python

"""Tests for `rw_calibration` package."""

import pytest

from click.testing import CliRunner

from rw_calibration import rw_calibration
from rw_calibration import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()

    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "Error: please indicate the path to World Coordinates File" in result.output

    result = runner.invoke(cli.main, ["-w", "world_sample.txt"])
    assert result.exit_code == 0
    assert "Error: please indicate the path to Robot Coordinates File" in result.output

    # result = runner.invoke(
    #    cli.main, ["-w", "world_sample.txt", "-r", "robot_sample.txt"]
    # )
    # assert result.exit_code == 0
    # assert "rw_calibration.cli.main" in result.output

    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    # assert "--help  Show this message and exit." in help_result.output
