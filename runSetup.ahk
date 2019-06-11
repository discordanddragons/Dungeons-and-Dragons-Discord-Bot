#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.


^j::
IfWinExist, #general - Discord
    WinActivate
Send, {!}newChar Frodo{Enter}
sleep, 1500
Send, {!}newGame "Twin Towers" 4{Enter}
sleep, 1500
Send, {!}activeGame "Twin Towers"{Enter}
sleep, 1500
Send, {!}addPlayer Frodo{Enter}
