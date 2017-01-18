#!/usr/bin/env python

"""
Getting Input from a speech recognizer and checking it
based on the Verb Order Description-Structure
  parameters:
   ~action - filename of action model
   ~order  - filename of order model
   ~description - filename of location model
 
  publications:
   ~speech_input (std_msgs/String) -text input
   ~speech_output(std_msgs/String) -text output

"""

import roslib; roslib.load_manifest('hmi_interpreter')
from hmi_interpreter.srv import *
import rospy
import re
import sys

import pygtk
pygtk.require('2.0')
import gtk
import string 
import os
import commands
from std_msgs.msg import String

speech_output = ""

def call_main_server(data):
     rospy.wait_for_service("main_server")
     try: 
          main_server = rospy.ServiceProxy("main_server", text_parser)
          resp1 = main_server(speech_output)
          result = resp1.result
          return result
     except rospy.ServiceException, e:
          print "Service call failed: %s"%e
     
def add_agent_method(agent):
     rospy.wait_for_service("add_agent_name")
     print "in the agent server"
     try: 
          add_agent_name = rospy.ServiceProxy("add_agent_name", text_parser)
          resp1 = add_agent_name(agent)
          return resp1.result
     except rospy.ServiceException, e:
          print "Service call failed: %s"%e
          

def add_viewpoint(viewpoint):
     rospy.wait_for_service("add_viewpoint")
     print "in the agent server"
     try: 
          add_viewpoint = rospy.ServiceProxy("add_viewpoint", text_parser)
          resp1 = add_viewpoint(viewpoint)
     except rospy.ServiceException, e:
          print "Service call failed: %s"%e
          
def subscriberCB(data):
     global speech_output
     speech_input = data.data
     speech_input = speech_input.lower()
     speech_input = re.sub('next to', 'next', speech_input)
     speech_input = re.sub(' the ', ' ', speech_input)
     speech_input = re.sub(' a ', ' ', speech_input)
     speech_input = re.sub(' of ', ' ', speech_input)
     speech = speech_input.split(' ')
     speech_output = ""
     agent = "robot"
     print speech_input
     speech_and = speech_input.split('and ')
     if len(speech_and) >= 1:
          if speech[0] == "red" or speech[0] == "blue":
               agent = add_agent_method(speech[0]+"-wasp")
          elif speech[0] == "hawk" or speech[0] == "donkey" or speech[0] == "robot":
               add_agent_method(speech[0])
          else:
               speech_output = speech[0]
               if len(speech) >= 2:
                    if speech[1] == "there" or speech[1] == "me" or speech[1] == "for":
                         speech_output = speech_output + "-" + speech[1]
                    else:
                         speech_output = speech_output + " " + speech[1]
                    if len(speech) >= 3:
                         if speech[2] == "your":
                              add_viewpoint("yes")# get agent-name-server
                              speech_input = re.sub(' your ', ' ', speech_input)
                              speech = speech_input.split(' ')
                              speech_output = speech[0]+" "+speech[2]
                         else:
                              speech_output = speech_output + " " + speech[2]
                         if len(speech) >= 4:
                              speech_output = speech_output + " "+ speech[3]
                         if len(speech) >= 5:
                              speech_output = speech_output + " "+ speech[4]
                         if len(speech) >= 6:
                              speech_output = speech_output + " "+ speech[5]
                         if len(speech) >= 7:
                              speech_output = speech_output + " "+ speech[6]
                         if len(speech) >= 8:
                              speech_output = speech_output + " "+ speech[7]
     else:
          speech = speech_and[0].split(" ")
          if len(speech) >= 1:
               if speech[0] == "red" or speech[0] == "blue":
                    agent = add_agent_method(speech[0]+"-wasp")
               elif speech[0] == "hawk" or speech[0] == "donkey" or speech[0] == "robot":
                    add_agent_method(speech[0])
               else:
                    speech_output = speech[0]
               if len(speech) >= 2:
                    if speech[1] == "there" or speech[1] == "me" or speech[1] == "for":
                         speech_output = speech_output + "-" + speech[1]
                    else:
                         speech_output = speech_output + " " + speech[1]
               if len(speech) >= 3:
                    if speech[2] == "your":
                         add_viewpoint("yes")# get agent-name-server
                         speech_input = re.sub(' your ', ' ', speech_input)
                         speech = speech_input.split(' ')
                         speech_output = speech[0]+" "+speech[2]
                    else:
                         speech_output = speech_output + " " + speech[2]
               if len(speech) >= 4:
                    speech_output = speech_output + " "+ speech[3]
               if len(speech) >= 5:
                    speech_output = speech_output + " "+ speech[4]
               if len(speech) >= 6:
                    speech_output = speech_output + " "+ speech[5]
               if len(speech) >= 7:
                    speech_output = speech_output + " "+ speech[6]
               if len(speech) >= 8:
                    speech_output = speech_output + " "+ speech[7] 
     
          speech_output_1 = speech_output
          speech_output = ""
          speech = speech_and[1].split(" ")
          if len(speech_and) >= 1:
               if speech[0] == "red" or speech[0] == "blue":
                    agent = add_agent_method(speech[0]+"-wasp")
               elif speech[0] == "hawk" or speech[0] == "donkey" or speech[0] == "robot":
                    add_agent_method(speech[0])
               else:
                    speech_output = speech[0]
               if len(speech) >= 2:
                    if speech[1] == "there" or speech[1] == "me" or speech[1] == "for":
                         speech_output = speech_output + "-" + speech[1]
                    else:
                         speech_output = speech_output + " " + speech[1]
               if len(speech) >= 3:
                    if speech[2] == "your":
                         add_viewpoint("yes")# get agent-name-server
                         speech_input = re.sub(' your ', ' ', speech_input)
                         speech = speech_input.split(' ')
                         speech_output = speech[0]+" "+speech[2]
                    else:
                         speech_output = speech_output + " " + speech[2]
               if len(speech) >= 4:
                    speech_output = speech_output + " "+ speech[3]
               if len(speech) >= 5:
                    speech_output = speech_output + " "+ speech[4]
               if len(speech) >= 6:
                    speech_output = speech_output + " "+ speech[5]
               if len(speech) >= 7:
                    speech_output = speech_output + " "+ speech[6]
               if len(speech) >= 8:
                    speech_output = speech_output + " "+ speech[7]

          speech_output = speech_output_1 +"and "+speech_output
                                                            
     if speech_output != "":
          result = call_main_server(speech_output)
          
     
     
def start_recognizer():
     rospy.init_node("speechToText_node")
     rospy.loginfo("Starting recognizer... ")
     rospy.Subscriber("internal/recognizer/output", String, subscriberCB)
     print "Ready for speechToText with Subscriber"
     rospy.spin()

if __name__ == "__main__":
     start_recognizer()
    
