"""Entry point: `savegame-editor` console script and `python -m savegame_editor`."""
from __future__ import annotations

import sys

from loguru import logger

from savegame_editor.app import SaveEditorApp
from savegame_editor.config.settings import load_settings


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    settings = load_settings()
    logger.remove()
    logger.add(
        settings.log_path,
        level=settings.log_level,
        rotation="5 MB",
        retention=3,
        enqueue=True,
    )
    logger.info("savegame-editor-gui {} booting", __import__("savegame_editor").__version__)
    app = SaveEditorApp(settings)
    return app.run(argv)


if __name__ == "__main__":
    raise SystemExit(main())