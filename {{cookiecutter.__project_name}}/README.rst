{% for i in range({{cookiecutter.project_name}}|length) %}={% endfor %}
{{cookiecutter.project_name}}
{% for i in range({{cookiecutter.project_name}}|length) %}={% endfor %}

{{cookiecutter.project_short_description}}

.. image:: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
    :target: http://creativecommons.org/licenses/by-nc-sa/4.0/
    :alt: CC BY-NC-SA 4.0

.. image:: https://github.com/Dashstrom/lastlogcsv/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Dashstrom/lastlogcsv/actions/workflows/tests.yml
    :alt: Tests result

.. image:: https://github.com/Dashstrom/lastlogcsv/actions/workflows/publish.yml/badge.svg
    :target: https://github.com/Dashstrom/lastlogcsv/actions/workflows/publish.yml
    :alt: Build result

.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status

.. image:: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
    :target: http://creativecommons.org/licenses/by-nc-sa/4.0/
    :alt: CC BY-NC-SA 4.0

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style: black

.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/pylint-dev/pylint
    :alt: Linter: pylint

..  code-block:: bash

    git clone https://github.com/Dashstrom/easterobot
    cd easterobot


How to install docker
*********************

On rasbian run these command before install docker :

..  code-block:: bash

    sudo apt install --reinstall raspberrypi-bootloader raspberrypi-kernel
    sudo reboot

Install docker from script

..  code-block:: bash

    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker "${USER}"
    sudo apt remove docker-ce
    pip3 install docker-compose

Some usefull commands
*********************

..  code-block:: bash

    docker compose up -d --build
    docker compose logs -f
    docker compose exec bot bash
    docker compose stop
    docker compose down --volumes --rmi 'all'

Generate images
***************


..  code-block:: bash

    pip3 install requirements-tools.txt
    python3 tools/cropping.py images/eggs.png images/eggs -s 13

Run test
********

..  code-block:: bash

pip3 install requirements-dev.txt
isort .
black .

Update
******

..  code-block:: bash

    docker compose stop
    git pull
    nano easterobot/data/config.yml
    docker compose up -d --build

Backups
*******

Export backups

..  code-block:: bash

    docker compose stop
    docker run --rm -v "easterobot_database:/database" -v "easterobot_logs:/logs" -v "$PWD":/backup ubuntu tar czvf /backup/backup.tar.gz -C / database logs
    docker compose up -d

Import backups

..  code-block:: bash
    docker compose stop
    docker run --rm -v "easterobot_database:/database" -v "easterobot_logs:/logs" -v "$PWD":/backup ubuntu bash -c "cd / && rm -rf /{database,logs}/* && tar xvfP /backup/backup.tar.gz"
    docker compose up -d

License
*******

This work is licensed under a `Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License < http://creativecommons.org/licenses/by-nc-sa/4.0/>`_.
