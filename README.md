# 📚 Archive Librarian

Download books from [archive.org](https://archive.org) as real PDFs you can keep on your computer — including the borrow-protected ones.

**Built so anyone can use it.** No Terminal, no Python install, no setup commands. Just click and click.

---

## 📥 Download

### 👉 [**Click here to download Archive Librarian for Mac**](https://github.com/sabi-c/archive-librarian/releases/latest/download/Archive.Librarian.dmg)

(Apple Silicon Macs — M1, M2, M3, M4. For Intel Macs see [bottom of this page](#intel-macs).)

---

## How to install (literally 30 seconds)

1. **Click the download link above.** A file called `Archive Librarian.dmg` lands in your Downloads folder.

2. **Double-click it.** A window opens showing the app and an Applications shortcut.

3. **Drag the Archive Librarian icon onto Applications.** That's it — installed.

4. **Open Applications, find Archive Librarian, double-click it.**

   The first time you open it, macOS may pop up a warning saying *"cannot be opened because Apple cannot check it for malicious software."* This is normal for apps not sold through the App Store. To get past it:

   - **Right-click** (or two-finger click on a trackpad) on Archive Librarian in your Applications folder
   - Choose **Open** from the menu
   - Click **Open** in the dialog that appears

   You only have to do this once. After that, it just opens normally.

---

## Setup wizard (first launch)

When you open the app the first time, it walks you through:

1. **Do you have a free archive.org account?** If not, it opens the signup page in your browser. Sign up with any email — takes 30 seconds.

2. **Enter your archive.org email and password.** Type them into the dialog boxes. Your password is hidden as you type, and stored encrypted in your Mac's Keychain (the same place Safari saves your website passwords).

3. **The app tests your login** against archive.org and shows ✓ Login confirmed.

4. **Pick where to save your books.** Default is `Books/Archive` in your home folder. You can pick anywhere.

5. **Done.** The main menu appears with: Download Book, View Library, Settings, Quit.

---

## How to use it

### Download a book

Open the app → click **Download Book** → paste the archive.org URL → click Download.

### How to find a borrowable book on archive.org

1. Go to [archive.org](https://archive.org) in your browser
2. Sign in (top right)
3. Search for the book you want
4. On the book's page, click the orange **"Borrow for 1 hour"** button
5. The book opens in a reader — copy the URL from your browser's address bar
6. Paste it into the app

### View your library

Click **View Library** in the main menu. The folder opens in Finder.

### Change settings

Click **Settings** in the main menu to re-run the setup wizard (change credentials, change folder, etc.).

---

## Troubleshooting

**"Login failed" during setup**
Your archive.org password might be wrong. Try logging in to archive.org in your browser. If that works, click Settings in the app and re-enter your password.

**"Cannot be opened because Apple cannot check it"**
See step 4 above — right-click → Open the first time. This is a one-time thing.

**Download takes forever**
Books are big — typical download is 3–5 minutes for a medium-quality PDF (50–150 MB). For a long book at the highest quality, it can be 10+ minutes.

**App won't open at all**
Try restarting your Mac and trying again. If that doesn't work, contact whoever sent you this app.

**Where are my books?**
By default in `Books/Archive` in your home folder. Click **View Library** in the app to open the folder in Finder.

---

## How to uninstall

- Drag **Archive Librarian** from your Applications folder to the Trash
- Open the **Keychain Access** app (in Applications → Utilities), search for "archive.org", and delete the entry
- Your downloaded books in `Books/Archive` are yours and stay where they are

---

## <a name="intel-macs"></a>For Intel Macs (or developers who want to install from source)

The .dmg above only works on Apple Silicon Macs (M1, M2, M3, M4). If you have an older Intel Mac, or you'd rather install from source code:

1. Make sure Python 3.11+ is installed: `brew install python@3.13` (install [Homebrew](https://brew.sh) first if needed)
2. Download this repo: click the green **Code** button → **Download ZIP**
3. Unzip, open Terminal, `cd` into the unzipped folder
4. Run `./install.sh`

After install, use the `librarian` command:

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

The actual download protocol — the part that turns archive.org's protected book pages into real PDFs — comes from [MiniGlome's Archive.org-Downloader](https://github.com/MiniGlome/Archive.org-Downloader). The macOS app wrapper, native dialogs, installer, and credential handling were built around it. See [ATTRIBUTION.md](ATTRIBUTION.md) for full details.

---

## Personal use only

This tool is for downloading books you have legitimate access to read via your free archive.org account. Don't redistribute downloaded copyrighted PDFs.
