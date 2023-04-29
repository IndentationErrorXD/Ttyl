from main import *
from tkinter import messagebox, filedialog
from main import _date, _save_

if _date > date.today():
    cal.set_date(date)
    messagebox.showwarning("Time travel not possible", "Cannot select future date")
else:
    if unsaved_changes:
        save_qn = messagebox.askyesno("Confirm Save", "Save changes?")
        if save_qn:
            _save_()
        else:
            unsaved_changes = False
