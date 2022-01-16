#!/usr/bin/env python

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import actionlib
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import sys
from getkey import getkey


#Uso de la acción move_base en ROS para moverse a un punto determinado
#En ROS una acción es como una petición de un "cliente" a un "servidor"
#En este caso este código es el cliente y el servidor es ROS
#(en concreto el nodo de ROS 'move_base')
class ClienteMoveBase:
    def __init__(self):
        #creamos un cliente ROS para la acción, necesitamos el nombre del nodo 
        #y la clase Python que implementan la acción
        #Para mover al robot, estos valores son "move_base" y MoveBaseAction
        self.client =  actionlib.SimpleActionClient('move_base',MoveBaseAction)
        #esperamos hasta que el nodo 'move_base' esté activo`
        self.client.wait_for_server()

    def moveTo(self, x, y):
        #un MoveBaseGoal es un punto objetivo al que nos queremos mover
        goal = MoveBaseGoal()
        #sistema de referencia que estamos usando
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.pose.position.x = x   
        goal.target_pose.pose.position.y = y
        #La orientación es un quaternion. Tenemos que fijar alguno de sus componentes
        goal.target_pose.pose.orientation.w = 1.0

        #enviamos el goal 
        self.client.send_goal(goal)
        #vamos a comprobar cada cierto tiempo si se ha cumplido el goal
        #get_state obtiene el resultado de la acción 
        state = self.client.get_state()
        #ACTIVE es que está en ejecución, PENDING que todavía no ha empezado
        while state==GoalStatus.ACTIVE or state==GoalStatus.PENDING:
            rospy.Rate(10)   #esto nos da la oportunidad de escuchar mensajes de ROS
            state = self.client.get_state()
        return self.client.get_result()
        
        

def callback(msg): 
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
    #incializacion varibales
    i = 0
    sumaD = 0 #variable para lecturas de la derecha
    sumaC = 0 #variable para lecturas del centro
    sumaI = 0 #variable para lecturas de la izquierdas
    esD = 0
    esI = 0
    esC = 0
    
    #avanza en linea recta
    cmd = Twist()
    cmd.linear.x = 0.3
    pub.publish(cmd)


    for lectura in msg.ranges: 
        
        #sumatorio distancias angulo derecha
        if (i < 25 or (i > 335 and i < 360)): 
            # los valores de lectura nan (objeto demasiado lejos), cambiarlos por una distancia alta
            if (lectura < 0.3):
            	esC = 1
            	
            sumaC = sumaC + lectura
            
        
        #sumatorio distancias angulo centro
        elif i >= 25 and i < 75:  
            if (lectura < 0.3):
            	esD = 1
            	
            sumaD = sumaD + lectura
            
        #sumatorio distancias angulo izquierda
        elif i > 285 and i < 335:
        
           if (lectura < 0.3):
            	esI = 1
           sumaI = sumaI + lectura
           
            
        i = i + 1
        
	# se comprueba si hay algun obstaculo delante
    if (sumaC < sumaD and sumaC < sumaI and sumaC < 40 or esC > 0):
        # si el obstaculo esta mas a la derecha gira a la izquierda
        if sumaD < sumaI:
            cmd.angular.z = 2
            pub.publish(cmd)

        # si el obstaculo esta mas a la izquierda gira a la derecha
        else:
            cmd.angular.z = -2
            pub.publish(cmd)
        
           
    # si hay un obstaculo muy cercano a la izquierda gira a la derecha
    if (sumaI < 30 or esI > 0):
        cmd.angular.z = 2
        pub.publish(cmd)
    
    # si hay un obstaculo muy cercano a la derecha gira a la izquierda
    if (sumaD < 30 or esD > 0): 
        cmd.angular.z = -2
        pub.publish(cmd)


while (1):
    quieto = 0
    if quieto == 0:
        rospy.init_node('read_scan')
        sub = rospy.Subscriber('/scan', LaserScan, callback)
        cliente = ClienteMoveBase()
        cmd = Twist()
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        mesa = input ('¿Quiere que el robot vaya a su mesa? Si as así introduzca en número de mesa:')
        while mesa != 0:
            quieto = 1
            cmd.linear.x = 0
            cmd.angular.z = 0
            pub.publish(cmd)
            if mesa == '1':
                result = cliente.moveTo(0.65, 1)
                result = cliente.moveTo(-2.3, 0)
                mesa = 0
                break

            if mesa == '2':
                result = cliente.moveTo(0.65, 0)
                result = cliente.moveTo(-2.3, 0)
                mesa = 0
                break

            if mesa == '3':
                result = cliente.moveTo(0.65, -1)
                result = cliente.moveTo(-2.3, 0)
                mesa = 0
                break

            if mesa == '4':
                result = cliente.moveTo(-0.5, 1)
                result = cliente.moveTo(-2.3, 0)
                mesa = 0
                break

            if mesa == '5':
                result = cliente.moveTo(-0.5, 0)
                result = cliente.moveTo(-2.3, 0)
                mesa = 0
                break

            if mesa == '6':
                result = cliente.moveTo(-0.5, -1)
                result = cliente.moveTo(-2.3, 0)
                mesa = 0
                break

            if mesa == '7':
                result = cliente.moveTo(-1.5, 1)
                result = cliente.moveTo(-2.3, 0)
                mesa = 0
                break

            if mesa == '8':
                result = cliente.moveTo(-1.5, 0)
                result = cliente.moveTo(-2.3, 0)
                mesa = 0
                break

            if mesa == '9':
                result = cliente.moveTo(-1.5, -1)
                result = cliente.moveTo(-2.3, 0)
                mesa = 0
                break

   

rospy.spin()
