#!/usr/bin/env python
# coding: utf-8


def render(base_scen):
    """
    Compile RMarkdown report of scenario results
    
    This method calls an R script, compile_report.R, which renders an RMarkdown file,
    Plot_Disruption_Results.Rmd. The end results is a stand-alone HTML file with the compiled resiliency disruption results
    """

    import subprocess
    import shutil
    import webbrowser
    import os

    subprocess.Popen(['Rscript.exe', 'compile_report.R', base_scen],
                     stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                                 
    here = os.getcwd()

    webbrowser.open('file://' + os.path.realpath(os.path.join(here, 'Disruption_Results.html')))

