#include "ros/ros.h"
#include "std_msgs/String.h"

#include <sstream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include "sensor_msgs/Image.h"
#include <cstdlib>
#include <string>
#include "hmi_interpreter/text_parser.h"
#include <stdlib.h> 
#include <ros/package.h>

using namespace std;
using namespace cv;


static int indexy;
static int indexi;
static string kette;
static int indexer;
static std_msgs::String ts;
ros::Subscriber sub;


void callback(const sensor_msgs::ImageConstPtr& msg)
{
  ROS_INFO_STREAM("DID WORK");
  std::string path = ros::package::getPath("hmi_interpreter") + "/nodes_py/logfiles/imgs/";
  cv::imwrite(path+kette,cv_bridge::toCvShare(msg, "bgr8")->image);
  cv::waitKey(30);
}


bool check(hmi_interpreter::text_parser::Request  &req,
	   hmi_interpreter::text_parser::Response &res)
{  
  ROS_INFO_STREAM("aehm");
  indexy = 1;
  indexer = rand() % 10000;
  stringstream ss;
  ss << indexer;
  string str = ss.str();
  kette = req.goal+".jpg";
  res.result = req.goal+".jpg";
  return true;
}

int main(int argc, char **argv)
{
  // extern int indexy;
  ros::init(argc, argv, "GetThatString");
  ros::NodeHandle n;
  ros::NodeHandle nh;
  ros::NodeHandle n_pub;
  ros::Rate loop_rate(2);

  ros::Publisher chatter_pub = n_pub.advertise<std_msgs::String>("img_publisher", 1000);
  ts.data = "";
	    chatter_pub.publish(ts);
  ros::ServiceServer service = n.advertiseService("store_image", check);
  indexy = 0;
  indexi = 0;
  kette = "";
  while(ros::ok())
    {
      
      if(indexy == 1)
      	{
      	  while(indexi < 5)
      	    {
	      ros::Subscriber  sub = nh.subscribe("/camera/rgb/image_raw", 1, callback);
	      
	      //ROS_INFO_STREAM(indexi);
	      // ROS_INFO_STREAM(indexy == 1);
	      //    std::cout << indexy << std::endl;
	      
	      indexi = indexi +1;
	      if (indexi >= 4)
		{
		  break;
		}
	      loop_rate.sleep();
	      ros::spinOnce();
	    }
	
	  
	  
	  ts.data = kette;
	    chatter_pub.publish(ts);
	  // ROS_INFO_STREAM(kette);
	  indexy = 0;
	  indexi = 0;
		}  
      ros::spinOnce();
    }
  //ros::spin();

  return 0;
}
