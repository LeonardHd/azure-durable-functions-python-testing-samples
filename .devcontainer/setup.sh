#!/usr/bin/env bash

npm install -g azurite # TODO: add to devcontainer setup.
azurite --silent &

pip install -r requirements.txt
pip install -r function_app/requirements.txt
