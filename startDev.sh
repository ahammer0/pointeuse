#!/bin/bash
echo "Activate venv"
. ./.venv/bin/activate
echo "Start flask"
flask --app webserver run --debug --extra-files ./templates/*:./static/*
