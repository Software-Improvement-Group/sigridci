# Sigrid AI Explanations
Sigrid AI Explanations transform complex software insights into clear, actionable guidance. Weather you are evaluating system architecture, investigating security findings, or assessing code functionality, these explanations help you understand what matters and how to act on it.

Powered by advanced AI, Sigrid delivers two explanation types: **AI Static Explanations** and **GenAI Explanations**, each designed to enhance your software quality journey in distinct ways.

## AI Static Explanations
The Sigrid platform performs comprehensive quality analysis across over 300 technologies, evaluating critical dimensions including Security, Reliability, Maintainability, and Architecture Quality. This results in tens of thousands of unique code quality checks. Sigrid's AI Static Explanations ensure that every finding is presented with detailed context, technology-specific recommendations, and actionable mitigation strategies.

### Where can I find AI Static Explanations?
AI Static Explanations are integrated throughout the Sigrid platform. The following capabilities currently include AI-powered insights:
- [Maintainability](../../docs/capabilities/system-maintainability.md) (Refactoring Candidates)
- [Open Source Health](../../docs/capabilities/system-open-source-health.md) (License implications)
- [Security findings](../../docs/capabilities/system-security.md)
- Reliability findings
- Cloud Readiness findings
- Green Code findings

<img src="../images/ai-explanations/ai-explanations.gif" width="800" />

Please note that Sigrid's knowledge base is continuously expanding.

### Which technologies are covered by the AI Static Explanations?
Technology availability for AI Static Explanations depends on the capability you are evaluating.

- For explanations on the Refactoring Candidates in Maintainability, refer to the [list of supported technologies](../reference/technology-support.md#list-of-supported-technologies) table.
- For AI Static Explanations on Security, Reliability, Cloud Readiness, and Green Code findings, the availability of explanations depends on whether the capability supports the technology.
- Open Source Health (License implications) findings are technology-agnostic.

### What do I do to use the AI Static Explanations?
No action required. AI Static Explanations are **enabled by default** for all Sigrid users. Since these explanations are generated through our private infrastructure without sharing any client code or data externally, they are safe and ready to use immediately.

### Does Sigrid share my code with external AI providers to generate the AI Static Explanations?
No. Sigrid's AI Static Explanations are generated using SIG's private LLM instance, ensuring full compliance with SIG's security and data sovereignty policies. Your code and data remain protected and are not shared with external AI providers.

### Is the advice in the AI Static Explanations specific to my source code?

No. AI Static Explanations are pre-generated per individual quality check and provide technology-consistent guidance.
While not customized to your specific codebase, explanations show examples in your code's technology, making recommendations immediately relevant and actionable.

### What data does Sigrid use to generate the AI Static Explanations?
Sigrid AI Static Explanations leverage:
- **SIG's 20+ years of software consultancy expertise** - Accumulated knowledge of software development practices and best practices
- Industry-leading data sources, including:
    - **[OWASP](https://owasp.org)** - Web application security standards
    - **[OpenCRE](https://opencre.org)** - Common requirements enumeration
    - **[Common Weakness Enumeration (CWE)](https://cwe.mitre.org)** - Software weakness classification
    - **[National Vulnerability Database (NIST)](https://nvd.nist.gov/)**
- **Best-in-class tooling documentation** - Integration with leading code scanning tools used by Sigrid for its code analysis
- **[Building Maintainable Software, Java Edition](https://learning.oreilly.com/library/view/building-maintainable-software/9781491955987/)** - SIG's published reference on maintainable code practices

---


## GenAI Explanations
Sigrid GenAI Explanations bridge the gap between complex technical data and clear business insights. When facing unfamiliar code, architecture decisions, or vulnerability management questions, these explanations provide the context you need to move forward with confidence.

Designed for both technical professionals and business stakeholders, GenAI Explanations translate technical complexity into clarity, showing you in plain language what matters, why it matters, and what comes next.

### Enabling GenAI Explanations
Sigrid GenAI Explanations require interaction with external AI models to generate on-demand insights. Because your data and code are transmitted to these models, SIG requires explicit consent and contractual alignment before activation.

We are committed to data governance and will never process your codebase or information without your explicit authorization. Enabling GenAI Explanations requires two components:
1. **AI Explanations license** - An additional license that grants access to GenAI Explanations
2. **AI addendum** - An addendum to your Sigrid contract, specific for AI usage

Contact your account manager or CSM at SIG for more information and to request activation.

### Discovering GenAI Explanations Across Sigrid Capabilities
Sigrid GenAI Explanations adapt to each capability they support, providing contextual insights tailored to your specific needs. Currently available across these key areas:

#### System Overview:
Gain an intelligent architectural summary of your entire system directly from your System Overview dashboard.
Click the AI button <img src="../images/ai-explanations/ai-live-explanation-icon-with-new.png" class="inline" /> in the System Details tab to generate a comprehensive explanation that transforms raw file structure into business-aligned insights.

This explanation analyzes your systems composition and delivers:
- **Codebase purpose and primary function** - What your system is designed to do
- **Architecture and core components** - How your system is logically organized
- **Key technologies and frameworks** - The technology stack driving your system
- **Design patterns and structural organization** - Architectural decisions evident in your code organization
- **Notable functionalities** - Capabilities and features inferred from your system's structure
- Overall quality assessment - Initial impression of the system's architectural maturity and organization

Perfect for teams new to a system, stakeholders seeking quick context, or anyone needing to understand a codebase at a glance.

#### Code Explorer
Navigate your codebase with confidence. Select any file in the Code Explorer and click the AI button <img src="../images/ai-explanations/ai-live-explanation-icon-with-new.png" class="inline" /> to receive an intelligent analysis from two perspectives:

**Functional Perspective** - Understanding for business stakeholders
Understand what the code does from a business standpoint:
- Core functionality and business purpose
- What problem the code solves
- Business value and impact
- Key business concepts at work

**Technical Perspective** - Understanding for developers and architects
Deep dive into how the code works:
- Programming language and paradigm: what technology and approach are used
- Architecture and design patterns: structural organization and design decisions
- Implementation details: key technical components and how they interact
- Libraries and frameworks: dependencies and third-party tools in use
- Code concepts: both functional (what it does) and technical concepts (how it's implemented)

These explanations are perfect for:
- **Bridging communication gaps** between business teams and development teams who need to understand the same code differently
- **Accelerating onboarding** when engineers encounter unfamiliar modules or legacy systems
- **Supporting code reviews** with immediate context on purpose and technical approach
- **Maintaining institutional knowledge** when original developers have moved on to other projects

#### Architecture Quality

Understand what your Architecture Quality scores mean and how they impact your system's long-term maintainability.

Navigate to the Architecture Explore and select a component of interest. The GenAI explanations are available for:

**Summary** - An overview of all architecture scores for the selected component.
Select the Summary tab and click the AI button <img src="../images/ai-explanations/ai-live-explanation-icon-with-new.png" class="inline" /> to receive an overview of your component's architecture quality scores.

The Summary explanation delivers:
- **Architecture score summary** - The component's overall architecture score relative to industry benchmarks.
- **Improvements overview** - A prioritized breakdown of system properties requiring attention, including priority areas of improvement, architectural strengths to maintain, and actionable recommendations to maximise your architecture score building on existing strengths.


**Individual System Properties** - Detailed explanations for each architecture capability for the selected component.
Select a specific system property tab and click the AI button <img src="../images/ai-explanations/ai-live-explanation-icon-with-new.png" class="inline" /> next to the component name to receive a detailed explanation of its quality score.

The System Property explanation delivers:
- **Clear capability definition** - What this architecture property measures and why it matters for your system's long-term viability
- **Score analysis** - What your specific score means relative to the industry benchmark
- **Risk and benefits** - For good scores: strategies to maintain and leverage your strength; for lower scores: current risks and benefits of improvement, with specific and implementable advice
- **Related properties** - How this metric influences and is influenced by related architectural characteristics, enabling you to see the bigger picture and identify cascading improvements
- **Business and technical impact** - How this architectural aspect affects the maintainability, testability, deployment, and system evolution

Architecture quality explanations are perfect for:
- **Architects and technical leaders** evaluating component health, identifying refactoring priorities, and making informed trade-offs
- **Development teams** implementing targeted architectural improvements
- **Strategic planning** by understanding architectural dependencies and reinforcement
- **Knowledge sharing** when explaining why certain components are architecturally strong or problematic

For deeper context on architecture quality, see the [Architecture Quality](../../docs/capabilities/architecture-quality.md) documentation.

#### Open Source Health

Access and address risk in your software supply chain with detailed vulnerability intelligence. Navigate to the Open Source Health tab in Sigrid, select a dependency with vulnerabilities, and click on the AI button <img src="../images/ai-explanations/ai-live-explanation-icon-with-new.png" class="inline"/> next to the vulnerability to access comprehensive analysis.

The explanation delivers:
- **Problem description** - What the vulnerability is, how it works, and its potential dangers
- **Vulnerability scope** - Which versions and usage patterns are affected versus those that are safe
- **Mitigation strategies** - Concrete, prioritized steps to remediate the risk
- **Technical risks** - How attackers could exploit the vulnerability and what system-level consequences to expect
- **Business risks** - Impact on data security, compliance obligations, customer trust, and operational continuity
- **Additional resources** - Links to authoritative sources for deeper research

Perfect for:
- **Security teams** prioritizing remediation efforts with clear risk and impact assessment
- **Development teams** understanding what makes a dependency vulnerable and how to fix it
- **Compliance and risk management** connecting technical vulnerabilities to business and regulatory consequences
- **Decision-makers** weighing the cost and urgency of dependency updates against business priorities

For deeper context on open source health, see the [Open Source Health](../../docs/capabilities/system-open-source-health.md) documentation.

### Which technologies are covered by the GenAI Explanations?
Technology availability for GenAI Explanations depends on the capability you are evaluating.
- For GenAI explanations in the [Code Explorer](#code-explorer), refer to the [list of supported technologies](../reference/technology-support.md#list-of-supported-technologies);
- GenAI explanations in the [System Overview](#system-overview), the [Architecture Quality properties](#architecture-quality), and [Open Source Health vulnerabilities](#open-source-health) are technology-agnostic.

### Data Security and Privacy

#### Does Sigrid share my code with external AI models or providers?

Yes, and we do so responsibly. Your code and data are transmitted securely to AI models for explanation generation, following SIG's enterprise-grade security and data sovereignty policies.

#### Is GenAI Explanation usage safe?

Absolutely. Multi-layered safeguards protect your intellectual property and data throughout the explanation generation process.

#### Which AI models does Sigrid use?

Sigrid currently leverages Anthropic's Haiku and Sonnet models for GenAI Explanation generation. We use **AWS Bedrock** as our infrastructure provider. AWS Bedrock ensures:
- No data storage or caching of generated explanations
- Zero use of your data for model training
- No sharing of data with third parties

#### How is my data handled during and after explanation generation?

Your code and data are safely sent to our models provider, AWS Bedrock. The models use your data temporarily only to generate the requested explanation.

- Explanations are generated on-demand only: when you click the AI button, only the strictly necessary information is sent to our models provider
- No storage, caching, or logging by SIG: the explanation is not saved after generation, every time you click the AI button a new explanation is generated
- AWS Bedrock does not retain any generated content beyond the time it takes to generate the explanation
- AWS Bedrock does not share your data with any third parties
- AWS Bedrock does not use your data for model training
- Your data remains ephemeral throughout the process

---

## Feedback and support
Your insights help us continually improve these explanations. If you have suggestions or questions regarding any AI explanation, please
**[contact our support team](mailto:support@softwareimprovementgroup.com)**.

--- 
## Disclaimer
Sigrid's AI explanations have been compiled with the greatest care and based on best-in-class data sources. While we strive to deliver accurate and reliable information, AI-generated content may contain inaccuracies or errors. **Always verify critical information with authoritative sources** before making any significant decisions based on these explanations.
