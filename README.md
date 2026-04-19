# 📚 Archive Librarian

Download books from [archive.org](https://archive.org) as real PDFs you can keep on your computer — including the borrow-protected ones.

**Built for non-technical users.** No Terminal commands. Just double-click.

---

## How to install (3 minutes, no Terminal needed)

### Step 1 — Download

Click the green **"Code"** button at the top of [this page](https://github.com/sabi-c/archive-librarian) → **"Download ZIP"**.

Your Mac will save a file called `archive-librarian-main.zip` to your Downloads folder.

### Step 2 — Unzip

Double-click `archive-librarian-main.zip` in your Downloads folder. Mac will create an `archive-librarian-main` folder right next to it.

### Step 3 — Move it somewhere permanent

Drag the `archive-librarian-main` folder from Downloads into your **Documents** folder (or anywhere you'll remember). The app needs to live somewhere permanent — don't leave it in Downloads.

### Step 4 — Install

Open the folder and **double-click `Install Archive Librarian.command`**.

A black window (Terminal) will open. Don't worry — text scrolling by is normal. The actual setup happens in friendly dialog boxes that pop up on top.

> **First time only:** macOS may say "cannot be opened because it is from an unidentified developer." If so:
>
> - **Right-click** (or Control-click) the file → **Open** → click **Open** in the dialog
> - This only happens the first time. After that you can just double-click.

The installer will:

- Check that Python is installed (offers to install it for you if not)
- Set up the app
- Add a "Download Book" shortcut to your Desktop
- Walk you through entering your archive.org login through pop-up dialogs

### Step 5 — Set up your archive.org account

The wizard will ask if you have an archive.org account. If not, it'll open the [free signup page](https://archive.org/account/signup) for you. Sign up (takes 30 seconds), verify your email, then come back and click "OK."

Then the wizard asks for your archive.org email and password. Type them in — your password is hidden as you type. Mac stores it securely in Keychain (the same place Safari saves your website passwords).

The wizard tests your login against archive.org and shows a green "✓ Login confirmed" pop-up when it works.

You're done.

---

## How to use it (every day)

### Download a book

**Double-click `Download Book`** on your Desktop.

A pop-up asks for the archive.org URL. Paste it in. Click "Download." Wait a few minutes. Done — the book is saved as a PDF in your books folder.

### How to find a borrowable book on archive.org

1. Go to [archive.org](https://archive.org) in your browser
2. Sign in (top right)
3. Search for the book you want
4. On the book's page, click the orange **"Borrow for 1 hour"** button
5. The book opens in a reader — copy the URL from your browser's address bar
6. Paste that URL into the "Download Book" pop-up

That's it. The borrow-and-download cycle takes a few seconds; the actual download takes a few minutes depending on the book.

### Where do my books go?

By default: a folder called `Books/Archive` inside your home folder.

You can change this during setup (the wizard asks) or anytime later by re-running the wizard.

---

## Things you might want to know

### How is my password stored?

In macOS **Keychain** — the same encrypted vault Safari uses for website passwords. It's never written to a plain text file or sent anywhere except to archive.org when you log in. To change or remove it, re-run the install command.

### What if the download doesn't work?

- **"Login failed"**: your password might be wrong. Try logging in to archive.org in your browser. If that works, re-run the installer to re-enter your password.
- **"Book isn't borrowable"**: a few archive.org books need special access (academic accounts etc). Most books work. If a specific book doesn't, search for an alternate copy.
- **Download hangs**: archive.org sometimes throttles. Cancel and retry.

### How big are the books?

Default quality is medium — about 50–150 MB per book, takes 3–5 minutes to download. Nice and readable, doesn't fill your hard drive.

### Will this break with macOS updates?

It uses standard macOS tools that have been stable for many years. The only thing that changes occasionally is Python — if a major Mac update breaks it, just re-download from this page and run the installer again.

### How do I uninstall?

- Drag the `archive-librarian-main` folder to the Trash
- Drag `Download Book.command` from your Desktop to the Trash
- Open the **Keychain Access** app (in Applications → Utilities), search for "archive.org," and delete the entry
- Your downloaded books in `Books/Archive` are yours and stay put

---

## For the curious / technical

If you'd rather use the Terminal directly:

```bash
librarian download <archive.org URL>    # download a book
librarian list                          # see your library
librarian status                        # check credentials
librarian setup                         # re-run the wizard
librarian creds set                     # change credentials
librarian creds delete                  # remove credentials
```

The `librarian` command is installed by the setup script.

---

## Credits

The actual download protocol — the part that turns archive.org's protected book pages into real PDFs — comes from [MiniGlome's Archive.org-Downloader](https://github.com/MiniGlome/Archive.org-Downloader). The friendly Mac wrapper, dialogs, installer, and credential handling were built around it. See [ATTRIBUTION.md](ATTRIBUTION.md) for full details.

---

## Personal use only

This tool is for downloading books you have legitimate access to read via your free archive.org account. Don't redistribute downloaded copyrighted PDFs.
