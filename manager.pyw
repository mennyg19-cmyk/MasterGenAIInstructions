# === What's in this file ===
# GUI manager for MasterGenAIInstructions.
#
# launch()              -- Entry point, builds and shows the main window
# BootstrapFrame        -- Tab for creating new projects
# ApplyFrame            -- Tab for applying rules to existing projects
# UpdateFrame           -- Tab for pushing updates to all registered projects
# RegistryFrame         -- Tab for viewing/managing the project registry
#
# Uses tkinter (built into Python). No external dependencies.
# Double-click this file on Windows to run without a console window (.pyw extension).

import json
import os
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TEMPLATE_DIR = SCRIPT_DIR / "template"
REGISTRY_FILE = SCRIPT_DIR / "registry.json"


def load_registry():
    if REGISTRY_FILE.exists():
        try:
            data = json.loads(REGISTRY_FILE.read_text())
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, ValueError):
            return []
    return []


def save_registry(registry):
    REGISTRY_FILE.write_text(json.dumps(registry, indent=2))


def register_project(path):
    registry = load_registry()
    path_str = str(Path(path).resolve())
    if path_str not in registry:
        registry.append(path_str)
        save_registry(registry)
    return path_str


def copy_rules_to(target_dir):
    rules_dest = Path(target_dir) / ".cursor" / "rules"
    rules_dest.mkdir(parents=True, exist_ok=True)
    rules_src = TEMPLATE_DIR / ".cursor" / "rules"
    copied = 0
    for f in rules_src.iterdir():
        if f.is_file():
            shutil.copy2(f, rules_dest / f.name)
            copied += 1
    shutil.copy2(TEMPLATE_DIR / "AGENTS.md", Path(target_dir) / "AGENTS.md")
    return copied


def copy_supporting_if_missing(target_dir):
    results = []
    for filename in ["DECISION-LOG.md", "TESTING-STRATEGY.md", "HANDOFF.md"]:
        dest = Path(target_dir) / filename
        if not dest.exists():
            shutil.copy2(TEMPLATE_DIR / filename, dest)
            results.append(f"  [created]  {filename}")
        else:
            results.append(f"  [skipped]  {filename} (already exists)")
    return results


class BootstrapFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Create a New Project", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 15))

        form = ttk.Frame(self)
        form.pack(fill="x")

        ttk.Label(form, text="Project name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var, width=50).grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)

        ttk.Label(form, text="Description:").grid(row=1, column=0, sticky="w", pady=5)
        self.desc_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.desc_var, width=50).grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)

        ttk.Label(form, text="Destination:").grid(row=2, column=0, sticky="w", pady=5)
        dest_frame = ttk.Frame(form)
        dest_frame.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=5)
        self.dest_var = tk.StringVar()
        ttk.Entry(dest_frame, textvariable=self.dest_var, width=40).pack(side="left", fill="x", expand=True)
        ttk.Button(dest_frame, text="Browse...", command=self.browse_dest).pack(side="left", padx=(5, 0))

        self.github_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form, text="Create private GitHub repo", variable=self.github_var).grid(row=3, column=1, sticky="w", padx=(10, 0), pady=5)

        form.columnconfigure(1, weight=1)

        ttk.Button(self, text="Create Project", command=self.create, style="Accent.TButton").pack(anchor="w", pady=(20, 10))

        self.output = scrolledtext.ScrolledText(self, height=12, state="disabled", font=("Consolas", 9))
        self.output.pack(fill="both", expand=True, pady=(10, 0))

    def browse_dest(self):
        d = filedialog.askdirectory(title="Choose parent directory")
        if d and self.name_var.get():
            self.dest_var.set(os.path.join(d, self.name_var.get()))
        elif d:
            self.dest_var.set(d)

    def log(self, msg):
        self.output.configure(state="normal")
        self.output.insert("end", msg + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")
        self.update_idletasks()

    def create(self):
        name = self.name_var.get().strip()
        desc = self.desc_var.get().strip()
        dest = self.dest_var.get().strip()

        if not name:
            messagebox.showerror("Error", "Project name is required.")
            return
        if not dest:
            dest = str(Path.cwd() / name)
            self.dest_var.set(dest)
        if Path(dest).exists():
            messagebox.showerror("Error", f"Destination already exists:\n{dest}")
            return

        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

        self.log(f"Creating project: {name}")
        self.log(f"Destination: {dest}")
        self.log("")

        shutil.copytree(str(TEMPLATE_DIR), dest)
        self.log("[copied] Template files")

        for md_file in Path(dest).rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            content = content.replace("{{PROJECT_NAME}}", name).replace("{{DESCRIPTION}}", desc)
            md_file.write_text(content, encoding="utf-8")
        for mdc_file in Path(dest).rglob("*.mdc"):
            content = mdc_file.read_text(encoding="utf-8")
            content = content.replace("{{PROJECT_NAME}}", name).replace("{{DESCRIPTION}}", desc)
            mdc_file.write_text(content, encoding="utf-8")
        self.log("[replaced] Placeholders")

        subprocess.run(["git", "init", "-b", "main"], cwd=dest, capture_output=True)
        subprocess.run(["git", "add", "-A"], cwd=dest, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial project scaffold from MasterGenAIInstructions"], cwd=dest, capture_output=True)
        self.log("[git] Initialized and committed")

        if self.github_var.get():
            result = subprocess.run(["gh", "repo", "create", name, "--private", "--source", ".", "--push"],
                                    cwd=dest, capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"[github] Private repo created and pushed")
            else:
                self.log(f"[github] Failed: {result.stderr.strip()}")

        register_project(dest)
        self.log("[registered] Added to registry")
        self.log("")
        self.log(f"Done! Open {dest} in Cursor.")


class ApplyFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Apply Rules to Existing Project", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 15))

        path_frame = ttk.Frame(self)
        path_frame.pack(fill="x")
        ttk.Label(path_frame, text="Project path:").pack(side="left")
        self.path_var = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.path_var, width=50).pack(side="left", fill="x", expand=True, padx=(10, 5))
        ttk.Button(path_frame, text="Browse...", command=self.browse).pack(side="left")

        ttk.Button(self, text="Apply Rules", command=self.apply, style="Accent.TButton").pack(anchor="w", pady=(20, 10))

        self.output = scrolledtext.ScrolledText(self, height=15, state="disabled", font=("Consolas", 9))
        self.output.pack(fill="both", expand=True, pady=(10, 0))

    def browse(self):
        d = filedialog.askdirectory(title="Choose existing project")
        if d:
            self.path_var.set(d)

    def log(self, msg):
        self.output.configure(state="normal")
        self.output.insert("end", msg + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")
        self.update_idletasks()

    def apply(self):
        target = self.path_var.get().strip()
        if not target or not Path(target).exists():
            messagebox.showerror("Error", "Directory does not exist.")
            return

        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

        self.log(f"Applying rules to: {target}")
        self.log("")

        count = copy_rules_to(target)
        self.log(f"  [copied]   .cursor/rules/ ({count} rule files)")
        self.log(f"  [copied]   AGENTS.md")

        for line in copy_supporting_if_missing(target):
            self.log(line)

        self.log("  [skipped]  README.md (not overwriting)")
        self.log("  [skipped]  .gitignore (not overwriting)")

        register_project(target)
        self.log("  [registered] Added to registry")
        self.log("")
        self.log("Done!")


class UpdateFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Update All Registered Projects", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 15))

        ttk.Label(self, text="Copies the latest .cursor/rules/ and AGENTS.md to every registered project.",
                  wraplength=500, justify="left").pack(anchor="w", pady=(0, 10))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(anchor="w", pady=(0, 10))
        ttk.Button(btn_frame, text="Update All", command=self.update_all, style="Accent.TButton").pack(side="left")
        self.commit_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(btn_frame, text="Also commit changes in each project", variable=self.commit_var).pack(side="left", padx=(15, 0))

        self.output = scrolledtext.ScrolledText(self, height=15, state="disabled", font=("Consolas", 9))
        self.output.pack(fill="both", expand=True, pady=(10, 0))

    def log(self, msg):
        self.output.configure(state="normal")
        self.output.insert("end", msg + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")
        self.update_idletasks()

    def update_all(self):
        registry = load_registry()
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

        if not registry:
            self.log("Registry is empty. Nothing to update.")
            return

        self.log(f"Updating {len(registry)} project(s)...")
        self.log("")

        updated = []
        missing = []

        for project_path in registry:
            if not Path(project_path).exists():
                self.log(f"  [missing]  {project_path}")
                missing.append(project_path)
                continue

            count = copy_rules_to(project_path)
            self.log(f"  [updated]  {project_path} ({count} rules)")
            updated.append(project_path)

        if missing:
            cleaned = [p for p in registry if p not in missing]
            save_registry(cleaned)
            self.log(f"\n  Removed {len(missing)} missing project(s) from registry.")

        if self.commit_var.get() and updated:
            self.log("")
            for project_path in updated:
                result = subprocess.run(["git", "status", "--porcelain"], cwd=project_path, capture_output=True, text=True)
                if result.stdout.strip():
                    subprocess.run(["git", "add", ".cursor/rules/", "AGENTS.md"], cwd=project_path, capture_output=True)
                    subprocess.run(["git", "commit", "-m", "Update rules from MasterGenAIInstructions"],
                                   cwd=project_path, capture_output=True)
                    subprocess.run(["git", "push"], cwd=project_path, capture_output=True)
                    self.log(f"  [committed] {project_path}")
                else:
                    self.log(f"  [no changes] {project_path}")

        self.log(f"\nDone! Updated {len(updated)} project(s).")


class RegistryFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Registered Projects", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 15))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(0, 10))
        ttk.Button(btn_frame, text="Add Project...", command=self.add_project).pack(side="left")
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_selected).pack(side="left", padx=(10, 0))
        ttk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side="left", padx=(10, 0))

        self.listbox = tk.Listbox(self, height=15, font=("Consolas", 9), selectmode="extended")
        self.listbox.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, "end")
        for path in load_registry():
            exists = "  " if Path(path).exists() else "  [MISSING] "
            self.listbox.insert("end", f"{exists}{path}")

    def add_project(self):
        d = filedialog.askdirectory(title="Choose a project folder to register")
        if d:
            registered = register_project(d)
            self.refresh()
            messagebox.showinfo("Added", f"Registered:\n{registered}")

    def remove_selected(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        registry = load_registry()
        to_remove = set()
        for idx in selected:
            text = self.listbox.get(idx).strip()
            if text.startswith("[MISSING]"):
                text = text.replace("[MISSING]", "").strip()
            to_remove.add(text)
        registry = [p for p in registry if p not in to_remove]
        save_registry(registry)
        self.refresh()


def launch():
    root = tk.Tk()
    root.title("MasterGenAIInstructions Manager")
    root.geometry("700x550")
    root.minsize(600, 450)

    try:
        root.tk.call("source", str(Path(__file__).parent / "azure.tcl"))
        root.tk.call("set_theme", "light")
    except tk.TclError:
        pass

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    notebook.add(BootstrapFrame(notebook), text="  New Project  ")
    notebook.add(ApplyFrame(notebook), text="  Apply to Existing  ")
    notebook.add(UpdateFrame(notebook), text="  Update All  ")
    notebook.add(RegistryFrame(notebook), text="  Registry  ")

    root.mainloop()


if __name__ == "__main__":
    launch()
