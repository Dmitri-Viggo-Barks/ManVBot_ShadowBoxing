Currently work in progress :P
<br>
<br>
Will add files relating to hardware components in the future
<br>
<br>
<br>
>Code Notes:
<br>


   * Serial Communication

    
Within ['main.py'](main.py), specifically the serial's target port and baud rate synchronization at ['line 61'](main.py#L61), the target port and baud rate must be the same as the target port of where the Arduino UNO is connected to and the set baud rate for the serial connection. The target port can be seen in the tools section in the Arduino IDE environment. The baud rate on the other hand can be seen in either the sketch itself or the serial monitor (assuming both are matched).
<br>
<br>
  * Video Capturing Device Configuration


Within ['main.py'](main.py), the camera configuration at ['line 88'](main.py#L88) has the video capture device set at index 0. 'index=0' defaults the capture-device that would be used to the last-used capture device, this is a laptop's webcam by default for most. Change index to index+=1 until desired capture device is used.
<br>
<br>
<br>


>Physical Circuitry


The connections of each electrical component and device are as follows:
<br>
<br>
  * Positive Connection


1. Input Voltage (~5 V)
2. Input Power Servo 1 (Horizontal or Vertical)
3. Input Power Servo 2 (Horizontal or Vertical)
4. (5) 100 µF Capacitor (with >5 V rating) Positive Terminal


All five 100 µF Capacitors are in parallel. Together, all amounts to 500 µF.
<br>
<br>
  * Negative Connection


1. GND Voltage
2. Servo 1 GND (Horizontal or Vertical)
3. Servo 2 GND (Horizontal or Vertical)
4. (5) 100 µF Capacitor Negative Terminal
5. Arduino UNO GND
<br>
<br>
<br>


>Pan-Tilt Sub-Bot


Follow Arduino projects documentation and YouTube tutorials :P