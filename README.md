# WCRA-AI
Graduation Project repo.
![Markdown logo](![grad-project logo](image.png))

<p>
This repo will contain a summary to my graduation project,
WCRA-AI ===> "Wireless Chess Robotic Arm based on Artificial Intelligence"
</p>

## Abstract

<p>

Wireless Chess Robotic Arm (WCRAI for short) is a robotic arm capable of playing chess, it can be
controlled over the network as well this is where the word wireless came from. The purpose of this project is
to create a robot using modern technologies like computer vision, convolutional neural networks, and the
Internet of things that’s capable of playing chess. There is an increasing demand for smart robots that can
make their own decisions in a changing environment and this idea is an interesting application of the
concept. The arm was designed in a way that can generalize the usage of the arm later in pick-and-place
operations, Servo motors controlled by an Arduino carried out the movement of the arm. movement limiting
switches were added to protect the servo motors also attached to Arduino. A camera was placed above the
chessboard and attached to a Raspberry pi, and numerous programs and functions were created in order
to process and convert the image into notation describing the position of the chess game, depending on the
mode ( single player, multiplayer ) notation is sent either to the chess engine (powered by NegaMax
algorithm also running on the Pi) which decides which move to play or to the server to transmit it to the
other player robot arm ( a web page in current conditions ).
</p>