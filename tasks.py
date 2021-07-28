# type: ignore

from invoke import task


@task
def setup_profiling_tools(c):
    """
    Sets up all the profiling tools
    """

    result = c.run("which poetry", warn=True)
    if result.return_code == 1:
        print("poetry not present. Installing poetry.")

    c.sudo("apt install kcachegrind")
    c.sudo("pip install pyprof2calltree")
    c.sudo("pip install snakeviz")
    c.sudo(
        "apt install gir1.2-gtk-3.0 python3-gi python3-gi-cairo python3-numpy graphviz"
    )
    c.sudo("pip install xdot gprof2dot")


@task(
    help={
        "tool": "Tool to use for visualization. Possible values: cachegrind, pyinstrument, snakeviz, xdot. DEFAULT: cachegrind"
    }
)
def open_profiling(c, tool="cachegrind"):
    if tool == "cachegrind":
        c.run("pyprof2calltree -i profiling/results/results.prof -k")
    elif tool == "pyinstrument":
        c.run("xdg-open profiling/results/results.html")
    elif tool == "snakeviz":
        c.run("snakeviz profiling/results/results.prof")
    elif tool == "xdot":
        c.run(
            "gprof2dot -f pstats profiling/results/results.prof -o profiling/results/results.dot"
        )
        c.run("xdot profiling/results/results.dot")
