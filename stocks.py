import random
from pygame import draw as d
from pygame import Color
from pygame import Rect
import numpy as np
import math

class Stock:
    def __init__(self, surface, time_step, initial_value, color):
        self.surface = surface
        self.history = []
        self.markers = []
        self.value = initial_value
        self.time_step = time_step
        self._visible_length = 0.8
        self.color = color
    
    def step(self):
        if self.value < 0: self.value = 0
        self.history.append(self.value)
        
        self.markers = list(map(lambda m: (m[0], m[1], m[2] + 1), self.markers))

    def add_marker(self, player, action):
        self.markers.append((player, action, 0))
    
    def react(self, action):
        ...
    
    def max_visible(self):
        visible_length = int((self.surface.get_width() * self._visible_length) / self.time_step)
        return max(self.history[-visible_length:]) if len(self.history) > 0 else 100
    
    def draw_scale_lines(self, surface): 
        bottom = surface.get_height()
        max_value = self.max_visible()
        
        scale = (surface.get_height() * 0.8)/ (1.2 * max_value)
        intervals = [0.01, 0.1, 1, 10, 50, 100, 500, 1000, 10000, 100000, 1000000]
        val_spacing = min(intervals, key=lambda x:abs(x-(max_value / 5)))
        line_height = val_spacing * scale
        amount_of_lines = math.ceil(surface.get_height() / line_height)
        
        d.line(surface, "0xdddddd", (0, bottom), (surface.get_width(), bottom))
        for i in range(1, amount_of_lines):
            d.line(surface, "0x303030", (0, bottom - i * line_height), (surface.get_width(), bottom - i * line_height))
        
        return scale, val_spacing
    
    def draw(self, font):
        width = self.surface.get_width()
        height = self.surface.get_height()
        
        header = self.surface.subsurface(0, 0, width, 25)
        graph = self.surface.subsurface(0, 25, width, height - 25)
        graph_height = graph.get_height()
        
        # Draw graph
        scale, line_spacing = self.draw_scale_lines(graph)
        visible_length = int((width * self._visible_length) / self.time_step)
        current_pos = (0, graph_height - (self.history[-visible_length] if len(self.history) > visible_length else self.history[0]) * scale)
        for value in self.history[-visible_length:]:
            interpolation = min(max(1 - value / self.max_visible(), 0), 1)
            color = Color(0, 255, 0).lerp(Color(255, 0, 0), interpolation)
            next_pos = (current_pos[0] + self.time_step, graph_height - value * scale)
            d.line(self.surface, color, current_pos, next_pos)
            current_pos = next_pos
        
        # Draw markers
        for marker in self.markers:
            p1 = (current_pos[0] - marker[2] * self.time_step, graph_height - self.history[-marker[2]] * scale)
            p2 = (p1[0], p1[1] + (25 if marker[1] else -25))
            
            color = marker[0].sell_color if marker[1] else marker[0].buy_color
            
            d.line(self.surface, color, p1, p2)
            d.circle(self.surface, color, p2, 4, width=0)
            
        # Draw header and border
        header.fill(self.color)
        d.rect(self.surface, Color(100, 100, 100), Rect(0, 0, width, height), width=1)
        stock_value_text = font.render(f'Stock value: ${self.value:.2f}', True, "black")
        line_spacing_text = font.render(f'Line: ${line_spacing:.2f}', True, "black")
        header.blit(stock_value_text, (10, 2))
        header.blit(line_spacing_text, (width - line_spacing_text.get_width() - 10, 2))
        
class RandStock(Stock):
    def __init__(self, surface, time_step, initial_value, flux, color):
        self.flux = flux
        super().__init__(surface, time_step, initial_value, color)
    
    def step(self):
        self.value += self.value * (random.random() - 0.5) * self.flux
        super().step()

class LogStock(Stock):
    def __init__(self, surface, time_step, initial_value, flux, color):
        self.change = []
        self.flux = flux
        super().__init__(surface, time_step, initial_value, color)
    
    def step(self):
        prev = self.value
        
        self.value += self.value * (random.random() - 0.5) * self.flux
        if len(self.change) > 0: 
            avg_change = sum(self.change[-10:]) / len(self.change[-10:])
            self.value += avg_change
        
        self.change.append(self.value - prev)
        super().step()
        
class LineStock(Stock):
    def __init__(self, surface, time_step, initial_value, k, color):
        self.k = k
        super().__init__(surface, time_step, initial_value, color)
    
    def step(self):
        self.value += self.k
        super().step()
        
class RandStock2(Stock):
    def __init__(self, surface, time_step, initial_value, flux, color):
        self.flux = flux
        super().__init__(surface, time_step, initial_value, color)
    
    def step(self):
        self.value += (random.random() - 0.5) * self.flux
        super().step()
        
class TrendyStock(Stock):
    def __init__(self, surface, time_step, initial_value, num_trends, color):
        self.trends = []
        for i in range(num_trends):
            trend = ((random.random() - 0.5), random.randint(1, (i+1) * 10))
            self.trends.append(trend)
        
        super().__init__(surface, time_step, initial_value, color)
    
    def step(self):
        for i, trend in enumerate(self.trends):
            self.value += trend[0]
            
            self.trends[i] = (trend[0], trend[1] - 1)
            if trend[1] == 0: 
                trend = ((random.random() - 0.5), random.randint(1, (i+1) * 10))
                self.trends[i] = trend
            
            self.value += (random.random() - 0.5) * 2
                
        super().step()

class BrownianStock(Stock):
    def __init__(self, surface, time_step, initial_value, color):
        super().__init__(surface, time_step, initial_value, color)
        self.history.append(initial_value)
 
    def step(self):    
        # Parameters
        drift = 0.0001          # Drift term (constant rate of return)
        volatility = 0.03      # Volatility (random fluctuation)
        delta_t = 1.0      # Time step size (daily)
 
        increment = drift * delta_t + volatility * np.sqrt(delta_t) * np.random.normal()
        self.value = self.history[-1] * np.exp(increment)
 
        super().step()