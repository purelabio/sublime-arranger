import sublime
import sublime_plugin

class CursorVerticalAlignCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    view = self.view
    sel  = self.view.sel()

    first_sel = sel[0]
    first_point = view.rowcol(first_sel.a)
    col_to_align = first_point[1]

    regions = []
    for cursor in sel:
      row = view.rowcol(cursor.a)[0]
      point = view.text_point(row, col_to_align)
      regions.append(point)

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
