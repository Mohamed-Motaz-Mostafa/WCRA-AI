# WCRA-AI
Graduation Project repo.


![grad-project img](image.png)

<p>
This repo will contain some info and code to my graduation project,
WCRA-AI ===> "Wireless Chess Robotic Arm based on Artificial Intelligence"

</p>

## About the Project

<p>
  
Developed a cutting-edge Wireless Chess Robotic Arm (WCRA-AI) capable of playing
chess autonomously. This project was an interesting application in fields like embedded systems, AI,
and IoT. The project utilized advanced technologies such as computer vision, convolutional neural
networks, and the Internet of Things (IoT) to create a robot that can make strategic decisions in a
dynamic environment. The robotic arm, controlled over a wireless network, was designed not only for
chess playing but also for potential applications in pick-and-place operations. The arm incorporated
servo motors controlled by an Arduino. A camera placed above the chessboard, connected to a
Raspberry Pi, processed the captured image using various programs and functions. Powered by a
**CNN model** the image was converted into chess notation describing the game's position, which was
then sent to a chess engine powered by the **NegaMax algorithm** on the Raspberry Pi for move
selection. Raspberry Pi and Arduino are connected by i2c connection to move the arm by the selected
chess move. In multiplayer mode, the notation was transmitted to the opponent via a web page hosted
on a server simulating as opponent's robot arm.

</p>

## Project block diagra
![block_diagram](https://github.com/Mohamed-Motaz-Mostafa/WCRA-AI/assets/156100459/5ee3654a-dfce-4e1c-bdce-1d408b6e4afa)





