# 📚 Archive Librarian

Download books from [archive.org](https://archive.org) as real PDFs you can keep on your computer — including the borrow-protected ones.

**v2.0 — Risograph Edition.** Native Mac window with a custom riso-print aesthetic. Zero terminal commands. Built so anyone can use it.

---

## 📥 Download

### 👉 [**Download Archive Librarian for Mac**](https://github.com/sabi-c/archive-librarian/releases/latest/download/Archive.Librarian.dmg)

(Apple Silicon Macs — M1, M2, M3, M4. For Intel see [bottom of this page](#intel-macs).)

---

## How to install (literally 30 seconds)

1. **Click the download link above.** A file called `Archive Librarian.dmg` lands in your Downloads folder.

2. **Double-click it.** A window opens showing the app and an Applications shortcut.

3. **Drag the Archive Librarian icon onto Applications.** Installed.

4. **Open Applications, find Archive Librarian, double-click it.**

   The first time you open it, macOS may pop up a warning saying *"cannot be opened because Apple cannot check it for malicious software."* This is normal for apps not sold through the App Store. To get past it:

   - **Right-click** (or two-finger click on a trackpad) on Archive Librarian in your Applications folder
   - Choose **Open** from the menu
   - Click **Open** in the dialog that appears

   You only have to do this once.

---

## What it looks like

A native Mac window in a custom riso-print aesthetic — deep blue ink on cream paper, halftone dot patterns, bold typography, editorial layout. Six screens covering the full flow:

| Screen | What it does |
|--------|-------------|
| **Welcome** | First-launch unboxing with five-step setup outline |
| **Login** | Email + password fields, live archive.org verification |
| **Dashboard** | Library counter, recent downloads, primary download action |
| **Downloading** | Live progress, the book itself rendered as a halftone cover |
| **Library** | Full browse, search, click any book to open in macOS Preview |
| **Settings** | Account, library folder, default quality, librarian behavior |

ARIA the librarian is the structural presence throughout — quiet, never chatty, surfaces only on milestones.

---

## Setup wizard (first launch)

1. **Already have a free archive.org account?** If not, the app opens the [signup page](https://archive.org/account/signup) for you.
2. **Enter your archive.org email and password.** Stored encrypted in macOS Keychain — never written to a plain file.
3. **Live verification** against archive.org confirms the credentials work.
4. **Pick where books save.** Default: `~/Books/Archive`.
5. **Done.** Dashboard appears.

---

## Daily use

Open Archive Librarian → click **Download Book** → paste an archive.org URL → wait a few minutes. Done. The book is in your library folder as a PDF.

To find a borrowable book: go to [archive.org](https://archive.org), sign in, search, click "Borrow for 1 hour" on any book, copy the URL from your browser, paste it in.

---

## How is my password stored?

In macOS **Keychain** — the same encrypted vault Safari uses. Never written to a plain file, never sent anywhere except archive.org during login. To remove it: open the app's Settings, click Delete next to credentials. Or run `librarian creds delete` in Terminal if you have the CLI.

---

## Troubleshooting

**"Login failed"** — Wrong password. Verify by signing in to archive.org in your browser, then re-enter via the app's Settings.

**"Cannot be opened because Apple cannot check it"** — Normal. Right-click → Open, one time. (Unsigned for distribution = unavoidable without paid Apple Developer ID.)

**Download takes forever** — Books are big. Typical 3–5 min for a medium-quality PDF. For really long books at high quality, 10+ min.

**Where are my books?** — Default `~/Books/Archive`. Open the app's Library view → it shows the path. Click a book → opens in macOS Preview.

---

## Uninstall

- Drag Archive Librarian from Applications to the Trash
- Open **Keychain Access** (Applications → Utilities), search "archive.org", delete the entry
- Books in your library folder are yours and stay put

---

## <a name="intel-macs"></a>For Intel Macs (or developers who want to install from source)

The .dmg is built for Apple Silicon only. For Intel, or to install from source:

1. `brew install python@3.13` (install [Homebrew](https://brew.sh) first if needed)
2. Download this repo's source (green Code button → Download ZIP)
3. Unzip, open Terminal, `cd` into the unzipped folder
4. Run `./install.sh`
5. Use `librarian` command in Terminal

CLI commands:

```bash
librarian setup                        # interactive setup wizard
librarian download <archive.org URL>   # download a book
librarian list                         # show your library
librarian status                       # check credentials + config
librarian creds set                    # change credentials
librarian creds delete                 # remove credentials
```

---

## Credits

The download protocol — turning archive.org's protected book pages into real PDFs — comes from [MiniGlome's Archive.org-Downloader](https://github.com/MiniGlome/Archive.org-Downloader). The native Mac wrapper, riso-aesthetic UI, dialogs, installer, and credential handling were built around it. See [ATTRIBUTION.md](ATTRIBUTION.md).

---

## Personal use only

This tool is for downloading books you have legitimate access to read via your free archive.org account. Don't redistribute downloaded copyrighted PDFs.
