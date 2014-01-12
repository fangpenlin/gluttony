from __future__ import unicode_literals

import pkg_resources
from pip.log import logger


def trace_dependencies(req, requirement_set, dependencies, _visited=None):
    """Trace all dependency relationship
    
    @param req: requirements to trace
    @param requirement_set: RequirementSet
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
        subreq = requirement_set.get_requirement(name)
        dependencies.append((req, subreq))
        trace_dependencies(subreq, requirement_set, dependencies, _visited)
