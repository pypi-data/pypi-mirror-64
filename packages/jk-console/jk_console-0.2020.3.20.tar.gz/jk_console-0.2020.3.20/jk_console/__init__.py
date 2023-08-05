﻿


__version__ = "0.2020.3.20"



from .Rect import Rect
from .Console import Console
from .ConsoleGraphics import ConsoleGraphics	# console buffer: cells with color ASCII string, text character and modification-flag; the buffer itself is without offset;
from .ConsoleBuffer import ConsoleBuffer		# console buffer: cells with color ASCII string, text character and modification-flag; the buffer itself has an offset value stored internall;
from .ConsoleBufferWO import ConsoleBufferWO	# simple version of ConsoleBuffer without modification flag
from .CharacterBuffer import CharacterBuffer	# int-based RGB values
from .IntRGB import IntRGB
from .ConsoleBufferRGB import ConsoleBufferRGB, FramedBoxSettingsRGB
from .SimpleTable import SimpleTable, SimpleTableCell, SimpleTableColumn, SimpleTableRow, SimpleTableConstants
from .EventCollector import EventCollector
from .FramedBoxSettingsRGB import FramedBoxSettingsRGB
from .ConsoleBufferRGB2 import ConsoleBufferRGB2



