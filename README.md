# AutonomousCar (Machine learning)

In this project I made cars on a car track, where every car has its own neural network to learn to drive without crashing.

The learning method is as follows:
  - Before any of the cars has reached the finish line, the next generation inherits the "brain" from the car with the longest driven distance
    from the generation before.
  - When a car or several cars have reached the finish line, the next generation inherits the "brain" from the car with the fastest finish time
    from the generation before. This makes the cars run faster and faster.

The neural networks takes in 5 inputs (distance to the left, left and up, straight up, right and up, and to the right).
The network outputs "wheel angle" to be able to turn and thrust (N) to accelerate the car.
Graphics for the distance sensors can be activated for illustration purposes, but slows the performance of the program.
I've used three layers in the network (no bias added to the neurons).

The CreatePath.py file lets you draw your own track, define start and finish line, and saves it to a txt-file, where the previous tracks are also stored.
If there are several tracks saved to the file, the program will switch between them randomly.


CLICK ON THE PICTURE TO SEE A VIDEO OF THE SELF-LEARNING CARS:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/KAJ82auTic8/0.jpg)](https://www.youtube.com/watch?v=KAJ82auTic8&feature=youtu.be)
