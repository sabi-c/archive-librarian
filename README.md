# archive-librarian

Download books from [archive.org](https://archive.org) as real PDFs — including the borrow-protected ones — so you can read them offline and keep them in your own library.

Built for macOS. Works on Linux too. Friendly first-run setup, secure credential storage, dead-simple to use.

---

## What this is

archive.org and openlibrary.org have an enormous collection of digitized books. Most of them are **borrow-protected**: you can read them in the browser for 1 hour or 14 days, but you can't download them as a PDF.

This tool downloads them as PDFs. Legally, in the sense that you have the same access via your archive.org account that the borrow flow grants you — this just produces a file you can keep instead of a 1-hour browser session.

You'll need a free [archive.org account](https://archive.org/account/signup) (takes 30 seconds).

---

## Install (one command)

```bash
cd archive-librarian
./install.sh
```

That script will:

1. Check you have Python 3.11 or newer
2. Set up an isolated Python environment for the tool
3. Install dependencies
4. Install a `librarian` command you can run from anywhere
5. Walk you through credentials and a test download

If `install.sh` says your install location isn't in your PATH, follow the on-screen instructions to add it to your shell config.

### If you don't have Python 3.11+

```bash
brew install python@3.13
```

(Install [Homebrew](https://brew.sh) first if needed.)

---

## How to use it

### Grab a book

1. Go to [archive.org](https://archive.org) and sign in
2. Find a book you want
3. Click **"Borrow for 1 hour"** on the book's page
4. Once it opens in the reader, copy the URL from your browser
5. In your terminal:

```bash
librarian download https://archive.org/details/SOMETHING
```

The PDF will land in your library folder (default: `~/Books/Archive`).

### Other commands

```bash
librarian status              # Check credentials and config
librarian list                # Show all downloaded books
librarian download URL [URL]  # Download one or more books
librarian setup               # Re-run the first-time setup walkthrough
librarian creds set           # Update your credentials
librarian creds delete        # Remove stored credentials
```

### Quality vs speed

Default is medium quality (resolution 3) — about 50–150 MB per book and 3–5 minutes to download. For best quality:

```bash
librarian download URL --resolution 0
```

Resolution 0 is best (200–500 MB, 10–15 minutes). Higher numbers are faster and lower quality.

---

## Where things live

- **Books** — `~/Books/Archive/` (configurable)
- **Catalog** — `~/Books/Archive/library.json` (auto-maintained)
- **Config** — `~/.archive-librarian/config.toml`
- **Credentials** — macOS Keychain (or `~/.archive-librarian/credentials` on Linux)

---

## How credentials are stored

On macOS, your password is stored in the system **Keychain** under the service name `archive.org`. It's encrypted at rest, the same way Safari and Mail store passwords. It's never written to a plaintext file or sent anywhere except to archive.org during login.

On Linux, the password lives in `~/.archive-librarian/credentials` with file permissions `0600` (only you can read it).

To change credentials: `librarian creds set`
To remove them: `librarian creds delete`

---

## Troubleshooting

**"Login failed" or "credentials wrong"** — Run `librarian setup` and re-enter. Make sure you can log in to archive.org in a browser with the same email/password.

**"librarian: command not found"** — The install script tried to put `librarian` in your PATH but might not have succeeded. Either fix your PATH (see install output) or run from the folder: `./librarian <command>`.

**"This book isn't borrowable"** — Some archive.org books require special accounts (academic, partner libraries, etc.). This tool handles standard borrow books and openly-downloadable books, but not those with extra restrictions.

**Download hangs partway** — archive.org sometimes throttles. Cancel (Ctrl-C) and retry. If it keeps happening, try lowering threads: edit `~/.archive-librarian/config.toml` and add `threads = 10`.

---

## Credits

The actual download protocol — the AES decryption flow that turns archive.org's protected book pages into real PDF pages — is from [MiniGlome's Archive.org-Downloader](https://github.com/MiniGlome/Archive.org-Downloader). That's the file `archive-org-downloader.py` in this folder; everything else is the wrapping (CLI, credential management, onboarding, library catalog).

---

## Removing it

```bash
rm -rf archive-librarian/
rm -rf ~/.archive-librarian/
librarian creds delete    # before removing the folder
sudo rm /usr/local/bin/librarian   # or ~/.local/bin/librarian
```

Books in `~/Books/Archive/` are yours and stay put.
