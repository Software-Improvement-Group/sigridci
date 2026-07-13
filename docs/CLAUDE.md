# CLAUDE.md

This file provides guidance to Claude Code when working on the Sigrid documentation. This file only covers the
documentation, see [../CLAUDE.md](../CLAUDE.md) for instructions when working on the source code.

## Architecture

- The Sigrid documentation is generated using [GitHub Pages](https://docs.github.com/en/pages).
- All documentation is written in Markdown.
- The documentation is automatically updated after each commit using GitHub Actions.
- The public URL for the Sigrid documentation is [docs.sigrid-says.com](https://docs.sigrid-says.com).

## Commands

- Run `python3 -m unittest` to run all unit tests.
- Run `python3 -m unittest test.test_documentation` to specifically run the unit tests for the documentation.
- These tests should always pass before making a commit.

## Instructions

- All links to elsewhere in the documentation should use a relative URL and point to Markdown files.
  - The only exception is `menu.html`, which is the template that points to the HTML version of each page.
  - This is checked by the unit tests.
- All images should be located in the `docs/images` directory.
  - This is checked by the unit tests.
- All images should have an explicit width set using the `<img src="..." width="123" />` notation.
- Following a paragraph with the `{: .attention }` will turn that paragraph into a highlighted block.
- Source code containing HTML characters should be wrapped betweeen `{% raw %}` and `{% endraw %}`.

## Updating the release notes

- Every major new feature should be documented in `docs/reference/release-notes.md`.
- The release notes are grouped per sprint to not overwhelm the reader. This means every heading in the release
  notes refers to the first Monday of our 2 week sprint.
- The format of each entry is `**Feature/Category**: Description of the change. Why it is useful.`.
- Every entry in the release notes must contain a link to elsewhere in the documentation where you can find more
  information about that feature.
