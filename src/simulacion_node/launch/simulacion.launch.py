from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    pkg_share = FindPackageShare('simulacion_node')
    
    map_arg = DeclareLaunchArgument(
        'map',
        default_value='Laberinto1',
        description='Nombre del archivo .world (sin extensión) para cargar en Gazebo'
    )
    
    selected_map = LaunchConfiguration('map')
    
    # Configuraciones
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    model_path = PathJoinSubstitution([pkg_share, 'description', 'robot_description.urdf'])
    rviz_config = PathJoinSubstitution([pkg_share, 'rviz', 'config.rviz'])
    joy_config_path = PathJoinSubstitution([pkg_share, 'config', 'xbox.config.yaml'])
    
    
    world_path = PathJoinSubstitution([
        pkg_share, 
        'worlds', 
        [selected_map, '.world']
    ])
    
    # 1. Gazebo (Lanzado como servidor correctamente)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py'])
        ]),
        launch_arguments={'world': world_path}.items()
    )

    # 2. Publicadores de estado
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', model_path]),
            'use_sim_time': use_sim_time
        }]
    )

    # 3. Spawn del Robot
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'sam_bot', '-topic', 'robot_description'],
        output='screen'
    )
    # 4. Teleoperación con Mando (Sustituye al teclado)
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{'use_sim_time': use_sim_time, 'deadzone': 0.1}]
    )
    
    # 4. Teleoperación profesional (incluye remapeo a /cmd_vel)
    teleop_joy_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        parameters=[joy_config_path, {'use_sim_time': use_sim_time}],
        remappings=[('/cmd_vel', '/demo/cmd_vel')]
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='True'),
        map_arg,
        gazebo,
        robot_state_publisher,
        spawn_entity,
        joy_node,
        teleop_joy_node,
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': use_sim_time}]
        )
    ])