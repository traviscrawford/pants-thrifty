from __future__ import (absolute_import, division, generators, nested_scopes,
                        print_function, unicode_literals, with_statement)

from pants.backend.jvm.targets.exportable_jvm_library import \
    ExportableJvmLibrary


class ThriftyLibrary(ExportableJvmLibrary):
  default_sources_globs = '*.thrift'
