# Mission On Mars Robotics Challenge 2016/1 by UNINORTE (MMRC'16)

Source codes for the MMRC'16 that took place in UNINORTE-Manaus in Jun/16. This project tries to replicate the Mathwork Competition in France that happen every year (https://www.mathworks.com/academia/student-challenge/mission-on-mars.html), using a prototype robot with Raspberry Pi and Arduino Due and programming with MATLAB. In this case, we use a Raspberry with OpenCV and any Arduino with a capable Serial Comm and support for Arduino Motor Shield.

# Description of the project

The project use a simple 2WD robot placed in an Arena that resemble a Martian soil and atmosphere. The optimal arena has 3x3 meters. Cardboard boxes are placed randomly across the arena to simulate rocks and others obstacles for the robot. The robot don't have any communication with the team and vice-versa. The objective: find a green circle or ball inside the arena, avoiding obstacles and walking the best and fastest way. When finding the ball, the robot takes a photo of the place (site).

The best robot is the one that finds the green ball (a tennis ball for example) faster without hitting the obstacles. 

The code and hardware described here are the basic setup, available by the teacher to the teams use as an example. It's necessary to make some changes to optimize the robot for the competition.

# Requirements (Hardware)

- 1x Arduino UNO rev.3 (avaliable in: http://www.filipeflop.com/pd-6b58d-placa-uno-r3-cabo-usb-para-arduino.html?ct=3d60d&p=1&s=1);
- 1x Raspberry Pi 2 B+ or 3 (avaliable in: http://www.filipeflop.com/pd-31a472-raspberry-pi-3-model-b.html?ct=9334a&p=1&s=1);
- 1x Arduino Motor Shield L293D (avaliable in: http://www.filipeflop.com/pd-6b643-motor-shield-l293d-driver-ponte-h-para-arduino.html?ct=3d60f&p=1&s=1);
- 2x DC motors (avaliable in: http://www.filipeflop.com/pd-11d0db-motor-dc-3-6v-com-caixa-de-reducao-e-eixo-duplo.html?ct=41d95&p=1&s=1);
- 1x Servo Motor 9g SG90 (avaliable in: http://www.filipeflop.com/pd-71590-micro-servo-9g-sg90-towerpro.html?ct=93346&p=1&s=1);
- 1x Ultrassonic Sensor HC-SR04 (avaliable in: http://www.filipeflop.com/pd-6b8a2-sensor-de-distancia-ultrassonico-hc-sr04.html?ct=41d97&p=1&s=1).

And others parts, like the car chassi itself and wheels. We recommend the usage of this robotic car kit (http://www.filipeflop.com/pd-9dd47-kit-chassi-2wd-robo-para-arduino.html?ct=93347&p=1&s=1).

# Requirements (Software)

- Arduino Tools 1.6 or later;
- Raspbian Jessie with kernel 4.0 or later;
- Adafruit AFMotor Shield 1.0 Library or later;
- Ultrasonic Library from ITead Studio (iteadstudio.com).

All these libraries are already in this repository. Just download it and install in your computer.
The Arduino tools and Raspbian OS can be found googling it! Same with the installation methods.

# Connections with Arduino, Motor Shield and Raspberry 

The Arduino Shield goes directly above the Arduino UNO without any other connection. The Raspberry is connected directly with Arduino by USB port. The Arduino will be recognized by Raspberry as a ttyACMX or ttyUSBX device in /dev folder (check this in Raspberry, the 'X' is a number of the device, starting in 0 to inf - check that too). Note that a Linux OS will be already installed in your Raspberry.

The webcam used can be any with an USB 2.1 support, connected directly to Raspberry Pi, the camera will be recognized by Raspberry as videoCapture by OpenCV library.

The Servo Motor is used to move the ultrasonic sensor left to right in order to check if the environment have some obstacles. The code keeps the servo in sleep state. When the ultrasonic sensor notice any obstacle nearby (in front of robot in this case), the servo moves the sensor to left and right in order where the robot can move.

The Motor Shield use a secondary battery (recommended a 1300mAh with 12VDC) to power the 2 DC motors that are used to move the robot, and the servo, that is used to move the ultrasonic sensor.

Other connections can be seen in figure below:

![mmrc16](https://cloud.githubusercontent.com/assets/6139272/21539899/5f7b9544-cd81-11e6-86c3-f8f8039f8cba.png)

The fritzing is in the important files folder.

# Acknowledgements

Many thanks to Aldemir Teixeira Jr. and Antônio Marcos for helping me with the Arduino optimization. Thanks to Adrian Rosebrock from blog http://www.pyimagesearch.com to share the code of tracking ball used here.
