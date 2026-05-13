En este repositorio hay una simulación que usa Gazebo Classic y Rviz2 para usar en eventos o stand del equipo Star-UMA.

Consiste en un nodo de teleoperación usando un mando de la Xbox para controlar un robot diferencial en una serie de laberintos. 
De manera que la gente que se acerque pueda conducir el robot en la simulación y al mismo tiempo desde Rviz pueda ver como escanea el lugar con el sensor lidar.

Para usarlo se necesita lo siguiente:

-Linux con Ubuntu 22.04

-ROS2 Humble

-Rviz2

-Gazebo Classic

-Un mando para teleoperar

Para usarlo es sencillo, clona el repositorio en un workspace y compílalo,. Listo, ya lo tienes.
Para lanzarlo tienes que ejecutar 

ros2 launch simulacion_node simulacion.launch.py

Con esto se lanzará el Gazebo Classic con un laberinto predeterminado y un robot diferencial dentro de él. Además se lanzará el rviz2 con el sensor láser detectando las paredes.
y la cámara con lo que está viendo el robot.

Cuando se quiera resetear el mapa cerramos el programa y se lanza el launch de nuevo.
Si se quiere cambiar de mapa se puede detallar como argumento en el terminal. 

ros2 launch simulacion_node simulacion.launch.py map:=Laberinto2
