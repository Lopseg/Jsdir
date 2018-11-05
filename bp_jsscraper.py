#DEVELOPED BY RAFAEL 'LOPSEG' RODRIGUES DA SILVA 11/05/2018
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
import time


PATH_EXTRACTOR = '/home/lopseg/tools/content/rue/jsextractor.rb'
PATH_TMP_FILE = " /home/lopseg/tools/.burpjscrapper.tmp"

print "REMEMBER TO EDIT THE FILE TO ADD THE CORRECT PATH TO EXTRACTOR AND AN WRITABLE PATH TO THE TMP FILE"

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

      command = "ruby "+PATH_EXTRACTOR+" "+PATH_TMP_FILE
      cmd = subprocess.Popen(command,shell=True,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
      output = cmd.stdout.read()
      print "Urls or possible urls paths found:\n"
      print output

    return
