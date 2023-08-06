import time, sys, datetime, glob, re, sys, time, os, copy
from flask import url_for
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter

def addSavePlot(fileString, myDir, plotCount):
    fileArrayWithPlot=[]
    savefigText="plt.savefig('"+myDir+"/static/plot"+str(plotCount)+".png')"
    match = re.compile(r"###p")
    items = re.findall(match, fileString)
    for item in items:
        savefigText="plt.savefig('"+myDir+"/static/plot"+str(plotCount)+".png')"
        fileString=fileString.replace(item, savefigText)
    return fileString 
def convertCells(cellDict):
    # Return a deep copy of cellList with code replaced with html-ized code
    tempCells=copy.deepcopy(cellDict)
    for x in tempCells['id']:
        tempCells['code_html']=highlight(tempCells['code'][x], PythonLexer(), HtmlFormatter())
        if tempCells['image/png'][x]:
            tempCells['image/png_html'][x]='<img src="data:image/png;base64, '+tempCells['image/png'][x]+'" />'
        if tempCells['stdout'][x]:
            tempCells['stdout_html'][x]=highlight(tempCells['stdout'][x], BashLexer(), HtmlFormatter())
        if tempCells['stderr'][x]:
            tempCells['stderr_html'][x]=highlight(tempCells['stderr'][x], BashLexer(), HtmlFormatter())
    return tempCells 
def convertLedgerToHtml(cellList, part='all'):
    # Return a deep copy of cellList with code replaced with html-ized code
    tempCells=copy.deepcopy(cellList)
    for cell in tempCells:
        cell['code']=highlight(cell['code'], PythonLexer(), HtmlFormatter())
        if cell['image/png']:
            cell['image/png']='<img src="data:image/png;base64, '+cell['image/png']+'" />'
        if cell['stdout']:
            cell['stdout']=highlight(cell['stdout'], BashLexer(), HtmlFormatter())
        if cell['stderr']:
            cell['stderr']=highlight(cell['stderr'], BashLexer(), HtmlFormatter())
    return tempCells 

def output(output):
    temp_output=copy.deepcopy(output)
    for cell in temp_output:
        if cell:
            if cell['image/png']:
                cell['image/png']='<img src="data:image/png;base64, '+cell['image/png']+'" />'
            if cell['stdout']:
                cell['stdout']=highlight(cell['stdout'], BashLexer(), HtmlFormatter())
            if cell['stderr']:
                cell['stderr']=highlight(cell['stderr'], BashLexer(), HtmlFormatter())
    return temp_output

