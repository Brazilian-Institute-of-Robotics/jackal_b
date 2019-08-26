# jackal_b

# Guide to use Jackal goaltogoal

------------------------- RUN JACKAL --------------------
1- Build and source 
 cd jackal_ws; catkin_make; source devel/setup.bash
 
2- rosrun

3- Launch the jackal 

DO that 

In terminal 1 :

roslaunch jackal_gazebo jackal_world.launch config:=front_laser gui:=false

In terminal 2 :

roslaunch jackal_viz view_robot.launch

-----------or-------------

roslaunch jackal_gazebo jackal_world.launch

------------------------ Jackal with joy -----------------------------
1- run the joy node

rosrun joy joy_node 

2-  run the plugin

rosrun advisoring jackalteleop.py

-----------------or ---------------
1 - rosrun

2- roslaunch advisoring jackal_run.launch 

3- done.
---------------------------- Jackal go to goal----------------------
1 - rosrun

2 - roslaunch jackal_gazebo jackal_world.launch

3- rosrun advisoring gotogoal_jackal2.py
