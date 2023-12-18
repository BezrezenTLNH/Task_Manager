### Hexlet tests and linter status:
[![Actions Status](https://github.com/BezrezenTLNH/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/BezrezenTLNH/python-project-52/actions)
[![Actions Status](https://github.com/BezrezenTLNH/python-project-52/actions/workflows/my_tests.yml/badge.svg)](https://github.com/BezrezenTLNH/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/8ed5b54af38ecf127288/maintainability)](https://codeclimate.com/github/BezrezenTLNH/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/8ed5b54af38ecf127288/test_coverage)](htgit tps://codeclimate.com/github/BezrezenTLNH/python-project-52/test_coverage)

# Task manager
[**Task manager**](https://task-manager-3atw.onrender.com) is a tool for project management. 
 
With its help, you can assign tasks to employees and monitor their implementation

### Requirement
* Python
* Poetry
* Postgres / Sqlite3


### Installation
**Setting up enviroment**
```
git clone git@github.com:BezrezenTLNH/python-project-52.git
cd task-manager
make build
```
**Configure .env in the root folder**

**Install poetry with command:**
```
    python -m pip install poetry
```
 
**Start server for development**
```bash
  make dev
```
 
**Start production server**
```bash
  make start
```