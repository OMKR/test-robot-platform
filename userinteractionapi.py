# Copyright (c) 2014 Tampere University of Technology,
#                    Intel Corporation,
#                    OptoFidelity,
#                    and authors
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# pylint: disable = C0103, C0111, C0302, C0326
# pylint: disable = R0902, R0903, R0904, R0911, R0912, R0913, R0914, R0915
# pylint: disable = W0212

# coordinate handler helpers

# returns pos
def getPos(bbox, pos=(0.5, 0.5)):
    return (bbox[0][0] + pos[0] * (bbox[1][0] - bbox[0][0]), bbox[0][1] + pos[1] * (bbox[1][1] - bbox[0][1]))

def getClockwiseArcAngle(arcAngle=360):
    return abs(arcAngle)

def getCounterclockwiseArcAngle(arcAngle=360):
    return -abs(arcAngle)
    

# all element objects are immutable

class Element(object):
    def getPos(self, pos):
        raise NotImplementedError

class Location(Element):
    def __init__(self, pos):
        self._pos = pos
    
    def getPos(self, pos):
        return self._pos

class Area(Element):
    def __init__(self, upperLeftPos, lowerRightPos):
        self._bbox = (upperLeftPos, lowerRightPos)
    
    def getPos(self, pos):
        return getPos(self._bbox, pos)

    def getBbox(self):
        return self._bbox

class Image(Area):
    def __init__(self, image):
        # TODO
        pass

# consequtive words that may occupy non-rectangular area (i.e. there is no guarantee that any particular position within bounding box has a word at it)
class Text(Area):
    def __init__(self, text):
        # TODO
        pass
    
    def getWords(self):
        # TODO
        pass

# single word occupying rectangular area
class Word(Text):
    def __init__(self, word):
        # TODO
        pass
    
    def getWords(self):
        return (self,)


class UserInteractionApi(object):
    # argument types
    # pos:       tuple of two floats;   x, y coordinates, by default unity coordinates with origin at upper left corner of target area and (1.0, 1.0) at lower right corner, x increasing right and y increasing down
    # image:     reference to an image; exact format tbd., possibly path to image file
    # text:      str;                   text
    # element:   element object;        work area subpart
    # angle:     float;                 angle in degrees, clockwise from top unless otherwise indicated
    # distance:  float;                 length of gesture as proportion of maximal possible, maximum depends on gesture
    # duration:  float;                 time in seconds
    
    WORK_AREA = Area((0, 0), (1, 1))
    
    ANGLE_UP = 0.0
    ANGLE_RIGHT = 90.0
    ANGLE_DOWN = 180.0
    ANGLE_LEFT = 270.0
    
    
    # confirmed methods
    
    ###########################
    # tap (and hold) gestures #
    ###########################
    
    # arguments
    # element:  element to tap
    # image:    image to tap
    # text:     text to tap
    # pos:      position to tap within target area (entire work area for tap)
    # duration: minimum time to hold between press and release, 0.0 indicates ordinary tap 
    
    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; tap pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # touchAngle
    
    def tap(self, pos, duration=0.0, **kwargs):
        raise NotImplementedError
    
    def tapElement(self, element=WORK_AREA, pos=(0.5, 0.5), duration=0.0, **kwargs):
        raise NotImplementedError
    
    def tapImage(self, image, pos=(0.5, 0.5), duration=0.0, **kwargs):
        raise NotImplementedError
    
    def tapText(self, text, pos=(0.5, 0.5), duration=0.0, **kwargs):
        raise NotImplementedError
    
    ###########################################
    # drag gestures                           #
    # (sharp begin, straight move, sharp end) #
    ###########################################
    
    # arguments
    # beginElement:  element within which drag begins
    # endElement:    element within which drag ends (if angle is not given)
    # beginImage:    image within which drag begins
    # endImage:      image within which drag ends (if angle is not given)
    # beginText:     text within which drag begins
    # endText:       text within which drag ends (if angle is not given)
    # beginPos:      beginning position of drag within target area (entire work area for drag)
    # endPos:        ending position of drag within target area (entire work area for drag)
    # angle:         direction of drag gesture, if given pre-empts parameters for end position
    # distance:      distance to drag as proportion of distance from begin towards edge of work area, effective only if angle is given
    # beginDuration: minimum duration to hold between press and move
    # endDuration:   minimum duration to hold between move and release
    
    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; drag pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # dragDuration: duration of move
    
    def drag(self, beginPos, endPos, beginDuration=0.0, endDuration=0.0, **kwargs):
        raise NotImplementedError
    
    def dragElement(self, beginElement=WORK_AREA, endElement=WORK_AREA, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, beginDuration=0.0, endDuration=0.0, **kwargs):
        raise NotImplementedError
    
    def dragImage(self, beginImage, endImage=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, beginDuration=0.0, endDuration=0.0, **kwargs):
        raise NotImplementedError
    
    def dragText(self, beginText, endText=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, beginDuration=0.0, endDuration=0.0, **kwargs):
        raise NotImplementedError
    
    
    #############################################
    # swipe gestures                            #
    # (smooth begin, straight move, smooth end) #
    #############################################
    
    # arguments
    # beginElement:  element within which swipe begins
    # endElement:    element within which swipe ends (if angle is not given)
    # beginImage:    image within which swipe begins
    # endImage:      image within which swipe ends (if angle is not given)
    # beginText:     text within which swipe begins
    # endText:       text within which swipe ends (if angle is not given)
    # beginPos:      beginning position of swipe within target area (entire work area for swipe)
    # endPos:        ending position of swipe within target area (entire work area for swipe)
    # angle:         direction of swipe gesture, if given pre-empts parameters for end position
    # distance:      distance to swipe as proportion of distance from begin towards edge of work area, effective only if angle is given
    
    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; swipe pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # dragDuration: duration of move
    
    def swipe(self, beginPos, endPos, **kwargs):
        raise NotImplementedError
    
    def swipeElement(self, beginElement=WORK_AREA, endElement=WORK_AREA, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, **kwargs):
        raise NotImplementedError
    
    def swipeImage(self, beginImage, endImage=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, **kwargs):
        raise NotImplementedError
    
    def swipeText(self, beginText, endText=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, **kwargs):
        raise NotImplementedError
    
    
    ############################################
    # flick gestures                           #
    # (sharp begin, straight move, smooth end) #
    ############################################
    
    # arguments
    # beginElement:  element within which flick begins
    # endElement:    element within which flick ends (if angle is not given)
    # beginImage:    image within which flick begins
    # endImage:      image within which flick ends (if angle is not given)
    # beginText:     text within which flick begins
    # endText:       text within which flick ends (if angle is not given)
    # beginPos:      beginning position of flick within target area (entire work area for flick)
    # endPos:        ending position of flick within target area (entire work area for flick)
    # angle:         direction of flick gesture, if given pre-empts parameters for end position
    # distance:      distance to flick as proportion of distance from begin towards edge of work area, effective only if angle is given
    
    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; flick pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # dragDuration: duration of move
    
    def flick(self, beginPos, endPos, **kwargs):
        raise NotImplementedError
    
    def flickElement(self, beginElement=WORK_AREA, endElement=WORK_AREA, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, **kwargs):
        raise NotImplementedError
    
    def flickImage(self, beginImage, endImage=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, **kwargs):
        raise NotImplementedError
    
    def flickText(self, beginText, endText=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, **kwargs):
        raise NotImplementedError
    
    
    # unconfirmed methods
    
    #########################################
    # rotate gestures                       #
    # (sharp begin, curved move, sharp end) #
    #########################################
    
    # arguments
    # centerPos:  center of rotation
    # beginPos:   beginning position of rotation
    # element:    element within which rotation is performed
    # image:      image within which rotation is performed
    # text:       text within which rotation is performed
    # radius:     float; radius of rotation as proportion of distance from center of target area to nearest edge
    # beginAngle: beginning angle of rotation
    # direction:  direction of rotation
    # arcAngle:   angle of arc drawn by rotation
    
    def rotate(self, centerPos, beginPos, arcAngle=360, *kwargs):
        raise NotImplementedError
    
    # is offset needed?
    
    def rotateElement(self, element=WORK_AREA, radius=0.8, beginAngle=ANGLE_UP, arcAngle=360, *kwargs):
        raise NotImplementedError
    
    def rotateImage(self, image, radius=0.8, beginAngle=ANGLE_UP, arcAngle=360, *kwargs):
        raise NotImplementedError
    
    # is this variant needed?
    def rotateText(self, text, radius=0.8, beginAngle=ANGLE_UP, arcAngle=360, *kwargs):
        raise NotImplementedError
    
    ############################
    # image and text retrieval #
    ############################
    
    # are these needed, or are element objects enough?
    
    # returns bbox
    def locateImage(self, image, **kwargs):
        raise NotImplementedError
    
    # returns bbox
    def locateText(self, text, **kwargs):
        raise NotImplementedError


d = UserInteractionApi()

# tap coordinate
d.tap((0.5, 0.7))                # pos
d.tapElement(Location(0.5, 0.7)) # element
d.tapElement(pos=(0.5, 0.7))     # element

# tap center of text
d.tap(getPos(d.locateText("abc"))) # pos w. bboxes
d.tap(Text("abc").getPos())        # pos w. elements
d.tapElement(Text("abc"))          # element
d.tapText("abc")                   # text

# tap beginning of text
d.tap(getPos(d.locateText("abc"), (0.1, 0.5))) # pos w. bboxes
d.tap(Text("abc").getPos(0.1, 0.5))            # pos w. elements
d.tapElement(Text("abc"), (0.1, 0.5))          # element
d.tapText("abc", (0.1, 0.5))                   # text


# hold coordinate
d.tap((0.5, 0.7), holdTime=2.0) # parameter in tap


# rotate image full circle counterclockwise from top with pos
bbox = d.locateImage(imageId)
x, y = getPos(bbox)
d.rotate((x, y), (x, y + 0.8*(bbox[0][1] - y)))
# rotate image full circle counterclockwise from top with image
d.rotateImage(imageId)

# rotate image quarter circle clockwise from left with pos
bbox = d.locateImage(imageId)
x, y = getPos(bbox)
d.rotate((x, y), (x + 0.8*(bbox[0][0] - x, y)), direction=d.DIR_CLOCKWISE, arcAngle=90)
# rotate image quarter circle clockwise from left with bbox
d.rotateImage(imageId, beginAngle=d.ANGLE_LEFT, direction=d.DIR_CLOCKWISE, arcAngle=90)

