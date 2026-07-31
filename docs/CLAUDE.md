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
- Preview the documentation locally with Docker, so you don't need a Ruby toolchain on the host. Run this
  from the repository root, then open http://localhost:4000:

```
docker run --rm -v "$(pwd)/docs:/srv/jekyll" -v sigridci-docs-gems:/usr/local/bundle -p 4000:4000 -w /srv/jekyll ruby:3.1 sh -c "bundle install && bundle exec jekyll serve --host 0.0.0.0"
```

  - Use `ruby:3.1`, because the `github-pages` gem pins Jekyll 3.10, which does not run on newer Ruby versions.
  - The named volume caches the gems, so only the first run has to install them.
  - `bundle install` writes `docs/Gemfile.lock`, which is not committed.

## Instructions

- All links to elsewhere in the documentation should use a relative URL and point to Markdown files.
  - The only exception is `menu.html`, which is the template that points to the HTML version of each page.
  - This is checked by the unit tests.
- All images should be located in the `docs/images` directory.
  - This is checked by the unit tests.
- All images should have an explicit width set using the `<img src="..." width="123" />` notation.
- Following a paragraph with the `{: .attention }` will turn that paragraph into a highlighted block.
- Source code containing HTML characters should be wrapped betweeen `{% raw %}` and `{% endraw %}`.
- Liquid is processed inside Markdown pages, so a block repeated across several pages can live in
  `docs/_includes/` and be pulled in with {% raw %}`{% include name.md %}`{% endraw %}.
  - Group these per section in a subdirectory, for example the Guardrails and auto-fix agent blocks live in
    `docs/_includes/sigrid-mcp/` and are included as {% raw %}`{% include sigrid-mcp/name.md %}`{% endraw %}.
  - Relative links are allowed, but the unit tests resolve them from every page that includes the
    file, so a link has to be valid from all of them. Pages including the same file sit at different
    depths, so prefer an include with no links, and keep any link it does need in the including page.
  - Pass a parameter with {% raw %}`{% include name.md flag=true %}`{% endraw %} and read it as
    {% raw %}`{% if include.flag %}`{% endraw %}, for a block that varies slightly between pages.

## Updating the release notes

- Every major new feature should be documented in `docs/reference/release-notes.md`.
- The release notes are grouped per sprint to not overwhelm the reader. This means every heading in the release
  notes refers to the first Monday of our 2 week sprint.
- The format of each entry is `**Feature/Category**: Description of the change. Why it is useful.`.
- Every entry in the release notes must contain a link to elsewhere in the documentation where you can find more
  information about that feature.
