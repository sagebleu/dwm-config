# cmus socket interface
#
# by Enric Morales. Uncopyrighted, 2013

import re
from os import path
from socket import socket, AF_UNIX, SOCK_STREAM


class Cmus(object):
    def __init__(self, user):
        """
        Sets the only important variable here, which is the
        location of the cmus socket.
        """

        self.socket_path = path.join(path.expanduser('~' + user),
                                     '.cmus',
                                     'socket')

    def send_socket_cmd(self, cmd, rx=0):
        """
        Connects to the cmus socket and sends the 'cmd' command,
        not expecting any reply unless rx is some value higher
        than 0.
        """

        s = socket(AF_UNIX, SOCK_STREAM)
        s.connect(self.socket_path)

        if s.send((cmd + "\n").encode("ascii")) == 0:
            raise RuntimeError("Socket connection broken.")

        if rx > 0:
            answer = s.recv(rx)
            ret = str(answer)
        else:
            ret = None

        s.close()
        return ret

    def format_s(self, s):
        """
        Small function to convert 's' seconds into "mm:ss" format.
        """

        m = str(s // 60)
        s = s % 60

        if s < 10:
            s = "0" + str(s)
        else:
            s = str(s)

        out = m + ":" + s
        return out

    def is_playing(self):
        """
        Returns True if the player is playing.
        """

        return 'status playing' in self.send_socket_cmd('status',
                                                        rx=4096)

    def is_stopped(self):
        """
        Returns True if the player is stopped.
        """

        return 'status stopped' in self.send_socket_cmd('status',
                                                        rx=4096)

    def is_paused(self):
        """
        Returns True if the player is paused.
        """

        return 'status paused' in self.send_socket_cmd('status',
                                                       rx=4096)

    def play(self):
        """
        Sends the 'play' command over the socket.
        """

        if not self.is_playing():
            self.send_socket_cmd('player-play')
            return 'playing'
        else:
            return self.pause()

    def pause(self):
        """
        Sends the 'pause' command over the socket.
        """

        self.send_socket_cmd("player-pause")

        if self.is_paused():
            return 'paused'
        else:
            return 'playing'

    def stop(self):
        """
        Sends the 'stop' command over the socket.
        """

        if not self.is_stopped():
            self.send_socket_cmd('player-stop')
            return 'stopped'
        else:
            return 'already stopped'

    def nnext(self):
        """
        Sends the 'player-next' command over the socket.
        """

        self.send_socket_cmd('player-next')
        return 'next track'

    def status(self):
        """
        Returns a dictionary composed of the tags of the currently
        played file. The keys are the tag types and the values are the
        actual tag values.
        """

        output = {}
        status = self.send_socket_cmd('status', rx=4096)
        tags = re.findall(r'tag (\w+) (.*)\n', status, re.MULTILINE)
        duration = re.findall(r'duration (\w+)', status, re.MULTILINE)
        output = {k: v for k, v in tags}

        ##########################################
        if 'artist' not in output:
            output['artist'] = 'Unknown'

        if 'title' not in output:
            output['title'] = 'Untitled'
        ############################################

        if len(duration) > 0:
            output['duration'] = self.format_s(int(duration[0]))

        if self.is_paused():
            output['paused'] = True
        else:
            output['paused'] = False

        if self.is_stopped():
            output['stopped'] = True
        else:
            output['stopped'] = False

        if self.is_playing():
            output['playing'] = True
        else:
            output['playing'] = False

        return output

    def prev(self):
        """
        Sends the 'player-prev' command over the socket.
        """

        self.send_socket_cmd("player-prev")
        return 'previous track'

    def is_socket_alive(self):
        """
        Returns True if it's possible to connect to the socket,
        and False otherwise.
        """

        s = socket(AF_UNIX, SOCK_STREAM)

        try:
            s.connect(self.socket_path)
            s.close()
            return True
        except:
            return False
