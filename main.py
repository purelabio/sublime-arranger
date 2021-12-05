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
    sel = view.sel()

    if (len(sel) < 1): return
    sel = sel[0]

    reg = []
    lines = view.lines(sel)
    if (len(lines) > 2):
      reg = reduce_regions(lines)
    else:
      reg = reduce_regions([sel])

    view.sel().clear()
    view.sel().add_all([reg])


class arrange_easel(sublime_plugin.TextCommand):

  def run(self, edit, term, spaces, repeat):
    view    = self.view
    regions = view.sel()

    term   = term   or ""
    spaces = spaces or 128
    repeat = repeat or 10

    doc = sublime.Region(0, view.size())

    for region in reversed(view.lines(doc)):
      content = view.substr(region)
      content = (content.ljust(spaces) + term)
      view.replace(edit, region, content)

    view.sel().clear()
    view.sel().add_all(regions)


class arrange_easel_paste(sublime_plugin.TextCommand):

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


def reduce_regions(regs):
  shift = 0
  size = len(regs)

  if (size < 1):
    return []

  if (size <= 2):
    shift = 1
  else:
    regs = regs[1:size-1]

  beg = min(reg.begin() for reg in regs)
  end = max(reg.end()   for reg in regs)
  return sublime.Region(beg + shift, end - shift)

def test(expected, actual, msg):
  if expected != actual:
    raise Exception(msg + " expected: " + str(expected) + " actual: " + str(actual))

def test_reduce_selection():
  msg = "test_reduce_selection"

  test([], reduce_regions([]), msg)

  test(sublime.Region(3090+1, 3148-1),
    reduce_regions([
      sublime.Region(3090, 3148)
    ]),
    msg
  )

  test(sublime.Region(3090+1, 3212-1),
    reduce_regions([
      sublime.Region(3090, 3148),
      sublime.Region(3149, 3212),
    ]),
    msg
  )

  test(sublime.Region(3149, 3212),
    reduce_regions([
      sublime.Region(3090, 3148),
      sublime.Region(3149, 3212),
      sublime.Region(3213, 3276),
    ]),
    msg
  )

  test(sublime.Region(3149, 3327),
    reduce_regions([
      sublime.Region(3090, 3148),
      sublime.Region(3149, 3212),
      sublime.Region(3213, 3276),
      sublime.Region(3277, 3327),
      sublime.Region(3328, 3328),
    ]),
    msg
  )

  print("pass")

# Uncomment to run reduce selection tests.
# test_reduce_selection()


