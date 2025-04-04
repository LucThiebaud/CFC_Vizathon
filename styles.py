from constants import *

LAYOUT_STYLE = {
    "maxWidth": "100vw",
    "height": "100vh",
    "position": "relative",
    "margin": "0 auto",
    "overflow": "hidden",
    "fontFamily": "ChelseaRegular",
    "backgroundColor": COLOR_BLUE,
    "boxShadow": "0px 0px 20px rgba(0, 0, 0, 0.3)"
}

HEADER_BACKGROUND_STYLE = {
    "backgroundColor": COLOR_DARK_BLUE,
    "height": f"{HEADER_HEIGHT_VH}vh",
    "width": "100%",
    "position": "absolute",
    "top": "0",
    "left": "0",
    "zIndex": "1"
}

SIDEBAR_BACKGROUND_STYLE = {
    "backgroundColor": COLOR_DARK_BLUE,
    "height": "100%",
    "width": f"{SIDEBAR_WIDTH_VW}vw",
    "position": "absolute",
    "top": "0",
    "left": "0",
    "zIndex": "1"
}

LOGO_STYLE = {
    "position": "absolute",
    "top": f"{HEADER_HEIGHT_VH}vh",
    "left": f"{SIDEBAR_WIDTH_VW / 2}vw",
    "height": f"{LOGO_SIZE_VH}vh",
    "transform": "translate(-50%, -50%)",
    "zIndex": "6"
}

SEPARATION_LINE_STYLE = {
    "position": "absolute",
    "top": "0",
    "left": f"{SIDEBAR_WIDTH_VW}vw",
    "width": f"{LINEWIDTH_SEPARATION_VH}vh",
    "height": "100%",
    "backgroundColor": COLOR_SNOW,
    "zIndex": "3"
}

TAB_BAR_STYLE = {
    "position": "absolute",
    "top": "0",
    "left": f"{SIDEBAR_WIDTH_VW}vw",
    "height": f"{HEADER_HEIGHT_VH}vh",
    "display": "flex",
    "alignItems": "center",
    "width": f"{100 - SIDEBAR_WIDTH_VW}vw",
    "zIndex": "2"
}

PAGE_CONTENT_STYLE = {
    "position": "absolute",
    "top": f"{HEADER_HEIGHT_VH}vh",
    "left": f"{SIDEBAR_WIDTH_VW}vw",
    "width": f"{100 - SIDEBAR_WIDTH_VW}vw",
    "height": f"{100 - SIDEBAR_WIDTH_VW}vh",
    "padding": "2vh 2vw",
    "overflow": "auto",
    "color": COLOR_SNOW
}
