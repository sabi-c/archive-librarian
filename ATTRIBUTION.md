# Attribution

This package wraps and extends the following third-party work.

## archive-org-downloader.py

The core protocol implementation — the AES decryption flow that turns
archive.org's protected `/BookReader/BookReaderImages.php` responses into
JPEGs that can be assembled into a single PDF — is from
[MiniGlome/Archive.org-Downloader](https://github.com/MiniGlome/Archive.org-Downloader).

The file `archive-org-downloader.py` in this package is unmodified from
that project. It's redistributed here for convenience so the install is
a single self-contained folder.

If MiniGlome's project is helpful to you, consider supporting it via the
links in their repository.

## Original wrapping & CLI

Everything else in this package — `librarian` CLI, `creds.py`,
`onboarding.py`, `downloader.py`, `library.py`, `config.py`,
`install.sh`, `README.md` — was written for this package and is free
to copy, modify, and share.

## License

The MiniGlome script does not specify an explicit license. Per archive.org's
position on personal-use access, this tool is intended only for downloading
books you have legitimate access to read via your archive.org account.
Don't redistribute downloaded copyrighted PDFs.
