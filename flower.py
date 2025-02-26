import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class FlowerPlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filled Flower Animation with Center")

        # Create the main widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Setup canvas
        self.canvas = FigureCanvas(plt.figure(figsize=(10, 10)))
        layout.addWidget(self.canvas)
        self.canvas.figure.patch.set_facecolor('black')

        self.init_plot()
        self.anim = None

        # Start animation after a short delay
        QTimer.singleShot(50, self.start_animation)

    def init_plot(self):
        """Initialize the plot with proper limits and styles."""
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2.5, 1.5)
        self.ax.set_facecolor('black')
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        # Generate t values for flower
        self.t = np.linspace(0, 2 * np.pi, 1000)

        # Generate x values for the stem
        self.x_stem = np.linspace(0, 1.5, 500)

        # Precompute the radial function for the flower (petal effect)
        self.r_flower = 1 + 0.3 * np.cos(6 * self.t)

        # Total frames needed (stem + flower growth)
        self.total_frames = len(self.x_stem) + len(self.t)

        # Draw the stem first (so it stays in the background)
        self.stem_line, = self.ax.plot([], [], lw=2, color='green', zorder=1)  # Lower z-order

        # Placeholder for flower fill (higher z-order)
        self.flower_patch = self.ax.fill([], [], color='magenta', alpha=0.6, zorder=2)[0]  # Higher z-order

        # Create the center circle but don't display it yet
        self.center_circle = plt.Circle((0, 0), 0.2, color='orange', zorder=3, visible=True)  # Highest z-order
        self.ax.add_patch(self.center_circle)

    def update(self, frame):
        """Update the animation at each frame."""
        if frame >= self.total_frames:  # Stop animation when flower is fully drawn
            self.center_circle.set_visible(True)  # Show the center circle
            self.anim.event_source.stop()
            return

        # Update stem growth
        if frame < len(self.x_stem):
            stem_x = self.x_stem[:frame]  # Progressive growth
            stem_y = 1 - np.exp(self.x_stem[:frame])
            self.stem_line.set_data(stem_x, stem_y)

        # Update flower filling
        else:
            flower_progress = frame - len(self.x_stem)
            t_flower = self.t[:flower_progress]
            x_flower = self.r_flower[:flower_progress] * np.cos(t_flower)
            y_flower = self.r_flower[:flower_progress] * np.sin(t_flower)

            # Ensure flower is drawn on top
            self.flower_patch.remove()  # Remove previous fill
            self.flower_patch = self.ax.fill(x_flower, y_flower, color='magenta', alpha=0.6, zorder=2)[0]

        return self.stem_line, self.flower_patch, self.center_circle

    def start_animation(self):
        """Start the animation."""
        self.anim = animation.FuncAnimation(
            self.canvas.figure,
            self.update,
            frames=self.total_frames,  # Stop exactly after flower is drawn
            interval=5,
            blit=False,
            repeat=False  # No repetition
        )
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlowerPlotApp()
    window.showMaximized()  # Open in full screen
    sys.exit(app.exec())
