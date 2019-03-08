# -*- coding: utf-8; -*-
#!/usr/bin/env python
#
# (c) 2017 SENAI CIMATEC/ITV.
#
# This file is part of Geonosis systems.
#
#
from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['core'],
    package_dir={'': 'src'},
    scripts=['scripts/go_aruco_finished.py'],
    requires=['rospy', ' std_msgs']
)

setup(**d)