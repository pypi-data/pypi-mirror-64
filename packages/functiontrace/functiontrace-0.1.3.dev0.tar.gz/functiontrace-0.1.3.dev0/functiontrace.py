import argparse
import os
import shutil
import sys
import _functiontrace

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trace a script's execution.")
    parser.add_argument('--trace-memory', action="store_true", help="""Trace
                        memory allocations/frees when enabled.  This may add
                        tracing overhead, so is disabled by default.""")
    parser.add_argument('--output_dir', type=str, default=os.getcwd(),
                        help="The directory to output trace files to")
    parser.add_argument("script", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if len(args.script) == 0:
        print("Can't profile without a target")
        parser.print_help()
        sys.exit(1)

    # We need the functiontrace-server installed and locatable in order to
    # trace anything.
    if shutil.which("functiontrace-server") is None:
        print("Unable to find `functiontrace-server` in the current $PATH.", file=sys.stderr)
        print("See https://functiontrace.com#installation for installation instructions.", file=sys.stderr)
        sys.exit(1)

    # Find the directory this module was loaded from.  We want to temporarily
    # put our Python wrappers in the path, so this module includes a path/
    # subdirectory that we'll add to our path.
    root = os.path.join(os.path.dirname(__file__), "path")
    os.environ["PATH"] = root + os.pathsep + os.environ["PATH"]

    # Ignore ourselves, keeping sys.argv looking reasonable as the child script
    # will expect it to be sane.
    sys.argv[:] = args.script

    # Read in the script to be executed and compile their code.
    # NOTE: This looks pretty questionable, but it's effectively equivalent to
    # what cProfile is doing, so it can't be that bad.
    # TODO: I think this breaks __file__, which various scripts actually use.
    sys.path.insert(0, os.path.dirname(sys.argv[0]))
    with open(sys.argv[0], 'rb') as fp:
        code = compile(fp.read(), sys.argv[0], 'exec')

    # Setup our tracing environment, including configuring tracing features.
    if args.trace_memory:
        _functiontrace.config_tracememory()
    _functiontrace.begin_tracing(args.output_dir)

    # Run their code now that we're tracing.
    exec(code)
else:
    # We've been imported for some reason.  Figure out whatever information we
    # can, then start tracing.
    _functiontrace.begin_tracing(os.getcwd())
