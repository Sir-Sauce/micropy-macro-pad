import time
import board
from analogio import AnalogIn

potentiometer = AnalogIn(board.GP28_A2)  # potentiometer connected to A1, power & ground

while True:

    print((potentiometer.value,))      # Display value

    time.sleep(0.25)                   # Wait a bit before checking all again