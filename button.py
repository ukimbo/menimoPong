import pygame

class Button:
    def __init__(self, image, x_pos, y_pos, font, text_input, color, hover_color):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.text_input = text_input
        self.color = color
        self.hover_color = hover_color
        self.text = self.font.render(self.text_input, True, self.color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    def hover(self, position): #position is a tuple where (x position, y position)
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hover_color)
    def click(self, position): #position is a tuple where (x position, y position)
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            False

