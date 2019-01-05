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
      try:
          
          cmd = subprocess.Popen("python db/parser.py "+PATH_TMP_FILE.split('/')[1]+" "+host,shell=True,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE)

          print "A version of this js file has been beautified and saved at\n "+os.getcwd()+"/db/"+cmd.stdout.read().split('\n')[1]
      except:
          print 'In order to this feature work properly install jsbeatifier on your system with the instructions given at:\n'
          print 'https://github.com/Lopseg/Jspathextractor'
      return

