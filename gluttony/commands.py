from __future__ import unicode_literals
import sys
import os
import optparse
import json

from pip.log import logger
from pip.index import PackageFinder
from pip.req import RequirementSet, InstallRequirement, parse_requirements
from pip.locations import build_prefix, src_prefix

from dependency import trace_dependencies
from version import __version__


def pretty_project_name(req):
    """Get project name in a pretty form:
    
    name-version
    
    """
    return '%s-%s' % (req.name, req.installed_version)


class Command(object):
    bundle = False
    
    def __init__(self):
        self.parser = optparse.OptionParser(version="%prog " + __version__)
        self.parser.add_option(
            '-e', '--editable',
            dest='editables',
            action='append',
            default=[],
            metavar='VCS+REPOS_URL[@REV]#egg=PACKAGE',
            help='Install a package directly from a checkout. Source will be checked '
            'out into src/PACKAGE (lower-case) and installed in-place (using '
            'setup.py develop). You can run this on an existing directory/checkout (like '
            'pip install -e src/mycheckout). This option may be provided multiple times. '
            'Possible values for VCS are: svn, git, hg and bzr.')
        self.parser.add_option(
            '-r', '--requirement',
            dest='requirements',
            action='append',
            default=[],
            metavar='FILENAME',
            help='Install all the packages listed in the given requirements file.  '
            'This option can be used multiple times.')
        self.parser.add_option(
            '-f', '--find-links',
            dest='find_links',
            action='append',
            default=[],
            metavar='URL',
            help='URL to look for packages at')
        self.parser.add_option(
            '-i', '--index-url', '--pypi-url',
            dest='index_url',
            metavar='URL',
            default='http://pypi.python.org/simple',
            help='Base URL of Python Package Index (default %default)')
        self.parser.add_option(
            '--extra-index-url',
            dest='extra_index_urls',
            metavar='URL',
            action='append',
            default=[],
            help='Extra URLs of package indexes to use in addition to --index-url')
        self.parser.add_option(
            '--no-index',
            dest='no_index',
            action='store_true',
            default=False,
            help='Ignore package index (only looking at --find-links URLs instead)')
        self.parser.add_option(
            '-b', '--build', '--build-dir', '--build-directory',
            dest='build_dir',
            metavar='DIR',
            default=None,
            help='Unpack packages into DIR (default %s) and build from there' % build_prefix)
        self.parser.add_option(
            '-d', '--download', '--download-dir', '--download-directory',
            dest='download_dir',
            metavar='DIR',
            default=None,
            help='Download packages into DIR instead of installing them')
        self.parser.add_option(
            '--download-cache',
            dest='download_cache',
            metavar='DIR',
            default=None,
            help='Cache downloaded packages in DIR')
        self.parser.add_option(
            '--src', '--source', '--source-dir', '--source-directory',
            dest='src_dir',
            metavar='DIR',
            default=None,
            help='Check out --editable packages into DIR (default %s)' % src_prefix)
        self.parser.add_option(
            '-U', '--upgrade',
            dest='upgrade',
            action='store_true',
            help='Upgrade all packages to the newest available version')
        self.parser.add_option(
            '-I', '--ignore-installed',
            dest='ignore_installed',
            action='store_true',
            help='Ignore the installed packages (reinstalling instead)')
        
        # options for output
        self.parser.add_option(
            '-j', '--json',
            dest='json_file',
            metavar='FILE',
            help='JSON filename for result output')
        self.parser.add_option(
            '--pydot',
            dest='py_dot',
            metavar='FILE',
            help='Output dot file with pydot')
        self.parser.add_option(
            '--pygraphviz',
            dest='py_graphviz',
            metavar='FILE',
            help='Output dot file with PyGraphviz')
        self.parser.add_option(
            '--display', '--display-graph',
            dest='display_graph',
            action='store_true',
            help='Display graph with Networkx and matplotlib')
        self.parser.add_option(
            '-R', '--reverse',
            dest='reverse',
            action='store_true',
            help='Reverse the direction of edge')

    def run(self, options, args):
        if not options.build_dir:
            options.build_dir = build_prefix
        if not options.src_dir:
            options.src_dir = src_prefix
        if options.download_dir:
            options.no_install = True
            options.ignore_installed = True
        else:
            options.build_dir = os.path.abspath(options.build_dir)
            options.src_dir = os.path.abspath(options.src_dir)
        index_urls = [options.index_url] + options.extra_index_urls
        if options.no_index:
            logger.notify('Ignoring indexes: %s' % ','.join(index_urls))
            index_urls = []
        finder = PackageFinder(
            find_links=options.find_links,
            index_urls=index_urls)
        requirement_set = RequirementSet(
            build_dir=options.build_dir,
            src_dir=options.src_dir,
            download_dir=options.download_dir,
            download_cache=options.download_cache,
            upgrade=options.upgrade,
            ignore_installed=options.ignore_installed,
            ignore_dependencies=False,
        )
        
        for name in args:
            requirement_set.add_requirement(
                InstallRequirement.from_line(name, None))
        for name in options.editables:
            requirement_set.add_requirement(
                InstallRequirement.from_editable(name, default_vcs=options.default_vcs))
        for filename in options.requirements:
            for req in parse_requirements(filename, finder=finder, options=options):
                requirement_set.add_requirement(req)
        
        requirement_set.prepare_files(
            finder, 
            force_root_egg_info=self.bundle, 
            bundle=self.bundle,
        )
        
        return requirement_set

    def _output_json(self, json_file, dependencies):
        packages = set()
        json_deps = []
        for src, dest in dependencies:
            packages.add(src)
            packages.add(dest)
            json_deps.append([
                pretty_project_name(src),
                pretty_project_name(dest),
            ])

        json_packages = []
        for package in packages:
            json_packages.append(dict(
                name=package.name,
                installed_version=package.installed_version,
            ))

        with open(json_file, 'wt') as jfile:
            json.dump(dict(
                packages=json_packages,
                dependencies=json_deps,
            ), jfile, sort_keys=True, indent=4, separators=(',', ': '))
    
    def output(self, options, args, dependencies):
        """Output result
        
        """
        if options.reverse:
            dependencies = map(lambda x: x[::-1], dependencies)
        
        if options.json_file:
            self._output_json(options.json_file, dependencies)
            logger.notify("Dependencies relationships result is in %s now", 
                          options.json_file)
        
        if options.display_graph or options.py_dot or options.py_graphviz:
            import networkx as nx

            # extract name and version
            def convert(pair):
                return (
                    pretty_project_name(pair[0]), 
                    pretty_project_name(pair[1]),
                )
            plain_dependencies = map(convert, dependencies)
            dg = nx.DiGraph()
            dg.add_edges_from(plain_dependencies)
            if options.py_dot:
                logger.notify("Writing dot to %s with Pydot ...", 
                              options.py_dot)
                from networkx.drawing.nx_pydot import write_dot
                write_dot(dg, options.py_dot)
            if options.py_graphviz:
                logger.notify("Writing dot to %s with PyGraphviz ...", 
                              options.py_graphviz)
                from networkx.drawing.nx_agraph import write_dot
                write_dot(dg, options.py_graphviz)
            if options.display_graph:
                import matplotlib.pyplot as plt
                logger.notify("Drawing graph ...")
                if not plain_dependencies:
                    logger.notify("There is no dependency to draw.")
                else:
                    nx.draw(dg)
                    plt.show()
    
    def main(self, args):
        options, args = self.parser.parse_args(args)
        if not args:
            self.parser.print_help()
            return
        
        level = 1  # Notify
        logger.level_for_integer(level)
        logger.consumers.extend([(level, sys.stdout)])
        # get all files
        requirement_set = self.run(options, args)
        # trace dependencies
        logger.notify("Tracing dependencies ...")
        dependencies = []
        values = None
        if hasattr(requirement_set.requirements, 'itervalues'):
            values = list(requirement_set.requirements.itervalues())
        elif hasattr(requirement_set.requirements, 'values'):
            values = list(requirement_set.requirements.values())
        for req in values:
            trace_dependencies(req, requirement_set, dependencies)
        # output the result
        logger.notify("Output result ...")
        self.output(options, args, dependencies)
        requirement_set.cleanup_files()


def main():
    command = Command()
    command.main(sys.argv[1:])
        
if __name__ == '__main__':
    main()
