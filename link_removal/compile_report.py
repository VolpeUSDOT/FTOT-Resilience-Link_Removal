#!/usr/bin/env python
# coding: utf-8
    
def render(base_scen):
    """
    Compile RMarkdown report of scenario results
    
    This method calls an R script, compile_report.R, which renders an RMarkdown file, Disruption_Results.Rmd.
    The end result is a stand-alone HTML file with the compiled resiliency disruption results.
    """

    import subprocess
    import shutil
    import webbrowser
    import os
    
    R_process = subprocess.Popen(['Rscript.exe', 'compile_report.R', base_scen],
                                 stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    is_error = log_subprocess_error(R_process.stderr)

    here = os.getcwd()
    
    webbrowser.open('file://' + os.path.realpath(os.path.join(here, 'Disruption_Results.html')))

    return is_error


# ==================================================================


def log_subprocess_error(pipe):
    is_error = False

    for line in iter(pipe.readline, b''):  # b'\n'-separated lines
        if line != b'':
            is_error = True
            print('R PROCESS:', line.strip().decode('ascii'))

    return is_error

