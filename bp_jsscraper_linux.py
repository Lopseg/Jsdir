#DEVELOPED BY RAFAEL 'LOPSEG' RODRIGUES 05/11/2018
#SPECIAL THANKS TO jobertabma for EXTRACTOR.rb
#YOU CAN FIND THE TOOL IN
#https://github.com/jobertabma/relative-url-extractor


from burp import IBurpExtender
from burp import IContextMenuFactory

from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL

import subprocess
import threading
import os
import sys

PATH_EXTRACTOR = 'dependencies/jsextractor.rb'
PATH_TMP_FILE = "db/tmp.js"

print "Js Path Extractor"


class BurpExtender(IBurpExtender, IContextMenuFactory):

  def registerExtenderCallbacks(self, callbacks):
    self._callbacks = callbacks
    self._helpers   = callbacks.getHelpers()
    self.context    = None

    # we set up our extension
    callbacks.setExtensionName("BHP JS scraper")
    callbacks.registerContextMenuFactory(self)
    return

  def createMenuItems(self, context_menu):
    self.context = context_menu
    menu_list = ArrayList()
    menu_list.add(JMenuItem("Send to js scraper", actionPerformed=self.pre_scan))

    return menu_list


  def pre_scan(self,event):

    # grab the details of what the user clicked
    http_traffic = self.context.getSelectedMessages()
    for traffic in http_traffic:
      http_service = traffic.getHttpService()
      host         = http_service.getHost()

      print 'Scanning :' + host
      response_plain_text = open(PATH_TMP_FILE,'w')
      responseInfo=traffic.getResponse()

      for char in responseInfo:
          try:
              response_plain_text.write(str(unichr(char)))
          except:
              response_plain_text.write('.')

      response_plain_text.close()

      cmd = subprocess.Popen("ruby "+PATH_EXTRACTOR+" "+PATH_TMP_FILE,shell=True,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
      print "\nUrls or possible urls paths found:\n"
      print cmd.stdout.read()
      self.jsbeautify(host)


  def jsbeautify(self,host):
      filename = str(os.times()[4])+"-"+host+".js"
      cmd = subprocess.Popen("js-beautify "+PATH_TMP_FILE,shell=True,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
      error_output = cmd.stderr.read()
      if "js-beautify: command not found" in error_output or "js-beautify: not found" in error_output:
          print 'In order to jsbeautifier feature work properly, install jsbeatifier on your system with the following commands:\n'
          print 'sudo apt-get install jsbeautifier && pip install jsbeautifier'
          print "Please check if you can run it on the terminal first"
          sys.exit(0)
      try:
              self.save_to_file(filename,cmd.stdout.read())
              print "A version of this js file has been beautified and saved at\n "+os.getcwd()+"db/files-beatified/"+filename
      except:
              print "Error in writing to file at "+os.getcwd()+"db/files-beatified/"+filename
              print "Please check the write permissions of the folder/user"
      return
    
  def save_to_file(self,filename,data):
      with open("db/beautified-files/"+filename,'w') as f:
          f.write(data)
      return
