#!/usr/bin/python
# -*- coding: utf-8 -*-

import Xlib, Xlib.display
from itertools import cycle, islice, count
from time import strftime, sleep
from backend import Cmus

USER = 'enz'

def get_meminfo():
    with open('/proc/meminfo') as f:
        mem_total = int(f.next().split()[1])
        mem_free = int(f.next().split()[1])
        buffers = int(f.next().split()[1])
        cached = int(f.next().split()[1])
    return ((mem_total - mem_free) - (buffers + cached)) / 1024, mem_total/1024


def get_date(f='%d %b %Y  %H:%M'):
    return strftime(f)

def scroll(s, n):
    it = (islice(cycle(s+' '), k, k+n) for k in count(0))
    while True:
        yield ''.join(it.next())

def cmus_status():
    while True:
        try:
            cmus = Cmus(USER)
            status = cmus.status()
            if cmus.is_playing():
                art = status['artist']
                tit = status['title']
                text = scroll(' - '.join([art, tit]), 23)
                while cmus.is_socket_alive() and cmus.is_playing()\
                        and (status['artist'], status['title']) == (art, tit):
                        status = cmus.status()
                        yield '♫ ' + text.next()
            else:
                while not cmus.is_playing():
                    yield '[stop]'
        except:
            while not cmus.is_socket_alive():
                yield '[off]'

def main_loop():
    disp = Xlib.display.Display(':0')
    root = disp.screen().root
    state = cmus_status()
    while True:
        mem, tot  = get_meminfo()
        date = get_date()
        output = '%s | %s/%sMB | %s' % (state.next(), mem, tot, date)
        root.set_wm_name(output)
        root.get_wm_name()
        sleep(0.25)

if __name__ == '__main__':
    try:
        main_loop()
    except:
        pass
