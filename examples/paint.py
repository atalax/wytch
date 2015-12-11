#! /usr/bin/env python3
#
# Copyright (c) 2015 Josef Gajdusek
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from wytch import builder, colors, view, input, Wytch

w = Wytch(buffer = True)

class ColorButton(view.Widget):

    def __init__(self, color, board):
        super(ColorButton, self).__init__()
        self.color = color
        self.board = board
        self.focusable = False
        self.hstretch = False
        self.vstretch = False

    def render(self):
        if not self.canvas:
            return
        self.canvas.square(0, 0, self.canvas.width, self.canvas.height,
            bordercolor = self.color)

    def onmouse(self, me):
        if not me.pressed:
            return
        self.board.colors[me.button] = self.color

    @property
    def size(self):
        return (5, 2)

class DrawingBoard(view.Widget):

    def __init__(self):
        super(DrawingBoard, self).__init__()
        self.grid = None
        self.oldme = None
        self.colors = {}
        self.handlers.append(("c", self._onclear))

    def _onclear(self, kc):
        self.canvas.clear()

    def recalc(self):
        if not self.canvas:
            return
        if not self.grid or len(self.grid) != self.canvas.width \
                or len(self.grid[0]) != self.canvas.height:
            self.grid = [[False] * self.canvas.height for _ in range(self.canvas.width)]

    def onmouse(self, me):
        if me.released:
            key = self.oldme.button
        else:
            key = me.button
        color = self.colors.get(key, colors.DARKGREEN)
        if not self.oldme:
            self.canvas.set(me.x, me.y, " ", bg = color)
        else:
            self.canvas.line(self.oldme.x, self.oldme.y, me.x, me.y, bg = color)

        if me.released:
            self.oldme = None
        else:
            self.oldme = me


    def render(self):
        if not self.canvas:
            return
        for x, col in enumerate(self.grid):
            for y, v in enumerate(col):
                self.canvas.set(x, y, " ")

    @property
    def size(self):
        return (1, 1)

with w:
    board = DrawingBoard()
    w.root.handlers.append(("q", lambda _: w.exit()))
    with builder.Builder(w.root) as b:
        h = b.vertical() \
            .horizontal()
        for c in colors.c256[:16]:
            h.add(ColorButton(c, board))
        h.end().add(board)
