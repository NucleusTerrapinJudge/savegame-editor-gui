"""Application bootstrap — wires GUI, worker pool, and service container."""
from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from savegame_editor.config.settings import Settings
from savegame_editor.gui.main_window import MainWindow
from savegame_editor.services.editor_service import EditorService
from savegame_editor.utils.worker_pool import WorkerPool


class SaveEditorApp:
    """Owns the QApplication lifetime and the service graph."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def run(self, argv: list[str]) -> int:
        qt_app = QApplication(argv or ["savegame-editor"])
        qt_app.setApplicationName("savegame-editor-gui")
        qt_app.setOrganizationName("savegame-editor-gui")

        pool = WorkerPool(max_threads=self._settings.max_workers)
        service = EditorService(pool=pool, settings=self._settings)

        window = MainWindow(service=service)
        window.show()

        exit_code = qt_app.exec()
        pool.shutdown()
        return exit_code