from pygame import draw as d
from pygame import Rect

class Player:
    def __init__(self, name, starting_amount, stocks, buy_color, sell_color, controls):
        self.name = name
        self.cash = starting_amount
        self.stocks = stocks
        self.portfolio = [0 for s in stocks]
        self.buy_color = buy_color
        self.sell_color = sell_color
        self.controls = controls
        
        self.active_invest = True
        self.active_sell = True
        self.active_next = True
        self.active_prev = True
        
        self.selected_stock = 0
    
    def handle_input(self, keys):
        if keys[self.controls[0]] and self.active_invest:
            self.invest()
            self.active_invest = False
        if keys[self.controls[1]] and self.active_sell:
            self.sell()
            self.active_sell = False
        if keys[self.controls[2]] and self.active_next:
            self.selected_stock = (self.selected_stock + 1) % len(self.portfolio)
            self.active_next = False
        if keys[self.controls[3]] and self.active_prev:
            self.selected_stock = (self.selected_stock - 1) % len(self.portfolio)
            self.active_prev = False
        
        # Reset
        if not keys[self.controls[0]]:
            self.active_invest = True
        if not keys[self.controls[1]]:
            self.active_sell = True
        if not keys[self.controls[2]]:
            self.active_next = True
        if not keys[self.controls[3]]:
            self.active_prev = True
            
    
    def draw(self, surface, pos, font):
        player_text = font.render(f'{self.name}: ${self.cash:.2f}', True, 'white')
        surface.blit(player_text, pos)
        
        current_x = player_text.get_width() + 20
        for i, stock in enumerate(self.stocks):
            left_cursor_text = font.render('[', True, 'white')
            value_text = font.render(f'{self.portfolio[i]}', True, 'white')
            right_cursor_text = font.render(']', True, 'white')
            
            if self.selected_stock == i:
                surface.blit(left_cursor_text, (current_x, pos[1]))
            current_x += left_cursor_text.get_width() + 5
            
            d.rect(surface, stock.color, Rect(current_x, pos[1] + value_text.get_height() / 2 - 8, 16, 16))
            current_x += 16+5
            
            surface.blit(value_text, (current_x, pos[1]))
            current_x += value_text.get_width() + 5
            
            if self.selected_stock == i:
                surface.blit(right_cursor_text, (current_x, pos[1]))
            
            current_x += 40
        
    def invest(self, ):
        if self.cash >= self.stocks[self.selected_stock].value:
            self.cash -= self.stocks[self.selected_stock].value
            self.portfolio[self.selected_stock] += 1
            self.stocks[self.selected_stock].add_marker(self, 0)
    
    def sell(self): 
        if self.portfolio[self.selected_stock] > 0:
            self.cash += self.stocks[self.selected_stock].value
            self.portfolio[self.selected_stock] -= 1
            self.stocks[self.selected_stock].add_marker(self, 1)