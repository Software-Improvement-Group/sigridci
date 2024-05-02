# AI Explanations
The Sigrid platform checks code written in over 300 technologies on many quality aspects (like Security, Reliability, Maintainability, Architecture Quality, etc).
This amounts to tens of thousands of unique code checks that are performed by the Sigrid platform.
Generative AI is used as a solution to ensure each and every finding in every technology in Sigrid is presented with a detailed explanation of the problem at hand as well as with actionable and technology-specific mitigation advice.

## Does Sigrid send my code to ChatGPT?
No, Sigrid does not share your code or any other data with external parties, such as OpenAI's public ChatGPT service.
Sigrid makes use of its own private LLM instance in accordance with SIG's security and data sovereignty policies.

## Does Sigrid generate advice specific to my source code?
No. Currently, Sigrid AI explanations are pre-generated per individual quality check. This means the source code in which the finding was detected is not used in the generated explanation. 
Further augmentation and enrichment of the Sigrid platform using AI is planned in future releases. Please note that Sigrid does not make use of public LLM APIs, but instead runs it's own private LLM instance in accordance with SIG's security and data sovereignty policies.

## Where can I find AI explanations?
You can find several AI explanations through out the platform. 
Sigrid capabilities that have already been covered by AI explanations are:
- Maintainability Refactoring Candidates
- Security findings
- Reliability findings
- Performance Efficiency findings
- Cloud Readiness findings

<img src="../images/ai-explanations.gif" width="800" />

Please note that Sigrid's knowledge base is continuously expanding.

## How does Sigrid generate AI explanations?
Sigrid AI explanations are based on a unique knowledge base of invaluable sources on each and every technology, collected by SIG in over 20 years of software consultancy. Additionally, best in-class public data sources that are embedded in Sigrid’s explanations are [OWASP](https://owasp.org), [OpenCRE](https://opencre.org), [Common Weakness Enumeration](https://cwe.mitre.org) and [NIST National Vulnerability Database](https://nvd.nist.gov/).
Documentation from code scanning tools that Sigrid uses for its code analysis are also used to offer the best possible explanation of a finding.


## I have a question or suggestion regarding a specific explanation
Your feedback is much appreciated. Please [contact our support team](mailto:support@softwareimprovementgroup.com) should you have a question or suggestion for us regarding an AI explanation in Sigrid.

## Disclaimer
Sigrid's AI explanations have been compiled with the greatest care and based on best-in-class data sources. While we strive for presenting the most accurate information to our users possible, the nature of AI generated content is that it can contain inaccuracies or errors. Always verify critical information with reliable sources.
