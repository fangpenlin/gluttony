import os

import pkg_resources
from pip.log import logger
from pip.index import PackageFinder
from pip.req import RequirementSet, InstallRequirement
from pip.locations import build_prefix, src_prefix

def traceDependencys(req, requirementSet, dependencies, _visited=None):
    """Trace all dependency relationship
    
    @param req: requirements to trace
    @param requirements: RequirementSet
    @param dependencies: list for storing dependencies relationships
    @param _visited: visited requirement set
    """
    _visited = _visited or set()
    if req in _visited:
        return
    _visited.add(req)
    for reqName in req.requirements():
        try:
            name = pkg_resources.Requirement.parse(reqName).project_name
        except ValueError, e:
            logger.error('Invalid requirement: %r (%s) in requirement %s' % (
                reqName, e, req))
            continue
        subreq = requirementSet.get_requirement(name)
        dependencies.append((req, subreq))
        traceDependencys(subreq, requirementSet, dependencies, _visited)

def getDependencies(name, requirementSet=None, finder=None):
    """Get dependencies of a python project
    
    @param name: name of python project
    @param requirements: RequirementSet
    @param finder: PackageFinder
    """
    if requirementSet is None:
        requirementSet = RequirementSet(
            build_dir=os.path.abspath(build_prefix),
            src_dir=os.path.abspath(src_prefix),
            download_dir=None,
            download_cache=None,
            upgrade=False,
            ignore_installed=True,
            ignore_dependencies=False)
    if finder is None:
        finder = PackageFinder(find_links=[], 
                               index_urls=['http://pypi.python.org/simple'])

    # lead pip download all dependencies
    req = InstallRequirement.from_line(name, None)
    requirementSet.add_requirement(req)
    requirementSet.install_files(finder)
    
    # trace the dependencies relationships between projects
    dependencies = []
    traceDependencys(req, requirementSet, dependencies)
    return dependencies