# jackal_b
development platform for assimilation of robotic concepts
## What you will found in this repository:
* Teleoperation with joystick:

    ------------------------- RUN JACKAL --------------------

1 Build and source the workspace jackal_ws (if you have the workspace jackal_ws)

`Build and source cd jackal_ws; catkin_make; source devel/setup.bash`

If you want jackal with a laser scan:

In terminal:

`roslaunch jackal_gazebo jackal_world.launch config:=front_laser gui:=false`

If you want jackal without a laser scan:

`roslaunch jackal_gazebo jackal_world.launch`

* Jackal with joy 
1- Roscore

`roscore`

2- run the joy node

`rosrun joy joy_node`

3- run the plugin

`rosrun advisoring jackalteleop.py`

* Jackal go to goal 

1 - ` roscore`

2 - `roslaunch jackal_gazebo jackal_world.launch`

3- `rosrun advisoring gotogoal_jackal2.py`

* Jackal go to goal after aruco reconiction 

1 - ` roscore `

2 - `roslaunch jackal_gazebo jackal_world.launch`

3 - ` go_aruco_finished.py` 

4 - ` opencv4.py` 
