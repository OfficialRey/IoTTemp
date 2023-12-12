from engine.graphics.gui.widget import Button
from engine.util.constants import BLUE, WHITE


class LevelEditorSelectTextureButton(Button):

    def __init__(self, editor, texture_id=0):
        super().__init__((0, 0, 0, 0), hover_color=BLUE, background_color=WHITE)
        self.editor = editor
        self.texture_id = texture_id

    def on_press(self):
        self.editor.select_texture(self.texture_id)

    def on_release(self):
        pass


class LevelEditorScrollTextureButton(Button):

    def __init__(self, editor, direction: int):
        super().__init__((0, 0, 0, 0))
        self.editor = editor
        self.direction = direction

    def on_press(self):
        self.editor.scroll_texture(self.direction)

    def on_release(self):
        pass
