#!/usr/bin/env python
from Tkinter import *
import rospy
from std_msgs.msg import String
from instructor_mission.msg import protocol_dialogue
from instructor_mission.srv import call_cmd
import time
import sys
import rospkg

checker="false"


def func(event):
   print "return "
   e1.delete("end-1c",END)
   show_entry_fields()

def publisher_callback(data):
   print "publisher"
   if checker == "true":
      if data.data != "SWITCH":
         result = data.data
         print result
         print "mittig"
         result.replace("\n","")
         print result
         print "result: "
         string = String()
         string.data = result
         pub = rospy.Publisher('/internal/recognizer/output', String, queue_size=10)
         pub.publish(result)
      else:
         change_image_field()

def change_image_field():
   print "field"
   global checker
   if checker == "false":
      checker = "true"
      b1.config(image=on)    
   else:
      checker = "false"
      b1.config(image=off)

def show_entry_fields():
   print "show"
   print len(e1.get("1.0","0.0"))
   print len(e1.get("0.0",END))
   print len(e1.get("end-1c",END))
   print len(e1.get("1.0", "end-1c"))
   if len(e1.get("1.0", "end-1c")) == 0 or  len(e1.get("1.0", "end-1c")) == 1:
      window.insert(INSERT,'Please give a command!\n','rotcolor')
      e1.delete("1.0","end-1c")
   else:
      entry_text = e1.get("1.0","end-1c")
      e1.delete("1.0","end-1c")
      window.insert(INSERT,'Genius:  ','hcolor')
      window.insert(END,entry_text+'\n','hnbcolor')
      print entry_text
      print "mittig"
      entry_text.replace("\n","")
      print entry_text
      string = String()
      string.data = entry_text
      pub = rospy.Publisher('/internal/recognizer/output', String, queue_size=10)
      pub.publish(string)


if __name__ == "__main__":
   rospy.init_node('gui_node', anonymous=True)
   master = Tk()
   master.title("Dialogue Interface")
   window = Text(master, height=40, width=70)
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
   
   master.bind('<Return>',func)
   Button(master, text='Quit', font=('Arial', 12,'bold', 'italic'), foreground='#ff8000',command=master.quit).grid(row=5, column=1,sticky=W, padx=16)
   Button(master, text='Enter', font=('Arial', 12,'bold', 'italic'),command=show_entry_fields).grid(row=1, column=0, sticky=W, pady=4, padx=4)
   rospy.Subscriber("recognizer/output", String, publisher_callback)
 
   mainloop( )
  # rospy.spin()
   
