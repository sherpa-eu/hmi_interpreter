#!/usr/bin/env python
" author: Fereshta Yazdani"

from std_msgs.msg import String
from visualization_msgs.msg import *
import rospy
import os, sys
import os.path
import random

inFile = "hmi_cram_location_marker_tmp.json"
path = "/home/yazdani/work/docker/episodes/Rescue-Mission/scenario_0/episode_0/"

def publisher():
    pub = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=10)
    rospy.init_node('marker_publisher', anonymous=True)
    markerArray = MarkerArray()
    marker = Marker()
    counter = 1000
    with open(path+inFile,'r') as i:
        lines = i.readlines()
        
    for line in lines:
        tmp = line.split(",")
        setter = 1
        settery = 1
        setterz = 1
        counter = counter + 1
    #    print line
        for index in tmp:
            print index
            marker.id = counter
            marker.type = marker.CUBE
            marker.action = marker.DELETE
            marker.mesh_use_embedded_materials = True
            if "text" in index:
                print "Don't use this one!"
            elif "x" in index and setter == 1:
                tmpx = index.split(":")
                tmpx = tmpx[1]
                # marker.id = random.randint(1,100)
                marker.scale.x = float(tmpx)
                setter = 2
            elif "x" in index and setter == 2:
                tmpx = index.split(":")
                tmpx = tmpx[1]
                # marker.id = random.randint(1,100)
                marker.pose.position.x = float(tmpx)
                setter = 3
            elif "x" in index and setter == 3:
                setter = 1
                tmpx = index.split(":")
                tmpx = tmpx[1]
                marker.pose.orientation.x = float(tmpx)
            #    pub.publish(marker)
            elif "type" in index:
                print "Don't use this one!"
            elif "y" in index and settery == 1:
                tmpy = index.split(":")
                tmpy = tmpy[-1]
                # marker.id = random.randint(1,100)
                marker.scale.y = float(tmpy)
                settery = 2
            elif "y" in index and settery == 2:
                tmpy = index.split(":")
                tmpy = tmpy[-1]
                marker.pose.position.y = float(tmpy)
                settery = 3
            elif "y" in index and settery == 3:
                settery = 1
                tmpy = index.split(":")
                tmpy = tmpy[-1]
                marker.pose.orientation.y = float(tmpy)
                #pub.publish(marker)
            elif "z" in index and setterz == 1:
                tmpz = index.split("}")
                tmpz = tmpz[0].split(":")
                tmpz = tmpz[1]
                marker.scale.z = float(tmpz)
                setterz = 2
            elif "z" in index and setterz == 2:
                tmpz = index.split("}")
                tmpz = tmpz[0].split(":")
                tmpz = tmpz[1]
                marker.pose.position.z = float(tmpz)
                setterz = 3
            elif "z" in index and setterz == 3:
                tmpz = index.split("}")
                tmpz = tmpz[0].split(":")
                tmpz = tmpz[1]
                marker.pose.orientation.z = float(tmpz)
                setterz = 1
            elif "w" in index:
                tmpw = index.split("}")
                tmpw = tmpw[0].split(":")
                marker.pose.orientation.w = float(tmpw[1])
            elif "topic" in index:
                topic = index.split(":")
                marker.ns = topic[1]
            elif "a" in index:
                if "color" in index:
                    tmpa = index.split(":")
                    marker.color.a = 0.6#float(tmpa[-1])
                    marker.color.r = 1.0#float(tmpa[-1])
            elif "b" in index:
                if "oid" in index:
                    print ""
                else:
                    tmpb = index.split(":")
                    marker.color.b = 0.0#float(tmpb[-1])
            elif "g" in index:
                print index
                tmpg = index.split("}")
                tmpg = tmpg[0].split(":")
                marker.color.g = 0.0#float(tmpg[-1])
        
        markerArray.markers.append(marker)
        marker = Marker()
    pub.publish(markerArray)
    markerArray = MarkerArray()
    counter = 1000
                
if __name__== "__main__":
    
    publisher()
