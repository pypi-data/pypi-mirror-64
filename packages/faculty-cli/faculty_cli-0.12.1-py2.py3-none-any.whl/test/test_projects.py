import pytest
from click.testing import CliRunner

from faculty_cli.cli import cli
from faculty.clients.project import ProjectClient
import faculty.clients.base
from test.fixtures import PROJECT, USER_ID


@pytest.fixture
def mock_update_check(mocker):
    mocker.patch("faculty_cli.update.check_for_new_release")


@pytest.fixture
def mock_check_credentials(mocker):
    mocker.patch("faculty_cli.cli._check_credentials")


@pytest.fixture
def mock_user_id(mocker):
    mocker.patch("faculty_cli.auth.user_id", return_value=USER_ID)


def test_list_projects(
    mocker,
    mock_update_check,
    mock_check_credentials,
    mock_profile,
    mock_user_id,
):
    runner = CliRunner()
    schema_mock = mocker.patch("faculty.clients.project.ProjectSchema")
    mocker.patch.object(ProjectClient, "_get", return_value=[PROJECT])

    result = runner.invoke(cli, ["project", "list"])

    assert result.exit_code == 0
    assert result.output == PROJECT.name + "\n"

    ProjectClient._get.assert_called_once_with(
        "/user/{}".format(USER_ID), schema_mock.return_value
    )


def test_list_projects_verbose(
    mocker,
    mock_update_check,
    mock_check_credentials,
    mock_profile,
    mock_user_id,
):
    runner = CliRunner()
    schema_mock = mocker.patch("faculty.clients.project.ProjectSchema")
    mocker.patch.object(ProjectClient, "_get", return_value=[PROJECT])

    result = runner.invoke(cli, ["project", "list", "-v"])

    tpl = "Project Name    ID\n{}    {}\n"

    assert result.exit_code == 0
    assert result.output == tpl.format(PROJECT.name, PROJECT.id)

    ProjectClient._get.assert_called_once_with(
        "/user/{}".format(USER_ID), schema_mock.return_value
    )


def test_create_project(
    mocker,
    mock_update_check,
    mock_check_credentials,
    mock_profile,
    mock_user_id,
):
    runner = CliRunner()

    mocker.patch.object(ProjectClient, "create", return_value=PROJECT)
    result = runner.invoke(cli, ["project", "new", "test-project"])

    assert result.exit_code == 0
    assert result.output == "Created project {} with ID {}\n".format(
        PROJECT.name, PROJECT.id
    )

    ProjectClient.create.assert_called_once_with(USER_ID, "test-project")


def test_create_project_bad_request(
    mocker,
    mock_update_check,
    mock_check_credentials,
    mock_profile,
    mock_user_id,
):
    runner = CliRunner()
    response = faculty.clients.base.BadRequest("response", error="some error")
    mocker.patch.object(ProjectClient, "create", side_effect=response)

    result = runner.invoke(cli, ["project", "new", "test-project"])

    assert result.exit_code == 64
    assert result.output == "some error\n"
