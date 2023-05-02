"""
    ttkbootstrap demo

    ISSUES:
        - the legacy tk widgets do not update after DateDialog is used.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledText


def setup_demo(master):

    root = ttk.Frame(master, padding=10)
    style = ttk.Style()
    
    ttk.Separator(root).pack(fill=X, pady=10, padx=10)
    
    treeFrame = ttk.Frame(root, padding=5)
    treeFrame.pack(side=RIGHT, fill=BOTH, expand=YES)

    rframe = ttk.Frame(root, padding=5)
    rframe.pack(side=LEFT, fill=BOTH, expand=YES)

    treeLabel = ttk.Labelframe(
        treeFrame, text="Pedidos", padding=10
    )
    treeLabel.pack(fill=X, pady=10, side=TOP)

    

    ttframe = ttk.Frame(treeFrame)
    ttframe.pack(pady=5, fill=X, side=TOP)

    table_data = [
        ("South Island, New Zealand", 1),
        ("Paris", 2),
        ("Bora Bora", 3),
        ("Maui", 4),
        ("Tahiti", 5),
        ("South Island, New Zealand", 1),
        ("Paris", 2),
        ("Bora Bora", 3),
        ("Maui", 4),
        ("Tahiti", 5),
        ("South Island, New Zealand", 1),
        ("Paris", 2),
        ("Bora Bora", 3),
        ("Maui", 4),
        ("Tahiti", 5),
    ]

    tv = ttk.Treeview(master=treeLabel, columns=[0, 1], show=HEADINGS, height=5)
    for row in table_data:
        tv.insert("", END, values=row)

    tv.selection_set("I001")
    tv.heading(0, text="City")
    tv.heading(1, text="Rank")
    tv.column(0, width=300)
    tv.column(1, width=70, anchor=CENTER)
    tv.pack(side=LEFT, anchor=NE, fill=BOTH, expand=True)

    # text widget

    sb = ttk.Scrollbar(
        master=ttframe, orient=VERTICAL, bootstyle=(DANGER, ROUND)
    )
    sb.set(0.1, 0.9)
    #sb.pack(fill=X, pady=5, expand=YES)

    btn_group = ttk.Labelframe(master=rframe, text="Opções", padding=(10, 5))
    btn_group.pack(fill=X)

    menu = ttk.Menu(root)
    for i, t in enumerate(style.theme_names()):
        menu.add_radiobutton(label=t, value=i)

    default = ttk.Button(master=btn_group, text="solid button")
    default.pack(fill=BOTH, pady=2,expand=False)
    default.focus_set()

    return root

if __name__ == "__main__":

    app = ttk.Window("ttkbootstrap widget demo")

    bagel = setup_demo(app)
    bagel.pack(fill=BOTH, expand=YES)

    app.mainloop()
