#!/usr/bin/env python
#
# Copyright 2008, 2009 Hannes Hochreiner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

import argparse

import inkex
from inkex import Group, Script
from inkex.utils import NSS

class KeyBindings(inkex.EffectExtension):
    modes = ('slide', 'index', 'drawing')
    keyCodes = ('LEFT', 'RIGHT', 'DOWN', 'UP', 'HOME', 'END', 'ENTER', 'SPACE', 'PAGE_UP', 'PAGE_DOWN', 'ESCAPE')
    slideActions = {}
    slideCharCodes = {}
    slideKeyCodes = {}
    drawingActions = {}
    drawingCharCodes = {}
    drawingKeyCodes = {}
    indexActions = {}
    indexCharCodes = {}
    indexKeyCodes = {}

    def __init__(self):
        # Call the base class constructor.
        inkex.EffectExtension.__init__(self)

        effect = self
        class SlideAction(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                for value in values:
                    effect.slideOptions(self.dest, option_string, value, parser)

        class DrawingAction(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                for value in values:
                    effect.drawingOptions(self.dest, option_string, value, parser)

        class IndexAction(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                for value in values:
                    effect.indexOptions(self.dest, option_string, value, parser)

        self.arg_parser.add_argument('--tab', type=str, dest='what')
        self.arg_parser.add_argument('--slide_backWithEffects', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_nextWithEffects', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_backWithoutEffects', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_nextWithoutEffects', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_firstSlide', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_lastSlide', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_switchToIndexMode', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_switchToDrawingMode', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_setDuration', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_addSlide', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_toggleProgressBar', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_resetTimer', action=SlideAction, default='')
        self.arg_parser.add_argument('--slide_export', action=SlideAction, default='')
        self.arg_parser.add_argument('--drawing_switchToSlideMode', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathWidthDefault', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathWidth1', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathWidth3', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathWidth5', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathWidth7', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathWidth9', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathColourBlue', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathColourCyan', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathColourGreen', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathColourBlack', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathColourMagenta', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathColourOrange', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathColourRed', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathColourWhite', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_pathColourYellow', action=DrawingAction, default='')
        self.arg_parser.add_argument('--drawing_undo', action=DrawingAction, default='')
        self.arg_parser.add_argument('--index_selectSlideToLeft', action=IndexAction, default='')
        self.arg_parser.add_argument('--index_selectSlideToRight', action=IndexAction, default='')
        self.arg_parser.add_argument('--index_selectSlideAbove', action=IndexAction, default='')
        self.arg_parser.add_argument('--index_selectSlideBelow', action=IndexAction, default='')
        self.arg_parser.add_argument('--index_previousPage', action=IndexAction, default='')
        self.arg_parser.add_argument('--index_nextPage', action=IndexAction, default='')
        self.arg_parser.add_argument('--index_firstSlide', action=IndexAction, default='')
        self.arg_parser.add_argument('--index_lastSlide', action=IndexAction, default='')
        self.arg_parser.add_argument('--index_switchToSlideMode', action=IndexAction, default='')
        self.arg_parser.add_argument('--index_decreaseNumberOfColumns', action=IndexAction, default='')
        self.arg_parser.add_argument('--index_increaseNumberOfColumns', action=IndexAction, default='')
        self.arg_parser.add_argument('--index_setNumberOfColumnsToDefault', action=IndexAction, default='')

        NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

        self.slideActions["backWithEffects"] = "dispatchEffects(-1);"
        self.slideActions["nextWithEffects"] = "dispatchEffects(1);"
        self.slideActions["backWithoutEffects"] = "skipEffects(-1);"
        self.slideActions["nextWithoutEffects"] = "skipEffects(1);"
        self.slideActions["firstSlide"] = "slideSetActiveSlide(0);"
        self.slideActions["lastSlide"] = "slideSetActiveSlide(slides.length - 1);"
        self.slideActions["switchToIndexMode"] = "toggleSlideIndex();"
        self.slideActions["switchToDrawingMode"] = "slideSwitchToDrawingMode();"
        self.slideActions["setDuration"] = "slideQueryDuration();"
        self.slideActions["addSlide"] = "slideAddSlide(activeSlide);"
        self.slideActions["toggleProgressBar"] = "slideToggleProgressBarVisibility();"
        self.slideActions["resetTimer"] = "slideResetTimer();"
        self.slideActions["export"] = "slideUpdateExportLayer();"

        self.drawingActions["switchToSlideMode"] = "drawingSwitchToSlideMode();"
        self.drawingActions["pathWidthDefault"] = "drawingResetPathWidth();"
        self.drawingActions["pathWidth1"] = "drawingSetPathWidth(1.0);"
        self.drawingActions["pathWidth3"] = "drawingSetPathWidth(3.0);"
        self.drawingActions["pathWidth5"] = "drawingSetPathWidth(5.0);"
        self.drawingActions["pathWidth7"] = "drawingSetPathWidth(7.0);"
        self.drawingActions["pathWidth9"] = "drawingSetPathWidth(9.0);"
        self.drawingActions["pathColourBlue"] = "drawingSetPathColour(\"blue\");"
        self.drawingActions["pathColourCyan"] = "drawingSetPathColour(\"cyan\");"
        self.drawingActions["pathColourGreen"] = "drawingSetPathColour(\"green\");"
        self.drawingActions["pathColourBlack"] = "drawingSetPathColour(\"black\");"
        self.drawingActions["pathColourMagenta"] = "drawingSetPathColour(\"magenta\");"
        self.drawingActions["pathColourOrange"] = "drawingSetPathColour(\"orange\");"
        self.drawingActions["pathColourRed"] = "drawingSetPathColour(\"red\");"
        self.drawingActions["pathColourWhite"] = "drawingSetPathColour(\"white\");"
        self.drawingActions["pathColourYellow"] = "drawingSetPathColour(\"yellow\");"
        self.drawingActions["undo"] = "drawingUndo();"

        self.indexActions["selectSlideToLeft"] = "indexSetPageSlide(activeSlide - 1);"
        self.indexActions["selectSlideToRight"] = "indexSetPageSlide(activeSlide + 1);"
        self.indexActions["selectSlideAbove"] = "indexSetPageSlide(activeSlide - INDEX_COLUMNS);"
        self.indexActions["selectSlideBelow"] = "indexSetPageSlide(activeSlide + INDEX_COLUMNS);"
        self.indexActions["previousPage"] = "indexSetPageSlide(activeSlide - INDEX_COLUMNS * INDEX_COLUMNS);"
        self.indexActions["nextPage"] = "indexSetPageSlide(activeSlide + INDEX_COLUMNS * INDEX_COLUMNS);"
        self.indexActions["firstSlide"] = "indexSetPageSlide(0);"
        self.indexActions["lastSlide"] = "indexSetPageSlide(slides.length - 1);"
        self.indexActions["switchToSlideMode"] = "toggleSlideIndex();"
        self.indexActions["decreaseNumberOfColumns"] = "indexDecreaseNumberOfColumns();"
        self.indexActions["increaseNumberOfColumns"] = "indexIncreaseNumberOfColumns();"
        self.indexActions["setNumberOfColumnsToDefault"] = "indexResetNumberOfColumns();"

    def slideOptions(self, option, opt_str, value, parser):
        action = self.getAction(opt_str)

        valueArray = value.split(",")

        for val in valueArray:
            val = val.strip()

            if val in self.keyCodes:
                self.slideKeyCodes[val + "_KEY"] = self.slideActions[action]
            elif len(val) == 1:
                self.slideCharCodes[val] = self.slideActions[action]

    def drawingOptions(self, option, opt_str, value, parser):
        action = self.getAction(opt_str)

        valueArray = value.split(",")

        for val in valueArray:
            val = val.strip()

            if val in self.keyCodes:
                self.drawingKeyCodes[val + "_KEY"] = self.drawingActions[action]
            elif len(val) == 1:
                self.drawingCharCodes[val] = self.drawingActions[action]

    def indexOptions(self, option, opt_str, value, parser):
        action = self.getAction(opt_str)

        valueArray = value.split(",")

        for val in valueArray:
            val = val.strip()

            if val in self.keyCodes:
                self.indexKeyCodes[val + "_KEY"] = self.indexActions[action]
            elif len(val) == 1:
                self.indexCharCodes[val] = self.indexActions[action]

    def effect(self):
        # Check version.
        scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.5']", namespaces=NSS)

        if len(scriptNodes) != 1:
            inkex.errormsg(_("The JessyInk script is not installed in this SVG file or has a different version than the JessyInk extensions. Please select \"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" menu to install or update the JessyInk script.\n\n"))

        # Remove old master slide property
        for node in self.document.xpath("//svg:g[@jessyink:customKeyBindings='customKeyBindings']", namespaces=NSS):
            node.getparent().remove(node)

        # Set custom key bindings.
        nodeText = "function getCustomKeyBindingsSub()" + "\n"
        nodeText += "{" + "\n"
        nodeText += "    var keyDict = new Object();" + "\n"
        nodeText += "    keyDict[SLIDE_MODE] = new Object();" + "\n"
        nodeText += "    keyDict[INDEX_MODE] = new Object();" + "\n"
        nodeText += "    keyDict[DRAWING_MODE] = new Object();" + "\n"

        for key, value in self.slideKeyCodes.items():
            nodeText += "    keyDict[SLIDE_MODE][" + key + "] = function() { " + value + " };" + "\n"

        for key, value in self.drawingKeyCodes.items():
            nodeText += "    keyDict[DRAWING_MODE][" + key + "] = function() { " + value + " };" + "\n"

        for key, value in self.indexKeyCodes.items():
            nodeText += "    keyDict[INDEX_MODE][" + key + "] = function() { " + value + " };" + "\n"

        nodeText += "    return keyDict;" + "\n"
        nodeText += "}" + "\n\n"

        # Set custom char bindings.
        nodeText += "function getCustomCharBindingsSub()" + "\n"
        nodeText += "{" + "\n"
        nodeText += "    var charDict = new Object();" + "\n"
        nodeText += "    charDict[SLIDE_MODE] = new Object();" + "\n"
        nodeText += "    charDict[INDEX_MODE] = new Object();" + "\n"
        nodeText += "    charDict[DRAWING_MODE] = new Object();" + "\n"

        for key, value in self.slideCharCodes.items():
            nodeText += "    charDict[SLIDE_MODE][\"" + key + "\"] = function() { " + value + " };" + "\n"

        for key, value in self.drawingCharCodes.items():
            nodeText += "    charDict[DRAWING_MODE][\"" + key + "\"] = function() { " + value + " };" + "\n"

        for key, value in self.indexCharCodes.items():
            nodeText += "    charDict[INDEX_MODE][\"" + key + "\"] = function() { " + value + " };" + "\n"

        nodeText += "    return charDict;" + "\n"
        nodeText += "}" + "\n"

        # Create new script node
        group = self.svg.add(Group())
        script = group.add(Script())
        script.text = nodeText
        group.set("jessyink:customKeyBindings", "customKeyBindings")
        group.set("onload", "this.getCustomCharBindings = function() { return getCustomCharBindingsSub(); }; this.getCustomKeyBindings = function() { return getCustomKeyBindingsSub(); };")

    def getAction(self, varName):
        parts = varName.split('_')
        if len(parts) != 2:
            raise Exception("Error parsing variable name.")
        return parts[1]

if __name__ == '__main__':
    KeyBindings().run()
