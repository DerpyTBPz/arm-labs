import serial
import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

SERIAL_PORT = '/dev/ttyUSB0' 
BAUD_RATE = 460800
FFT_BINS = 256
FS = 16000
MIN_FREQ = 250  

csv_file = open("spectrum_data.csv", "w", newline="")
csv_writer = csv.writer(csv_file)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Помилка відкриття порту: {e}")
    exit()

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6))

plt.subplots_adjust(bottom=0.2)

x = np.linspace(0, FS / 2, FFT_BINS)
line, = ax.plot(x, np.zeros(FFT_BINS), color='#00FF00', lw=1.5)

ax.set_title("STM32 Real-Time FFT Spectrum", fontsize=14)
ax.set_xlabel("Частота (Гц)", fontsize=12)
ax.set_ylabel("Амплітуда", fontsize=12)

ax.set_xlim(MIN_FREQ, FS / 2)
ax.grid(color='gray', linestyle='--', alpha=0.5)

ax_slider = plt.axes([0.15, 0.05, 0.7, 0.03]) 
y_slider = Slider(
    ax=ax_slider,
    label='Max Y ',
    valmin=1000,      
    valmax=200000,    
    valinit=50000,   
    color='#00FF00'
)

def update(frame):
    if ser.in_waiting > 0:
        try:
            line_data = ser.readline().decode('ascii', errors='ignore').strip()
            
            if line_data:
                values = [float(v) for v in line_data.split(',') if v]
                
                if len(values) == FFT_BINS:
                    line.set_ydata(values)
                    
                    ax.set_ylim(0, y_slider.val)
                    
                    csv_writer.writerow(values)
                    
        except ValueError:
            pass
    return line,

print(f"Слухаю порт {SERIAL_PORT}... Натисніть Ctrl+C для зупинки.")
ani = FuncAnimation(fig, update, interval=10, blit=True, cache_frame_data=False)

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    ser.close()
    csv_file.close()
    print("\nДані збережено в spectrum_data.csv. Порт закрито.")