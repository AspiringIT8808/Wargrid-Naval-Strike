"""Every screen has the same four hooks; App calls them."""


class Screen:
    def __init__(self, app):
        self.app = app

    @property
    def game(self):
        return self.app.game

    def enter(self, **kwargs):
        """Called each time App.goto() switches to this screen."""

    def on_event(self, event):
        """One pygame event (click, key...)."""

    def update(self):
        """Once per frame, before drawing."""

    def draw(self):
        """Once per frame."""
