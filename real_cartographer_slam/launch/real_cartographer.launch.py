import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import TimerAction

from launch_ros.actions import Node

def generate_launch_description():

    cartographer_config_dir = os.path.join(get_package_share_directory('real_cartographer_slam'), 'config')
    configuration_basename = 'real_cartographer.lua'

    return LaunchDescription([
        
        Node(
            package='cartographer_ros', 
            executable='cartographer_node', 
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': False}],
            arguments=['-configuration_directory', cartographer_config_dir,
                       '-configuration_basename', configuration_basename],
            remappings=[
                    ("/tf", "/cleaner_2/tf"),
                    ("/odom", "/cleaner_2/odom"),
                    ("/scan", "/cleaner_2/scan"),
                ],
        ),
            
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': False}],
            arguments=['-resolution', '0.01', '-publish_period_sec', '1.0'],
                remappings=[
                    ("/tf", "/cleaner_2/tf"),
                    ("/odom", "/cleaner_2/odom"),
                    ("/scan", "/cleaner_2/scan"),
                ],
        ),

        TimerAction(
                period=2.0,
                actions=[
                    Node(
                        package="tf2_ros",
                        executable="static_transform_publisher",
                        name="static_transform_publisher",
                        namespace="",
                        output="screen",
                        remappings=[
                            ("/tf", "/cleaner_2/tf"),
                        ],
                        arguments=[
                            "0.075", "0", "0.150", "0", "0", "0", "base_footprint", "cleaner_2/laser_sensor_link"
                        ]
                    ),

                ]
            )      
    ]) 