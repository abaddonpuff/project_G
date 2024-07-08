WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


class InputBox:
    """
    A class to store InputBox Settings
    """

    def __init__(self):
        """
        Initialize input box's settings
        """
        self.color_inactive = GRAY
        self.color_active = BLACK
        self.color = self.color_inactive
        self.active = False
