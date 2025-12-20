import matplotlib.pyplot as plt
import io

import yaml
from PySide6.QtGui import QImage


class Plot:
    def __init__(self, data: dict = None):
        if data is None:
            data = dict()
        self.series = data.get("series", [])
        self.grid = data.get("grid", {})
        self.x_limits = data.get("x_limits", None)
        self.y_limits = data.get("y_limits", None)

    def make_image(self) -> QImage:
        plt.figure()
        for r in self.series:
            plt.plot(r["x"], r["y"], **r["config"])
        if self.grid:
            plt.grid(True, **self.grid)
        if self.x_limits:
            plt.xlim(self.x_limits)
        if self.y_limits:
            plt.ylim(self.y_limits)
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image = QImage()
        image.loadFromData(buffer.getvalue())
        return image

    def get_data_dict(self):
        result = dict()
        result["series"] = self.series
        result["grid"] = self.grid
        result["x_limits"] = self.x_limits
        result["y_limits"] = self.y_limits
        return result

    def add_series(self, x, y, **kwargs):
        self.series.append(
            {"x": [float(v) for v in x], "y": [float(v) for v in y], "config": kwargs}
        )

    def set_grid(self, **kwargs):
        self.grid = kwargs

    def set_x_limits(self, *args):
        self.x_limits = args

    def set_y_limits(self, *args):
        self.y_limits = args


if __name__ == "__main__":
    import numpy as np

    x = np.linspace(-10, 10, 41)

    plot = Plot()
    plot.add_series(x, x**2, linewidth=2, linestyle="solid", color="tab:blue")
    plot.add_series(x, x**3, linewidth=4, linestyle="solid", color="tab:red")
    plot.add_series(x, 2 * x, linewidth=4, linestyle="solid", color="tab:red")
    plot.set_grid(alpha=0.5, linestyle="dashed")

    print(yaml.dump(plot.get_data_dict(), default_flow_style=False, sort_keys=False))
