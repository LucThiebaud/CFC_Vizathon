# Colors
COLOR_DARK_BLUE = '#140a47'
COLOR_BLUE = '#001489'
COLOR_SNOW = '#FFFAFA'
COLOR_LIGHT_BLUE = "#5db9ff"
COLOR_YELLOW = '#ffff6a'
COLOR_UNDER_TRAINING_LOAD = '#ffbf00'
COLOR_OPTIMAL_TRAINING_LOAD = '#01b053'
COLOR_DANGER_LOAD = '#fe0002'
COLOR_BLACK = '#000000'
COLOR_GREEN = '#2da44e'
COLOR_RED = '#ef0a0a'

# Logo Chelsea
URL_CHELSEA_LOGO = 'https://tmssl.akamaized.net//images/wappen/head/631.png'

# Layout and dimensions
HEADER_HEIGHT_VH = 6
SIDEBAR_WIDTH_VW = 7
LOGO_SIZE_VH = 14
LINEWIDTH_SEPARATION_VH = 0.1
FONTSIZE_TAB_VH = "2.5vh"
SCALE_IMAGE_PLAYER_SIDEBAR_VW = 4.5

# Tabs configuration
TAB_TITLES = ['OVERVIEW', 'LOAD DEMAND', 'RECOVERY']
TAB_IDS = [f"tab-{i+1}" for i in range(len(TAB_TITLES))]
TAB_WIDTH = f"calc((100vw - {SIDEBAR_WIDTH_VW}vw) / {len(TAB_TITLES)})"

# Police size
TITLE_SIZE = 4
SUBTITLE_SIZE = 3
BODY_SIZE = 2
