import launch
import launch_ros
import os

from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

  use_sim_time = launch.substitutions.LaunchConfiguration('use_sim_time')
  world = launch.substitutions.LaunchConfiguration('world')
  robot_id = launch.substitutions.LaunchConfiguration('robot_id')

  ld = launch.LaunchDescription()

  ld.add_action(launch.actions.DeclareLaunchArgument(
    name='robot_id',
    description='Identifier of the robot that will be spawned',
    default_value='summit',
  ))

  ld.add_action(launch.actions.DeclareLaunchArgument(
    name='use_sim_time',
    description='Use simulation (Gazebo) clock if true',
    choices=['true', 'false'],
    default_value='true',
  ))

  ld.add_action(launch.actions.DeclareLaunchArgument(
    name='world',
    description='World to load',
    default_value=[launch_ros.substitutions.FindPackageShare('turtlebot3_gazebo'), '/worlds/', 'turtlebot3_house.world']
  ))

  
  summit_xl_gazebo = get_package_share_directory('summit_xl_gazebo')

  ld.add_action(launch.actions.IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      os.path.join(summit_xl_gazebo, 'launch', 'default.launch.py')
    ),
    launch_arguments={
      'verbose': 'false',
      'world': world,
      'robot_id': robot_id,
      'use_sim_time': use_sim_time,
    }.items(),
  ))

  ld.add_action(launch.actions.IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      os.path.join(get_package_share_directory('summit_xl_navigation'), 'launch', 'nav2_bringup_launch.py'),
    ), 
    launch_arguments={
      'namespace': robot_id,
      'params_file': os.path.join(get_package_share_directory('summit_xl_navigation'), 'params', 'nav2_params.yaml') # without this line "params_file" is initialized by another action
    }.items(),
  ))

  return ld
