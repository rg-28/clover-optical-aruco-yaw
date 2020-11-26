# clover-drone-optical-yaw

This repository contains the packages required for optical flow and aruco marker based navigation of COEX clover drone (simulation).

* For running the simulation follow these steps given below:
    * Clone this repository into a catkin workspace named as **clover_ws**
    * Run the following commands to setup the required dependencies for your simulation.
        Installing PX4 prerequisites:
        * **cd ~/clover_ws/src/Firmware/Tools/setup**
        * **sudo ./ubuntu.sh --no-nuttx**

        Patching Gazebo plugins:
        * **cd ~/clover_ws/src/Firmware/Tools/sitl_gazebo**
        * **wget https://raw.githubusercontent.com/CopterExpress/clover_vm/master/assets/patches/sitl_gazebo.patch**
        * **patch -p1 < sitl_gazebo.patch**
        * **rm sitl_gazebo.patch**

        Installing Geographiclib Dataset:
        * **cd ~/**
        * **wget https://raw.githubusercontent.com/mavlink/mavros/6f5bd5a1a67c19c2e605f33de296b1b1be9d02fc/mavros/scripts/install_geographiclib_datasets.sh**
        * **chmod +x ./install_geographiclib_datasets.sh**
        * **sudo ./install_geographiclib_datasets.sh**
        * **rm ./install_geographiclib_datasets.sh**

        Buiilding the simulator:
        * **cd ~/clover_ws**
        * **catkin build**

        **Note:** If there comes an error while building the packages related to **cv2.aruco** the run the following command and try again:
        * **python3 -m pip install opencv-contrib-python**

        Testing if the simulation is running or not:
        * **source ~/clover_ws/devel/setup.bash**
        * **roslaunch clover_simulation simulator.launch**

        Installing QGroundControl:
        * **sudo usermod -a -G dialout $USER**
        * **sudo apt-get remove modemmanager -y**
        * **sudo apt install gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl -y**
        * Logout and login again to enable the change to user permissions.
        * Download [QGroundControl.AppImage](https://s3-us-west-2.amazonaws.com/qgroundcontrol/latest/QGroundControl.AppImage)
        * Move to where the above file has been downloaded.
        * **chmod +x ./QGroundControl.AppImage**
        * **./QGroundControl.AppImage**  (or double click)

        Changing the required PID parameters: (Perform these steps while the simulation is running.)
        * Open QGroundControl
        * Move to **Settings** and then the **Parameters** section of the QGroundControl
        * In the serch bar enter **MPC_VEL_XY_P**
        * Check if its value is set to **0.9** (if not, change it and then save it).
    * For running the automatic version of the simulation (i.e. without entering any required values) run the following commands:
        * **source ~/clover_ws/devel/setup.bash**
        * **roslaunch clover_simulation simulator.launch**
        * **rosrun clover_simulation offboard_node_auto.py**
    * For running the user dependent version of the simulation (i.e. the required values are entered by the user) run the following commands:
        * **source ~/clover_ws/devel/setup.bash**
        * **roslaunch clover_simulation simulator.launch**
        * **rosrun clover_simulation offboard_node_user.py**
