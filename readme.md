

# Sublime Arrange Text

Tiny Plugin for Sublime Text for alignment in the column of cursors and text.

## Keyboard shortcuts for  Apple Macintosh

Vertical align cursors
- use <kbd>⌘ cmd</kbd> + <kbd>^ ctrl</kbd> + <kbd>⇪ shift</kbd> + <kbd>↑</kbd> or <kbd>⌘ cmd</kbd> + <kbd>^ ctrl</kbd> + <kbd>⇪ shift</kbd> + <kbd>↓</kbd>
- press <kbd>⌘ cmd</kbd> + <kbd>\\</kbd>

Vertical align text
- use <kbd>⌘ cmd</kbd> + <kbd>d</kbd> to [Quick Add Next](https://www.sublimetext.com/docs/2/multiple_selection_with_the_keyboard.html)
- press <kbd>⌘ cmd</kbd> + <kbd>⌥ alt</kbd> + <kbd>\\</kbd>

Vertical align find string in selection
- use <kbd>⌘ cmd</kbd> + <kbd>E</kbd> to slurp find string
- select region to align and press
- <kbd>⌘ cmd</kbd> + <kbd>⇪ shift</kbd> + <kbd>\\</kbd> to align;

## Keyboard shortcuts for Linux and Windows

Vertical align cursors
- use <kbd>^ ctrl</kbd> + <kbd>⇪ shift</kbd> + <kbd>↑</kbd> or <kbd>^ ctrl</kbd> + <kbd>⇪ shift</kbd> + <kbd>↓</kbd>
- press <kbd>^ ctrl</kbd> + <kbd>\\</kbd>

Vertical align text
- use <kbd>^ ctrl</kbd> + <kbd>d</kbd> to [Quick Add Next](https://www.sublimetext.com/docs/2/multiple_selection_with_the_keyboard.html)
- press <kbd>^ ctrl</kbd> + <kbd>⌥ alt</kbd> + <kbd>\\</kbd>

Vertical align find string in selection
- use <kbd>^ ctrl</kbd> + <kbd>E</kbd> to slurp find string
- select region to align and press
- <kbd>^ ctrl</kbd> + ⇪ <kbd>⇪ shift</kbd> + <kbd>\\</kbd> to align;

## Demo

![Demo](https://raw.githubusercontent.com/purelabio/sublime-vertical-align/master/demo.gif)

## Description

The remaining aligners work on a different principle. They require configuration and align the texts vertically in accordance with a predetermined set of characters and / or require setting indents counts, etc. Unlike all the others, this one does not make assumptions about what should be equalized and how.

Instead, this plugin in the spirit of sublime text provides the user with the ability to apply alignment based on cursors and selections. Allows you to align cursors, align texts on each line before the cursor and use the selection to search for alignment in the selected area. Very small code size, without affecting the text editor braking itself.