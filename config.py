import os

from dynaconf import Dynaconf, Validator
from google import auth


def default_gcp_project(conf, _):
    if project_id := conf.gcp_project:
        return project_id
    else:
        _, project_id = auth.default()
        print(f'default project set: {project_id}')
        return project_id


settings = Dynaconf(
    validators=[
        Validator('FROM_PATH',
                  default='./',
                  description='The path to read json files from',
                  messages={'condition': '{name} {value} either does not exist or is not readable by user'},
                  condition=lambda fp: os.access(fp, os.F_OK) and os.access(fp, os.R_OK)),

        Validator('TO_PATH',
                  default='./',
                  description='The path to write json files to',
                  messages={'condition': '{name} {value} either does not exist or is not writable by user'},
                  condition=lambda fp: os.access(fp, os.F_OK) and os.access(fp, os.W_OK)),

        Validator('FROM_LANG',
                  description='The language to translate from, defaults to en-US',
                  default='en-US'),
        Validator('TO_LANG',
                  description='The language to translate to,  defaults to is-IS',
                  default='is-IS'),

        Validator('GCP_PROJECT',
                  description='the Goggle Cloud Platform project id',
                  default=default_gcp_project)
    ],
    envvar_prefix="TRALA",
    settings_files=['settings.toml', ],
)
