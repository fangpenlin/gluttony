from __future__ import unicode_literals
import os
import unittest
import tempfile
import shutil
import json

from gluttony import commands


class TestGluttony(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_command(self):
        json_path = os.path.join(self.temp_dir, 'flask.json')

        command = commands.Command()
        command.main(['flask==0.10.1', '--json={}'.format(json_path)])

        with open(json_path, 'rb') as jfile:
            result = json.load(jfile)

        pkg_map = {}
        packages = set([p['name'] for p in result['packages']])
        expected_packages = set([
            'flask', 
            'Werkzeug', 
            'itsdangerous', 
            'Jinja2',
            'markupsafe',
        ])
        self.assertEqual(packages, expected_packages)

        for p in result['packages']:
            pkg_map[p['name']] = p
        self.assertEqual(pkg_map['flask']['installed_version'], '0.10.1')

        dependencies = set([
            (src.split('-')[0], dest.split('-')[0]) 
            for src, dest in result['dependencies']
        ])
        expected_dependencies = set([
            ('flask', 'Werkzeug'),
            ('flask', 'itsdangerous'),
            ('flask', 'Jinja2'),
            ('Jinja2', 'markupsafe'),
        ])
        self.assertEqual(dependencies, expected_dependencies)

    def test_build_cleanup(self):
        # run the command twice, to ensure the build folder is removed correctly
        self.test_command()
        self.test_command()
