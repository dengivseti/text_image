from PIL import Image, ImageDraw, ImageFont

class IMAGE:
    def __init__(self):
        self.filename = 'default.jpg'

    def save(self, filename=None):
        self.image.save(filename or self.filename)

    def text_size(self, text):
        return self.font.getsize(text)

    def text_preparation(self, text, width):
        lines = []
        line = []
        words = text.split(' ')
        height = 0
        line_heigth = self.text_size(text)[1]
        for word in words:
            if '\n' in word:
                newline_words = word.split('\n')
                new_line = ' '.join(line + [newline_words[0]])
                size = self.text_size(new_line)
                if size[0] <= width:
                    line.append(newline_words[0])
                else:
                    lines.append(line)
                    line = [newline_words[0]]
                lines.append(line)
                if len(word.split('\n')) > 2:
                    for i in range(1, len(word.split('\n')) - 1): lines.append([newline_words[i]])
                line = [newline_words[-1]]
            else:
                new_line = ' '.join(line + [word])
                size = self.text_size(new_line)
                if size[0] <= width:
                    line.append(word)
                else:
                    lines.append(line)
                    line = [word]
        if line:
            lines.append(line)
        lines = [' '.join(line) for line in lines]
        height = len(lines) * line_heigth
        return height, lines

    def text_place(self, lines):
        x = self.margin[3]
        height = self.margin[0]
        for index, line in enumerate(lines):
            total_size = self.text_size(line)
            if self.place == 'left':
                self.write_text(x, height, line)
            elif self.place == 'right':
                x_left = self.width + x - total_size[0]
                self.write_text(x_left, height, line)
            elif self.place == 'center':
                x_left = int(x + ((self.width - total_size[0])/2))
                self.write_text(x_left, height, line)
            elif self.place == 'justify':
                words = line.split()
                if index == len(lines) - 1 or len(words) == 1:
                    self.write_text(x, height, line)
                    continue
                line_without_spaces = ''.join(words)
                space_width = (self.width - total_size[0]) / (len(words) - 1.0)
                start_x = x
                for word in words[:-1]:
                    self.write_text(start_x, height, word)
                    word_size = self.text_size(word)
                    start_x += word_size[0] + space_width
                last_word_size = self.text_size(words[-1])
                last_word_x = x + self.width - last_word_size[0]
                self.write_text(last_word_x, height, words[-1])
            height += total_size[1]

    def write_text(self, x, y, text):
        self.draw.text((x, y), text, font=self.font, fill=self.color_text)

    def text_image(self, text, font, font_size=12, color_text=(0, 0, 0),
                   color_background=(255, 255, 255),
                   place='left', margin = (0, 0, 0, 0), max_width=100, filename=None):
        self.font = ImageFont.truetype(font, font_size)
        self.color_text = color_text
        self.place = place
        self.margin = margin
        self.width = max_width - self.margin[1] - self.margin[3]
        heigth, lines = self.text_preparation(text, self.width)
        max_heigth = heigth + self.margin[0] + self.margin[2]
        self.image = Image.new('RGB', [max_width, max_heigth], color=color_background)
        self.draw = ImageDraw.Draw(self.image)
        self.text_place(lines)
        self.save(filename)


