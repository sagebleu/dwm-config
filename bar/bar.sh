#!/bin/sh

#     --  bar.sh: a simple & stupid statusbar for dwm... Nothing more. --


while true ; do
    DATE=`date +'%d %b %Y  %H:%M'`

    MemTotal=`awk 'NR == 1 {print $2}' /proc/meminfo`
    MemFree=`awk 'NR == 2 {print $2}' /proc/meminfo`
    Buffers=`awk 'NR == 3 {print $2}' /proc/meminfo`
    Cashed=`awk 'NR == 4 {print $2}' /proc/meminfo`
    Used=`expr '(' '(' $MemTotal - $MemFree ')' - '(' $Buffers + $Cashed ')' ')' / 1024`

    RAM="$Used/`expr $MemTotal / 1024`MB"

    #MocState=`mocp -Q %state`
    #case $MocState in
    #  "PLAY"|"PAUSE")
    #    MOC=`mocp -Q %artist\ -\ %song\ [%ct/%tt]`
    #    ;;
    #  "STOP")
    #    MOC="[stop]"
    #    ;;
    #  *)
    #    MOC="[off]"
    #    ;;
    #esac

    CmusState=`cmus-remote -Q 2> /dev/null | head -n1`
    case $CmusState in
      "status playing")
        artist=`cmus-remote -Q | grep artist | cut -d ' ' -f 3- | sed '2,3d'`
        title=`cmus-remote -Q | grep title | cut -d ' ' -f 3-`
        CMUS="♫ $artist - $title"
        ;;
      "status paused")
        artist=`cmus-remote -Q | grep artist | cut -d ' ' -f 3- | sed '2,3d'`
        title=`cmus-remote -Q | grep title | cut -d ' ' -f 3-`
        CMUS="  $artist - $title"
        ;; 
      "status stopped"*)
          CMUS="[stop]"
          ;;
       *)
        CMUS="[off]"
        ;;
    esac

    xsetroot -name "$CMUS  |  $RAM  |  $DATE"
    sleep 0.25s
done

