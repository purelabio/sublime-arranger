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

      if col < col_first and len(text) < col_first:
        self.view.insert(edit, cursor.a, " " * (col_first - col + tabs_diff))

    sel.clear()
    sel.add_all(regions)


class TextVerticalAlignCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    view = self.view
    sel  = self.view.sel()

    max_col = max([view.rowcol(x.a)[1] for x in sel])

    for point in sel:
      rowcol = self.view.rowcol(point.a)
      self.view.insert(edit, point.a, " " * (max_col - rowcol[1]))
