def template_timer():
    data = {
        "timer.zsh": """function snakypy_timer () {
    snakypy__timer_prefix1="$(snakypy::fg red " " "$SNAKYPY__SEPARATOR" "")"
    snakypy__timer_prefix2="$(snakypy::fg "$SNAKYPY__TIMER_PREFIX_COLOR" "" \\
"$SNAKYPY__TIMER_PREFIX_TEXT" " ")"
    if [[ $SNAKYPY__TIMER_SECOND_ENABLE == True ]]; then
        get_timer="$(date +%H:%M:%S)"
    else
        get_timer="$(date +%H:%M)"
    fi
    timer="$(snakypy::fg "$SNAKYPY__TIMER_COLOR" "" "[$(snakypy::icon "\\ufa1a" \\
"T:")${get_timer}]" " ")"
    if [[ $SNAKYPY__TIMER_ENABLE == True ]]; then
        echo "${timer}"
    fi
}
SNAKYPY__APPLY_TIMER="\\$(snakypy_timer)"
export SNAKYPY__APPLY_TIMER
"""
    }
    return data
