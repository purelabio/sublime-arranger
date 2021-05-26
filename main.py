import sublime
import sublime_plugin

class arrange_cursor_vertical(sublime_plugin.TextCommand):

  def run(self, edit):
    view                = self.view
    sel                 = view.sel()
    _, first_column     = view.rowcol(sel[0].a)
    first_text          = view.substr(view.line(sel[0].a))
    tabs_count_at_first = first_text.count('\t')
    regions             = []

    for cursor in sel:
      row, col    = view.rowcol(cursor.a)
      text        = view.substr(view.line(cursor.a))
      tabs_count  = text.count('\t')
      tabs_diff   = tabs_count_at_first - tabs_count
      text_length = len(text)
      point       = view.text_point(row, first_column)

      regions.append(point)

      if col < first_column and text_length < first_column:
        spaces     = " " * (first_column - text_length + tabs_diff)
        text_point = view.text_point(row, text_length)
        view.insert(edit, text_point, spaces)

    sel.clear()
    sel.add_all(regions)


class arrange_text_vertical(sublime_plugin.TextCommand):

  def run(self, edit):
    view    = self.view
    sel     = view.sel()
    max_col = max([view.rowcol(min(x.a, x.b))[1] for x in sel])

    for point in sel:
      selection_start = min(point.a, point.b)
      rowcol          = view.rowcol(selection_start)
      spaces          = " " * (max_col - rowcol[1])
      view.insert(edit, selection_start, spaces)


# TODO Reduce the number of spaces to the index
class arrange_use_selection(sublime_plugin.TextCommand):

  def run(self, edit):
    view     = self.view
    position = view.viewport_position()

    block_to_arrange = view.sel()
    if block_to_arrange is None: return

    text_to_arrange  = self.get_slurp_find_text()
    if text_to_arrange  is None: return

    line_regions = view.lines(block_to_arrange[0])

    max_index = max([
      view.substr(view.line(cursor)).find(text_to_arrange)
      for cursor in line_regions
    ])

    line_regions.reverse()

    for cursor in line_regions:
      line   = view.line(cursor)
      substr = view.substr(line)
      index  = substr.find(text_to_arrange)
      start  = min(line.a, line.b) + index
      rowcol = view.rowcol(start)
      spaces = " " * (max_index - index)

      if index == -1: continue

      view.insert(edit, start, spaces)

    restore = lambda: view.set_viewport_position(position, animate=False)
    sublime.set_timeout(restore, 0)


  def get_slurp_find_text(self):
    view            = self.view
    selected_region = view.sel()[0]

    view.run_command("find_next")
    view.run_command("find_prev")
    sel = view.sel()

    if len(sel) == 0: return None

    text = view.substr(sel[0])
    view.sel().clear()
    view.sel().add(selected_region)

    return text


class arrange_reduce_selection(sublime_plugin.TextCommand):

  def run(self, edit):
    view = self.view
    sel  = view.sel()
    regions = view.lines(sel[0])

    if (len(regions) < 3):
      return

    view.run_command("expand_selection", {"to": "line"})

    regions = view.lines(sel[0])
    new_regions = regions[1:len(regions)-1]
    new_regions = [(x.a, x.b) for x in new_regions]
    positions = [x for xs in new_regions for x in xs]
    new_region = sublime.Region(min(positions), max(positions))

    sel.clear()
    sel.add_all([new_region])

class arrange_easel(sublime_plugin.TextCommand):

  def run(self, edit, term, spaces, repeat):
    view = self.view

    term   = term   or "|"
    spaces = spaces or 128
    repeat = repeat or 10

    blank = (term + "\n").rjust(spaces)
    text = blank
    for i in range(repeat):
      text += blank

    for region in view.sel():
        view.insert(edit, region.begin(), text)
