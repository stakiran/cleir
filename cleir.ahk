; cleir - version 0.0.1

____preparation____:

SetWorkingDir %A_ScriptDir%
CoordMode Mouse, Screen
FileEncoding, CP65001

#SingleInstance force
#Persistent

; consts
BASEDIR = %A_ScriptDir%
FULLPATH_SCRIPT = %A_ScriptFullPath%

____main____:

prev_clipboard = %clipboard%

Loop
{
  current_clipboard = %clipboard%

  if prev_clipboard <> %current_clipboard%
  {
    prev_clipboard = %current_clipboard%
    Run, pythonw %BASEDIR%\cle.py
  }

  Sleep, 1000
}

Return

ExitFunc:
  ExitApp
Return
