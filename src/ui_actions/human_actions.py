import random
import time

class HumanActions:
    def __init__(self, page):
        self.page = page

    def random_delay(self, min_delay=0.3, max_delay=0.7):
        jitter = random.uniform(-0.3, 0.3)
        delay = random.uniform(min_delay, max_delay) + jitter
        delay = max(0, delay)
        time.sleep(delay)

    def human_mouse_move(self, element, min_delay=0.05, max_delay=0.25, overshoot_chance=0.15):
        """
        Moves mouse to a random spot in the element (sometimes overshoots).
        """
        box = element.bounding_box()
        if not box:
            return
        # Pick a random point inside the element
        x = box['x'] + random.uniform(0.15, 0.85) * box['width']
        y = box['y'] + random.uniform(0.2, 0.9) * box['height']
        # Sometimes overshoot
        if random.random() < overshoot_chance:
            x_over = x + random.uniform(-22, 18)
            y_over = y + random.uniform(-18, 17)
            self.page.mouse.move(x_over, y_over, steps=random.randint(5, 14))
            self.random_delay(0.07, 0.18)
        self.page.mouse.move(x, y, steps=random.randint(4, 11))
        self.random_delay(min_delay, max_delay)

    def human_hover(self, element, min_delay=0.1, max_delay=0.3):
        self.human_mouse_move(element, min_delay, max_delay)
        element.hover()
        self.random_delay(min_delay, max_delay)

    # def human_click(self, element, min_delay=0.23, max_delay=0.45):
    #     self.human_mouse_move(element)
    #     element.hover()
    #     self.random_delay(min_delay, max_delay)
    #     element.click()
    #     self.random_delay(min_delay, max_delay)

    def human_click(self, element):
        if not element:
            return False
        box = element.bounding_box()
        if not box:
            return False
        x = box["x"] + random.uniform(0.2, 0.8) * box["width"]
        y = box["y"] + random.uniform(0.2, 0.8) * box["height"]
        self.page.mouse.move(x, y)
        self.human_sleep(0.2, 0.4)
        element.hover()
        self.human_sleep(0.2, 0.4)
        element.click()
        self.human_sleep(0.3, 0.7)
        return True

    def human_scroll(self, amount, min_delay=0.34, max_delay=0.62):
        # Move mouse to random area before scrolling, as if grabbing scroll bar
        self.page.mouse.move(
            random.uniform(100, 1200),
            random.uniform(150, 750),
            steps=random.randint(2, 9)
        )
        self.random_delay(min_delay, max_delay)
        self.page.evaluate(f"window.scrollBy(0, {amount})")
        self.random_delay(min_delay, max_delay)

    def human_fidget_mouse(self, chance=0.18):
        if random.random() < chance:
            x = random.uniform(30, 1500)
            y = random.uniform(25, 900)
            self.page.mouse.move(x, y, steps=random.randint(7, 20))
            self.random_delay(0.05, 0.2)
