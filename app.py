"""BeamCheck Pro desktop interface."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from beam import Analysis, CANTILEVER, Design, SECTIONS, SIMPLE
from design_io import open_design, save_design
from exports import export_csv


NAVY = "#173655"
COLORS = ("#205991", "#177b75", "#b54d15")
PLOTS = (("Shear", "kips"), ("Bending moment", "kip-ft"), ("Deflection", "in"))


def fmt(value):
    return f"{value:.2f}".rstrip("0").rstrip(".") if abs(value) >= .005 else "0"


def peaks(analysis):
    return analysis.shear, analysis.moment, analysis.maximum_deflection


def support_text(analysis):
    text = f"Left reaction {fmt(analysis.left)} kips"
    if analysis.design.support == SIMPLE:
        return f"{text}   |   Right reaction {fmt(analysis.right)} kips"
    return f"{text}   |   Fixed-end moment {fmt(analysis.fixed)} kip-ft"


def load_labels(design):
    return [
        *(f"P{i}   {fmt(p)} kips at {fmt(x)} ft" for i, (p, x) in enumerate(design.points, 1)),
        *(f"U{i}   {fmt(q)} kip/ft from {fmt(a)} to {fmt(b)} ft"
          for i, (q, a, b) in enumerate(design.uniforms, 1)),
    ] or ["No applied loads."]


def check_text(name, check, unit):
    return (f"{name}  {check.status}    {fmt(check.actual)} / {fmt(check.allowable)} {unit}\n"
            f"{fmt(check.utilization)}% used   |   {fmt(check.margin)} {unit} remaining")


def draw_beam(axis, analysis):
    design = analysis.design
    span = design.span
    axis.set_title(support_text(analysis), loc="left", fontsize=9, color=NAVY)
    axis.plot([0, span], [0, 0], color=NAVY, lw=4)
    if design.support == SIMPLE:
        axis.scatter([0, span], [-0.17, -0.17], marker="^", s=100, color=NAVY)
    else:
        axis.plot([0, 0], [-.34, .24], color=NAVY, lw=6)
    for index, (_, start, end) in enumerate(design.uniforms):
        height = .45 + index * .14
        axis.plot([start, end], [height, height], color=COLORS[1], lw=1)
        for x in np.linspace(start, end, 6):
            axis.annotate("", (x, 0), (x, height),
                          arrowprops={"arrowstyle": "->", "color": COLORS[1], "lw": .8})
        axis.text((start + end) / 2, height + .02, f"U{index + 1}",
                  ha="center", fontsize=8, color=COLORS[1])
    for index, (_, x) in enumerate(design.points):
        height = .65 + index * .13
        axis.annotate(f"P{index + 1}", (x, 0), (x, height), ha="center", fontsize=8,
                      color=COLORS[0], arrowprops={"arrowstyle": "->", "color": COLORS[0]})
    axis.set_xlim(-.06 * span, 1.06 * span)
    axis.set_ylim(-.46, max(.95, .78 + .14 * max(len(design.points), len(design.uniforms))))
    axis.set_xlabel(f"{fmt(span)} ft span", fontsize=8)
    axis.set_yticks([])
    axis.set_xticks([])
    for spine in axis.spines.values():
        spine.set_visible(False)


def draw_diagrams(axes, analysis):
    rows = np.asarray(list(analysis.rows()))
    for i, (axis, (name, unit), color, peak) in enumerate(zip(axes, PLOTS, COLORS, peaks(analysis))):
        location = "N/A" if peak.x is None else f"{fmt(peak.x)} ft"
        axis.set_title(f"{name}   |   Max abs. {fmt(abs(peak.value))} {unit} at {location}",
                       loc="left", fontsize=9, color=NAVY)
        axis.plot(rows[:, 0], rows[:, i + 1], color=color, lw=1.7)
        axis.fill_between(rows[:, 0], 0, rows[:, i + 1], color=color, alpha=.12)
        axis.axhline(0, color="#788798", lw=.6)
        axis.set_xlim(0, analysis.design.span)
        axis.set_ylabel(unit, fontsize=8)
        axis.tick_params(labelsize=8)
        axis.grid(alpha=.20)
        if i == 2:
            axis.invert_yaxis()
    axes[-1].set_xlabel("Distance from left end (ft)", fontsize=8)


def scroll_panel(parent):
    frame = ttk.Frame(parent)
    canvas = tk.Canvas(frame, highlightthickness=0, background="#ffffff")
    scrollbar = ttk.Scrollbar(frame, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    contents = ttk.Frame(canvas, padding=14)
    window = canvas.create_window(0, 0, anchor="nw", window=contents)
    contents.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window, width=event.width))
    return frame, contents


class BeamApp:
    def __init__(self, root):
        self.root = root
        root.title("BeamCheck Pro")
        root.geometry("1180x850")
        root.minsize(880, 580)
        menu = tk.Menu(root)
        self.file_menu = tk.Menu(menu, tearoff=False)
        self.file_menu.add_command(label="Open…", command=self.open_file)
        self.file_menu.add_command(label="Save…", command=self.save_file)
        menu.add_cascade(label="File", menu=self.file_menu)
        root.configure(menu=menu)
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", foreground=NAVY)
        style.configure("TButton", padding=5)
        style.configure("Primary.TButton", background=NAVY, foreground="white")
        style.map("Primary.TButton", background=[("active", "#28557d"), ("disabled", "#687984")])

        header = tk.Label(root, text="BeamCheck Pro", anchor="w", padx=20, pady=13,
                          bg=NAVY, fg="white", font=("Segoe UI", 19, "bold"))
        header.pack(fill="x")
        panes = ttk.Panedwindow(root, orient="horizontal")
        panes.pack(fill="both", expand=True)
        controls, self.controls = scroll_panel(panes)
        results, self.results = scroll_panel(panes)
        panes.add(controls, weight=1)
        panes.add(results, weight=3)
        root.after_idle(lambda: panes.sashpos(0, 385))
        self.variables = {key: tk.StringVar() for key in ("support", "span", "material", "section", "limit")}
        self.load_rows = {"points": [], "uniforms": []}
        self.pending = None
        self.analysis = None
        self.drag = None

        ttk.Label(self.controls, text="Beam settings", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        self.choice("Support", "support", (SIMPLE, CANTILEVER))
        span_row = ttk.Frame(self.controls)
        span_row.pack(fill="x", pady=4)
        ttk.Label(span_row, text="Span (ft)").pack(side="left")
        ttk.Entry(span_row, textvariable=self.variables["span"], width=8).pack(side="right")
        self.scale = ttk.Scale(self.controls, from_=4, to=40, command=self.scale_changed)
        self.scale.pack(fill="x")
        self.choice("Material", "material", tuple(SECTIONS)).bind("<<ComboboxSelected>>", self.material_changed)
        self.section_box = self.choice("Section", "section", ())
        self.choice("Deflection limit", "limit", ("L/240", "L/360"))
        self.load_groups = {}
        self.add_buttons = {}
        for key, label in (("points", "Point loads"), ("uniforms", "Uniform loads")):
            ttk.Label(self.controls, text=label, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(14, 2))
            self.load_groups[key] = ttk.Frame(self.controls)
            self.load_groups[key].pack(fill="x")
            button = ttk.Button(self.controls, text=f"Add {label[:-1].lower()}", style="Primary.TButton",
                                command=lambda group=key: self.add_default(group))
            button.pack(anchor="w", pady=4)
            self.add_buttons[key] = button
        ttk.Button(self.controls, text="Reset Example", command=lambda: self.populate(Design())).pack(anchor="w", pady=14)
        self.error = ttk.Label(self.controls, foreground="#a22a31", wraplength=315)
        self.error.pack(fill="x")

        self.status = ttk.Label(self.results, font=("Segoe UI", 14, "bold"))
        self.status.pack(anchor="w")
        cards = ttk.Frame(self.results)
        cards.pack(fill="x", pady=8)
        self.check_labels = [ttk.Label(cards, padding=8, font=("Segoe UI", 10)) for _ in range(2)]
        for label in self.check_labels:
            label.pack(side="left", fill="both", expand=True)
        self.recommendation = ttk.Label(self.results, wraplength=620, justify="left")
        self.recommendation.pack(anchor="w")
        self.apply_button = ttk.Button(self.results, text="Apply Recommendation", style="Primary.TButton",
                                       command=self.apply_recommendation)
        self.apply_button.pack(anchor="w", pady=6)
        self.export_buttons = ttk.Frame(self.results)
        self.export_buttons.pack(anchor="w")
        self.csv_button = ttk.Button(self.export_buttons, text="Export CSV",
                                     command=lambda: self.export_file("CSV results", ".csv", export_csv))
        self.csv_button.pack(side="left", padx=(0, 6))
        self.load_summary = ttk.Label(self.results, justify="left")
        self.load_summary.pack(anchor="w", pady=4)
        self.hover = ttk.Label(self.results, text="Hover over a diagram to inspect values.")
        self.hover.pack(anchor="w", pady=4)
        self.figure = Figure(figsize=(6.6, 7), dpi=100, layout="constrained")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.results)
        self.canvas.get_tk_widget().pack(fill="x")
        self.canvas.mpl_connect("motion_notify_event", self.cursor_move)
        self.canvas.mpl_connect("button_press_event", self.drag_start)
        self.canvas.mpl_connect("button_release_event", self.drag_end)
        self.canvas.mpl_connect("figure_leave_event", lambda event: self.clear_hover())
        for variable in self.variables.values():
            variable.trace_add("write", self.schedule)
        self.populate(Design())
        self.refresh()

    def choice(self, label, key, options):
        row = ttk.Frame(self.controls)
        row.pack(fill="x", pady=4)
        ttk.Label(row, text=label).pack(side="left")
        box = ttk.Combobox(row, textvariable=self.variables[key], values=options, state="readonly", width=23)
        box.pack(side="right")
        return box

    def open_file(self):
        path = filedialog.askopenfilename(parent=self.root, filetypes=[("Beam design", "*.json")])
        if path:
            try:
                design = open_design(path)
            except (OSError, ValueError, ArithmeticError, np.linalg.LinAlgError) as error:
                messagebox.showerror("Could not open design", str(error), parent=self.root)
                return
            self.populate(design)
            self.refresh()

    def current_results(self):
        if self.pending is not None:
            self.refresh()
        if self.analysis is None:
            messagebox.showerror("Results unavailable", "Correct the highlighted input before continuing.",
                                 parent=self.root)
        return self.analysis

    def save_file(self):
        analysis = self.current_results()
        if analysis is None:
            return
        path = filedialog.asksaveasfilename(parent=self.root, defaultextension=".json",
                                           filetypes=[("Beam design", "*.json")])
        if path:
            try:
                save_design(path, analysis)
            except (OSError, ValueError) as error:
                messagebox.showerror("Could not save design", str(error), parent=self.root)

    def export_file(self, label, extension, writer):
        analysis = self.current_results()
        if analysis is None:
            return
        path = filedialog.asksaveasfilename(parent=self.root, defaultextension=extension,
                                           filetypes=[(label, f"*{extension}")])
        if path:
            try:
                writer(path, analysis)
            except (OSError, ValueError) as error:
                messagebox.showerror(f"Could not export {label}", str(error), parent=self.root)

    def scale_changed(self, value):
        if not getattr(self, "syncing_scale", False):
            self.variables["span"].set(str(round(float(value) * 4) / 4))

    def material_changed(self, event=None):
        options = [item.name for item in SECTIONS[self.variables["material"].get()]]
        self.section_box.configure(values=options)
        self.variables["section"].set(options[0])

    def populate(self, design):
        for key in self.variables:
            value = getattr(design, key)
            self.variables[key].set(f"L/{value}" if key == "limit" else str(value))
        self.section_box.configure(values=[section.name for section in SECTIONS[design.material]])
        for key, rows in self.load_rows.items():
            for frame, _ in rows:
                frame.destroy()
            rows.clear()
            for values in getattr(design, key):
                self.add_row(key, values)
            self.update_add_button(key)
        self.schedule()

    def add_default(self, key):
        try:
            span = float(self.variables["span"].get())
        except ValueError:
            span = 20
        self.add_row(key, (10, span / 2) if key == "points" else (1, 0, span))

    def add_row(self, key, values):
        frame = ttk.Frame(self.load_groups[key])
        frame.pack(fill="x", pady=4)
        labels = ("kips", "At (ft)") if key == "points" else ("kip/ft", "Start (ft)", "End (ft)")
        variables = []
        for name, value in zip(labels, values):
            field = ttk.Frame(frame)
            field.pack(side="left", fill="x", expand=True)
            ttk.Label(field, text=name).pack(anchor="w")
            variable = tk.StringVar(value=str(value))
            ttk.Entry(field, textvariable=variable, width=7).pack(anchor="w")
            variable.trace_add("write", self.schedule)
            variables.append(variable)
        item = (frame, variables)
        self.load_rows[key].append(item)
        ttk.Button(frame, text="Remove", command=lambda: self.remove_row(key, item)).pack(side="right", anchor="s")
        self.update_add_button(key)
        self.schedule()

    def remove_row(self, key, item):
        self.load_rows[key].remove(item)
        item[0].destroy()
        self.update_add_button(key)
        self.schedule()

    def update_add_button(self, key):
        self.add_buttons[key].configure(state="disabled" if len(self.load_rows[key]) >= 10 else "normal")

    def read_design(self):
        entries = {key: variable.get() for key, variable in self.variables.items()}
        entries["limit"] = entries["limit"].removeprefix("L/")
        for key, rows in self.load_rows.items():
            entries[key] = tuple(tuple(variable.get() for variable in variables) for _, variables in rows)
        return Design(**entries)

    def schedule(self, *args):
        if self.pending is not None:
            self.root.after_cancel(self.pending)
        self.pending = self.root.after(110, self.refresh)

    def refresh(self):
        if self.pending is not None:
            self.root.after_cancel(self.pending)
            self.pending = None
        self.figure.clear()
        self.guides = []
        self.diagram_axes = []
        self.beam_axis = None
        try:
            self.analysis = analysis = Analysis(self.read_design())
        except (ValueError, ArithmeticError, np.linalg.LinAlgError) as error:
            self.analysis = None
            message = str(error) if isinstance(error, ValueError) else "The loads produced a numerical overflow."
            self.error.configure(text=message)
            self.status.configure(text="Results unavailable", foreground="#a22a31")
            for label in [*self.check_labels, self.recommendation, self.load_summary, self.hover]:
                label.configure(text="")
            self.apply_button.configure(state="disabled")
            self.canvas.draw_idle()
            return

        self.error.configure(text="")
        self.syncing_scale = True
        self.scale.set(analysis.design.span)
        self.syncing_scale = False
        checks = (analysis.bending, analysis.deflection)
        failed = [name for name, check in zip(("bending", "deflection"), checks) if check.status == "FAIL"]
        summary = f"FAIL · {' and '.join(failed).capitalize()} exceeds the limit" if failed else "PASS · Both checks within limits"
        self.status.configure(text=summary, foreground="#a22a31" if failed else "#216346")
        for label, name, unit, check in zip(self.check_labels, ("Bending", "Deflection"), ("ksi", "in"), checks):
            color = "#216346" if check.utilization < 70 else "#79530d" if check.utilization <= 100 else "#a22a31"
            label.configure(text=check_text(name, check, unit), foreground=color)
        section = analysis.recommendation
        recommendation = "No listed beam passes"
        if section:
            bending, deflection = analysis.checks(section)
            weight = f" · {section.weight} lb/ft" if section.weight else ""
            recommendation = (f"Recommended: {section.name}{weight}   |   "
                              f"{fmt(bending.actual)} ksi bending   |   {fmt(deflection.actual)} in deflection")
        self.recommendation.configure(text=recommendation)
        self.apply_button.configure(state="normal" if section else "disabled")
        self.load_summary.configure(text="\n".join(load_labels(analysis.design)))
        self.clear_hover()
        axes = self.figure.subplots(4, 1, gridspec_kw={"height_ratios": [1.05, 1, 1, 1]})
        self.beam_axis, *self.diagram_axes = axes
        draw_beam(self.beam_axis, analysis)
        draw_diagrams(self.diagram_axes, analysis)
        self.guides = [axis.axvline(0, color="#56677b", lw=.8, visible=False) for axis in self.diagram_axes]
        self.canvas.draw_idle()

    def apply_recommendation(self):
        if self.analysis and self.analysis.recommendation:
            self.variables["section"].set(self.analysis.recommendation.name)

    def drag_start(self, event):
        if not self.analysis or event.inaxes is not self.beam_axis or event.xdata is None:
            return
        positions = self.analysis.design.points
        if positions:
            index = min(range(len(positions)), key=lambda i: abs(positions[i][1] - event.xdata))
            if abs(positions[index][1] - event.xdata) <= self.analysis.design.span * .04:
                self.drag = self.load_rows["points"][index][1][1]

    def drag_end(self, event):
        self.drag = None

    def cursor_move(self, event):
        if not self.analysis or event.xdata is None:
            self.clear_hover()
            return
        if self.drag is not None and event.inaxes is self.beam_axis:
            x = max(0, min(self.analysis.design.span, round(event.xdata * 4) / 4))
            self.drag.set(str(x))
            return
        if event.inaxes not in self.diagram_axes:
            self.clear_hover()
            return
        x = event.xdata
        span = self.analysis.design.span
        points = [position for _, position in self.analysis.design.points
                  if 0 < position < span and abs(position - x) < span / 100]
        if points:
            x = min(points, key=lambda position: abs(position - x))
        shear, moment, deflection = self.analysis.sample(x)
        shear_text = fmt(shear)
        if points:
            shear_text = f"{fmt(self.analysis.sample(x, 'left')[0])} → {shear_text}"
        self.hover.configure(text=f"{fmt(x)} ft   |   V {shear_text} kips   |   M {fmt(moment)} kip-ft   |   y {fmt(deflection)} in")
        for guide in self.guides:
            guide.set_xdata([x, x])
            guide.set_visible(True)
        self.canvas.draw_idle()

    def clear_hover(self):
        self.hover.configure(text="Hover over a diagram to inspect values." if self.analysis else "")
        if any(guide.get_visible() for guide in self.guides):
            for guide in self.guides:
                guide.set_visible(False)
            self.canvas.draw_idle()


if __name__ == "__main__":
    window = tk.Tk()
    BeamApp(window)
    window.mainloop()
