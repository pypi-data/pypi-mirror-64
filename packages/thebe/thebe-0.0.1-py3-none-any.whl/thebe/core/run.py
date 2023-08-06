from itertools import zip_longest
import copy
import time, sys, datetime, glob, re, sys, time, os, copy
from hashlib import md5
from io import StringIO
from subprocess import Popen, PIPE
from flask import url_for
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter
from flask_socketio import emit, SocketIO
import satyrn.core.constants as Constant

def getPlotData(globalScope, localScope):
    code=Constant.GetPlot
    redirected_output=sys.stdout=StringIO()
    redirected_error=sys.stderr=StringIO()
    stdout=''
    stderr=''
    sys.path.append(os.getcwd())
    try:
        exec(code, globalScope, localScope)
        stdout=redirected_output.getvalue().rstrip()
        stderr=''
    except Exception as e:
        stdout=redirected_output.getvalue()
        stderr=str(e)
    sys.path.pop()
    sys.stdout=sys.__stdout__
    sys.stderr=sys.__stderr__
    if stdout==Constant.EmptyGraph:
        stdout=''
    return stdout
def cells(cells, globalScope, localScope):
    cellOutput=[]
    for cellLoc, changed in enumerate(cells):
        stdout=''
        stderr=''
        plotData=''
        #If a cell has not changed keep the current output
        if changed:
            stdout, stderr, plotData=runWithExec(cell['code'][cellLoc], globalScope, localScope)
            changed=False
            cells['stdout'][cellLoc]=stdout
            cells['stderr'][cellLoc]=stderr
            cells['image/png'][cellLoc]=plotData
        #Keep the master list updated
        else:
            stdout=cells['stdout'][cellLoc]
            stderr=cells['stderr'][cellLoc]
            plotData=cells['image/png'][cellLoc]
        cellOutput.append({'stdout':stdout, 'stderr':stderr, 'image/png':plotData})
    return cellOutput
def runNewCells(cellsToRun, globalScope, localScope):
    cellOutput=[]
    plots=[]
    for cellCount, cell in enumerate(cellsToRun):
        #Keep the master list updated
        if cell['changed']:
            stdout, stderr, plotData=runWithExec(cell['code'], globalScope, localScope)
            cell['stdout']=stdout
            cell['stderr']=stderr
            cell['image/png']=plotData
            cell['changed']=False
        #If a cell has not changed keep the current output
        else:
            stdout=cell['stdout']
            stderr=cell['stderr']
            plotData=cell['image/png']
        cellOutput.append({'stdout':stdout, 'stderr':stderr, 'image/png':plotData})
    print('After run:\t%s'%[cell['image/png'][-10:] for cell in cellsToRun])
    return cellOutput
def runWithExec(cellCode, globalScope, localScope):
    #runs one cell of code and return plotdata and std out/err
    redirected_output=sys.stdout=StringIO()
    redirected_error=sys.stderr=StringIO()
    stdout=''
    stderr=''
    try:
        sys.path.append(os.getcwd())
        exec(cellCode, globalScope, localScope)
        stdout=redirected_output.getvalue()
        stderr=''
    except Exception as e:
        stdout=redirected_output.getvalue()
        stderr=str(e)
    finally:
        sys.path.pop()
        sys.stdout=sys.__stdout__
        sys.stderr=sys.__stderr__
    plotData=getPlotData(globalScope, localScope)
    return stdout, stderr, plotData
