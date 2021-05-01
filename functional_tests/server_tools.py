import os

MANAGE_DOT_PY = 'python3 manage.py'


def format_app_name(function):
    def inner(staging_server, *args):
        staging_server = staging_server.split('.')[0]
        result = function(staging_server, *args)
        return result
    return inner

@format_app_name
def reset_database(staging_server):
    os.system(f'heroku pg:reset --app={staging_server} --confirm {staging_server}')
    os.system(f"heroku run '{MANAGE_DOT_PY} makemigrations && {MANAGE_DOT_PY} migrate' --app=rs-django-todo-list-staging")

@format_app_name
def _get_server_env_vars(staging_server):
    env_vars = os.popen(f'heroku run  env  --app={staging_server}').read().split('\n')
    env_vars = [vars.split('=') for vars in env_vars]
    env_vars_filtered = list(filter(lambda container: len(container) != 1, env_vars))
    return {var[0]: var[1] for var in env_vars_filtered}

@format_app_name
def create_session_on_server(staging_server, email):
    session_key = os.popen(f'heroku run {MANAGE_DOT_PY} create_session {email} --app={staging_server}').read()
    return session_key.strip()

