# RobotRestaurante
Código para la navegación de un robot en un restaurante, que se le pueda llamar para ir a una mesa concreta.
Se trata de la simulación del turtlebot3 como si estuviese en un restaurante. Para ello, al lanzar el código (más abajo explicado) comenzará a navegar por el mapa, hasta que se le añada un numero del 1 al 9. Cada número representa una mesa. EL robot irá a esa mesa, después irá a cocina, y volverá a navegar esquivando objetos hasta que otra mesa le llame.

Instrucciones para simular

Lanzar el mundo de Gazebo: 
$ export TURTLEBOT3_MODEL=burger
$ roslaunch turtlebot3_gazebo turtlebot3_world.launch

Lanzar el nodo de navegación:
$ export TURTLEBOT3_MODEL=burger
$ roslaunch turtlebot3_navigation turtlebot3_navigation.launc map_file:=$HOME/map.yaml

Para este paso utilizar el mapa map.yaml, que se adjunta en la carpeta.

Estimar la posición:
Utilizar el 2D Pose Estimate de rviz y lanar el teleop
$ roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
Realizarlo igual que en prácticas anteriores.

Lanzar el fichero de python:
$ python AlgoritmoFinal.py

El robot comenzará a navegar evitando obstáculos y mientras se preguntará por terminal: ¿Quiere que el robot vaya a su mesa? Si as así introduzca en número de mesa:'
El robot seguirá su tarea original hasta que se introduzca un número del 1 al 9. No se podrá introducir otro número hasta que no se hayan terminado las subtareas correspondientes y el robot vuelva a navegar. 

