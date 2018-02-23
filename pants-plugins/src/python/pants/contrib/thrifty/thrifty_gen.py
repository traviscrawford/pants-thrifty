from __future__ import (absolute_import, division, generators, nested_scopes,
                        print_function, unicode_literals, with_statement)

import logging
import os

from pants.backend.jvm.targets.java_library import JavaLibrary
from pants.backend.jvm.tasks.nailgun_task import NailgunTaskBase
from pants.base.build_environment import get_buildroot
from pants.base.exceptions import TaskError
from pants.base.workunit import WorkUnitLabel
from pants.contrib.thrifty.thrifty_library import ThriftyLibrary
from pants.java.jar.jar_dependency import JarDependency
from pants.task.simple_codegen_task import SimpleCodegenTask
from twitter.common.collections import OrderedSet

logger = logging.getLogger(__name__)


class ThriftyGen(NailgunTaskBase, SimpleCodegenTask):

  @classmethod
  def register_options(cls, register):
    super(ThriftyGen, cls).register_options(register)

    def thrifty_jar(name):
      return JarDependency(org='com.microsoft.thrifty', name=name, rev='0.4.3')

    cls.register_jvm_tool(register,
                          'javadeps',
                          classpath=[
                            thrifty_jar(name='thrifty-compiler')
                          ],
                          classpath_spec='//:thrifty-compiler',
                          help='Runtime dependencies for the Microsoft Thrifty compiler')
    cls.register_jvm_tool(register, 'thrifty-compiler', classpath=[thrifty_jar(name='thrifty-compiler')])

  def __init__(self, *args, **kwargs):
    """Generates Java files from .proto files using the Thrifty protobuf compiler."""
    super(ThriftyGen, self).__init__(*args, **kwargs)

  def synthetic_target_type(self, target):
    return JavaLibrary

  def is_gentarget(self, target):
    return isinstance(target, ThriftyLibrary)

  def synthetic_target_extra_dependencies(self, target, target_workdir):
    thrifty_runtime_deps_spec = self.get_options().javadeps
    return self.resolve_deps([thrifty_runtime_deps_spec])

  def format_args_for_target(self, target, target_workdir):
    """Calculate the arguments to pass to the command line for a single target."""
    sources = OrderedSet(target.sources_relative_to_buildroot())
    args = ['--out={0}'.format(target_workdir)]
    args.extend(sources)
    return args

  def execute_codegen(self, target, target_workdir):
    args = self.format_args_for_target(target, target_workdir)
    if args:
      result = self.runjava(classpath=self.tool_classpath('thrifty-compiler'),
                            main='com.microsoft.thrifty.compiler.ThriftyCompiler',
                            args=args,
                            workunit_name='compile',
                            workunit_labels=[WorkUnitLabel.TOOL])
      if result != 0:
        raise TaskError('Thrifty compiler exited non-zero ({0})'.format(result))

  def _calculate_proto_paths(self, target):
    """Computes the set of paths that thrifty uses to lookup imported protos.

    The protos under these paths are not compiled, but they are required to compile the protos that
    imported.
    :param target: the JavaThriftyLibrary target to compile.
    :return: an ordered set of directories to pass along to thrifty.
    """
    proto_paths = OrderedSet()
    proto_paths.add(os.path.join(get_buildroot(), self.context.source_roots.find(target).path))

    def collect_proto_paths(dep):
      if not dep.has_sources():
        return
      for source in dep.sources_relative_to_buildroot():
        if source.endswith('.thrift'):
          root = self.context.source_roots.find_by_path(source)
          if root:
            proto_paths.add(os.path.join(get_buildroot(), root.path))

    collect_proto_paths(target)
    target.walk(collect_proto_paths)
    return proto_paths
