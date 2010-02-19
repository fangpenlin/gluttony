'''
Created on 2010/2/19

@author: Victor Lin (bornstub@gmail.com)
         Twitter: http://twitter.com/victorlin
         Blog: http://blog.ez2learn.com
'''
import sys
import os
import optparse
import pickle

from pip.log import logger
from pip.index import PackageFinder
from pip.req import RequirementSet, InstallRequirement, parse_requirements
from pip.locations import build_prefix, src_prefix

from dependency import traceDependencys

class Command(object):
    bundle = False
    
    def __init__(self):
        self.parser = optparse.OptionParser()
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
        
        # options for output
        self.parser.add_option(
            '-p', '--pickle', '--pickle-file',
            dest='pickle_file',
            metavar='FILE',
            help='Pickled filename for result output')
        self.parser.add_option(
            '--dot', '--dot-file',
            dest='dot_file',
            metavar='FILE',
            help='Dot filename for result output')
        self.parser.add_option(
            '--display-graph',
            dest='display_graph',
            action='store_true',
            help='Display graph with Networkx and matplotlib')

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
        requirementSet = RequirementSet(
            build_dir=options.build_dir,
            src_dir=options.src_dir,
            download_dir=options.download_dir,
            download_cache=options.download_cache,
            upgrade=False,
            ignore_installed=True,
            ignore_dependencies=False)
        
        requirements = []
        for name in args:
            requirements.append(
                InstallRequirement.from_line(name, None))
        for name in options.editables:
            requirements.append(
                InstallRequirement.from_editable(name, default_vcs=options.default_vcs))
        for filename in options.requirements:
            for req in parse_requirements(filename, finder=finder, options=options):
                requirements.append(req)
        # add all requirements into requirements set
        for req in requirements:
            requirementSet.add_requirement(req)
        
        requirementSet.install_files(finder, 
                                      force_root_egg_info=self.bundle, 
                                      bundle=self.bundle)
        
        return requirements, requirementSet
    
    def output(self, options, args, dependencies):
        """Output result
        
        """
        if options.pickle_file:
            file = open(options.pickle_file, 'wb')
            pickle.dump(dependencies, file)
            file.close()
            logger.notify("Dependencies relationships result is in %s now", 
                          options.pickle_file)
        
        if options.display_graph or options.dot_file:
            try:
                import networkx as nx
                import matplotlib.pyplot as plt
                dg = nx.DiGraph()
                dg.add_edges_from(dependencies)
                if options.dot_file:
                    nx.write_dot(dg, options.dot_file)
                if options.display_graph:
                    nx.draw(dg)
                    plt.show()
            except ImportError:
                logger.error("In order to display graph, you must install networkx and matplotlib")
                return
    
    def main(self, args):
        options, args = self.parser.parse_args(args)
        if not args:
            self.parser.print_help()
            return
        
        level = 1 # Notify
        logger.level_for_integer(level)
        logger.consumers.extend([(level, sys.stdout)])
        # get all files
        requirements, requirementSet = self.run(options, args)
        # trace dependencies
        logger.notify("Tracing dependencies ...")
        dependencies = []
        for req in requirements:
            traceDependencys(req, requirementSet, dependencies)
        # output the result
        logger.notify("Output result ...")
        self.output(options, args, dependencies)
        
def main():
    command = Command()
    command.main(sys.argv[1:])
        
if __name__ == '__main__':
    main()