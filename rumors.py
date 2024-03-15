import random

class RumorManager:
    def __init__(self, surface, rumors_file, rest_cooldown, stocks):
        self.surface = surface
        self.rumors = self.init_rumors(rumors_file)
        self.rest_cooldown = rest_cooldown
        self.stocks = stocks
        self.active_rumor = None
        self.active_stock = None
        self.cooldown = self.get_rest_cooldown()
    
    def step(self):
        self.cooldown -= 1
        
        if self.cooldown <= 0:
            if self.active_rumor == None:
                self.active_rumor = random.choice(self.rumors)
                self.active_stock = random.choice(self.stocks)
                self.active_rumor.activate(self.active_stock)
                self.cooldown = self.active_rumor.get_duration()
            else:
                self.active_rumor.deactivate(self.active_stock)
                self.active_rumor = None
                self.active_stock = None
                self.cooldown = self.get_rest_cooldown()
    
    def get_rest_cooldown(self):
        return random.normalvariate(self.rest_cooldown, self.rest_cooldown / 10)
    
    def draw(self, font):
        self.surface.fill('black')
        if self.active_rumor is None:
            rumor_text = font.render('Stocker Market', True, 'white')
            self.surface.blit(rumor_text, (10, 0))
        else:
            rumor_text = font.render(self.active_rumor.get_message(self.active_stock), True, self.active_stock.color)
            self.surface.blit(rumor_text, (10, 0))
    
    def init_rumors(self, rumors_file):
        rumors = []
        
        with open(rumors_file, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:
                sections = line.split(':')
                rumor = Rumor(sections[0], float(sections[1]), float(sections[2]), float(sections[3]), int(sections[4]))
                rumors.append(rumor)
        
        return rumors

class Rumor:
    def __init__(self, message, prob, good_magnitude, bad_magnitude, duration):
        self.message = message
        self.prop = prob
        self.good_magnitude = good_magnitude
        self.bad_magnitude = bad_magnitude
        self.duration = duration
    
    def get_duration(self):
        return random.normalvariate(self.duration, self.duration / 10)
    
    def get_message(self, stock):
        return self.message.replace('[stock]', 'Walla')
    
    def activate(self, stock):
        self.stock = stock
        
        outcome = random.random() < self.prop
        stock.set_influence(self.good_magnitude if outcome else -self.bad_magnitude)
    
    def deactivate(self, stock):
        stock.set_influence(0)