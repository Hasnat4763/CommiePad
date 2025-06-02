from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
import busio
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.extensions.display import Display, SSD1306, TextEntry, ImageEntry
import board

keyboard = KMKKeyboard()


keyboard.row_pins = ()
keyboard.col_pins = (
    board.GP3,  # SW1
    board.GP4,  # SW2
    board.GP2,   # SW3
    board.GP1,   # SW4
    board.GP0,   # SW5
    board.GP28,   # SW6
)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- Keymap (change as needed) ---
keyboard.keymap = [
    [KC.MEDIA_NEXT_TRACK, KC.MEDIA_PREV_TRACK, KC.MEDIA_STOP, KC.MEDIA_PLAY_PAUSE, KC.E, KC.F]
]
i2c_bus = busio.I2C(board.GP_7, board.GP_6)

driver = SSD1306(

    i2c=i2c_bus,

    device_address=0x3C,
)
display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=32, # screen size
    flip = False, # flips your display content
    flip_left = False, # flips your display content on left side split
    flip_right = False, # flips your display content on right side split
    brightness=0.8, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    dim_time=20, # time in seconds to reduce screen brightness
    dim_target=0.1, # set level for brightness decrease
    off_time=60, # time in seconds to turn off screen
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.1, # set level for brightness decrease
    powersave_off_time=30, # time in seconds to turn off screen
)
keyboard.extensions.append(display)
encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.GP26, board.GP27, board.GP29),)  # Rotary A, B, Switch
encoder_handler.map = [((KC.VOLD, KC.VOLU),)]  # Rotate: volume down/up
keyboard.modules.append(encoder_handler)

# --- RGB (SK6812 Neopixels) ---
rgb = RGB(pixel_pin=board.GP6,
        num_pixels=6,
        val_limit=100,
        hue_default=0,
        sat_default=100,
        rgb_order=(1, 0, 2),  # GRB WS2812
        val_default=100,
        hue_step=5,
        sat_step=5,
        val_step=5,
        animation_speed=1,
        breathe_center=1,  # 1.0-2.7
        knight_effect_length=3,
        animation_mode=AnimationModes.STATIC,
        reverse_animation=False,
        refresh_rate=60,
        )
keyboard.extensions.append(rgb)
# --- Go ---
if __name__ == '__main__':
    keyboard.go()
