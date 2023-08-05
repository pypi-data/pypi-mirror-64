# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['learnupon']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'learnupon',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Swimlane Learnupon\n\n## Description\nA python package for interacting with the LearnUpon LMS.\n\n## Installation\n```\npip install learnupon\n```\n\n## Usage\n```python\nfrom learnupon import LearnUpon\n\nlearnupon = LearnUpon(portal_url="https://myportal.learnupon.com", \n                      username="abc123", password="def456")\n# Get all users\nusers = learnupon.get_users()\n# Get user by email\nuser = learnupon.search_for_user(email=\'some.user@company.com\')\n# Get user by user_id\nuser_again = learnupon.get_user(user_id=user[\'id\'])\n# Create a new user\nnew_user = learnupon.create_user(email=\'some.user@company.com\',\n                                 password="Thisisapassword")\n# Invite a new user by email                      \nnew_user = learnupon.invite_user(email_address="new_user@mycompany.com")\n# Get Courses (Optional name filter)\ncourses = learnupon.get_courses(name=\'Course Name\')\n# Get All Groups\ngroups = learnupon.get_groups(title="Group Name")\n# Create Group Invite\ngroup_invites = learnupon.create_group_invite(group_id=groups[0]["id"], \n                                             email_addresses=[\'user1@company.com\', \'user2@company.com\'])\n```',
    'author': 'Michael Butler',
    'author_email': 'michael.butler@swimlane.com',
    'url': 'https://github.com/swimlane/swimlane-learnupon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
