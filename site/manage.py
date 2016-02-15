#!/usr/bin/env python
import os
import sys
import re
import dotenv

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    os.environ.setdefault("ENV", "default")

    env_file = os.path.abspath(os.path.join('envs',"%s.env" % os.getenv('ENV')))
    print('*' * 80)
    print("Read environment from '{}'".format(env_file))
    print('*' * 80)
    dotenv.read_dotenv(env_file)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
