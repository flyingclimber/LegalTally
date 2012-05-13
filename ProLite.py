'''Class library for ProLite signs'''

#Colors
class ProLite:
    colors = dict({
    'DIM_RED':'<CA>',
    'RED':'<CB>',
    'BRIGHT_RED':'<CC>',
    'ORANGE':'<CD>',
    'BRIGHT_ORANGE' : '<CE>',
    'LIGHT_YELLOW' : '<CF>',
    'YELLOW' : '<CG>',
    'BRIGHT_YELLOW' : '<CH>',
    'LIME' : '<CI>',
    'DIM_LIME' : '<CJ>',
    'BRIGHT_LIME' : '<CK>',
    'BRIGHT_GREEN' : '<CL>',
    'GREEN' : '<CM>',
    'DIM_GREEN' : '<CN>',
    'YELLOW_GREEN_RED' : '<CO>',
    'RAINBOW_DEFAULT' : '<CP>',
    'RED_GREEN_3D' : '<CQ>',
    'RED_YELLOW_3D' : '<CR>',
    'GREEN_RED_3D' : '<CS>',
    'GREEN_YELLOW_3D' : '<CT>',
    'GREEN_ON_RED' : '<CU>',
    'RED_ON_GREEN' : '<CV>',
    'ORANGE_ON_GREEN_3D' : '<CW>',
    'LIME_ON_RED_3D' : '<CX>',
    'GREEN_ON_RED_3D' : '<CY>',
    'RED_ON_GREEN_3D' : '<CZ>'})

#Character Size/Format - There are eight character sizes or formats
    formats = dict({
        'NORMAL_DEFAULT' : '<SA>',
        'BOLD_WIDE' : '<SB>',
        'ITALIC' : '<SC>',
        'BOLD_ITALIC_WIDE' : '<SD>',
        'FLASHING_NORMAL' : '<SE>',
        'FLASHING_BOLD_WIDE' : '<SF>',
        'FLASHING_ITALIC' : '<SG>',
        'FLASHING_BOLD_ITALIC_WIDE' : '<SH>'})

#Functions - These are the available functions for displaying the text
    functions = dict({
        'RANDOM_COLOUR_AND_EFFECT' : '<FA>',
        'OPEN_FROM_THE_CENTER' : '<FB>',
        'HIDE_THE_TEXT' : '<FC>',
        'APPEAR' : '<FD>',
        'SCROLLING_COLOURS' : '<FE>',
        'CLOSE_RIGHT_TO_LEFT' : '<FF>',
        'CLOSE_LEFT_TO_RIGHT' : '<FG>',
        'CLOSE_TOWARD_CENTER' : '<FH>',
        'SCROLL_UP_FROM_THE_BOTTOM' : '<FI>',
        'SCROLL_DOWN_FROM_THE_TOP' : '<FJ>',
        'TWO_LAYERS_SLIDE_TOGETHER' : '<FK>',
        'FALLING_DOTS_FORM_TEXT' : '<FL>',
        'PAC_MAN_GRAPHIC' : '<FM>',
        'CREATURES' : '<FN>',
        'BEEP_THE_SIGN_BEEPS' : '<FO>',
        'PAUSE_SHORT_DELAY' : '<FP>',
        'SLEEP_BLANK_SCREEN' : '<FQ>',
        'RANDOM_DOTS_FORM_TEXT' : '<FR>',
        'ROLL_MESSAGE_LEFT_TO_RIGHT' : '<FS>',
        'SHOW_TIME_AND_DATE_NO_FORMATTING_CHOICES' : '<FT>',
        'TEXT_COLOUR_CHANGES_EACH_TIME' : '<FU>',
        'THANK_YOU_IN_CURSIVE' : '<FV>',
        'WELCOME_IN_CURSIVE' : '<FW>',
        'SPEED_1' : '<FX>',
        'SPEED_2' : '<FY>',
        'SPEED_3' : '<FZ>'})

    #PAGES
PAGE_1 = '<PA>'

#UNIT
UNIT = '<ID01>'
