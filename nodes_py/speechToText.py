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

action=''
property=''
description=''
order=''
pointer=''
speech_output = ""
agentname=""
agent=''
# def callTheService(speech_output):
#      rospy.wait_for_service("callInstruction")
#      try:
#           callInstruction = rospy.ServiceProxy("callInstruction", text_parser)
#           result = callInstruction(speech_output)
#           print result.result
#           return result.result
#      except rospy.ServiceExcepton, e:
#           print "Service call failes %s"%e


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
          

def start_server():
     rospy.init_node('speechToText_Node')
     action_param = "~action"
     order_param = "~order"
     description_param = "~description"
     property_param = "~property"
     pointer_param = "~pointer"
     agent_param = "~agent"
     if rospy.has_param(action_param) and rospy.has_param(order_param) and rospy.has_param(description_param) and rospy.has_param(pointer_param) and rospy.has_param(property_param) and rospy.has_param(agent_param) :
          start_recognizer(action_param, order_param, description_param, pointer_param, property_param, agent_param)
     else:
          rospy.logwarn("action and order and description parameters need to be set to start recognizer.")
          
def subscriberCB(data):
     global speech_output
     file_action = open(action,'r')
     file_order = open(order, 'r')
     file_description = open(description,'r')
     file_property = open(property,'r')
     file_pointer = open(pointer,'r')
     file_agent = open(agentfile,'r')
     speech_input = data.data
     speech_input = speech_input.lower()
     #speech_input = re.sub(' to ', ' ', speech_input)
     speech_input = re.sub(' the ', ' ', speech_input)
     speech_input = re.sub(' of ', ' ', speech_input)
     speech = speech_input.split(' ')
     read_action = file_action.read()
     read_order = file_order.read()
     read_description = file_description.read()
     read_property = file_property.read()
     read_pointer = file_pointer.read()
     read_agent = file_agent.read()
     speech_output = ""
     agent = "robot"
     # print speech
     
     if len(speech) >= 1:
          if speech[0] in read_agent:
               if speech[0] == "redwasp":
                    splitter = speech[0].split('dw')
                    agent = add_agent_method(splitter[0]+"d"+"-"+"w"+splitter[1])
               elif speech[0] == "greenwasp":
                    splitter = speech[0].split('nw')
                    add_agent_method(splitter[0]+"n"+"-"+"w"+splitter[1])
               else:
                    add_agent_method(speech[0])
          if speech[0] in read_action:
               if speech[0] == "takepicture":
                    splitter = speech[0].split('ep')
                    speech_output = splitter[0]+"e"+" "+"p"+splitter[1]
               elif speech[0] == "showpicture":
                    splitter = speech[0].split('wp')
                    speech_output = splitter[0]+"w"+" "+"p"+splitter[1]
               elif speech[0] == "chargerobot":
                    splitter = speech[0].split('er')
                    speech_output = splitter[0]+"e"+" "+"r"+splitter[1]
               elif speech[0] == "takeoff":
                    splitter = speech[0].split('eo')
                    speech_output = splitter[0]+"e"+" "+"o"+splitter[1]
               elif speech[0] == "scanarea":
                    splitter = speech[0].split('na')
                    speech_output = splitter[0]+"n"+" "+"a"+splitter[1]
               elif speech[0] == "comeback":
                    splitter = speech[0].split('eb')
                    speech_output = splitter[0]+"e"+" "+"b"+splitter[1]
               else:
                    speech_output = speech[0]
          if len(speech) >= 2:
               if speech[1] in read_order:
                    speech_output = speech_output + " "+ speech[1]
          if len(speech) >= 3:
               if speech[2] in read_description or speech[2] in read_pointer or speech[2] in read_order or speech[2] in read_property:
                    speech_output = speech_output + " "+ speech[2]
          if len(speech) >= 4:
               if speech[3] in read_description or speech[3] in read_pointer or speech[3] in read_order or speech[3] in read_property:
                    speech_output = speech_output + " "+ speech[3]
          if len(speech) >= 5:
               if speech[4] in read_description or speech[4] in read_pointer or speech[4] in read_order or speech[4] in read_property:
                    speech_output = speech_output + " "+ speech[4]
          if len(speech) >= 6:
               if speech[5] in read_description or speech[5] in read_pointer or speech[5] in read_order or speech[5] in read_property:
                    speech_output = speech_output + " "+ speech[5]
          if len(speech) >= 7:
               if speech[6] in read_description or speech[6] in read_pointer or speech[6] in read_order or speech[6] in read_property:
                    speech_output = speech_output + " "+ speech[6]
          if len(speech) >= 8:
               if speech[7] in read_description or speech[7] in read_pointer or speech[7] in read_order or speech[7] in read_property:
                    speech_output = speech_output + " "+ speech[7]
    
     if speech_output != "":
          result = call_main_server(speech_output)
          
    # print "result of ros_parser: "
    # print result

        # Go to tree next to that rock

        # get input from publisher and checking if words are fitting
        # get input of publisher and storing them in an array...
        # rospy.init_node('speech_recognizer')
        # s = rospy.Service('speech_recognizer', speech_recognizer, initialize)
        # print "Ready for getting the instructions"
        # rospy.spin()
     
     
def start_recognizer(action_param, order_param, description_param, pointer_param, property_param, agent_param):
     global action
     global order
     global description
     global property
     global pointer
     global agentfile

     rospy.loginfo("Starting recognizer... ")
     action = rospy.get_param(action_param)
     order = rospy.get_param(order_param)
     description = rospy.get_param(description_param)
     property = rospy.get_param(property_param)
     pointer = rospy.get_param(pointer_param)
     agentfile = rospy.get_param(agent_param)
     # rospy.init_node("speechToText_server")
     # s = rospy.Service("speechToText", text_parser, subscriberCB)
     rospy.Subscriber("speechToText", String, subscriberCB)
     print "Ready for speechToText with Subscriber"
     rospy.spin()

     # service server
     # geht durch und dann der
     # server ruft client auf ros_parser
     # rospy.wait_for_service("speechToText_service")
     # , text_parser, subscribeCB)
     #rospy.Subscriber("/recognizer/output", String, subscriberCB)
     # rospy.spin()


     

if __name__ == "__main__":
     start_server()
    
