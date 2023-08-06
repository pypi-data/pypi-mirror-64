import json
import click
from flask import Blueprint
from .use_cases import NewRole, CreateUser
from .models import WhitelistToken

command_flask_auth = Blueprint(
    'command_flask_auth',
    __name__,
    cli_group='flask_auth'
)


@command_flask_auth.cli.command(
    'role-new',
    help="Create a Role"
)
@click.option('-n', '--name', 'name', required=True, prompt=True)
@click.option('-p', '--permissions', 'permissions',
              help='''JSON example: '{"key": "value"}' ''')
def role_new(**kwargs):
    request = dict()
    for (key, value) in kwargs.items():
        if value is not None:
            request[key] = value
    try:
        if 'permissions' in request:
            request['permissions'] = json.loads(request['permissions'])
        use_case = NewRole()
        result = use_case.handle(request)
        click.echo("Create a Role: {}. {}".format(
            result.message,
            result.errors if result.errors else ""
        ))
    except Exception as e:
        click.echo("Create a Role ERROR: {}".format(e))


@command_flask_auth.cli.command(
    'user-new',
    help='Create User'
)
@click.option('-r', '--role', required=True, prompt='Role',
              help='User role')
@click.option('-u', '--username', required=True, prompt='Username',
              help='Your username to login')
@click.option('--password', required=True, prompt=True,
              hide_input=True, confirmation_prompt=True,
              help='Your password to login')
@click.option('-f', '--funder_identifier', required=False,
              help='Funder identifier')
def new(
    role: str,
    username: str,
    password: str,
    funder_identifier: str = None
):
    click.echo('Creation of user started.')
    use_case = CreateUser()
    request = dict(
        role=role,
        username=username,
        password=password,
        password_confirmed=password
    )
    if funder_identifier:
        request['funder_identifier'] = funder_identifier
    result = use_case.handle(request)
    msn = 'NO completed!' if result.http_code >= 300 else 'completed!'
    click.echo("Creation {}: {}".format(msn, result.message))


@command_flask_auth.cli.command(
    'clear-tokens',
    help='Clear all tokens of the WhitelistToken'
)
def clear_tokens():
    WhitelistToken.drop_collection()

    click.echo('Token cleanup completed')
