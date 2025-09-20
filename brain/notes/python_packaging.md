## Python Packaging

Snyk needs a requirements.txt file to do SAST on python code. Given a .whl package a requirements file can be generated.

1. create a venv and activate it
    - make sure to use the proper python version on the venv
    - example of specifying version: `python3.9 -m venv my_venv`
    ```bash
    python -m venv python_requirements
    cd python_requirements
    source bin/activate
    ```
2. install the wheel
    ```bash
    pip install example.whl
    ```
2. run pip freeze
    ```bash
    pip freeze > requirements.txt
    ```
