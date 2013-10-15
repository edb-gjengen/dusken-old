django:
    pkg.installed:
        - names:
            - python-dev
            - python-virtualenv
            - python-pip
            - postgresql-server-dev-9.1
            

/vagrant/dusken/venv:
virtualenv.managed:
    - no_site_packages: True
    - runas: vagrant
    - requirements: /vagrant/requirements.txt
    - require:
        - pkg: python-virtualenv


# TODO: you are here
# http://www.barrymorrison.com/2013/Mar/11/deploying-django-with-salt-stack/
# http://www.barrymorrison.com/2013/Apr/21/deploying-django-with-salt-now-with-postgresql/

/vagrant/dusken/settings.py:
  - file.managed:
  - source: salt://django/settings.py
  - template: jinja

dusken-setup:
    cmd.run:
        - user: vagrant
        - name: ". venv/bin/activate/ && python manage.py syncdb && python manage.py runserver"
