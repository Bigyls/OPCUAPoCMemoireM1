from tkinter import Canvas
from math import cos, pi, sin
from typing import Iterator

class RoundedCanvas(Canvas):
	minimum_steps = 10  # lower values give pixelated corners

	@staticmethod
	def get_cos_sin(radius: int) -> Iterator[tuple[float, float]]:
		steps = max(radius, RoundedCanvas.minimum_steps)
		for i in range(steps + 1):
			angle = pi * (i / steps) * 0.5
			yield (cos(angle) - 1) * radius, (sin(angle) - 1) * radius

	def create_rounded_box(self, x0: int, y0: int, x1: int, y1: int, radius: int, color: str) -> int:
		points = []
		cos_sin_r = tuple(self.get_cos_sin(radius))
		for cos_r, sin_r in cos_sin_r:
			points.append((x1 + sin_r, y0 - cos_r))
		for cos_r, sin_r in cos_sin_r:
			points.append((x1 + cos_r, y1 + sin_r))
		for cos_r, sin_r in cos_sin_r:
			points.append((x0 - sin_r, y1 + cos_r))
		for cos_r, sin_r in cos_sin_r:
					points.append((x0 - cos_r, y0 - sin_r))
		return self.create_polygon(points, fill=color)
