#!/usr/bin/env python

from instructor_mission.srv import *
import rospy

speech_output = ""
value = ""

def parsing(res):
    global value
    result = res.split(" ")
    value = ""
    # if result[1] == "picture":
    #     action = result[0]+"-picture"
    #     shape = "null"
    #     spatial = "null"
    #     pointing = "false"
    #     object = "null"
    #     value = action + " " + spatial + " " + shape + " " + pointing + " " +object
    # elif len(result) == 2:
    #     print "und nun?"
    #     if result[1] == "area" or result[1] == "region":
    #         action = "scan-area"
    #         spatial = "null"
    #     elif result[1] == "back":
    #         action = "come-back"
    #         spatial = "null"
    #     elif result[1] == "off":
    #         action = "take-off"
    #         spatial = "null"
    #     else:
    #         action = result[0]
    #         spatial = result[1]
    #     value = action + " " + spatial + " " + "null" + " " + "false" + " " +"null"
   

    new_result = res.split(" and ")
    if len(new_result) == 1:
        resume = new_result[0].split(" ")
       
        if len(resume) == 1:
            if resume[0] == "stop":
                value = resume[0] + " null " + "null" + " " + "false" + " " +"null"
            elif resume[0] == "follow-me":
                value = resume[0]+" "+ "null" + " null" + " " + "false" + " " +"null"
            elif resume[0] == "go-there" or resume[0] == "move-there":
                value = resume[0]+" "+ "null" + " null" + " " + "false" + " " +"null"
            elif resume[0] == "land":
                value = resume[0]+" "+ "null" + " null" + " " + "false" + " " +"null"
            #elif resume[0] == "go-straight" or resume[0] == "go-ahead" or "move-straight" or resume[0] == "move-ahead":
                #value = resume[0]+" "+ "null" + " null" + " " + "false" + " " +"null"
        elif len(resume) == 2:
            if resume[1] == "picture":
                value = resume[0]+ "-picture" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "area" or resume[1] == "region":
                value = resume[0]+ "-area" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "back":
                value = resume[0]+ "-back" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "robot":
                value = resume[0]+ "-robot" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "off":
                value = resume[0]+ "-off" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[0] == "follow":
                value = resume[0]+ "-me" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[0] == "look-for" or resume[0] == "search-for":
                value = resume[0]+" "+ "null" + " null" + " " + "false" + " " +resume[1]
            else:
                action = resume[0]
                spatial = resume[1]
                value = action+" "+ spatial + " null" + " " + "false" + " " +"null"
        elif len(resume) == 3:
         
            if resume[0] == "look" and resume[1] == "for":
                action = resume[0]+"-for"
                spatial = "null"
                object = resume[2]
                value = action+" "+ spatial + " null" + " " + "false" + " " +object
            elif resume[0] == "search" and resume[1] == "for":
                action = resume[0]+"-for"
                spatial = "null"
                object = resume[2]
                value = action+" "+ spatial + " null" + " " + "false" + " " +object
            elif resume[0] == "scan" and resume[1] == "that":
                value = "scan"+" "+ "null" + " null" + " " + "true" + " " +resume[2]
            else:
                action = resume[0]
                spatial = resume[1]
                object = resume[2]
                value = action+" "+ spatial + " null" + " " + "false" + " " +object
        elif len(resume) == 4:
            action = resume[0]
            spatial = resume[1]
            if resume[2] == "to" or resume[2] == "right" or resume[2] == "left" or resume[2] == "behind" or resume[2] == "close" or resume[2] == "front" or resume[2] == "back" or resume[2] == "next":
                spatial2 = resume[2]
                object = resume[3]
                value = action + " "+ spatial+ " "+ "null"+" "+"false"+" null"+" 1 "+spatial2+ " "+"null"+" "+"false"+" "+object
            elif resume[2] == "big" or resume[2] == "small":
                value = action + " "+ spatial+ " "+ resume[2]+" "+"false "+resume[3]               
            elif resume[2] == "that":
                value = action + " "+ spatial+ " "+ "null"+" "+"true "+resume[3]

        elif len(resume) == 5:
            action = resume[0]
            spatial = resume[1]
            if resume[2] == "to" or resume[2] == "right" or resume[2] == "left" or resume[2] == "behind" or resume[2] == "close" or resume[2] == "front" or resume[2] == "back" or resume[2] == "next":
                spatial2 = resume[2]
                object = resume[4]
                if resume[3] == "big" or resume[3] == "small":
                    shape = resume[3]
                    pointing = "false"
                else:
                    shape = "null"
                    pointing = "true"
                value = action+" "+spatial+" "+"null"+" "+"false"+ " "+"null"+" 1 "+ spatial2+ " "+shape+" "+pointing+" "+object
            elif resume[3] == "to" or resume[3] == "right" or resume[3] == "left" or resume[3] == "behind" or resume[3] == "close" or resume[3] == "front" or resume[3] == "back" or resume[3] == "next":
                value = action+" "+resume[1]+" "+"null"+" "+"false"+" "+resume[2]+" 1 "+resume[3]+ " null "+"false"+" "+resume[4]
        elif len(resume) == 6: #Go to big tree next rock or Go to tree next big rock
            action=resume[0]
            spatial = resume[1]
            if resume[2] == "big" or resume[2] == "small":
                shape = resume[2]
                value = action+" "+spatial+" "+shape+" "+"false"+ " "+resume[3]+" 1 "+resume[4]+" "+"null"+" "+"false "+resume[5]
            elif resume[2] == "that":
                pointing = "true"
                value = action+" "+spatial+" "+"null"+" "+"true"+ " "+resume[3]+" 1 "+resume[4]+" "+"null"+" "+"false "+resume[5]
            
            if resume[4] == "big" or resume[4] == "small":
                shape2 = resume[4]
                value = action+" "+spatial+" "+"null"+" "+"false"+ " "+resume[2]+" 1 "+resume[3]+" "+shape2+" "+"false "+resume[5]
            elif resume[4] == "that":
                value = action+" "+spatial+" "+"null"+" "+"false"+ " "+resume[2]+" 1 "+resume[3]+" "+"null"+" "+"true "+resume[5]
                                
            
        elif len(resume) == 7: #Go to big tree next big rock
            action=resume[0]
            spatial = resume[1]
            spatial2 = resume[4]
            object = resume[3]
            object2 =resume[6]
            shape = "null"
            shape2 = "null"
            pointing = "false"
            pointing2 = "false"
            if resume[2] == "big" or resume[2] == "small":
                shape = resume[2]
            elif resume[2] == "that":
                pointing = "true"

            if resume[5] == "big" or resume[5] == "small":
                shape2 = resume[5]
            elif resume[5] == "that":
                pointing2 = "true"
                
            value = action+" "+spatial+" "+shape+" "+pointing+" "+object+" 1 "+spatial2+" "+shape2+" "+pointing2+" "+object2
    
    if len(new_result) >= 2:
        resume = new_result[0].split(" ")
     
        if len(resume) == 1:
            if resume[0] == "stop":
                value = resume[0] + " null " + "null" + " " + "false" + " " +"null"
            elif resume[0] == "follow-me":
                value = resume[0]+" "+ "null" + " null" + " " + "false" + " " +"null"
            elif resume[0] == "go-there" or resume[0] == "move-there":
                value = resume[0]+" "+ "null" + " null" + " " + "false" + " " +"null"
            #elif resume[0] == "go-straight" or resume[0] == "go-ahead" or "move-straight" or resume[0] == "move-ahead":
                #value = resume[0]+" "+ "null" + " null" + " " + "false" + " " +"null"
        elif len(resume) == 2:
            if resume[1] == "picture":
                value = resume[0]+ "-picture" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "area" or resume[1] == "region":
                value = resume[0]+ "-area" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "back":
                value = resume[0]+ "-back" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "robot":
                value = resume[0]+ "-robot" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "off":
                value = resume[0]+ "-off" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[0] == "follow":
                value = resume[0]+ "-me" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[0] == "look-for" or resume[0] == "search-for":
                value = resume[0]+" "+ "null" + " null" + " " + "false" + " " +resume[1]
            else:
                action = resume[0]
                spatial = resume[1]
                value = action+" "+ spatial + " null" + " " + "false" + " " +"null"
        elif len(resume) == 3:
       
            if resume[0] == "look" and resume[1] == "for":
                action = resume[0]+"-for"
                spatial = "null"
                object = resume[2]
                value = action+" "+ spatial + " null" + " " + "false" + " " +object
            elif resume[0] == "search" and resume[1] == "for":
                action = resume[0]+"-for"
                spatial = "null"
                object = resume[2]
                value = action+" "+ spatial + " null" + " " + "false" + " " +object
            elif resume[0] == "scan" and resume[1] == "that":
                value = "scan"+" "+ "null" + " null" + " " + "true" + " " +resume[2]
            else:
                action = resume[0]
                spatial = resume[1]
                object = resume[2]
                value = action+" "+ spatial + " null" + " " + "false" + " " +object
        elif len(resume) == 4:
            action = resume[0]
            spatial = resume[1]
            if resume[2] == "to" or resume[2] == "right" or resume[2] == "left" or resume[2] == "behind" or resume[2] == "close" or resume[2] == "front" or resume[2] == "back" or resume[2] == "next":
                spatial2 = resume[2]
                object = resume[3]
                value = action + " "+ spatial+ " "+ "null"+" "+"false"+" null"+" 1 "+spatial2+ " "+"null"+" "+"false"+" "+object
            elif resume[2] == "big" or resume[2] == "small":
                value = action + " "+ spatial+ " "+ resume[2]+" "+"false "+resume[3]               
            elif resume[2] == "that":
                value = action + " "+ spatial+ " "+ "null"+" "+"true "+resume[3]

        elif len(resume) == 5:
            action = resume[0]
            spatial = resume[1]
            if resume[2] == "to" or resume[2] == "right" or resume[2] == "left" or resume[2] == "behind" or resume[2] == "close" or resume[2] == "front" or resume[2] == "back" or resume[2] == "next":
                spatial2 = resume[2]
                object = resume[4]
                if resume[3] == "big" or resume[3] == "small":
                    shape = resume[3]
                    pointing = "false"
                else:
                    shape = "null"
                    pointing = "true"
                value = action+" "+spatial+" "+"null"+" "+"false"+ " "+"null"+" 1 "+ spatial2+ " "+shape+" "+pointing+" "+object
            elif resume[3] == "to" or resume[3] == "right" or resume[3] == "left" or resume[3] == "behind" or resume[3] == "close" or resume[3] == "front" or resume[3] == "back" or resume[3] == "next":
                value = action+" "+resume[1]+" "+"null"+" "+"false"+" "+resume[2]+" 1 "+resume[3]+ " null "+"false"+" "+resume[4]
        elif len(resume) == 6: #Go to big tree next rock or Go to tree next big rock
            action=resume[0]
            spatial = resume[1]
            if resume[2] == "big" or resume[2] == "small":
                shape = resume[2]
                value = action+" "+spatial+" "+shape+" "+"false"+ " "+resume[3]+" 1 "+resume[4]+" "+"null"+" "+"false "+resume[5]
            elif resume[2] == "that":
                pointing = "true"
                value = action+" "+spatial+" "+"null"+" "+"true"+ " "+resume[3]+" 1 "+resume[4]+" "+"null"+" "+"false "+resume[5]
            
            if resume[4] == "big" or resume[4] == "small":
                shape2 = resume[4]
                value = action+" "+spatial+" "+"null"+" "+"false"+ " "+resume[2]+" 1 "+resume[3]+" "+shape2+" "+"false "+resume[5]
            elif resume[4] == "that":
                value = action+" "+spatial+" "+"null"+" "+"false"+ " "+resume[2]+" 1 "+resume[3]+" "+"null"+" "+"true "+resume[5]
                                
            
        elif len(resume) == 7: #Go to big tree next big rock
            action=resume[0]
            spatial = resume[1]
            spatial2 = resume[4]
            object = resume[3]
            object2 =resume[6]
            shape = "null"
            shape2 = "null"
            pointing = "false"
            pointing2 = "false"
            if resume[2] == "big" or resume[2] == "small":
                shape = resume[2]
            elif resume[2] == "that":
                pointing = "true"

            if resume[5] == "big" or resume[5] == "small":
                shape2 = resume[5]
            elif resume[5] == "that":
                pointing2 = "true"
        value_1 = value
        ########################################################################################################
        ########################################################################################################
        resume = new_result[1].split(" ")
  
        if len(resume) == 1:
            if resume[0] == "stop":
                value = value_1+" 0 "+resume[0] + " null " + "null" + " " + "false" + " " +"null"
            elif resume[0] == "follow-me":
                value = value_1+" 0 "+resume[0]+" "+ "null" + " null" + " " + "false" + " " +"null"
            elif resume[0] == "go-there" or resume[0] == "move-there":
                value = value_1+" 0 "+resume[0]+" "+ "null" + " null" + " " + "false" + " " +"null"
            #elif resume[0] == "go-straight" or resume[0] == "go-ahead" or "move-straight" or resume[0] == "move-ahead":
                #value = resume[0]+" "+ "null" + " null" + " " + "false" + " " +"null"
        elif len(resume) == 2:
            if resume[1] == "picture":
                value = value_1+" 0 "+resume[0]+ "-picture" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "area" or resume[1] == "region":
                value = value_1+" 0 "+resume[0]+ "-area" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "back":
                value = value_1+" 0 "+resume[0]+ "-back" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "robot":
                value = value_1+" 0 "+resume[0]+ "-robot" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[1] == "off":
                value = value_1+" 0 "+resume[0]+ "-off" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[0] == "follow":
                value = value_1+" 0 "+resume[0]+ "-me" + " null " + "null" + " " + "false" + " " +"null"
            elif resume[0] == "look-for" or resume[0] == "search-for":
                value = value_1+" 0 "+resume[0]+" "+ "null" + " null" + " " + "false" + " " +resume[1]
            else:
                action = resume[0]
                spatial = resume[1]
                value = value_1+" 0 "+action+" "+ spatial + " null" + " " + "false" + " " +"null"
        elif len(resume) == 3:
     
            if resume[0] == "look" and resume[1] == "for":
                action = resume[0]+"-for"
                spatial = "null"
                object = resume[2]
                value = value_1+" 0 "+action+" "+ spatial + " null" + " " + "false" + " " +object
            elif resume[0] == "search" and resume[1] == "for":
                action = resume[0]+"-for"
                spatial = "null"
                object = resume[2]
                value = value_1+" 0 "+action+" "+ spatial + " null" + " " + "false" + " " +object
            elif resume[0] == "scan" and resume[1] == "that":
                value = value_1+" 0 "+"scan"+" "+ "null" + " null" + " " + "true" + " " +resume[2]
            else:
                action = resume[0]
                spatial = resume[1]
                object = resume[2]
                value = value_1+" 0 "+action+" "+ spatial + " null" + " " + "false" + " " +object
        elif len(resume) == 4:
            action = resume[0]
            spatial = resume[1]
            if resume[2] == "to" or resume[2] == "right" or resume[2] == "left" or resume[2] == "behind" or resume[2] == "close" or resume[2] == "front" or resume[2] == "back" or resume[2] == "next":
                spatial2 = resume[2]
                object = resume[3]
                value = value_1+" 0 "+action + " "+ spatial+ " "+ "null"+" "+"false"+" null"+" 1 "+spatial2+ " "+"null"+" "+"false"+" "+object
            elif resume[2] == "big" or resume[2] == "small":
                value = value_1+" 0 "+action + " "+ spatial+ " "+ resume[2]+" "+"false "+resume[3]               
            elif resume[2] == "that":
                value = value_1+" 0 "+action + " "+ spatial+ " "+ "null"+" "+"true "+resume[3]

        elif len(resume) == 5:
            action = resume[0]
            spatial = resume[1]
            if resume[2] == "to" or resume[2] == "right" or resume[2] == "left" or resume[2] == "behind" or resume[2] == "close" or resume[2] == "front" or resume[2] == "back" or resume[2] == "next":
                spatial2 = resume[2]
                object = resume[4]
                if resume[3] == "big" or resume[3] == "small":
                    shape = resume[3]
                    pointing = "false"
                else:
                    shape = "null"
                    pointing = "true"
                value = value_1+" 0 "+action+" "+spatial+" "+"null"+" "+"false"+ " "+"null"+" 1 "+ spatial2+ " "+shape+" "+pointing+" "+object
            elif resume[3] == "to" or resume[3] == "right" or resume[3] == "left" or resume[3] == "behind" or resume[3] == "close" or resume[3] == "front" or resume[3] == "back" or resume[3] == "next":
                value = value_1+" 0 "+action+" "+resume[1]+" "+"null"+" "+"false"+" "+resume[2]+" 1 "+resume[3]+ " null "+"false"+" "+resume[4]
        elif len(resume) == 6: #Go to big tree next rock or Go to tree next big rock
            action=resume[0]
            spatial = resume[1]
            if resume[2] == "big" or resume[2] == "small":
                shape = resume[2]
                value = value_1+" 0 "+action+" "+spatial+" "+shape+" "+"false"+ " "+resume[3]+" 1 "+resume[4]+" "+"null"+" "+"false "+resume[5]
            elif resume[2] == "that":
                pointing = "true"
                value = value_1+" 0 "+action+" "+spatial+" "+"null"+" "+"true"+ " "+resume[3]+" 1 "+resume[4]+" "+"null"+" "+"false "+resume[5]
            
            if resume[4] == "big" or resume[4] == "small":
                shape2 = resume[4]
                value = value_1+" 0 "+action+" "+spatial+" "+"null"+" "+"false"+ " "+resume[2]+" 1 "+resume[3]+" "+shape2+" "+"false "+resume[5]
            elif resume[4] == "that":
                value = value_1+" 0 "+action+" "+spatial+" "+"null"+" "+"false"+ " "+resume[2]+" 1 "+resume[3]+" "+"null"+" "+"true "+resume[5]
                                
            
        elif len(resume) == 7: #Go to big tree next big rock
            action=resume[0]
            spatial = resume[1]
            spatial2 = resume[4]
            object = resume[3]
            object2 =resume[6]
            shape = "null"
            shape2 = "null"
            pointing = "false"
            pointing2 = "false"
            if resume[2] == "big" or resume[2] == "small":
                shape = resume[2]
            elif resume[2] == "that":
                pointing = "true"

            if resume[5] == "big" or resume[5] == "small":
                shape2 = resume[5]
            elif resume[5] == "that":
                pointing2 = "true"
            value =  value_1+" 0 "+action+" "+spatial+" "+shape+" "+pointing+" "+object+" 1 "+spatial2+" "+shape2+" "+pointing2+" "+object2
    print value

    

def call_parser(req):
    print "Returning the value"
    parsing(req.goal)
    speech_output = value
    return text_parserResponse(speech_output)


def start_parser_server():
    rospy.init_node("rosparser_server")
    s = rospy.Service("ros_parser", text_parser, call_parser)
    print "Parser is ready for new instructions!"
    rospy.spin()

if __name__== "__main__":
    start_parser_server()
