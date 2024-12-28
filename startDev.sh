#!/bin/bash
flask --app webserver run --debug --extra-files ./templates/*:./static/*
