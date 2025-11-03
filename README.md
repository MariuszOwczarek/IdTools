
```markdown
# 🆔 idtool — Hexagonal ID Generator

CLI tool for generating and storing unique identifiers (`UUID4`, `KSUID`, `ULID`, `SHA256`)  
with clean, hexagonal architecture — ports, adapters, and application services.

---

## 🚀 Features

- ✅ Generate IDs using one of four providers:
  - `uuid4`
  - `ksuid`
  - `ulid`
  - `sha256`
- 💾 Store results in:
  - JSONL file (`ids.jsonl`)
  - SQLite database (`ids.db`)
- 🎨 Beautiful CLI output (via [Rich](https://github.com/Textualize/rich))
- ⚙️ Configurable via command-line options
- 🧱 Clean, layered structure — domain, application, adapters, entrypoints

---

## 🧩 Project Structure

```

idtool/
├─ pyproject.toml
├─ README.md
├─ idtool/
│  ├─ domain/          # Ports, Entities, Enums, Errors (core domain)
│  ├─ application/     # Use-cases (Generate / List IDs) + Services (composition)
│  ├─ adapters/        # Implementations: providers & repositories
│  ├─ entrypoints/     # Typer CLI commands and Rich output
│  └─ config/          # Default paths and settings
└─ tests/              # Unit and end-to-end tests

````

This structure follows a **hexagonal (ports & adapters)** pattern:
- Domain defines contracts (`ports`).
- Adapters implement them (JSONL, SQLite, UUID, ULID...).
- Application orchestrates use-cases.
- Entrypoints expose CLI commands.

---

## 🛠️ Installation

### Option 1 — Local (recommended for development)

```bash
git clone https://github.com/yourusername/idtool.git
cd idtool
pip install -e .
````

After installation, the command `idtool` will be available globally.

### Option 2 — Manual

```bash
python -m idtool.entrypoints.cli
```

---

## 🧮 Usage

### Generate IDs

```bash
idtool gen --provider uuid4 --repo jsonl --count 5
```

**Options:**

| Flag            | Description                                      | Default |
| --------------- | ------------------------------------------------ | ------- |
| `--provider`    | ID provider (`uuid4`, `ksuid`, `sha256`, `ulid`) | `uuid4` |
| `--repo`        | Storage backend (`jsonl`, `sqlite`)              | `jsonl` |
| `--count`, `-n` | How many IDs to generate                         | `1`     |
| `--no-color`    | Disable colored output                           | `false` |

### List IDs

```bash
idtool list --repo jsonl --limit 10
```

Shows last saved IDs in a rich table.

---

## 🧠 Example Output

```
╔════════════════════════════════════╗
║           ID List                  ║
╚════════════════════════════════════╝
Generated 5 ID(s)
Provider: uuid4
Id: 3f92dbf8-cf04-4c3a-9d53-38b934c3d292

Saved 5 record(s) to ids.jsonl
```

---

## 🧱 Architecture Overview

| Layer           | Responsibility                 | Example                               |
| --------------- | ------------------------------ | ------------------------------------- |
| **Domain**      | Core business logic, contracts | `IdProvider`, `IdRepository`          |
| **Application** | Use-cases, coordination        | `generate_ids`, `list_ids`            |
| **Adapters**    | Implementations of ports       | `JsonlIdRepository`, `UUIDIdProvider` |
| **Entrypoints** | User-facing interfaces         | Typer CLI commands                    |
| **Config**      | Paths, settings                | `config/settings.py`                  |

The application layer never touches infrastructure or UI code —
only uses domain ports, making it easy to test and extend.

---

## 🧪 Running Tests

```bash
pytest
```

Unit tests cover:

* Providers and repositories
* Use-cases (with mocks)
* CLI (end-to-end, Rich output)

---

## 🧭 Roadmap

* [ ] Add `delete` and `export` commands
* [ ] Introduce configurable storage paths
* [ ] Add environment variable support (`.env`)
* [ ] Extend test coverage
* [ ] Package release on PyPI

---

## 📜 License

MIT © 2025 — created for educational and practical purposes.

---

## 🙌 Acknowledgements

* [Typer](https://typer.tiangolo.com) — elegant CLI framework
* [Rich](https://github.com/Textualize/rich) — rich terminal output
* [SQLAlchemy](https://www.sqlalchemy.org) — SQLite support
* [ulid-py](https://pypi.org/project/ulid-py/) & [python-ksuid](https://pypi.org/project/python-ksuid/) — unique ID generation
```