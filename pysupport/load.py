# Copyright (c) 2017 Melown Technologies SE
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# *  Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# *  Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# This glue code used by pysupport/load.cpp
#
# Input: fullname, contents, binary
# Output: module
# Throws: ImportError
#

import sys
version = sys.version_info[0] * 100 + sys.version_info[1]

if version < 307:
    def new_module(fullname):
        import imp
        return imp.new_module(fullname)
else:
    def new_module(fullname):
        import importlib.util
        import importlib.machinery
        spec = importlib.machinery.ModuleSpec(fullname, None)
        return importlib.util.module_from_spec(spec)

class Loader:
    def __init__(self, fullname, contents, compiled=False):
        self.fullname = fullname
        self.contents = contents
        self.compiled = compiled

    def load_module(self, fullname):
        import sys
        global new_module, version

        # this must be here
        if fullname in sys.modules:
            return sys.modules[fullname]

        mod = sys.modules.setdefault(fullname, new_module(fullname))
        mod.__file__ = "<%s>" % fullname
        mod.__loader__ = self

        if self.compiled:
            import marshal
            # TODO: use buffer slice
            offset = 8;
            if version >= 300:
                offset += 4
            if version >= 307:
                offset += 4
            code = marshal.loads(self.contents[offset:])
        else:
            code = compile(self.contents, mod.__file__, "exec")

        exec(code, mod.__dict__)
        return mod

module = Loader(fullname, contents, compiled).load_module(fullname)
