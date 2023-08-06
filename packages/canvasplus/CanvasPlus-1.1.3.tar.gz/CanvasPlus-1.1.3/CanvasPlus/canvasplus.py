'''
Luke-zhang-04
Canvas Plus v1.1.3 (https://github.com/Luke-zhang-04/CanvasPlus)
Copyright (C) 2020 Luke-zhang-04

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://github.com/Luke-zhang-04/CanvasPlus/blob/master/LICENSE.
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
from typing import Tuple, Union, List, Callable, Dict

#warnings
import warnings

print("Hello from CanvasPlus")

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


class Transformations:
    def rotate(self, tagOrId: Union[int, str], x: Real, y: Real, amount: Real, unit: str = "rad", warn: bool = True) -> None:
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
            (self.coords(tagOrId)[i], self.coords(tagOrId)[i+1]) for i in range(0, len(self.coords(tagOrId)), 2)
        ]
        for xPt, yPt in cords:
            num = angle * (complex(xPt, yPt) - offset) + offset
            newCords.append(num.real)
            newCords.append(num.imag)
        
        objType = self.tk.call(self._w, 'type', tagOrId)
        if objType == "polygon":
            self.coords(tagOrId, *newCords)
        else:
            if (warn):
                warnings.warn(
                    "WARNING! Canvas element of type " + objType + " is not supported. Rotation may not look as expected. " + 
                    "Use the to_polygon() method to turn the " + objType + " into a polygon.",
                    UnsupportedObjectType
                )
            self.coords(tagOrId, *newCords)


class CanvasPlus(Canvas, WidgetWindowsm, Transformations):
    '''Improved Canvas widget with more functionality to display graphical elements like lines or text.'''

    def clone(self, tagOrId: Union[int, str], *args: List[int]) -> int:
        '''clones tagOrId and places is at optional coordinates, or places is on top of the first object'''
        if len(args) == 0:
            args = self.coords(tagOrId)
        
        output = self.get_attributes(tagOrId)
        
        return self._create(
            self.tk.call(self._w, 'type', tagOrId),
            args,
            output
        )
        
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

    def get_attributes(self, tagOrId: Union[int, str]) -> Dict:
        '''Returns all properties of tagOrId'''
        properties = self.itemconfig(tagOrId)
        return {key: properties[key][-1] for key in properties}

    get_attr = get_attributes

    def __iter__(self) -> iter:
        '''Creates iterator of everything on the canvas'''
        return iter(self.find_all())

    def to_polygon(self, tagOrId: Union[int, str]) -> int:
        '''converts rectangle to polygon'''
        output = self.get_attributes(tagOrId)

        cords = [self.tk.getdouble(x) for x in self.tk.splitlist(self.tk.call((self._w, 'coords') + tuple([tagOrId])))]

        if output["width"] == '0.0':
            output["outline"] = ''

        if self.tk.call(self._w, 'type', tagOrId) == "rectangle":
            newCords = [
                cords[0], cords[1],
                cords[2], cords[1],
                cords[2], cords[3],
                cords[0], cords[3]
            ]
        else:
            raise InvalidObjectType("Invalid canvas element \"" + self.tk.call(self._w, 'type', tagOrId) + "\"")

        self.tk.call((self._w, 'delete') + tuple([tagOrId]))

        return self._create('polygon', newCords, output)

    poly = to_polygon

    def tags_bind(
        self, tagsOrIds: Union[Union[int, str], Tuple[Union[int, str]], List[Union[int, str]]],
        sequences: Union[str, Tuple[str], List[str]] = None,
        funcs = Union[Callable, Tuple[Callable], List[Callable]], add = None) -> Union[str, List[str]]:
        '''Binds either multiple tags to one function, or multiple tags to multiple functions with matching indicies in one function
        
        i.e (tag1, tag2, tag3), func1 will bind tag1, tag2, tag3 into fun1, while (tag1, tag2, tag3), (func1, func2, func3) will bind tag1 to func1, tag2 to func2, tag3 to func3.
        '''
        if type(tagsOrIds) == int and callable(funcs): #normal tag_bind
            return self._bind((self._w, 'bind', tagsOrIds),sequences, funcs, add)
        else:
            bindings = []
            if type(funcs) not in [list, tuple]:
                funcs = tuple([funcs])
            if type(sequences) not in [list, tuple]:
                sequences = tuple([sequences])

            for index, obj in enumerate(tagsOrIds):
                bindings.append(
                        self._bind((self._w, 'bind', obj),
                        sequences[index%len(sequences)],
                        funcs[index%len(funcs)],
                        add
                    )
                )
            return bindings


def _test():
    #Imports
    from tkinter import Tk, StringVar, DoubleVar
    import math

    #set up canvas
    root = Tk()
    canvas = CanvasPlus(root, width=800, height=800, background = "white")
    canvas.pack()

    #create circle function
    canvas.create_circle(300, 600, 100, fill = "black", outline = "green", width = 3)
    
    #create rounded rectangle function
    canvas.create_round_rectangle(
        400, 550, 500, 650, radius = 75, fill = "blue", outline = "orange", width = 5
    )   

    #create arrow function and rotate it to by 310 degrees clockwise
    arrow = canvas.create_arrow(600, 600, 50, 50, 150, 20, fill = "grey", outline = "black")
    canvas.rotate(arrow, 600, 600, 310, unit="deg")

    #create a rectangle and convert it to a polygon; then rotate it by pi/4 radians (45 degrees)
    rect = canvas.create_rectangle(100, 550, 200, 650, fill = "#f7a8c6", width = 0)
    canvas.clone(rect)
    rect = canvas.poly(rect)
    canvas.rotate(rect, 150, 600, math.pi/4)

    #create an entry and set it's default value
    content = StringVar()
    canvas.create_entry(0, 0, anchor = "nw", textvariable = content, fg = "blue", bg = "gold")
    content.set("This is CanvasPlus v1.1.3")

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
        5, 75, font = ("Times", "24"), fg = "black", bg = "green", text = "By Luke-zhang-04", anchor = "nw"
    )

    canvas.update()
    canvas.mainloop()

if __name__ == "__main__":
    _test()

print("Imported successfully")