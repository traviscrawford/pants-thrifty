namespace java org.pantsbuild.contrib.thrifty.common

include "org/pantsbuild/contrib/thrifty/common/common.thrift"

struct ClientLog {
  1: common.Common common;
  2: string message;
}
