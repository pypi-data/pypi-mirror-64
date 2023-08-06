"""
Starting Template Simple

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template_simple
"""
import arcade
import pyglet.gl as gl

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Starting Template Simple"

from pyglet.gl import GL_NEAREST
from pyglet.gl import GL_LINEAR

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)
        self.sprite_list_1 = None
        self.sprite_list_2 = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.sprite_list_1 = arcade.SpriteList()
        self.sprite_list_2 = arcade.SpriteList()

        sprite = arcade.Sprite(":resources:images/tiles/dirtHill_right.png")
        sprite.center_x = 100
        sprite.center_y = 200
        # sprite.angle = 45
        self.sprite_list_1.append(sprite)

        sprite = arcade.Sprite(":resources:images/tiles/dirtHill_right.png")
        sprite.center_x = 300.5
        sprite.center_y = 200.5
        self.sprite_list_1.append(sprite)

        sprite = arcade.Sprite(":resources:images/tiles/dirtHill_right.png")
        sprite.center_x = 500
        sprite.center_y = 200
        sprite.scale = .66666
        self.sprite_list_1.append(sprite)

        sprite = arcade.Sprite(":resources:images/items/coinGold.png")
        sprite.center_x = 700
        sprite.center_y = 100
        sprite.scale = 2
        self.sprite_list_1.append(sprite)
        print(sprite.width)

        sprite = arcade.Sprite(":resources:images/tiles/dirtHill_right.png")
        sprite.center_x = 100
        sprite.center_y = 300
        # sprite.angle = 45
        self.sprite_list_2.append(sprite)

        sprite = arcade.Sprite(":resources:images/tiles/dirtHill_right.png")
        sprite.center_x = 300.5
        sprite.center_y = 300
        self.sprite_list_2.append(sprite)

        sprite = arcade.Sprite(":resources:images/tiles/dirtHill_right.png")
        sprite.center_x = 500
        sprite.center_y = 300
        sprite.scale = .5
        self.sprite_list_2.append(sprite)

        sprite = arcade.Sprite(":resources:images/items/coinGold.png")
        sprite.center_x = 700
        sprite.center_y = 300
        sprite.scale = 2
        self.sprite_list_2.append(sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()
        self.sprite_list_1.draw()
        self.sprite_list_2.draw(filter=gl.GL_NEAREST)



def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
