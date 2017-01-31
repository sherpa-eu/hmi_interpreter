#!/usr/bin/env python
import roslib; roslib.load_manifest('hmi_interpreter')
from Tkinter import *

import rospy
from std_msgs.msg import String
from hmi_interpreter.msg import protocol_dialogue
from hmi_interpreter.srv import *
import time
import sys
import rospkg
import thread
from geometry_msgs.msg import *
import tf
import math

thread1 = ""
thread2 ="2"
res = ""
checker="false"

def get_pointer(a,s):
   listener = tf.TransformListener()
   rate = rospy.Rate(10.0)
   pose = PoseStamped()
   while not rospy.is_shutdown():
      try:
         (trans_right,rot_right) = listener.lookupTransform('/map', '/busy_genius/right_hand', rospy.Time(0))
         (trans_left,rot_left) = listener.lookupTransform('/map', '/busy_genius/left_hand', rospy.Time(0))
         break
      except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
         continue

   print "please"
   if trans_right[2] >= trans_left[2]:
      pose.pose.position.x = trans_right[0]
      pose.pose.position.y = trans_right[1]
      pose.pose.position.z = trans_right[2]
      pose.pose.orientation.x = rot_right[0]
      pose.pose.orientation.y = rot_right[1]
      pose.pose.orientation.z = rot_right[2]
      pose.pose.orientation.w = rot_right[3]
   else:
      pose.pose.position.x = trans_left[0]
      pose.pose.position.y = trans_left[1]
      pose.pose.position.z = trans_left[2]
      pose.pose.orientation.x = rot_left[0]
      pose.pose.orientation.y = rot_left[1]
      pose.pose.orientation.z = rot_left[2]
      pose.pose.orientation.w = rot_left[3]

   string = String()
   string.data = "set"
   rospy.wait_for_service('pointing_server')
   try:
      pointing_server = rospy.ServiceProxy("pointing_server", pointer)
      resp1 = pointing_server(string,pose)
      result = resp1.result
      return result
   except rospy.ServiceException, e:
      print "Service call failed: %s"%e
       
def compare_thread(data,var):
   global thread1
   global thread2
   print "--->data"
   print data
   if thread1 != thread2:
      print "waiting"
   else:
      if data != "NO":
         thread1 = "1"
         thread2 = "2"
         string = String()
         string.data = data
         print data
         print string
         change_image_field()
         pub.publish(string)
      else:
         print "teeest"
         thread1 = ""
         thread2 = "2"
     # client_sending(res.capitalize())

def sleeping_time(res, delay):
   global thread2
   time.sleep(delay)
   thread2 = res 
   thread.start_new_thread(compare_thread, (res,1,))

def execute_tasks(res, delay):
   time.sleep(delay)
   change_image_field()
   pub.publish(string)
  # client_sending(res.capitalize())

def func(event):
   e1.delete("end-1c",END)
   show_entry_fields()

def callback_thread(data,y):
   global res 
   global thread1
   res = String()
   if checker == "false" and data.data == "TURNON" or checker == "false" and data.data == "ON" or checker == "false" and data.data == "SWITCH ON":
      checker == "false"
      change_image_field()
      return
   elif data.data == "TURNON" or data.data == "ON" or data.data == "SWITCH ON":
      return
   if checker == "true":
      if data.data != "SWITCH":
         result = data.data
         if result == "COMEBACK":
            result="COME BACK"
         elif result == "TAKEPICTURE":
            result = "TAKE PICTURE"
         elif result == "TAKEOFF":
            result="TAKE OFF"
         elif result == "MOUNT RED WASP":
            result ="MOUNT RED_WASP"
         elif result == "MOUNT BLUE WASP":
            result="MOUNT BLUE_WASP"
         string = String()
         string.data = result.upper()
         if result.upper() == "ROBOTS":
            result = "ROBOT"
         window.delete("1.0", "end-1c")
         window.insert(INSERT,'Genius:  ','hcolor')
         window.insert(END,result.upper()+'\n','hnbcolor')
         if result=="GO THERE" or "THERE" in result:
            thread.start_new_thread(get_pointer, (string.data,5,))
         if result.upper() == "HAWK" or result.upper() == "RED WASP" or result.upper() == "BLUE WASP" or result.upper() == "DONKEY" or result.upper() == "ROBOT": 
            pub.publish(result.upper())
            return
         res = string.data
         thread1 = res
         publisher = rospy.Publisher('display_text', String, queue_size=10)
         publisher.publish(res)
         thread.start_new_thread(sleeping_time, (res,5,))
         thread.start_new_thread(compare_thread, (res,1,))
      else:
         change_image_field()

def publisher_callback(data):
   thread.start_new_thread(callback_thread, (data, 1,))    
   
def speaker_callback(data):
   change_image_field()

def change_image_field():
   global checker
   if checker == "false":
      checker = "true"
      b1.config(image=on)
   else:
      checker = "false"
      b1.config(image=off)

def show_entry_fields():
   if len(e1.get("1.0", "end-1c")) == 0 or  len(e1.get("1.0", "end-1c")) == 1:
      window.delete("1.0", "end-1c")
      window.insert(INSERT,'Please give a command!\n','rotcolor')
      e1.delete("1.0","end-1c")
   else:
      entry_text = e1.get("1.0","end-1c")
      e1.delete("1.0","end-1c")
      result = entry_text.upper() 
      if result == "COMEBACK":
         result = "COME BACK"
      elif result == "TAKEPICTURE":
         result="TAKE PICTURE"
      elif result == "SCANFOREST":
         result="SCAN FOREST"
      elif result == "SCANAREA":
         result="SCAN AREA"
      elif result == "TAKEOFF":
         result="TAKE OFF"
      window.delete("1.0", "end-1c")
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      print "teest"
      if result == "GO THERE" or "THERE" in result:
         thread.start_new_thread(get_pointer, (res,5,))
      if result == "ROBOTS":
         result = "ROBOT"
      result.replace("\n","")
      string = String()
      string.data = entry_text.upper()
      publisher = rospy.Publisher('display_text', String, queue_size=10)
      publisher.publish(result.upper())
      pub.publish(result.upper())



if __name__ == "__main__":
   rospy.init_node('gui_node', anonymous=True)
   master = Tk()
   master.title("Dialogue Interface")
   window = Text(master, height=5, width=70)
   window.tag_configure('big', font=('Verdana',20,'bold'))
   scroll = Scrollbar(master, command=window.yview)
   window.tag_configure('big', font=('Verdana',20,'bold'))
   window.tag_configure('hcolor', foreground='#476042', 
                        font=('Tempus Sans ITC', 12, 'bold'))
   window.tag_configure('hnbcolor', foreground='#476042', 
                        font=('Tempus Sans ITC', 12, 'italic'))
   window.tag_configure('rotcolor', foreground='#EF4423', 
                        font=('Tempus Sans ITC', 12, 'bold'))
   
   window.tag_config('coordinate',borderwidth=100)
   window.grid(row=4, columnspan = 1)
   
   dialog_label = Label(master)
   e1 = Text(master, width=45, height=2)
   
   #package path
   rospack = rospkg.RosPack()
   #rospack.list_pkgs() 
   path = rospack.get_path('hmi_interpreter')
   path = path+"/img"
   #mic
   b1 = Button(master, command=change_image_field)
   e1.grid(row=1, column=0, pady=4, padx=4)
   b1.grid(row=4, column=1,sticky=W, pady=4, padx=4)
   mi = PhotoImage(file=path+"/speaker_off.png")
   off = mi.subsample(5,5)
   b1.config(image=off)
   mis = PhotoImage(file=path+"/speaker_on.png")
   on = mis.subsample(5,5)
   pub = rospy.Publisher('/internal/recognizer/output', String, queue_size=10)

   master.bind('<Return>',func)
   Button(master, text='Quit', font=('Arial', 12,'bold', 'italic'), foreground='#ff8000',command=master.quit).grid(row=5, column=1,sticky=W, padx=16)
   Button(master, text='Enter', font=('Arial', 12,'bold', 'italic'),command=show_entry_fields).grid(row=1, column=0, sticky=W, pady=4, padx=4)
   rospy.Subscriber("recognizer/output", String, publisher_callback)
   rospy.Subscriber("/speaker_on", String, speaker_callback)
   mainloop( )
   #rospy.spin()
   
