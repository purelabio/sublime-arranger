import sublime
import sublime_plugin

class CursorVerticalAlignCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    view = self.view
    sel  = self.view.sel()

    row_first, col_first = view.rowcol(sel[0].a)
    text_first = view.substr(view.line(sel[0].a))
    tabs_count_first = text_first.count('\t')
    regions = []
    for cursor in sel:
      row, col = view.rowcol(cursor.a)

      text  = view.substr(view.line(cursor.a))
      tabs_count = text.count('\t')

      tabs_diff = tabs_count_first - tabs_count

      point = view.text_point(row, col_first)
      regions.append(point)

      text_len = len(text)
      if col < col_first and text_len < col_first:
        self.view.insert(edit, view.text_point(row, text_len), " " * (col_first - text_len + tabs_diff))

    sel.clear()
    sel.add_all(regions)


class TextVerticalAlignCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    view = self.view
    sel  = self.view.sel()

    max_col = max([view.rowcol(min(x.a, x.b))[1] for x in sel])

    for point in sel:
      selection_start = min(point.a, point.b)
      rowcol = self.view.rowcol(selection_start)
      self.view.insert(edit, selection_start, " " * (max_col - rowcol[1]))
