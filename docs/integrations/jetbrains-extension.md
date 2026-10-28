# Sigrid extension for JetBrains IDEs

The JetBrains plugin is another Sigrid IDE extension, alongside the [Sigrid extension for VS Code](vscode-extension.md), that helps you work on Sigrid findings without leaving your IDE. You can browse findings, triage them, and navigate straight to the relevant code. The plugin works across all JetBrains platforms, including IntelliJ, Rider, and any other JetBrains IDE you use.

The plugin is available on the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/32479-sigrid).

This plugin also includes a **Fix with AI** feature, described below, that hands findings off to Claude Code directly from the findings panel. If you want AI coding assistant integration without the findings panel itself, see [Sigrid Axis](../axis/README.md).

What you can do with it:

- Browse Maintainability, Security, Open Source Health, and Architecture findings directly in your IDE
- See a **Prioritized tab** that merges findings from all capabilities into a single ranked list, and shows a high-priority findings list, so you know where to start
- Filter by risk level or status, or search across all findings
- See only the findings for the file you're currently editing
- See **your files first** — findings in files you've changed on your branch are pinned at the top
- Group findings by file for a structural overview
- Triage findings — update status and add remarks — without opening Sigrid in your browser
- Double-click a finding to jump straight to the relevant line of code
- Open the full finding detail page in Sigrid when you need more context
- Fix findings with AI. Send one or more findings to Claude Code, using the **Fix with AI** toolbar button or the right-click **Fix it with Claude Code** menu, to have them fixed for you without leaving your IDE.
- Create Jira or Azure DevOps issues directly from one or more findings, via a unified "Create Issue" button
- **Onboard a new system** — if your system isn't in Sigrid yet, the plugin offers an Onboard button to upload it directly from the IDE

## Requirements

The plugin works with the following JetBrains IDEs, version **2026.1 or later**:

IntelliJ IDEA (Community & Ultimate), PyCharm (Community & Professional), WebStorm, GoLand, PhpStorm, RubyMine, CLion, Rider, Android Studio, and Aquua.

<img src="../images/ide/jetbrains-tools.png" width="500" />

You'll also need a Sigrid account with API access.

## Installing the plugin

 To install it you can he plugin you can download it from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/32479-sigrid) or in the IDE by searching Sigrid plugin. 

<img src="../images/ide/jetbrains-sigrid-marktplce.png" width="700" />
<img src="../images/ide/jetbrains-sigrid-plugin.png" width="700" />

1. Open your JetBrains IDE and go to **Settings → Plugins**
2. Click the gear icon (⚙️) and choose **Install Plugin from Disk**
3. Select the ZIP file you downloaded and restart the IDE

## Setting it up

Most settings are global, configured once and shared across all your projects. Go to **Settings → Tools → Sigrid** and fill in your **API Key** and **Portfolio Name**. If you're on a self-hosted Sigrid instance, add your URL there too — otherwise leave it blank and it'll default to `https://sigrid-says.com`.

<img src="../images/ide/jetbrains-setting-global-.png" width="700" />

At the project level (**Settings → Tools → Sigrid → Project**), you need to fill in the **System** field — this is required, and tells the plugin which codebase to load findings for. If it's left blank, no findings will load. **Subsystem** is optional, only needed if you want to narrow things down further.

<img src="../images/ide/jetbrains-setting-global-project.png" width="700" />

You can leave **API Key**, **Portfolio Name**, and **Sigrid URL** blank at the project level — the plugin automatically falls back to your global settings, so you don't have to repeat them for every project. You'd only override them here if you have a separate Sigrid account for this specific project, which is rare.


## Opening the plugin

Once configured, look for the **Sigrid** tab at the bottom of your IDE. If you don't see it, you can open it from **View → Tool Windows → Sigrid**, or press `Cmd+Shift+A` (Mac) / `Ctrl+Shift+A` (Windows/Linux) and search for "Sigrid Tool Window".

The panel has three tabs — **Maintainability**, **Security**, and **Open Source Health** — each showing the findings Sigrid has for your system.

<img src="../images/ide/jetbrains-maintainability.png" width="700" />

## Navigating findings

Double-click any finding to jump to the exact file and line. If a finding has multiple locations, a picker appears so you can choose which one to go to. The icon on the right side of each row opens the full finding detail page in Sigrid in your browser.

## Filtering and searching findings

When working with a large number of findings it can be hard to focus on what matters most. You can narrow down the findings list using the filter controls and the search bar at the top of the panel.

**To show only findings for the file you're currently editing**, toggle the **Active** button in the toolbar. Only findings related to the open file are shown. The filter state is remembered per tab.

**To filter by risk level**, click the filter icon (▽) next to the **Risk** column header. A dropdown appears with the risk levels available in your current findings — for example Very High, High, or Medium. Only options that exist in the active findings table are shown. Select one or more risk levels to show only findings that match. Deselect to remove the filter.

**To filter by status**, click the filter icon (▽) next to the **Status** column header. A dropdown appears with the available statuses, such as Raw, Accepted, and False Positive.

**To search across all findings**, use the search bar in the top-right corner of the panel. The list updates in real time as you type.

You can combine the active file filter, risk, status, and search filters at the same time.

<img src="../images/ide/jetbrains-open-ource-health.png" width="700" />

### Prioritized tab

The Prioritized tab shows a single, ranked list of findings across all capabilities — Security, Reliability, Open Source Health, and Maintainability — ordered by what matters most. Instead of switching between tabs to decide where to start, you get one list with the most important findings at the top.

The panel has tabs for **Prioritized**, **Maintainability**, **Security**, and **Open Source Health**. The Prioritized tab combines findings from the other tabs into one ranked view. The capability-specific tabs still work exactly as before.

<img src="../images/ide/jetbrains-prio-tab.png" width="700" />

#### How findings are ranked

Findings are ranked in the following order:

1. **Security findings and OSH vulnerabilities** — always at the top, regardless of severity. Only OSH dependencies with a known vulnerability are included, ranked by vulnerability risk (real CVE/CVSS data). Duplicate vulnerabilities and dependencies sharing a library name are collapsed into one finding.
2. **Reliability findings** — ranked below Security, above Maintainability.
3. **Duplication findings** — sequenced before other Maintainability findings when their files overlap with files that also have other Maintainability findings. Sorted by the number of duplicated lines (largest first), since their severity is always the same.
4. **Other Maintainability findings** — ranked by severity, then by size (unit size by weight, unit complexity by McCabe, unit interfacing by parameter count, module coupling by fan-in). Findings with the same priority, category, and location are ordered by start line.

The **Why** column explains why each finding appears where it does — for example, "Security objective met — Security findings are always prioritized" or "Ranked by severity, then size."

#### Objectives awareness

Findings in a capability whose quality objective is already met are dampened by one severity tier. Security and Reliability findings are always prioritized regardless of whether their objective is met.

For Maintainability, the plugin compares the current rating against the configured target. If no target is set, it falls back to a 3.0-star market benchmark. Open Source Health also compares against the market benchmark. The Maintainability rating is fetched once when the project opens and refreshed when Sigrid settings change.

#### Your files

When you're working on a branch, the Prioritized tab pins findings in files you've changed at the top of the list, in a **"Your files"** section. This includes files with committed changes since the branch left the default branch, and files with uncommitted edits. The section updates in real time as you work.

This requires the Git plugin for detecting which files changed on the branch. Uncommitted changes are detected with any VCS.

Files listed in "Your files" are never deprioritized, even if they have no recent activity in Sigrid's change history. The Why column shows "Prioritized because you modified this file."

#### Deprioritization of inactive files

Maintainability findings in files with no recent Git activity are deprioritized — they drop one severity tier and appear lower in the list instead of being hidden. The **Why** column shows the reason, including the date range checked.

When the Git plugin is available, the plugin checks the local Git history over the last 12 months before deprioritizing a file. Without the Git plugin, only Sigrid's shorter change-history window is used.

Security and Reliability findings are never deprioritized based on activity.

#### Exclusion and test-code filtering

Findings in vendored, generated, or config files are excluded from the Prioritized tab. Findings in test code are routed to a separate lane and do not appear in the main list.

#### Progressive disclosure

The Prioritized tab shows the **top 50 findings** by default. A **"Show all"** button at the bottom of the list reveals the rest, and a **"Show top 50"** button collapses it again. The total count is always visible — for example, "Showing top 50 of 535 findings."

Searching and filtering always cover every finding, not just the visible 50. You don't need to click "Show all" before searching.

#### Group by file

A toggle nests Prioritized findings under expandable file rows. Each finding appears under its first file location. Expand/collapse state is kept across searches, filters, and refreshes.

#### Line numbers

Security and Reliability findings show the file and line number in the Location column (for example, `GroupsAPI.java:54`). When multiple findings appear in the same file, they are sorted by line number. The line number is also included in the search and in the title when using Fix with AI.

---

### Architecture tab

The Architecture tab lists undesirable and cyclic dependencies between components, derived from the raw architecture graph of your system. It shows which components have problematic dependencies so you can address structural issues.

The architecture graph is shared with the Prioritized tab in a single request, and responses are cached between tabs until you press **Refresh**.

Architecture findings support **Fix with AI** — select one or more findings and use the Fix with AI button to generate a prompt for resolving the dependency issue.

---

### Onboarding a system from the IDE

When the configured system does not exist in Sigrid yet, the plugin's tool window explains this and offers an **"Onboard"** button. Clicking it uploads the repository to Sigrid, respecting your `.gitignore` to skip files that shouldn't be included.

Onboarding takes a few minutes. Use **Refresh** to check whether analysis has completed.

<img src="../images/ide/jetbrains-arch-tab.png" width="700" />


## Editing findings

You can update a finding's status and add a remark directly from the findings panel, without opening Sigrid in your browser.

To edit a finding, select one or more rows and do one of the following:

- Press **F2**
- Click the edit button in the toolbar
- Right-click and choose **Edit…** from the context menu

Batch edits are supported for up to 25 findings at a time.

## Fixing findings with AI

Any finding that involves a code change can be sent straight to Claude Code instead of being fixed by hand. Select one or more findings in the Maintainability, Security, or Open Source Health panel, then either click the **Fix with AI** button in the toolbar, or right-click and choose **Fix it with Claude Code** from the context menu.

<img src="../images/ide/jetbrains-fix-w-ai.png" width="700" />

This builds a natural-language prompt describing the selected findings, their severity, and their file locations, and hands it to the `claude` CLI in a terminal. If the [Sigrid Axis plugin](../axis/installation.md#install-the-claude-code-plugin) for Claude Code is installed and enabled, the prompt also points Claude Code to the right Sigrid Axis skill for the category involved, so Claude can pull extra context from Sigrid while it works. If the plugin isn't detected, the prompt falls back to plain instructions instead, and a one-time notification offers a link to install it.

<img src="../images/ide/sig-jetbrains-azuredevops-create-issue.png" width="700" />

## Creating issues from findings

You can turn one or more findings into a Jira issue or an Azure DevOps work item without leaving your IDE. Once at least one tracker is configured, a **Create Issue** button appears in the toolbar above the findings list. If you've configured both Jira and Azure DevOps, the button becomes a split button: clicking it directly creates an issue in whichever tracker you configured first, and the dropdown arrow next to it lets you pick the other tracker, or jump straight to **Issue Tracker Settings**.

<img src="../images/ide/sig-jetbrains-azuredevops-create-issue.png" width="700" />

### Setting up Jira

Go to **Settings → Tools → Sigrid → Jira** (this is a project-level setting) and fill in:

- **Base URL** — your Jira site, e.g. `https://yourcompany.atlassian.net`
- **User** — the email or username for the Jira account the plugin should act as
- **Token** — a Jira personal access token, generated from your Atlassian account at **id.atlassian.com → Security → API tokens**. Don't use your Jira password here.
- **Project Key** — the short, uppercase code Jira uses to prefix issue IDs in the target project (for example, the key for issue `SCRUM-1` is `SCRUM`). You can find it in the project's issue IDs or in its URL.

<img src="../images/ide/jetbrains-jira-setting.png" width="700" />

### Creating a Jira issue

To create an issue, select one or more findings in the Maintainability, Security, or Open Source Health panel, then click **Create Issue** in the toolbar (or pick **Jira** from the dropdown if Azure DevOps is also configured).

<img src="../images/ide/jetbrains-jira-findings.png" width="700" />

A dialog opens where you can edit the issue title and preview the auto-generated description, which lists each finding's title, severity, and file locations, before submitting.

<img src="../images/ide/jetbrains-jira-createissue.png" width="500" />

Once created, a notification confirms the new issue and links straight to it in Jira.

<img src="../images/ide/jetbrains-jira-issue-created.png" width="700" />

The issue itself carries over the same finding details from the description preview, so anyone picking it up in Jira has the full context without needing to open Sigrid.

<img src="../images/ide/jetbrains-jira-issue-2.png" width="700" />

If issue creation fails, Jira usually reports this as a generic permission error even when the real cause is different. Check, in order:

1. The **Project Key** matches exactly what's shown in Jira (case-sensitive)
2. The **Base URL** points to the correct Jira site
3. The Jira account behind your token has permission to create issues in that specific project
4. The **User** matches the account that generated the token

### Setting up Azure DevOps

Azure DevOps settings are split across two pages. Go to **Settings → Tools → Sigrid → Issue Trackers → Azure DevOps** (a global setting, shared across all your projects) and fill in:

- **Organization URL** — your Azure DevOps organization, e.g. `https://dev.azure.com/yourorganization`
- **Personal Access Token** — a token with **Work Items (Read & write)** scope, generated from **User settings → Personal access tokens → New Token** in Azure DevOps

<img src="../images/ide/sig-jetbrains-azuredevops-global-set.png" width="700" />

**Project Name** is set per-project rather than globally, since each IntelliJ project you work in will typically map to a different Azure DevOps project. Go to **Settings → Tools → Sigrid → Issue Trackers → Azure DevOps → Project Settings** and fill in:

- **Project Name** — the Azure DevOps project where work items will be created, e.g. `SigridTest`. This field is required.
- **Organization URL** — leave blank to use the global Organization URL
- **Personal Access Token** — leave blank to use the global PAT

<img src="../images/ide/sig-jetbrains-azuredevops-project-set.png" width="700" />

### Creating an Azure DevOps work item

Select one or more findings the same way you would for a Jira issue, then click **Create Issue** in the toolbar (or pick **Azure DevOps** from the dropdown if Jira is also configured).

A dialog opens where you can enter a title and choose the **work item type** from a dropdown — the available types are loaded directly from your Azure DevOps project, so they'll match whatever process template it uses (for example, a Scrum project offers Task, Bug, Feature, Impediment, and Product Backlog Item). The dialog also lets you preview the auto-generated description, which lists each finding's title, severity, and file locations, before submitting.

<img src="../images/ide/sig-jetbrains-azuredevops-create-isssue2.png" width="700" />
<img src="../images/ide/sig-jetbrains-azuredevops-workitems.png" width="700" />

Click **Create**. A success notification appears showing the work item number, with an **Open in Browser** link to view it directly in Azure DevOps.

<img src="../images/ide/sig-jetbrains-azuredevops-tasks-2.png" width="700" />

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.
