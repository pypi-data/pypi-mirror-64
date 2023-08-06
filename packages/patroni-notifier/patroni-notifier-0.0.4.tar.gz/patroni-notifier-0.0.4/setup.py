# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patroni_notifier']

package_data = \
{'': ['*'], 'patroni_notifier': ['templates/*', 'templates/sections/*']}

install_requires = \
['boto3>=1.10.12,<2.0.0',
 'click>=7.0,<8.0',
 'haproxy-stats>=1.5,<2.0',
 'humanize>=0.5.1,<0.6.0',
 'jinja2>=2.10.3,<3.0.0',
 'python-consul>=1.1.0,<2.0.0',
 'python-dateutil>=2.8,<3.0',
 'python-magic>=0.4.15,<0.5.0',
 'pytz>=2019.3,<2020.0',
 'pyyaml>=5.1,<6.0',
 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['patroni-notify = patroni_notifier.core:patroni_notify']}

setup_kwargs = {
    'name': 'patroni-notifier',
    'version': '0.0.4',
    'description': 'Patoni notification system using jinja2 templates',
    'long_description': '# Patroni Notifier\n\n![](https://github.com/jaredvacanti/patroni-notifier/workflows/Publish%20to%20PyPI/badge.svg)\n![PyPI](https://img.shields.io/pypi/v/patroni-notifier?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/patroni-notifier?style=flat-square)\n\nThis is a simple command line program to send templated emails from AWS SES in response\nto Patroni database events.\n\n## Supported Actions\n\naction | description\n--- | ---\nreload | reconfigure a running database \nrestart | `-HUP` sent to main process\nrole_change | promotions from replica to master\nstart | start postgresql process\nstop | stop/pause postgresql process\nbackup | backup and upload to s3 \n\n\n\n# Quick Start\n\n### Installation\n\n```\npip install patroni-notifier\n```\n\nCurrently emails are sent using Amazon SES. Authenication can use IAM roles\nor you can place a `aws.env` in your home directory with credentials.\n\n\n```\nUsage: patroni-notify <action> <role> <cluster_name> [OPTIONS]\n\n  Query the metastore for relevant Patroni information and send notification\n\nArguments:\n  action: <action>  The action.  [required]\n\n[OPTIONS]:\n  --config-file PATH      The path to the configuration file.  [default:\n                          /etc/patroni.yml]\n  --metastore TEXT        The DCS address.  [default: consul]\n  --logo-url TEXT         The logo url.\n  --logo PATH             The logo to be base64 encoded and embedded.\n  --email-sender TEXT     The email address to send notifications from.\n  --email-recipient TEXT  The email address to recieve notifications.\n  --haproxy-addr TEXT     The HAProxy TCP load-balancer address.\n  -h, --help              Show this message and exit.\n```\n\n### Configuration\n\nSystem-wide configurations are done in the `patroni.yml` file required for \nPatroni operations. You can further specify a config file location using \n`--config` as a command line option, which defaults to `/config/patroni.yml`.\n\n\n**Required Settings** in patroni.yml:\n\n```\npostgresql:\n  callbacks:\n    on_reload: /usr/local/bin/patroni-notify\n    on_restart: /usr/local/bin/patroni-notify\n    on_role_change: /usr/local/bin/patroni-notify\n    on_start: /usr/local/bin/patroni-notify\n    on_stop: /usr/local/bin/patroni-notify\n\npatroni_notifier:\n  email_sender: John Doe <example.com>\n  email_recipient: test@example.com\n  email_subject: Sample Subject\n  dashboard_url: http://example.com/dashboard/\n  logo_url: example-url\n  logo_link_url: http://www.example.com\n  haproxy:\n    address: 10.0.1.139:9001\n    load_balancers:\n      master_postgresql: backend_master\n      replicas_postgresql: backend_replicas\n```\n\nPatroni invokes callback scripts to run on certain database events. \nPatroni will pass the action, role and cluster name. Internally,\n`patroni-notifier` will parse the action to determine what html template\nto use.\n\n\n# Development\n\nIn order to access the Distributed Configuration Storage (DCS), the S3\nbackups, and the access rights to send test emails from SES, the test\nenvironment needs to run on an EC2 instance or be provided with the correct\nroles.\n\n- VSCode SSH Remote Login\n- `git clone https://github.com/jaredvacanti/patroni-notifier.git`\n- `cd patroni-notifier`\n- `sudo apt-get install python3-venv`\n- `python3 -m venv .venv`\n- `. .venv/bin/activate`\n- `pip install --upgrade pip`\n- `pip install poetry`\n- `poetry install`\n- Install Remote Python Debugger (VSCode Extension)\n\n\n## Tests\n\n```\npoetry run tox\n```\n\n## License\n\nMIT License\n\nCopyright (c) 2019-2020\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'Jared Vacanti',
    'author_email': 'jaredvacanti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jaredvacanti/patroni-notifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
