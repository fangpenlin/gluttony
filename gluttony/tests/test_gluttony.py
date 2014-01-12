from __future__ import unicode_literals
import os
import unittest
import tempfile
import shutil
import pickle

from gluttony import commands


class TestGluttony(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_command(self):
        pickle_path = os.path.join(self.temp_dir, 'flask.pickle')

        command = commands.Command()
        command.main(['flask==0.10.1', '--pickle={}'.format(pickle_path)])

        with open(pickle_path, 'rb') as pfile:
            dependencies = pickle.load(pfile)

        dependencies = set([
            (src.name, dest.name) for src, dest in dependencies
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
