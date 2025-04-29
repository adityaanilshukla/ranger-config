import os
from ranger.api.commands import Command
from ranger.core.loader import CommandLoader

class extract_here(Command):
    def execute(self):
        """ Extract selected .zip files to the current directory using 'unzip'. """
        cwd = self.fm.thisdir
        marked_files = tuple(cwd.get_selection())

        def refresh(_):
            cwd = self.fm.get_directory(original_path)
            cwd.load_content()

        if not marked_files:
            return

        one_file = marked_files[0]
        original_path = cwd.path

        self.fm.copy_buffer.clear()
        self.fm.cut_buffer = False

        for f in marked_files:
            if not f.path.lower().endswith('.zip'):
                self.fm.notify(f"Skipping non-zip file: {f.basename}", bad=True)
                continue

            descr = f"Extracting: {os.path.basename(f.path)}"
            obj = CommandLoader(
                args=["unzip", "-o", f.path, "-d", original_path],
                descr=descr,
                read=True
            )
            obj.signal_bind("after", refresh)
            self.fm.loader.add(obj)

# class compress(Command):
#     def execute(self):
#         """ Compress marked files into a zip archive using the 'zip' command. """
#         cwd = self.fm.thisdir
#         marked_files = cwd.get_selection()
#
#         if not marked_files:
#             self.fm.notify("No files selected for compression", bad=True)
#             return
#
#         # Get output archive name from the command line, default to 'archive.zip'
#         parts = self.line.strip().split()
#         if len(parts) < 2:
#             self.fm.notify("Usage: :compress <output.zip>", bad=True)
#             return
#
#         archive_name = parts[1]
#         if not archive_name.lower().endswith(".zip"):
#             archive_name += ".zip"
#
#         rel_paths = [os.path.relpath(f.path, cwd.path) for f in marked_files]
#
#         descr = f"Compressing to: {archive_name}"
#         obj = CommandLoader(
#             args=["zip", "-r", archive_name] + rel_paths,
#             descr=descr,
#             read=True
#         )
#
#         def refresh(_):
#             cwd = self.fm.get_directory(cwd.path)
#             cwd.load_content()
#
#         obj.signal_bind("after", refresh)
#         self.fm.loader.add(obj)
#
#     def tab(self, tabnum):
#         """ Auto-complete with current folder name + .zip """
#         return [f"compress {os.path.basename(self.fm.thisdir.path)}.zip"]
