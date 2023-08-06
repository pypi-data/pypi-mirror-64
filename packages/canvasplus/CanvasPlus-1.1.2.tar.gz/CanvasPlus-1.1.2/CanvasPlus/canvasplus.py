'''
Luke-zhang-04
Canvas Plus v1.1.2 (https://github.com/Luke-zhang-04/CanvasPlus)
Copyright (C) 2020 Luke-zhang-04

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://github.com/Luke-zhang-04/CanvasPlus/blob/master/LICENSE.
'''

#tkinter
from tkinter import (
    Canvas, Button, Checkbutton, Entry, Frame, Label, LabelFrame, Listbox,
    PanedWindow, Radiobutton, Scale, Scrollbar, Spinbox
)

#complex numbers and stuff
import cmath, math

#stuff for typing hints
from numbers import Real

#typing
from typing import Tuple

#warnings
import warnings

class Error(Exception):
   '''Base class for other exceptions'''
   pass

class InvalidUnitError(Error):
    '''Raised when unit is not recognised'''
    pass

class UnsupportedObjectType(UserWarning):
    '''raised when object type is not supported'''
    pass

class InvalidObjectType(Error):
    '''raised when object type not supported'''
    pass

class WidgetWindows:
    '''Class for createing widgets as windows within the canvas'''

    windowProperties = ["anchor", "height", "state", "tags", "width", "window"]

    def _create_widget(self, x, y, widget, **kwargs):
        '''internal function: creates widget of widget type and puts it onto the canvas'''
        widgetKwargs = {}
        windowKwargs = {}
        for key, val in kwargs.items():
            if key in self.windowProperties:
                windowKwargs[key] = val
            else:
                widgetKwargs[key] = val

        newWidget = widget(self, **widgetKwargs)
        if "window" not in windowKwargs: windowKwargs["window"] = newWidget
        return self.create_window(x, y, **windowKwargs), newWidget
    
    def create_button(self, x: Real, y: Real, **kwargs) -> Tuple[int, Button]:
        '''
        create button with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the Button widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, Button, **kwargs)
        
    def create_checkbutton(self, x: Real, y: Real, **kwargs) -> Tuple[int, Checkbutton]:
        '''
        create checkbutton with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the Checkbutton widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, Checkbutton, **kwargs)

    def create_entry(self, x: Real, y: Real, **kwargs) -> Tuple[int, Entry]:
        '''
        create text entry box with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the Entry widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, Entry, **kwargs)
    
    def create_frame(self, x: Real, y: Real, **kwargs) -> Tuple[int, Frame]:
        '''
        create frame with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the Frame widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, Button, **kwargs)

    def create_label(self, x: Real, y: Real, **kwargs) -> Tuple[int, Label]:
        '''
        create label with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the Label widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, Label, **kwargs)

    def create_labelframe(self, x: Real, y: Real, **kwargs) -> Tuple[int, LabelFrame]:
        '''
        create label with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the LabelFrame widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, LabelFrame, **kwargs)

    def create_listbox(self, x: Real, y: Real, **kwargs) -> Tuple[int, Listbox]:
        '''
        create listbox with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the Listbox widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, Listbox, **kwargs)

    def create_panedwindow(self, x: Real, y: Real, **kwargs) -> Tuple[int, PanedWindow]:
        '''
        create panned window with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the PanedWindow widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, PanedWindow, **kwargs)

    def create_radiobutton(self, x: Real, y: Real, **kwargs) -> Tuple[int, Radiobutton]:
        '''
        create radiobutton with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the Radiobutton widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, Radiobutton, **kwargs)
    
    def create_scale(self, x: Real, y: Real, **kwargs) -> Tuple[int, Scale]:
        '''
        create scale with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the Scale widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, Scale, **kwargs)
    
    def create_scrollbar(self, x: Real, y: Real, **kwargs) -> Tuple[int, Scrollbar]:
        '''
        create scrollbar with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the Scrollbar widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, Scrollbar, **kwargs)

    def create_spinbox(self, x: Real, y: Real, **kwargs) -> Tuple[int, Spinbox]:
        '''
        create spinbox with cordinates x y

        Kwargs are automatically allocated to the correct element, i.e background will be "allocated" towards the Spinbox widget while "anchor" will be allocated to the window creation
        '''
        return self._create_widget(x, y, Spinbox, **kwargs)


class CanvasPlus(Canvas, WidgetWindows):
    '''Improved Canvas widget with more functionality to display graphical elements like lines or text.'''

    def create_arrow(self, x1: Real, y1: Real, headLength: Real, headWidth: Real, bodyLength: Real, bodyWidth: Real, **kwargs) -> int:
        '''Create arrow with x1, y1 as the tip; headWith, headLengh as the length and width of the arrowhead; and bodyLength, bodyWidth as the length and width of the arrow body, as well as direction = val (0 by default)'''
        
        points = [
            x1, y1,
            x1-headWidth//2, y1+headLength,
            x1-bodyWidth//2, y1+headLength,
            x1-bodyWidth//2, y1+bodyLength,
            x1+bodyWidth//2, y1+bodyLength,
            x1+bodyWidth//2, y1+headLength,
            x1+headWidth//2, y1+headLength
        ]
        
        return self._create('polygon', points, kwargs)

    def create_circle(self, x: Real, y: Real, radius: Real, **kwargs) -> int:
        '''Create circle with coordinates x, y, radius'''
        return self._create('oval', [x+radius, y+radius, x-radius, y-radius], kwargs)

    def to_polygon(self, obj:int) -> int:
        '''converts rectangle to polygon'''
        properties = self.itemconfig(obj)
        output = {
            key: properties[key][-1] for key in properties
        }
        
        cords = [self.tk.getdouble(x) for x in self.tk.splitlist(self.tk.call((self._w, 'coords') + tuple([obj])))]

        if output["width"] == '0.0':
            output["outline"] = ''

        if self.tk.call(self._w, 'type', obj) == "rectangle":
            newCords = [
                cords[0], cords[1],
                cords[1], cords[2],
                cords[2], cords[3],
                cords[3], cords[0]
            ]
        else:
            raise InvalidObjectType("Invalid canvas element \"" + self.tk.call(self._w, 'type', obj) + "\"")

        self.tk.call((self._w, 'delete') + tuple([obj]))

        return self._create('polygon', newCords, output)

    poly = to_polygon

    def rotate(self, obj: int, x: Real, y: Real, amount: Real, unit: str = "rad") -> None:
        '''rotate obj on axis x, y by amount in degrees or radians clockwise'''
        if unit in ("d", "deg", "degree", "degrees"):
            amount *= math.pi/180 #convert to radians
        elif unit in ("r", "rad", "radian", "radians"):
            pass
        else:
            raise InvalidUnitError("Invalid unit \"" + unit + "\"")
        
        angle = cmath.exp(amount*1j)
        offset = complex(x, y)
        newCords = []
        cords = [
            (self.coords(obj)[i], self.coords(obj)[i+1]) for i in range(0, len(self.coords(obj)), 2)
        ]
        for xPt, yPt in cords:
            num = angle * (complex(xPt, yPt) - offset) + offset
            newCords.append(num.real)
            newCords.append(num.imag)
        
        objType = self.tk.call(self._w, 'type', obj)
        if objType == "polygon":
            self.coords(obj, *newCords)
        else:
            warnings.warn("WARNING! Canvas element of type " + objType + " is not supported. Rotation may not look as expected.", UnsupportedObjectType)
            self.coords(obj, *newCords)

    def create_round_rectangle(self, x1: Real, y1: Real, x2: Real, y2: Real, radius: Real = 25, **kwargs) -> int:
        '''Create circle with coordinates x1, y1, x2, y2, radius = val (default 25)'''
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2, 
            x1, y2-radius, 
            x1, y2-radius, 
            x1, y1+radius,
            x1, y1+radius, 
            x1, y1
        ]

        kwargs["smooth"] = True
        return self._create('polygon', points, kwargs)

def _test():
    #Imports
    from tkinter import Tk, StringVar, DoubleVar
    import math

    #set up canvas
    root = Tk()
    canvas = CanvasPlus(root, width=800, height=800, background = "white")
    canvas.pack()

    #create circle function
    canvas.create_circle(300, 300, 100, fill = "black", outline = "green", width = 3)
    
    #create rounded rectangle function
    canvas.create_round_rectangle(
        400, 400, 500, 500, radius = 75, fill = "blue", outline = "orange", width = 5
    )   

    #create arrow function and rotate it to by 310 degrees clockwise
    arrow = canvas.create_arrow(600, 600, 50, 50, 150, 20, fill = "grey", outline = "black")
    canvas.rotate(arrow, 600, 600, 310, unit="deg")

    #create a rectangle and convert it to a polygon; then rotate it by pi/4 radians (45 degrees)
    rect = canvas.create_rectangle(100, 100, 200, 200, fill = "#f7a8c6", width = 0)
    rect = canvas.poly(rect)
    canvas.rotate(rect, 150, 150, math.pi/4)

    #create an entry and set it's default value
    content = StringVar()
    canvas.create_entry(0, 0, anchor = "nw", textvariable = content, fg = "blue", bg = "gold")
    content.set("a default value")

    #create button to print the value in the previously cretaed entry
    canvas.create_button(
        5, 25, anchor = "nw", text = "button", width = 50, highlightbackground = "red",
        command = lambda e = content: print(e.get())
    )

    #create checkbutton and toggle it
    _, checkbutton = canvas.create_checkbutton(
        5, 50, anchor = "nw", bg = "brown", fg = "white", text = "My Checkbutton"
    )
    checkbutton.toggle()

    #create a label
    canvas.create_label(
        5, 75, font = ("Times", "24"), fg = "black", bg = "green", text = "Hello World!", anchor = "nw"
    )

    #create a scale
    canvas.create_scale(
        5, 100, anchor = "nw", bg = "yellow", activebackground = "gold", from_ = 0, to = 100
    )

    canvas.update()
    canvas.mainloop()

if __name__ == "__main__":
    _test()