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
message="manu"
change_field="false"
flag="true"
v = ""
entered="false"

def connect_to_julius(test,k):
   print "connect_to_julius"
   print test
   rospy.wait_for_service('julius_server')
   try:
      julius_server=rospy.ServiceProxy('julius_server',text_parser)
      resp1=julius_server(test)
      return resp1.result
   except rospy.ServiceException, e:
      print "Service call failed: %s"%e

def get_pointer(a,s):
   listener = tf.TransformListener()
   rate = rospy.Rate(10.0)
   pose = PoseStamped()
   listener.waitForTransform("/map", "/busy_genius/right_hand", rospy.Time(), rospy.Duration(4.0))
   while not rospy.is_shutdown():
      try:
         now = rospy.Time(0)
         listener.waitForTransform("/map", "/busy_genius/right_hand", now, rospy.Duration(4.0))
         (trans_right,rot_right) = listener.lookupTransform('/map', '/busy_genius/right_hand', now)
         (trans_left,rot_left) = listener.lookupTransform('/map', '/busy_genius/left_hand', now)
         break
      except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
         continue
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
      
 
def ShowChoice():
   global entered
   b1.config(image=off)
   window.delete("1.0", "end-1c")
   e1.delete("1.0","end-1c")
   if v.get() == 1:
      pub.publish("hawk")
      result = "GO THERE"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 2:
      pub.publish("hawk")
      result = "STOP"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 3:
      pub.publish("hawk")
      result = "SEARCH THAT LAKE FOR KITE"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 4:
      pub.publish("hawk")
      result = "GO TO HELIPAD"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 5:
      pub.publish("red wasp")
      result = "SEARCH THAT BRIDGE FOR VICTIM"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 6:
      pub.publish("blue wasp")
      result = "SEARCH THAT BRIDGE FOR VICTIM"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 7:
      pub.publish("donkey")
      result = "GO TO VICTIM"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 8: 
      pub.publish("blue wasp")
      result = "GO TO VICTIM"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 9:
      pub.publish("red wasp")
      result = "CHARGE"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 10:
      pub.publish("blue wasp")
      result = "TAKE PICTURE"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 11:
      pub.publish("blue wasp")
      result = "CHARGE"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,result+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 12:
      pub.publish("donkey")
      result = "UNMOUNT RED WASP"
      rule = "UNMOUNT RED WASP"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,rule+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   elif v.get() == 13:
      pub.publish("donkey")
      result = "UNMOUNT BLUE WASP"
      rule = "UNMOUNT BLUE WASP"
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,rule+'\n','hnbcolor')
      pub.publish(result)
      entered = "true"
   b1.config(image=off)
  # print result
   return

def compare_thread(data,var):
   global thread1
   global thread2
   if thread1 != thread2:
      print "waiting"
   else:
      print "data"
      print data != "CANCEL"
      print data
      if data != "CANCEL":
         thread1 = "1"
         thread2 = "2"
         string = String()
         string.data = data
         print data
         print "string"
         print string
         change_image_field()
         pub.publish(string)
      else:
         print "kjdkjsakdaj"
         thread1 = ""
         thread2 = "2"
         print "sjdiasjdisajdisajdoisa"
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
   global get_agent
   res = String()
   if checker == "false":
      # change_image_field()
      return
   else:
      if data.data != "SWITCH":
         result = data.data
         if " AND " in result:
            result = result.split(" AND ")
            if result[0] == "COMEBACK":
               result="COME BACK"+" AND "+ result[1]
            elif result[0] == "TAKEPICTURE":
               result = "TAKE PICTURE"+" AND "+ result[1]
            elif result[0] == "TAKEOFF":
               result="TAKE OFF"+" AND "+ result[1]
            elif result[0] == "MOUNT RED WASP":
               result ="MOUNT RED_WASP"+" AND "+ result[1]
            elif result[0] == "MOUNT BLUE WASP":
               result="MOUNT BLUE_WASP"+" AND "+ result[1]
            elif result[1] == "COMEBACK":
               result=result[0]+" AND "+"COME BACK"
            elif result[1] == "TAKEPICTURE":
               result =result[0]+" AND "+ "TAKE PICTURE"
            elif result[1] == "TAKEOFF":
               result=result[0]+" AND "+"TAKE OFF"
            elif result[1] == "MOUNT RED WASP":
               result =result[0]+" AND "+"MOUNT RED_WASP"
            elif result[1] == "MOUNT BLUE WASP":
               result=result[0]+" AND "+"MOUNT BLUE_WASP"
            elif result[0] == result[1]:
               result = result[0]
            else:
               result=result[0]+" AND "+result[1]
         else:
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
            elif result == "SEARCH THAT LAKE":
               return
            elif result == "FOR KITE":
               result = "SEARCH THAT LAKE FOR KITE"
            elif result == "FOR VICTIM":
               result = "SEARCH THAT LAKE FOR VICTIM"
               
         string = String()
         print "result"
         print result
         string.data = result.upper()
         if result.upper() == "ROBOTS":
            result = "ROBOT"
         window.delete("1.0","end-1c")
         window.delete("2.0","end-1c")
         window.delete("0.0","end-1c")
         window.delete("end-1c",END)
         window.insert(INSERT,'Genius:  ','hcolor')
         window.insert(END,result.upper()+'\n','hnbcolor')
         if "MOVE" in result.upper():
            result = result.upper()
            result = result.split("MOVE")
            result = "GO"+result[1]
            string.data = result
         elif result=="GO THERE" or "THERE" in result:
            thread.start_new_thread(get_pointer, (string.data,5,))
         if result.upper() == "HAWK" or result.upper() == "RED WASP" or result.upper() == "BLUE WASP" or result.upper() == "DONKEY" or result.upper() == "ROBOT": 
            if result.lower() == "red wasp":
               get_agent = 1
               v.set(1)
            elif result.lower() == "blue wasp":
               get_agent = 2
               v.set(2)
            elif result.lower() == "hawk":
               get_agent = 3
               v.set(3)
            elif result.lower() == "donkey":
               get_agent = 4
               v.set(4)
            pub.publish(result.upper())
            return
         
           # pub.publish(result.upper())
         res = string.data
         thread1 = res
         publisher.publish(res)
         thread.start_new_thread(sleeping_time, (res,5,))
         thread.start_new_thread(compare_thread, (res,1,))
      else:
         change_image_field()

def publisher_callback(data):
   thread.start_new_thread(callback_thread, (data, 1,))    
   
def displayer_callback(data):
   window.delete("1.0", "end-1c")
   window.insert(INSERT,data.data,'rotcolor')
   e1.delete("1.0","end-1c")
   
#def speaker_callback(data):
#   if change_field == "true":
#      change_image_field()

def speaker_callback(data):
   if flag == "true":
      change_field = "false"
      time.sleep(3)
      print "now change it"
      change_image_field()
      publisher.publish("OK.Performing task!")
      

def change_image_field():
   global checker
   if checker == "false" and entered == "false":
      checker = "true"
      b1.config(image=on)
      thread.start_new_thread(connect_to_julius, ("true",1,))
   elif checker == "true" and entered == "false":
      checker = "false"
      b1.config(image=off)
      thread.start_new_thread(connect_to_julius, ("false",1,))

def show_entry_fields():
   global flag
   if len(e1.get("1.0", "end-1c")) == 0 or  len(e1.get("1.0", "end-1c")) == 1:
      window.delete("1.0", "end-1c")
      window.insert(INSERT,'Please, give a command!\n','rotcolor')
      e1.delete("1.0","end-1c")
      flag ="false"
   else:
      flag="false"
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
      if result.lower() == "red wasp":
         v.set(1)
      elif result.lower() == "blue wasp":
         v.set(2)
      elif result.lower() == "hawk":
         v.set(3)
      elif result.lower() == "donkey":
         v.set(4)
      result.replace("\n","")
      string = String()
      string.data = entry_text.upper()
      publisher.publish(result.upper())
      if result != "NO":
         pub.publish(result.upper())



if __name__ == "__main__":
   pubtimepoint = rospy.Publisher("/all_timepoints", String, queue_size=10)
   rospy.init_node('gui_node', anonymous=True)
   value = String()
   value.data = ""
   pubtimepoint.publish(value)
   master = Tk()
   master.title("HMI Dialogue Interface")
   v = IntVar()
   window = Text(master, height=7, width=70)
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
   window.insert(INSERT,'Please, select a command or use voice by pushing button!\n','rotcolor')
   rospack = rospkg.RosPack()
   path = rospack.get_path('hmi_interpreter')
   path = path+"/img"
   b1 = Button(master, command=change_image_field)
   e1.grid(row=1, column=0, pady=4, padx=4)
   b1.grid(row=4, column=1,sticky=W, pady=4, padx=4)

   mi = PhotoImage(file=path+"/speaker_off.png")
   off = mi.subsample(5,5)
   b1.config(image=off)
   mis = PhotoImage(file=path+"/speaker_on.png")
   on = mis.subsample(5,5)
   pub = rospy.Publisher('/internal/recognizer/output', String, queue_size=10)
   publisher = rospy.Publisher('display_command', String, queue_size=10)
   master.bind('<Return>',func)
   Button(master, text='Quit', font=('Arial', 12,'bold', 'italic'), foreground='#ff8000',command=master.quit).grid(row=5, column=0,sticky=W, padx=10)
   Button(master, text='Enter', font=('Arial', 12,'bold', 'italic'),command=show_entry_fields).grid(row=1, column=0, sticky=W, pady=4, padx=4)
   r1 = Radiobutton(master, text="optional: HAWK, GO THERE (need controllers) ",padx=10, variable=v, value=1,command=ShowChoice).grid(row=6, column=0,sticky=W, pady=5, padx=5)
   r2 = Radiobutton(master, text="HAWK, STOP ",padx=10, variable=v, value=2,command=ShowChoice).grid(row=7, column=0,sticky=W, pady=5, padx=5)
   r3 = Radiobutton(master, text="HAWK, SEARCH THAT LAKE FOR KITE (use controllers or click on openease) ",padx=10, variable=v, value=3,command=ShowChoice).grid(row=8, column=0,sticky=W, pady=5, padx=5)
   r4 = Radiobutton(master, text="HAWK, LAND ON HELIPAD",padx=0, variable=v, value=4, command=ShowChoice).grid(row=9, column=0,sticky=W, pady=5, padx=5) 
   r12 = Radiobutton(master, text="DONKEY, UNMOUNT RED WASP (if mounted)",padx=0, variable=v, value=12, command=ShowChoice).grid(row=10, column=0,sticky=W, pady=5, padx=5)
   r13 = Radiobutton(master, text="DONKEY, UNMOUNT BLUE WASP (if mounted)",padx=0, variable=v, value=13, command=ShowChoice).grid(row=11, column=0,sticky=W, pady=5, padx=5)
   r5 = Radiobutton(master, text="RED WASP, SEARCH THAT BRIDGE FOR VICTIM (click on openease)",padx=0, variable=v, value=5, command=ShowChoice).grid(row=12, column=0,sticky=W, pady=5, padx=5)
   r6 = Radiobutton(master, text="BLUE WASP, SEARCH THAT BRIDGE FOR VICTIM (click on openease)",padx=0, variable=v, value=6, command=ShowChoice).grid(row=13, column=0,sticky=W, pady=5, padx=5) 
   r7 = Radiobutton(master, text="DONKEY, GO TO VICTIM",padx=0, variable=v, value=7, command=ShowChoice).grid(row=14, column=0,sticky=W, pady=5, padx=5) 
   r8 = Radiobutton(master, text="BLUE WASP, GO TO VICTIM",padx=0, variable=v, value=8, command=ShowChoice).grid(row=15, column=0,sticky=W, pady=5, padx=5) 
   r9 = Radiobutton(master, text="RED WASP, CHARGE",padx=0, variable=v, value=9, command=ShowChoice).grid(row=16, column=0,sticky=W, pady=5, padx=5)
   r10 = Radiobutton(master, text="BLUE WASP, TAKE PICTURE",padx=0, variable=v, value=10, command=ShowChoice).grid(row=17, column=0,sticky=W, pady=5, padx=5)
   r11 = Radiobutton(master, text="BLUE WASP, CHARGE",padx=0, variable=v, value=11, command=ShowChoice).grid(row=18, column=0,sticky=W, pady=5, padx=5)
#   r1 = Radiobutton(master, text="RED WASP ",padx=10, variable=v, value=1,command=ShowChoice).grid(row=6, column=1,sticky=W, pady=4, padx=4)
#   r2 = Radiobutton(master, text="BLUE WASP",padx=0, variable=v, value=2, command=ShowChoice).grid(row=7, column=1,sticky=W, pady=4, padx=4) 
#   r3 = Radiobutton(master, text="HAWK",padx=0, variable=v, value=3, command=ShowChoice).grid(row=8, column=1,sticky=W, pady=4, padx=4)
#   r4 = Radiobutton(master, text="DONKEY",padx=0, variable=v, value=4, command=ShowChoice).grid(row=9, column=1,sticky=W, pady=4, padx=4) 
   rospy.Subscriber("recognizer/output", String, publisher_callback)
   rospy.Subscriber("/speaker_on", String, speaker_callback)
   rospy.Subscriber("/display_command",String, displayer_callback)
   mainloop( )
   #rospy.spin()
   
