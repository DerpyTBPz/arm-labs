import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

SERIAL_PORT = '/dev/ttyUSB0'  # Твій порт
BAUD_RATE = 460800
SAMPLES = 128  # Показуємо шматочок хвилі, щоб було гарно видно

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Помилка: {e}")
    exit()

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(SAMPLES)
line, = ax.plot(x, np.zeros(SAMPLES), color='#00FFFF', lw=1.5)

ax.set_title("Осцилограма мікрофона INMP441 (Часова область)", fontsize=14)
ax.set_xlabel("Семпли", fontsize=12)
ax.set_ylabel("Амплітуда", fontsize=12)
ax.set_ylim(-10000, 10000) # Базовий масштаб, потім розшириться
ax.grid(color='gray', linestyle='--', alpha=0.5)

def update(frame):
    if ser.in_waiting > 0:
        try:
            line_data = ser.readline().decode('ascii', errors='ignore').strip()
            if line_data:
                values = [float(v) for v in line_data.split(',') if v]
                if len(values) >= SAMPLES:
                    # Беремо лише перші SAMPLES значень для красивого графіка
                    plot_vals = values[:SAMPLES]
                    line.set_ydata(plot_vals)
                    
                    # Симетричне автомасштабування
                    max_val = max(abs(max(plot_vals)), abs(min(plot_vals)))
                    if max_val > ax.get_ylim()[1]:
                        ax.set_ylim(-max_val * 1.2, max_val * 1.2)
        except ValueError:
            pass
    return line,

ani = FuncAnimation(fig, update, interval=10, blit=True, cache_frame_data=False)
plt.show()