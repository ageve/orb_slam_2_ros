import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

#=====================================
#        VARIABLES
#=====================================
#[x y z yaw pitch roll frame_id child_frame_id ]
map_joint = ['0', '0', '0', '0', '0', '0', 'map', 'camera']

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = LaunchConfiguration('params_file')
    voc_file = LaunchConfiguration('voc_file')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        DeclareLaunchArgument(
            'params_file',
            default_value=os.path.join(
                get_package_share_directory("orb_slam2_ros"),
                'ros', 'config', 'params_usbCam.yaml'),
            description='Full path to the ROS2 parameters file to use for all launched nodes'),

        DeclareLaunchArgument(
            'voc_file',
            default_value=os.path.join(
                get_package_share_directory("orb_slam2_ros"),
                'orb_slam2', 'Vocabulary', 'ORBvoc.txt'),
            description='Full path to vocabulary file to use'),

        # MAP JOINT
        Node(
           package='tf2_ros',
           executable='static_transform_publisher',
           output='screen',
           arguments=map_joint),

        Node(
            parameters=[
              params_file,
              {"voc_file": voc_file,
               "use_sim_time": use_sim_time},
            ],
            package='orb_slam2_ros',
            executable='orb_slam2_ros_mono',
            name='orb_slam2_mono',
            output='screen'
        )
    ])
