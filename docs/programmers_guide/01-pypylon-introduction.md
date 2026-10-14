# Introduction

pypylon is the official Python language binding for the Basler pylon C++ APIs.

It enables Python applications to control cameras from Basler's machine vision product portfolio and to acquire images from the camera.

Basler cameras can be used in a wide range of applications. Among many others, the following machine vision applications are common:

- Factory automation
- Robotics
- Scientific imaging
- Quality inspection
- AI pipelines

## Software Stack

````mermaid
block
  columns 1
  A["Python Application"]
  down0<[" "]>(down)
  B["pypylon #40; Python API #41;"]
  down1<[" "]>(down)
  C["pylon SDKs #40;C#43;#43;#41;"]
  down2<[" "]>(down)
  D["GenTL and pylon Transport Layer"]
  down3<[" "]>(down)
  E["Camera and Grabber Hardware"]
````
Understanding the layered architecture helps debug issues (driver, transport, or application level).
