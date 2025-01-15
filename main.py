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


class arrange_reduce_selection(sublime_plugin.TextCommand):
  def run(self, edit):
    new_regs = self.reduce_regs()
    self.view.sel().clear()
    self.view.sel().add_all(new_regs)

  def reduce_regs(self):
    view = self.view
    sel  = view.sel()
    lines = self.lines()

    if len(lines) > 1:
      return reduce_regions_vsel(lines)

    return reduce_regions_hsel(sel)

  def lines(self):
    view = self.view
    sel  = view.sel()

    if len(sel) == 1:
      return view.lines(sel[0])

    return []


def reduce_regions_hsel(regs):
  res = []

  for reg in regs:

    if reg.begin() == reg.end():
      res.append(reg)
      continue

    beg = min(reg.begin(), reg.end()) + 1
    end = max(reg.begin(), reg.end()) - 1
    res.append(sublime.Region(beg, end))

  return res

def reduce_regions_vsel(regs):
  size = len(regs)

  if (size < 1):
    return []

  if (size <= 2):
    return [regs[0]]
  else:
    regs = regs[1:size-1]

  beg = min(reg.begin() for reg in regs)
  end = max(reg.end()   for reg in regs)
  return [sublime.Region(beg, end)]


def test(expected, actual, msg):
  if type(expected) != list:
    expected = [expected]

  for i in range(len(expected)):
    exp = expected[i]
    act = actual[i]
    if exp != act:
      raise Exception(msg + " expected: " + str(exp) + " actual: " + str(act))


def test_reduce_vsel():
  test([], reduce_regions_vsel([]), 'test_reduce_vsel')

  test(sublime.Region(3090, 3148),
    reduce_regions_vsel([
      sublime.Region(3090, 3148)
    ]),
    'test_reduce_vsel'
  )

  test(sublime.Region(3090, 3148),
    reduce_regions_vsel([
      sublime.Region(3090, 3148),
      sublime.Region(3149, 3212),
    ]),
    'test_reduce_vsel'
  )

  test(sublime.Region(3149, 3212),
    reduce_regions_vsel([
      sublime.Region(3090, 3148),
      sublime.Region(3149, 3212),
      sublime.Region(3213, 3276),
    ]),
    'test_reduce_vsel'
  )

  test(sublime.Region(3149, 3327),
    reduce_regions_vsel([
      sublime.Region(3090, 3148),
      sublime.Region(3149, 3212),
      sublime.Region(3213, 3276),
      sublime.Region(3277, 3327),
      sublime.Region(3328, 3328),
    ]),
    'test_reduce_vsel'
  )

  print('test_reduce_vsel — pass')

def test_reduce_hsel():
  test([
    sublime.Region(3020, 3020),
  ],
  reduce_regions_hsel([
    sublime.Region(3020, 3020),
  ]),
  'test_reduce_hsel')

  test([
    sublime.Region(3019+1, 3024-1),
    sublime.Region(3032+1, 3037-1),
    sublime.Region(3055+1, 3060-1),
    sublime.Region(3095+1, 3100-1),
  ],
  reduce_regions_hsel([
    sublime.Region(3019, 3024),
    sublime.Region(3032, 3037),
    sublime.Region(3055, 3060),
    sublime.Region(3095, 3100),
  ]),
  'test_reduce_hsel')

  print('test_reduce_hsel — pass')


# Uncomment to run reduce selection tests.
# test_reduce_vsel()
# test_reduce_hsel()

class clone_file_and_goto_definition(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the current view and its contents
        view = self.view

        # Get current window
        window = view.window()

        # List views before cloning
        existing_views = window.views()

        # Get the current cursor position
        cursor_position = view.sel()[0].begin()

        # Run the 'clone_file' command
        window.run_command('clone_file')

        # Set delay to allow Sublime to create a new view
        self.on_new_view(window, existing_views, cursor_position)

    def on_new_view(self, window, existing_views, cursor_position):
        # Identify new view by comparing with previous views
        new_view = None
        for view in window.views():
            if view not in existing_views:
                new_view = view
                break

        if new_view:
            # Set the cursor position in the new file
            new_view.sel().clear()
            new_view.sel().add(sublime.Region(cursor_position, cursor_position))

            # Scroll to the cursor position
            new_view.show_at_center(cursor_position)

            view.window().run_command('goto_definition')

