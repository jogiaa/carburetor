from pathlib import Path
from typing import Optional, Callable, Generator, List
from dataclasses import dataclass
import fnmatch


# --- Sealed Class Equivalents ---
class FileResult: pass


@dataclass
class FileDetails(FileResult):
    path: str
    size: int
    content: str


@dataclass
class FileError(FileResult):
    path: str
    error: Exception


class AnotherFileProcessor:
    def __init__(
            self,
            source_str: str,
            dest_str: Optional[str] = None,
            file_filter: Optional[List[str]] = None,
            ignored_directories: Optional[List[str]] = None,
            overwrite: bool = True
    ):
        self.source = Path(source_str).resolve()
        self.destination = Path(dest_str).resolve() if dest_str else None
        self.file_filter = file_filter if file_filter is not None else ["*.sh", "*.gradle", "temp/*", "*~" , "*.DS_Store"]
        self.ignored_directories = ignored_directories if ignored_directories is not None else ["venv", "test", ".git"]
        self.overwrite = overwrite

    def _is_ignored(self, path: Path) -> bool:
        rel_path = str(path.relative_to(self.source)) if self.source.is_dir() else str(path.name)
        return any(fnmatch.fnmatch(rel_path, pattern) for pattern in self.file_filter)

    def stream_files(self) -> Generator[FileResult, None, None]:
        print(f"🗃️ Scanning:")
        if self.source.is_file():
            print(f"👀 Scanning: {self.source}")
            if not self._is_ignored(self.source):
                yield self._read_file(self.source)
            else:
                print(f"🙈 Ignoring: {self.source}")
        elif self.source.is_dir():
            for file in self.source.rglob("*"):
                print(f"👀 Scanning: {file}")
                if file.is_file():
                    if self._is_ignored(file):
                        print(f"🙈 Ignoring: {file}")
                        continue
                    else:
                        print(f"🚶🏽 Going to read: {file}")
                        yield self._read_file(file)
        else:
            yield FileError(path=str(self.source.absolute()), error=FileNotFoundError(f"Source <<not>> found"))

    def _read_file(self, file: Path) -> FileResult:
        print(f"📖 Reading: {file}")
        try:
            content = file.read_text(encoding='utf-8')
            return FileDetails(path=str(file), size=file.stat().st_size, content=content)
        except Exception as e:
            return FileError(path=str(file), error=e)

    def save_file(self, result: FileDetails) -> FileResult:
        print(f"📝 Saving: {result.path}")
        try:
            src_path = Path(result.path)

            if self.destination:
                if self.source.is_file():
                    if self.destination.is_dir():
                        target = self.destination / src_path.name
                    else:
                        target = self.destination
                else:
                    relative = src_path.relative_to(self.source)
                    target = self.destination / relative
            else:
                target = src_path  # Overwrite in place

            if target.exists() and not self.overwrite:
                print(f"⚠️ Skipped (exists): {target}")
                return FileResult()

            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(result.content, encoding='utf-8')
            return FileResult()
        except Exception as e:
            return FileError(path=str("target"), error=e)


def main():
    source = "koin/examples/coffee-maker/src/main/kotlin/org/koin/example"
    destination = "koin/examples/coffee-maker-two/src/main/kotlin/org/koin/example"

    processor = AnotherFileProcessor(
        source_str=source,
        dest_str=destination,
        overwrite=True
    )

    for file in processor.stream_files():
        if isinstance(file, FileDetails):
            print(f"📄 Processing: {file.path}")
            file.content = file.content.upper()
            result = processor.save_file(file)
            if isinstance(result, FileError):
                print(f"❌ Save failed: {result}")
        elif isinstance(file, FileError):
            print(f"❌ Read failed: {file}")


if __name__ == "__main__":
    main()
