Technology support
==================

This page provides an overview of all technologies that can be analyzed by Sigrid for its various capabilities. 

## List of supported technologies

- The first column refers to how the technology is named in Sigrid's [scope configuration file](../reference/analysis-scope-configuration.md).
- The "auto-detect" column indicates whether Sigrid is able to automatically detect this technology. If this is *not* the case, indicated by an ⚠️, Sigrid *does* support this technology, but you will need to [configure it manually](analysis-scope-configuration.md#manual-technology-configuration).
- The column "supported Sigrid capabilities" does *not* list Open Source Health. The reason is that Open Source Health is based on open source ecosystems, not specific technologies. Refer to the section on [supported technologies for Open Source Health](#supported-open-source-ecosystems) for more information.
- In the list of supported capabilities:
  - "GenAI" indicates the technologies for which Sigrid offers AI-generated explanations on the source code. See the [GenAI Explanations](../reference/ai-explanations.md#genai-explanations) documentation for more information.
  - "Static AI" indicates the technologies for which Sigrid offers static explanations on the Maintainability findings. Support for other Static AI explanations on other Sigrid's capability depends on whether the technology is supported by the specific Sigrid capability. See the [AI Static Explanations](../reference/ai-explanations.md#ai-static-explanations) documentation for more information.
  - "Guardrails" indicates technologies supported by the live quality check in [Guardrails](../axis/guardrails.md)'s MCP tool in Sigrid Axis.
  - "AI Detection" indicates technologies supported by [AI Generated Code Detection](../capabilities/system-ai-governance.md#technology-support).

<a>Sigrid</a> \| <a>On-premise Sigrid</a> \| <a>Sigrid Local</a> \| <a>Sigrid Axis</a>
{: .technologySupportCategories }

| Name in configuration file    | Technology name(s)                     | Auto-detect | Supported Sigrid capabilities                                           | Notes                                       |
|-------------------------------|----------------------------------------|-------------|-------------------------------------------------------------------------|---------------------------------------------|
| `abap`                        | ABAP (SAP)                             | ✅          | Maintainability, Static AI, GenAI, Guardrails                           |
| `abapcds`                     | ABAP Core Data Services                | ✅          | Maintainability, Guardrails                                             |
| `abapsmartforms`              | ABAP SmartForms                        | ⚠️          | Maintainability, Architecture                                           |
| `abl`                         | Abl (OpenEdge)                         | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             |
| `acl`                         | ACL                                    | ✅          | Maintainability, Guardrails                                             |
| `accell`                      | Accell                                 | ✅          | Maintainability, Architecture, Guardrails                               |
| `actionscript`                | ActionScript                           | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `actionscript3`               | ActionScript 3                         | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `ada`                         | Ada                                    | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `adabasnatural`               | Adabas Natural                         | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `adfxml`                      | ADF XML                                | ⚠️          | Maintainability                                                         |
| `agilepoint`                  | AgilePoint                             | ⚠️          | Maintainability, Architecture                                           |
| `altovauml`                   | Altova UML                             | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `ansible`                     | Ansible                                | ✅          | Maintainability, Security, GenAI, Guardrails                            |
| `apachecamel`                 | Apache Camel                           | ✅          | Maintainability, Architecture, Guardrails                               |
| `apex`                        | Oracle APEX                            | ⚠️          | Maintainability, Architecture, GenAI                                    | [(4)](#notes), [(8)](#notes)                |
| `aps`                         | APS                                    | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `applicationmaster`           | Application Master                     | ✅          | Maintainability, Architecture, Guardrails                               |
| `ash`                         | ArtosScript (ash)                      | ⚠️          | Maintainability, Architecture                                           |
| `asp`                         | ASP                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `aspx`                        | ASP.NET                                | ✅          | Maintainability, Architecture, Security [(7)](#notes), Static AI, Guardrails |
| `assembly`                    | Assembly                               | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `aura`                        | Aura                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `axway`                       | Axway                                  | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `axystudio`                   | AxyStudio functions                    | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `axyworkflow`                 | AxyStudio workflows                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `baan`                        | Baan                                   | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `basic`                       | BASIC                                  | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `batch`                       | Batch                                  | ✅          | Maintainability, Architecture, Guardrails                               |
| `beanshell`                   | BeanShell                              | ✅          | Maintainability, Guardrails                                             |
| `beinformed`                  | Be Informed case management            | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `beinformedknowledgemodels`   | Be Informed knowledge models           | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `biztalk`                     | BizTalk                                | ✅          | Maintainability, Architecture, Guardrails                               |
| `biztalkrules`                | BizTalk Rules Engine                   | ✅          | Maintainability, Guardrails                                             |
| `blazerules`                  | Blaze BRM                              | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `blueprism`                   | Blue Prism                             | ✅          | Maintainability, Architecture, Guardrails                               |
| `blueriq`                     | Blueriq flows/processes                | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `blueriqexpressions`          | Blueriq expressions                    | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `bpel`                        | BPEL                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `bpm`                         | BPMN                                   | ⚠️          | Maintainability, Architecture                                           |
| `brail`                       | Brail                                  | ✅          | Maintainability, Guardrails                                             |
| `bsp`                         | Bsp                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `c`                           | C                                      | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails   |
| `cache`                       | Cache                                  | ⚠️          | Maintainability, Architecture                                           |
| `cacheobjectscript`           | Cache ObjectScript                     | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `ccl`                         | CCL                                    | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `cgdc`                        | CGDC                                   | ⚠️          | Maintainability, Architecture                                           |
| `cgt`                         | CGT                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `cicode`                      | Cicode                                 | ✅          | Maintainability, Architecture, Guardrails                               |
| `cl`                          | CL                                     | ⚠️          | Maintainability, Architecture                                           |
| `clearbasic`                  | Clearbasic                             | ✅          | Maintainability, Architecture, Guardrails                               |
| `clojure`                     | Clojure                                | ✅          | Maintainability, Guardrails                                             |
| `cobol`                       | Cobol                                  | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             |
| `coffeescript`                | CoffeeScript                           | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `coldfusion`                  | ColdFusion                             | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `configuration`               | Configuration                          | ✅          | Maintainability, Guardrails                                             | [(5)](#notes)                               |
| `coolgenc`                    | CoolGen C                              | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `coolgencobol`                | CoolGen Cobol                          | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `cpp`                         | C++                                    | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails, AI Detection |
| `csharp`                      | C#                                     | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails, AI Detection |
| `csp`                         | CSP                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `css`                         | CSS                                    | ✅          | Maintainability, Architecture, Static AI, Guardrails                    |
| `cypher`                      | Cypher                                 | ✅          | Maintainability, Architecture, Guardrails                               |
| `cucumber`                    | Cucumber                               | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `dart`                        | Dart (includes Flutter)                | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             |
| `datastage`                   | Datastage                              | ✅          | Maintainability, Architecture, Guardrails                               |
| `datastageetl`                | DatastageETL                           | ✅          | Maintainability, Architecture, Guardrails                               |
| `datastageworkflow`           | DatastageWorkflow                      | ✅          | Maintainability, Architecture, Guardrails                               |
| `db2`                         | DB2                                    | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `dcl`                         | Dcl                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `delphi`                      | Delphi                                 | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             |
| `delphiforms`                 | Delphi Forms                           | ✅          | Maintainability, Architecture, Guardrails                               |
| `deltacobol`                  | Delta/Cobol                            | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `docker`                      | Docker                                 | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails   |
| `documentumxcp`               | Documentum xCP                         | ✅          | Maintainability, Architecture, Guardrails                               |
| `drools`                      | Drools                                 | ✅          | Maintainability, Guardrails                                             |
| `dscript`                     | Dscript                                | ✅          | Maintainability, Guardrails                                             |
| `easytrieve`                  | Easytrieve                             | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `egl`                         | EGL                                    | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `ejs`                         | EJS                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `elixir`                      | Elixir                                 | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             |
| `embeddedsql`                 | C++ Embedded SQL                       | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `erb`                         | ERB                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `erlang`                      | Erlang                                 | ✅          | Maintainability, Security, Guardrails                                   |
| `esql`                        | ESQL                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `filetab`                     | File Tab                               | ✅          | Maintainability, Guardrails                                             |
| `finacle`                     | Finacle                                | ⚠️          | Maintainability, Architecture                                           |
| `freeformatcobol`             | Freeformat Cobol                       | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `freemarker`                  | Freemarker                             | ✅          | Maintainability, Architecture, Guardrails                               |
| `fme`                         | FME                                    | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `fortran`                     | FORTRAN                                | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `gensym`                      | Gensym                                 | ✅          | Maintainability, Architecture, Guardrails                               |
| `grpc`                        | gRPC                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `go`                          | Go (AKA GoLang)                        | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             |
| `gosu`                        | Gosu                                   | ⚠️          | Maintainability, Architecture, Security                                 |
| `groovy`                      | Groovy                                 | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails   |
| `gsp`                         | GSP                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `guidefinition`               | GUI Definition                         | ✅          | Maintainability, Guardrails                                             | [(5)](#notes)                               |
| `gupta`                       | Gupta                                  | ✅          | Maintainability, Architecture, Guardrails                               |
| `haml`                        | Haml                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `html`                        | HTML                                   | ✅          | Maintainability, Architecture, Guardrails                               | [(7)](#notes)                               |
| `hql`                         | HQL                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `ibmace`                      | IBM ACE                                | ✅          | Maintainability, Guardrails                                             |
| `ibmbpmbpd`                   | IBM BPM (BPD)                          | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `ibmbpmprocess`               | IBM BPM (Process)                      | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `ideal`                       | Ideal                                  | ✅          | Maintainability, Architecture, Guardrails                               |
| `informatica`                 | Informatica                            | ✅          | Maintainability, GenAI, Guardrails                                      |
| `informix4gl`                 | Informix 4GL                           | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `informixsql`                 | Informix SQL                           | ⚠️          | Maintainability, Architecture                                           |
| `ingres`                      | Ingres                                 | ⚠️          | Maintainability                                                         |
| `intershoppipeline`           | Intershop (Pipeline)                   | ⚠️          | Maintainability, Architecture                                           |
| `jasperreports`               | Jasper Reports                         | ✅          | Maintainability, Architecture, Guardrails                               |
| `jade`                        | Jade                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `java`                        | Java                                   | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails, AI Detection |
| `javafx`                      | Java FX                                | ✅          | Maintainability, Architecture, Guardrails                               |
| `javascript`                  | JavaScript (includes NodeJS)           | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails   | [(3)](#notes)                               | 
| `jbc`                         | JBC                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `jbpm`                        | jBPM                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `jcl`                         | JCL                                    | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `jcs`                         | JCS                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `jde`                         | JDE                                    | ✅          | Maintainability, Guardrails                                             |
| `jinja`                       | Jinja                                  | ✅          | Maintainability, Architecture, Guardrails                               |
| `jsf`                         | JSF                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `json`                        | JSON                                   | ✅          | Maintainability, Architecture                                           | [(5)](#notes)                               |
| `jsp`                         | JSP                                    | ✅          | Maintainability, Architecture, Security [(7)](#notes), Static AI, Guardrails |
| `kotlin`                      | Kotlin                                 | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails, AI Detection |
| `less`                        | Less                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `linc`                        | LINC                                   | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `lion`                        | Lion                                   | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `lodestar`                    | Lodestar                               | ✅          | Maintainability, Architecture, Guardrails                               |
| `logicapps`                   | Logic Apps                             | ⚠️          | Maintainability, GenAI                                                  |
| `logicnets`                   | LogicNets                              | ✅          | Maintainability, Architecture, Guardrails                               |
| `lotusscript`                 | LotusScript                            | ✅          | Maintainability, Architecture, Guardrails                               |
| `lua`                         | Lua                                    | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             |
| `magic`                       | Magic                                  | ✅          | Maintainability, Architecture, Guardrails                               |
| `magik`                       | Magik                                  | ✅          | Maintainability, Architecture, Guardrails                               |
| `magnum`                      | Magnum                                 | ✅          | Maintainability, Architecture, Guardrails                               |
| `matlab`                      | Matlab                                 | ⚠️          | Maintainability, Architecture                                           |
| `mediationflows`              | Mediation Flows                        | ✅          | Maintainability, Architecture, Guardrails                               |
| `mendix`                      | Mendix                                 | ✅          | Maintainability, Architecture, Security, Static AI, Guardrails          | [(9)](#notes), [(4)](#notes)                |
| `mendixflow`                  | Mendix microflows/nanoflows            | ✅          | Maintainability, Architecture, Security, Guardrails                     | [(11)](#notes)                              |
| `messagebuilder`              | MessageBuilder                         | ✅          | Maintainability, Architecture, Guardrails                               |
| `mpsbehavior`                 | MPS Behavior                           | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `mpsclass`                    | MPS Class                              | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `mpstranslator`               | MPS Translator                         | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `mule`                        | Mule                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `mtwize`                      | MtWize                                 | ✅          | Maintainability, Architecture, Guardrails                               |
| `murexdatadictionary`         | Murex Data Dictionary                  | ✅          | Maintainability, Architecture, Guardrails                               |
| `murexlookuptable`            | Murex Lookup Table                     | ✅          | Maintainability, Architecture, Guardrails                               |
| `murexscript`                 | Murex Script                           | ✅          | Maintainability, Architecture, Guardrails                               |
| `murexworkflow`               | Murex Workflow                         | ✅          | Maintainability, Architecture, Guardrails                               |
| `mustache`                    | Mustache (includes Handlebars)         | ✅          | Maintainability, Architecture, Guardrails                               |
| `nabsic`                      | Nabsic                                 | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `navascript`                  | NavaScript                             | ✅          | Maintainability, Guardrails                                             |
| `naviscript`                  | Naviscript                             | ⚠️          | Maintainability, Architecture                                           |
| `navision`                    | Navision (AKA Dynamics NAV, AL)        | ✅          | Maintainability, Architecture, Guardrails                               |
| `netiqidmpolicy`              | NetIQ IDM Policy                       | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `netiqidmrequest`             | NetIQ IDM Request                      | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `netiqidmworkflow`            | NetIQ IDM Workflow                     | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `netweaveridm`                | NetweaverIDM                           | ✅          | Maintainability, Architecture, Guardrails                               |
| `nonstopsql`                  | Nonstop SQL                            | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `normalizedsystemsjava`       | Normalized Systems Java                | ✅          | Maintainability, Architecture, Guardrails                               |
| `normalizedsystemsjavascript` | Normalized Systems JavaScript          | ✅          | Maintainability, Guardrails                                             |
| `normalizedsystemsmodel`      | Normalized Systems Model               | ✅          | Maintainability, Architecture, Guardrails                               |
| `normalizedsystemstypescript` | Normalized Systems TypeScript          | ✅          | Maintainability, Guardrails                                             |
| `objectivec`                  | Objective-C                            | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             |
| `odi`                         | ODI                                    | ⚠️          | Maintainability, Architecture                                           |
| `odm`                         | ODM                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `omt`                         | OMT                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `opa`                         | OPA                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `opc`                         | OPC                                    | ✅          | Maintainability, Guardrails                                             |
| `openroad`                    | OpenROAD 4GL                           | ⚠️          | Maintainability                                                         |
| `oraclebpm`                   | Oracle BPM                             | ✅          | Maintainability, Architecture, Guardrails                               |
| `oracleofsaa`                 | Oracle OFSAA                           | ✅          | Maintainability, Architecture, Guardrails                               |
| `oracleworkflow`              | Oracle Workflow                        | ✅          | Maintainability, Architecture, Guardrails                               |
| `ords`                        | ORDS                                   | ⚠️          | Maintainability                                                         |
| `osb`                         | OSB                                    | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `osbproxy`                    | OSB Proxy                              | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `osmprocess`                  | OSM Process                            | ⚠️          | Maintainability, Architecture                                           |
| `osmtask`                     | OSM Task                               | ✅          | Maintainability, Architecture, Guardrails                               |
| `outsystems`                  | OutSystems                             | ✅          | Maintainability, Architecture, GenAI, Guardrails                        | [(1)](#notes), [(4)](#notes), [(9)](#notes) |
| `pascal`                      | Pascal                                 | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `pega`                        | Pega                                   | ✅          | Maintainability, Guardrails                                             | [(1)](#notes), [(9)](#notes)                |
| `perl`                        | Perl                                   | ✅          | Maintainability, Architecture, Security [(7)](#notes), GenAI, Guardrails |
| `php`                         | PHP                                    | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails, AI Detection |
| `plc`                         | PLC                                    | ✅          | Maintainability, Architecture, GenAI, Guardrails                        | [(4)](#notes), [(8)](#notes)                |
| `plcfbd`                      | PLC Functional Block Diagram           | ✅          | Maintainability, Guardrails                                             |
| `plcil`                       | PLC Instruction List                   | ✅          | Maintainability, Guardrails                                             |
| `plcld`                       | PLC Ladder Diagram                     | ✅          | Maintainability, Guardrails                                             |
| `plcsfc`                      | PLC Sequential Function Chart          | ✅          | Maintainability, Guardrails                                             |
| `plcst`                       | PLC Structured Text                    | ✅          | Maintainability, GenAI, Guardrails                                      |
| `pli`                         | PL/I                                   | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `plsql`                       | Oracle PL/SQL                          | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             |
| `plsqlforms`                  | Oracle PL/SQL Forms                    | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `plsqlreports`                | Oracle PL/SQL Reports                  | ✅          | Maintainability, Guardrails                                             |
| `pluk`                        | PLUK                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `polymertemplates`            | Polymer Templates                      | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `powerbuilder`                | Powerbuilder                           | ✅          | Maintainability, Architecture, Guardrails                               |
| `powercenter`                 | PowerCenter                            | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `powerfx`                     | Power Fx (AKA Microsoft Power Apps)    | ✅          | Maintainability, GenAI, Guardrails                                      |
| `powershell`                  | Powershell                             | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             |
| `progress`                    | Progress (OpenEdge)                    | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails   |
| `prt`                         | PRT                                    | ✅          | Maintainability, Guardrails                                             |
| `puppet`                      | Puppet                                 | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `python`                      | Python                                 | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails, AI Detection |
| `r`                           | R                                      | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `radience`                    | Radience                               | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `razor`                       | Razor                                  | ✅          | Maintainability, Architecture, Static AI, Guardrails                    |
| `regelspraak`                 | ALEF Regelspraak                       | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `regelspraakhtml`             | ALEF Regelspraak (HTML export)         | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `rexx`                        | Rexx                                   | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `robot`                       | Robot                                  | ✅          | Maintainability, Guardrails                                             |
| `rpg`                         | RPG                                    | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `ruby`                        | Ruby (includes Ruby on Rails)          | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails   |
| `rust`                        | Rust                                   | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             | [(4)](#notes), [(8)](#notes)                |
| `salesforceapex`              | Salesforce Apex                        | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `salesforceflow`              | Salesforce Flow                        | ✅          | Maintainability, Architecture, Guardrails                               |
| `salesforceprocessbuilder`    | Salesforce Process Builder             | ✅          | Maintainability, Guardrails                                             |
| `sappo`                       | SAP PO                                 | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `sas`                         | SAS                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `sasflows`                    | SAS Flows                              | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `sass`                        | Sass                                   | ✅          | Maintainability, Architecture, Static AI, Guardrails                    |
| `scala`                       | Scala                                  | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails   |
| `scl`                         | SCL                                    | ⚠️          | Maintainability, Architecture                                           |
| `scr`                         | SCR                                    | ✅          | Maintainability, Architecture, Guardrails                               |
| `script`                      | Shell script                           | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `servicenow`                  | ServiceNow                             | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `siebeldeclarative`           | Siebel Declarative                     | ⚠️          | Maintainability, Architecture                                           | [(4)](#notes), [(8)](#notes)                |
| `siebeljs`                    | Siebel JS                              | ⚠️          | Maintainability, Architecture                                           | [(4)](#notes), [(8)](#notes)                |
| `siebelscripted`              | Siebel Scripted                        | ⚠️          | Maintainability, Architecture                                           | [(4)](#notes), [(8)](#notes)                |
| `siebelworkflow`              | Siebel Workflow                        | ⚠️          | Maintainability, Architecture                                           | [(4)](#notes), [(8)](#notes)                |
| `siebeltbui`                  | Siebel TBUI                            | ⚠️          | Maintainability, Architecture                                           | [(4)](#notes), [(8)](#notes)                |
| `slim`                        | Slim                                   | ✅          | Maintainability, Guardrails                                             |
| `smalltalk`                   | Smalltalk                              | ⚠️          | Maintainability, Architecture, GenAI                                    |
| `solidity`                    | Solidity                               | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `sonicesb`                    | Sonic ESB                              | ✅          | Maintainability, Architecture, Guardrails                               |
| `spl`                         | SPL                                    | ✅          | Maintainability, Guardrails                                             |
| `sqlj`                        | SQLJ                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `sqr`                         | SQR                                    | ⚠️          | Maintainability, Architecture                                           |
| `ssis`                        | SSIS                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `starlimssql`                 | StarLIMS                               | ✅          | Maintainability, Architecture, Guardrails                               |
| `streamserve`                 | StreamServe                            | ✅          | Maintainability, Architecture, Guardrails                               |
| `synapse`                     | Synapse                                | ⚠️          | Maintainability                                                         |
| `synon`                       | Synon                                  | ✅          | Maintainability, Architecture, Guardrails                               |
| `swift`                       | Swift                                  | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails, AI Detection |
| `t4`                          | T4                                     | ✅          | Maintainability, Guardrails                                             |
| `tacl`                        | TACL                                   | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `tal`                         | TAL                                    | ✅          | Maintainability, Guardrails                                             |
| `tandem`                      | Tandem                                 | ✅          | Maintainability, Architecture, GenAI, Guardrails                        | [(4)](#notes), [(8)](#notes)                |
| `tapestry`                    | Tapestry                               | ✅          | Maintainability, Architecture, Guardrails                               |
| `terraform`                   | Terraform                              | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails   |
| `thrift`                      | Thrift                                 | ✅          | Maintainability, Architecture, Guardrails                               |
| `thymeleaf`                   | Thymeleaf                              | ✅          | Maintainability, Architecture, Guardrails                               |
| `tibco`                       | TIBCO BW                               | ✅          | Maintainability, Architecture, Guardrails                               |
| `tibcobe`                     | TIBCO BE (XML)                         | ✅          | Maintainability, Architecture, Guardrails                               |
| `tibcobejava`                 | TIBCO BE (Java)                        | ✅          | Maintainability, Architecture, Guardrails                               |
| `tibcobestatemachine`         | TIBCO BE (State Machine)               | ✅          | Maintainability, Architecture, Guardrails                               |
| `tibcobw6`                    | TIBCO BW6                              | ✅          | Maintainability, Architecture, Guardrails                               |
| `tripleforms`                 | TriplEforms                            | ✅          | Maintainability, Guardrails                                             |
| `trs`                         | TRS                                    | ✅          | Maintainability, Guardrails                                             | [(4)](#notes), [(8)](#notes)                |
| `tsql`                        | T-SQL (Microsoft SQL Server, MS SQL))  | ✅          | Maintainability, Architecture, Static AI, GenAI, Guardrails             |
| `turtle`                      | Turtle                                 | ✅          | Maintainability, Guardrails                                             |
| `twig`                        | Twig                                   | ✅          | Maintainability, Guardrails                                             |
| `typescript`                  | TypeScript (includes React/TypeScript) | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails, AI Detection | [(10)](#notes)                              |
| `uil`                         | UIL (Motif)                            | ✅          | Maintainability, Architecture, Guardrails                               |
| `uniface`                     | Uniface                                | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `until`                       | Until                                  | ⚠️          | Maintainability, Architecture                                           |
| `vag`                         | Visual Age                             | ✅          | Maintainability, Architecture, Guardrails                               |
| `vagrecord`                   | Visual Age Record                      | ✅          | Maintainability, Architecture, Guardrails                               |
| `vb`                          | Visual Basic                           | ✅          | Maintainability, Architecture, Security [(7)](#notes), Static AI, GenAI, Guardrails |
| `vbnet`                       | Visual Basic .NET                      | ✅          | Maintainability, Architecture, Security [(7)](#notes), Static AI, GenAI, Guardrails |
| `velocity`                    | Velocity                               | ✅          | Maintainability, Architecture, Guardrails                               |
| `vgl`                         | VGL                                    | ✅          | Maintainability, Guardrails                                             |
| `visualforce`                 | VisualForce                            | ✅          | Maintainability, Guardrails                                             |
| `visualfoxpro`                | Visual FoxPro                          | ⚠️          | Maintainability                                                         |
| `visualrpg`                   | Visual RPG                             | ✅          | Maintainability, Architecture, Guardrails                               |
| `visualobjects`               | Visual Objects                         | ⚠️          | Maintainability, Architecture                                           |
| `vue`                         | Vue                                    | ✅          | Maintainability, Architecture, Security, Static AI, GenAI, Guardrails, AI Detection | [(2)](#notes)                               |
| `vulcan`                      | Vulcan.NET                             | ⚠️          | Maintainability, Architecture                                           |
| `webfocus`                    | WebFocus                               | ✅          | Maintainability, Architecture, Guardrails                               |
| `webmethods`                  | WebMethods                             | ✅          | Maintainability, Architecture, Guardrails                               |
| `websmart`                    | WebSmart                               | ✅          | Maintainability, Architecture, Guardrails                               | [(4)](#notes), [(8)](#notes)                |
| `websmartpanels`              | WebSmart Panels                        | ✅          | Maintainability, Guardrails                                             |
| `wonderware`                  | Wonderware                             | ✅          | Maintainability, Guardrails                                             |
| `wsdl`                        | WSDL                                   | ✅          | Maintainability, Architecture                                           |
| `wtx`                         | WTX                                    | ⚠️          | Maintainability                                                         |
| `xaml`                        | XAML                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `xml`                         | XML                                    | ✅          | Maintainability, Architecture                                           | [(5)](#notes)                               |
| `xpdl`                        | Tibco ActiveMatrix BPM                 | ✅          | Maintainability, Guardrails                                             |
| `xpp`                         | X++ AX                                 | ✅          | Maintainability, Architecture, GenAI, Guardrails                        | [(4)](#notes), [(8)](#notes)                |
| `xpp365`                      | X++ for Dynamics 365                   | ✅          | Maintainability, Architecture, GenAI, Guardrails                        | [(4)](#notes), [(8)](#notes)                |
| `xquery`                      | Xquery                                 | ✅          | Maintainability, Architecture, GenAI, Guardrails                        |
| `xsd`                         | XSD                                    | ✅          | Maintainability, Architecture                                           |
| `xslt`                        | XSLT                                   | ✅          | Maintainability, Architecture, Guardrails                               |
| `xul`                         | XUL                                    | ✅          | Maintainability, Guardrails                                             |
| `yaml`                        | YAML                                   | ✅          | Maintainability, Architecture                                           | [(5)](#notes)                               |
{: .technologySupportTable }

### Notes

1. Not supported by [on-premise Sigrid](../organization-integration/onpremise-integration.md).
2. Sigrid automatically detects whether you are using Vue in combination with JavaScript or Vue in combination
   with TypeScript.
3. Sigrid will automatically detect if you are using React within your JavaScript and/or TypeScript code.
4. Not supported by [Sigrid Local](../organization-integration/sigrid-local.md).
5. In most cases, configuration files are not considered part of production code and are therefore not relevant for Sigrid's maintainability analysis. Only add these technologies if you consider them part of the system's production code.
6. "Unknown technology" will be shown in Sigrid when the technology cannot be detected.
7. Requires an additional *Sigrid Security Checkmarx* license.
8. You can use Sigrid CI for this technology, but you will need to use a special option. See instructions on how to [technology conversion configuration](#technology-conversion-configuration) below.
9. Sigrid CI is not supported for this technology. You can still use Sigrid, but you will need to use one of the [alternative upload channels](../organization-integration/upload-instructions.md).
10. `typescript` should also be used with React and/or JSX files with TypeScript that use the `.ts` or `.tsx` file extensions.
11. Technology support is currently in beta, and not yet generally available. Contact SIG if you want to participate in this beta program.

### Framework-specific support

The [list of supported technologies](#list-of-supported-technologies) refers to the *base* technologies. 
For many modern technologies, the choice of frameworks has a significant impact on your system structure and architecture.
Sigrid therefore also provides support for framework-specific constructs for the following frameworks:

Android,
Angular,
ASP.NET Core,
Doctrine,
Entity Framework,
Flask,
GWT,
JavaFX,
Javalin,
JDBC,
JMS,
JNI,
JPA,
Hibernate,
Laminas,
Mongoose,
Qt,
RabbitMQ,
React,
S3,
SAP UI,
Spring,
Spring Boot,
Spring Cloud,
Spring Data,
Spring Kafka,
Styled Components,
Swing,
Svelte,
WPF
Vue,
Yii.

## Technology conversion configuration

For the vast majority of technologies, you can simply publish your repository and have your code analyzed by Sigrid. However, a small number of technologies cannot be analyzed by Sigrid in its "native" format. In those situations, Sigrid needs to convert these technologies to another format before it can be analyzed.

This configuration can be managed using the `--convert` [option in Sigrid CI](client-script-usage.md#command-line-options). This is only applicable for the following technologies:

| Technology               | Value of the `--convert` option                                         |
|--------------------------|-------------------------------------------------------------------------|
| ABB Control Builder      | `ABBControlBuilder`                                                     |
| Altova UML               | `AltovaUML`                                                             |
| Oracle APEX              | `Apex`                                                                  |
| Axway                    | `Axway`                                                                 |
| Axystudio                | `Axystudio`                                                             |
| BRM                      | `BRM`                                                                   |
| Be Informed              | `Beinformed`                                                            |
| Blueriq                  | `Blueriq`                                                               |
| Data Bricks              | `Databricks`                                                            |
| Ecostruxure              | `Ecostruxure`                                                           |
| FME                      | `FME`                                                                   |
| IBM BPM                  | `IbmBpm`                                                                |
| Infinite Blue            | `Infiniteblue`                                                          |
| JDE                      | `JDE`                                                                   |
| Linc                     | `Linc`                                                                  |
| Lion                     | `Lion`                                                                  |
| Lion/COBOL               | `LionCobol`                                                             |
| MicroFocus COBOL         | `MicroFocusCobol`                                                       |
| MPS                      | `MPSLanguage`                                                           |
| Nabsic                   | `Nabsic`                                                                |
| NetIQ IDM                | `NetIQIDM`                                                              |
| OSB Pipeline             | `OSBPipeline`                                                           |
| OutSystems               | `Outsystems` or `OutsystemsExporter` (contact SIG support for details)  |
| PEGA                     | `Pega` or `PegaFilter` (contact SIG support for details)                |
| Pentaho Data Integration | `Pentahodataintegration`                                                |
| PL/SQL Headstart         | `PlsqlHeadstart`                                                        |
| PL/SQL Forms             | `Plsqlforms`                                                            |
| Polymer                  | `Polymer`                                                               |
| PowerCenter              | `Powercenter`                                                           |
| Radience                 | `Radience`                                                              |
| Regelspraak              | `Regelspraak` or `Regelspraakhtml` (contact SIG support for details)    |
| Rust                     | `Rust`                                                                  |
| Sailpoint BeanShell      | `Sailpointbeanshell`                                                    |
| SAP PO                   | `Sappo`                                                                 |
| SAS Flows                | `Sasflows`                                                              |
| ServiceNow               | `ServiceNow`                                                            |
| Siebel                   | `SiebelProject` or `SiebelRepository` (contact SIG support for details) |
| Svelte                   | `Svelte`                                                                |
| Uniface                  | `Ssduniface` or `Unifacexml` (contact SIG support for details)          |
| Tandem                   | `Tandem`                                                                |
| TRS                      | `Trs`                                                                   |
| USoft                    | `Usoft` or `UsoftEsi` (contact SIG support for details)                 |
| WebSmart                 | `Websmart`                                                              |
| X++                      | `Xpp`                                                                   |
| X++ 365                  | `Axmodel`                                                               |

## Supported open source ecosystems

In addition to supporting 300+ technologies, Sigrid also supports various open source ecosystems for its Open Source Health capability. Note that different projects might use different open source ecosystems, even if they use the same technology. For example, there is no standardized way to manage open source dependencies in Java projects. Some Java projects use Maven, others use Gradle. This is why some technologies are listed multiple times in the table below.

| Open source ecosystem                                                                 | Common technologies    | Vulnerability risk | License risk | Freshness risk | Transitive dependencies | Notes                                                                            |
|---------------------------------------------------------------------------------------|------------------------|--------------------|--------------|----------------|-------------------------|----------------------------------------------------------------------------------|
| Bower                                                                                 | JavaScript             | ✅                 | ✅           | ✅             | ❌                      |                                                                                  |
| Cargo                                                                                 | Rust                   | ✅                 | ✅           | ✅             | ✅                      |                                                                                  |
| CocoaPods                                                                             | Swift, Objective-C     | ❌                 | ❌           | ❌             | ❌                      | End-of-life, as CocoaPods itself is shutting down.                               |
| Composer                                                                              | PHP                    | ✅                 | ✅           | ✅             | ✅                      |                                                                                  |
| Go Modules                                                                            | Go                     | ✅                 | ✅           | ✅             | ✅                      |                                                                                  |
| Gradle                                                                                | Java, Kotlin, Groovy   | ✅                 | ✅           | ✅             | ✅                      | [Instructions for publishing](../capabilities/osh-upload-instructions.md#gradle) |
| Hex                                                                                   | Erlang, Elixir         | ❌                 | ❌           | ❌             | ✅                      |                                                                                  |
| Ivy                                                                                   | Java                   | ✅                 | ✅           | ✅             | ✅                      |                                                                                  |
| LibMan                                                                                | JavaScript             | ✅                 | ✅           | ✅             | ❌                      |                                                                                  |
| [Mendix Marketplace](https://marketplace.mendix.com/link/components)                  | Mendix                 | ✅                 | ✅           | ✅             | ✅                      |
| [Mendix managed dependencies](https://docs.mendix.com/refguide/managed-dependencies/) | Mendix                 | ✅                 | ✅           | ✅             | ✅                      |
| Maven                                                                                 | Java                   | ✅                 | ✅           | ✅             | ✅                      | [Instructions for publishing](../capabilities/osh-upload-instructions.md#maven)  |
| NPM                                                                                   | JavaScript, TypeScript | ✅                 | ✅           | ✅             | ✅                      |                                                                                  |
| NuGet                                                                                 | C#                     | ✅                 | ✅           | ✅             | ✅                      |                                                                                  |
| PNPM                                                                                  | JavaScript, TypeScript | ✅                 | ✅           | ✅             | ✅                      |                                                                                  |
| Poetry                                                                                | Python                 | ✅                 | ✅           | ✅             | ✅                      | [Instructions for publishing](../capabilities/osh-upload-instructions.md#poetry) |
| pub.dev                                                                               | Dart, Flutter          | ✅                 | ❌           | ✅             | ❌                      |                                                                                  |
| PuppetForge                                                                           | Puppet                 | ❌                 | ✅           | ✅             | ❌                      |                                                                                  |
| PyPi                                                                                  | Python                 | ✅                 | ✅           | ✅             | ✅                      |                                                                                  |
| Python `pyproject.toml`                                                               | Python                 | ✅                 | ✅           | ✅             | ✅                      | [Instructions for publishing](../capabilities/osh-upload-instructions.md#python) |
| RubyGems                                                                              | Ruby                   | ✅                 | ✅           | ✅             | ✅                      |                                                                                  |
| SBT                                                                                   | Scala                  | ✅                 | ✅           | ✅             | ✅                      |                                                                                  |
| SwiftPM                                                                               | Swift                  | ❌                 | ✅           | ✅             | ❌                      |                                                                                  |
| UV                                                                                    | Python                 | ✅                 | ✅           | ✅             | ✅                      | [Instructions for publishing](../capabilities/osh-upload-instructions.md#python) |
| Unmanaged JAR files                                                                   | Java                   |                    |              |                |                         |                                                                                  |
| Unmanaged DLL files                                                                   | C#                     |                    |              |                |                         |                                                                                  |
| Unmanaged JS files                                                                    | JavaScript             |                    |              |                |                         |                                                                                  |

## Supported security analyzers

These are the supported security analyzers as you may see them in your security findings overview. You can use the literal text in the `Display name` below to enable or disable specific analyzers, if deemed necessary. For such configuration, see the [Security/Third Party Findings section section on the system security page](../reference/analysis-scope-configuration.md#third-party-findings).

Note this section only described *third party* security analysis analyzers. The results from these analyzers are then combined with the results from Sigrid's own security ruleset before being displayed.

| Display name           | Technologies                      | Notes                                         | Supports Sigrid CI |
|------------------------|-----------------------------------|-----------------------------------------------|--------------------|
| Bandit                 | Python                            |                                               | ✅                 |
| Checkmarx              | (many)                            | Requires *Sigrid Security Checkmarx* license. | ❌                 |
| ErrorProne.NET         | C#                                | Requires compiling code.                      | ✅                 |
| ESLint                 | JavaScript, TypeScript            |                                               | ✅                 |
| FB Contrib             | Java                              |                                               | ✅                 |
| FindSecBugs            | Java                              |                                               | ✅                 |
| FlawFinder             | C                                 |                                               | ✅                 |
| Google ErrorProne      | Java                              | Requires compiling code.                      | ✅                 |
| Gosec                  | Go                                |                                               | ✅                 |
| KICS                   | Docker, Ansible, Kubernetes, etc. |                                               | ✅                 |
| Microsoft Code Quality | C#                                | Requires compiling code.                      | ✅                 |
| MobSF                  | Android                           |                                               | ✅                 |
| MultithreadingAnalyzer | C#                                | Requires compiling code.                      | ✅                 |
| NodeJS Scan            | JavaScript, TypeScript            |                                               | ✅                 |
| Puma Security          | C#                                | Requires compiling code.                      | ✅                 |
| SecurityCodeScan       | C#                                | Requires compiling code.                      | ✅                 |
| SonarQube (C#)         | C#                                | Requires compiling code.                      | ✅                 |
| SonarQube (Java)       | Java                              | Requires compiling code.                      | ✅                 | 
| SpotBugs               | Java                              |                                               | ✅                 |
| SemGrep                | (many)                            |                                               | ✅                 |
| VMWare CSA             | Java, C#, configuration           | Cloud Suitability Analyzer.                   | ✅                 |

## Supported software quality standards

| Software quality standard                                                                                          | Relevant for capabilities                            |
|--------------------------------------------------------------------------------------------------------------------|------------------------------------------------------|
| [ISO 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010)                                       | Maintainability, Architecture, Security, Reliability |
| [SIG Security Model](https://softwareimprovementgroup.com/wp-content/uploads/SIG-Evaluation-Criteria-Security.pdf) | Security                                             |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/)                                                             | Security                                             |
| [ISO 5055](https://www.iso.org/standard/80623.html)                                                                | Security, Reliability                                |
| [CWE Top 25](https://cwe.mitre.org/top25/)                                                                         | Security                                             |
| [PCI DSS 4.0](https://blog.pcisecuritystandards.org/pci-dss-v4-0-resource-hub)                                     | Security                                             |
| [OWASP ASVS 4.0](https://owasp.org/www-pdf-archive/OWASP_Application_Security_Verification_Standard_4.0-en.pdf)    | Security                                             |
| [OWASP Low-code/No-code Top 10](https://owasp.org/www-project-top-10-low-code-no-code-security-risks/)             | Security                                             |

## Requesting additional technology support

Even with 300+ supported technologies, we are still continuously working on adding support for new technologies and frameworks and updating our technology support for new technology versions. You can contact us using the information provided below if you believe we should extend technology support for your organization.

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.
