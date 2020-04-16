/**
 * Copyright (c) 2020 Melown Technologies SE
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * *  Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * *  Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef pysupport_debugger_po_hpp_included_
#define pysupport_debugger_po_hpp_included_

#include <boost/program_options.hpp>

#include "utility/implicit-value.hpp"

#include "debugger.hpp"

namespace pysupport {

inline void configuration(DebuggerOptions &options
                          , boost::program_options::options_description &od)
{
    namespace po = boost::program_options;

    od.add_options()
        ("debug"
         , po::value<DebuggerMode>()
         ->implicit_value(DebuggerMode::interactive)
         , "Debugging mode. Default off. Use \"interactive\" (implicit) to "
         "start interactive debugger. Use \"post-mortem\" or \"pm\" to "
         "start interactive debugger on uncaught exception.")
        ;

    (void) options;
}

inline void configure(DebuggerOptions &options
                      , const boost::program_options::variables_map &vars)
{
    namespace po = boost::program_options;

    if (!vars.count("debug")) { return; }

    options.mode = vars["debug"].as<DebuggerMode>();
}

} // namespace pysupport

#endif // pysupport_debugger_po_hpp_included_
