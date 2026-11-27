Technology support
==================

This page provides an overview of all technologies that can be analyzed by Sigrid for its various capabilities. 

## List of supported technologies

- The second column refers to how the technology is named in Sigrid's [scope configuration file](../reference/analysis-scope-configuration.md).
- The "auto-detect" column indicates whether Sigrid is able to automatically detect this technology. If this is *not* the case, indicated by an ⚠️, Sigrid *does* support this technology, but you will need to [configure it manually](analysis-scope-configuration.md#manual-technology-configuration).
- The column "supported Sigrid capabilities" does *not* list Open Source Health. The reason is that Open Source Health is based on open source ecosystems, not specific technologies. Refer to the section on [supported technologies for Open Source Health](#supported-open-source-ecosystems) for more information.
- In the list of supported capabilities:
  - "AI explanations" indicates the technologies for which Sigrid offers (static) explanations on findings.
  - "AI detection" indicates technologies supported by [AI Generated Code Detection](../capabilities/system-ai-governance.md#technology-support).

<a>Sigrid (296)</a> \| <a>Sigrid Axis (251)</a> \| <a>Sigrid Local (249)</a>
{: .technologySupportCategories }

| Technology name                        | Name in configuration file    | Auto-detect | Supported Sigrid capabilities                                          | Notes                                       |
|----------------------------------------|-------------------------------|-------------|------------------------------------------------------------------------|---------------------------------------------|
| ABAP (SAP)                             | `abap`                        | ✅          | Maintainability, AI explanations                                       |
| ABAP Core Data Services                | `abapcds`                     | ✅          | Maintainability                                                        |
| ABAP SmartForms                        | `abapsmartforms`              | ⚠️          | Maintainability, Architecture                                          |
| Abl (OpenEdge)                         | `abl`                         | ✅          | Maintainability, Architecture, AI explanations                         |
| ACL                                    | `acl`                         | ✅          | Maintainability                                                        |
| Accell                                 | `accell`                      | ✅          | Maintainability, Architecture                                          |
| ActionScript                           | `actionscript`                | ⚠️          | Maintainability, Architecture                                          |
| ActionScript 3                         | `actionscript3`               | ✅          | Maintainability, Architecture                                          |
| Ada                                    | `ada`                         | ✅          | Maintainability, Architecture                                          |
| Adabas Natural                         | `adabasnatural`               | ⚠️          | Maintainability, Architecture                                          |
| ADF XML                                | `adfxml`                      | ⚠️          | Maintainability                                                        |
| AgilePoint                             | `agilepoint`                  | ⚠️          | Maintainability, Architecture                                          |
| Altova UML                             | `altovauml`                   | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Ansible                                | `ansible`                     | ✅          | Maintainability, Security                                              |
| Apache Camel                           | `apachecamel`                 | ✅          | Maintainability, Architecture                                          |
| Oracle APEX                            | `apex`                        | ⚠️          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| APS                                    | `aps`                         | ✅          | Maintainability, Architecture                                          |
| Application Master                     | `applicationmaster`           | ✅          | Maintainability, Architecture                                          |
| ArtosScript (ash)                      | `ash`                         | ⚠️          | Maintainability, Architecture                                          |
| ASP                                    | `asp`                         | ✅          | Maintainability, Architecture                                          |
| ASP.NET                                | `aspx`                        | ✅          | Maintainability, Architecture, Security [(7)](#notes), AI explanations |
| Assembly                               | `assembly`                    | ✅          | Maintainability, Architecture                                          |
| Aura                                   | `aura`                        | ✅          | Maintainability, Architecture                                          |
| Axway                                  | `axway`                       | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| AxyStudio functions                    | `axystudio`                   | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| AxyStudio workflows                    | `axyworkflow`                 | ✅          | Maintainability, Architecture                                          |
| Baan                                   | `baan`                        | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| BASIC                                  | `basic`                       | ⚠️          | Maintainability, Architecture                                          |
| Batch                                  | `batch`                       | ✅          | Maintainability, Architecture                                          |
| BeanShell                              | `beanshell`                   | ✅          | Maintainability                                                        |
| Be Informed case management            | `beinformed`                  | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Be Informed knowledge models           | `beinformedknowledgemodels`   | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| BizTalk                                | `biztalk`                     | ✅          | Maintainability, Architecture                                          |
| BizTalk Rules Engine                   | `biztalkrules`                | ✅          | Maintainability                                                        |
| Blaze BRM                              | `blazerules`                  | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| Blue Prism                             | `blueprism`                   | ✅          | Maintainability, Architecture                                          |
| Blueriq flows/processes                | `blueriq`                     | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Blueriq expressions                    | `blueriqexpressions`          | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| BPEL                                   | `bpel`                        | ✅          | Maintainability, Architecture                                          |
| BPMN                                   | `bpm`                         | ⚠️          | Maintainability, Architecture                                          |
| Brail                                  | `brail`                       | ✅          | Maintainability                                                        |
| Bsp                                    | `bsp`                         | ✅          | Maintainability, Architecture                                          |
| C                                      | `c`                           | ✅          | Maintainability, Architecture, Security, AI explanations               |
| Cache                                  | `cache`                       | ⚠️          | Maintainability, Architecture                                          |
| Cache ObjectScript                     | `cacheobjectscript`           | ✅          | Maintainability, Architecture                                          |
| CCL                                    | `ccl`                         | ⚠️          | Maintainability, Architecture                                          |
| CGDC                                   | `cgdc`                        | ⚠️          | Maintainability, Architecture                                          |
| CGT                                    | `cgt`                         | ✅          | Maintainability, Architecture                                          |
| Cicode                                 | `cicode`                      | ✅          | Maintainability, Architecture                                          |
| CL                                     | `cl`                          | ⚠️          | Maintainability, Architecture                                          |
| Clearbasic                             | `clearbasic`                  | ✅          | Maintainability, Architecture                                          |
| Clojure                                | `clojure`                     | ✅          | Maintainability                                                        |
| Cobol                                  | `cobol`                       | ✅          | Maintainability, Architecture, AI explanations                         |
| CoffeeScript                           | `coffeescript`                | ✅          | Maintainability, Architecture                                          |
| ColdFusion                             | `coldfusion`                  | ✅          | Maintainability, Architecture                                          |
| Configuration                          | `configuration`               | ✅          | Maintainability                                                        | [(5)](#notes)                               |
| CoolGen C                              | `coolgenc`                    | ⚠️          | Maintainability, Architecture                                          |
| CoolGen Cobol                          | `coolgencobol`                | ⚠️          | Maintainability, Architecture                                          |
| C++                                    | `cpp`                         | ✅          | Maintainability, Architecture, Security, AI explanations, AI detection |
| C#                                     | `csharp`                      | ✅          | Maintainability, Architecture, Security, AI explanations, AI detection |
| CSP                                    | `csp`                         | ✅          | Maintainability, Architecture                                          |
| CSS                                    | `css`                         | ✅          | Maintainability, Architecture, AI explanations                         |
| Cypher                                 | `cypher`                      | ✅          | Maintainability, Architecture                                          |
| Cucumber                               | `cucumber`                    | ✅          | Maintainability, Architecture                                          |
| Dart (includes Flutter)                | `dart`                        | ✅          | Maintainability, Architecture, AI explanations                         |
| Datastage                              | `datastage`                   | ✅          | Maintainability, Architecture                                          |
| DatastageETL                           | `datastageetl`                | ✅          | Maintainability, Architecture                                          |
| DatastageWorkflow                      | `datastageworkflow`           | ✅          | Maintainability, Architecture                                          |
| DB2                                    | `db2`                         | ⚠️          | Maintainability, Architecture                                          |
| Dcl                                    | `dcl`                         | ✅          | Maintainability, Architecture                                          |
| Delphi                                 | `delphi`                      | ✅          | Maintainability, Architecture, AI explanations                         |
| Delphi Forms                           | `delphiforms`                 | ✅          | Maintainability, Architecture                                          |
| Delta/Cobol                            | `deltacobol`                  | ✅          | Maintainability, Architecture                                          |
| Docker                                 | `docker`                      | ✅          | Maintainability, Architecture, Security, AI explanations               |
| Documentum xCP                         | `documentumxcp`               | ✅          | Maintainability, Architecture                                          |
| Drools                                 | `drools`                      | ✅          | Maintainability                                                        |
| Dscript                                | `dscript`                     | ✅          | Maintainability                                                        |
| Easytrieve                             | `easytrieve`                  | ✅          | Maintainability, Architecture                                          |
| EGL                                    | `egl`                         | ✅          | Maintainability, Architecture                                          |
| EJS                                    | `ejs`                         | ✅          | Maintainability, Architecture                                          |
| Elixir                                 | `elixir`                      | ✅          | Maintainability, Architecture, AI explanations                         |
| C++ Embedded SQL                       | `embeddedsql`                 | ⚠️          | Maintainability, Architecture                                          |
| ERB                                    | `erb`                         | ✅          | Maintainability, Architecture                                          |
| Erlang                                 | `erlang`                      | ✅          | Maintainability, Security                                              |
| ESQL                                   | `esql`                        | ✅          | Maintainability, Architecture                                          |
| File Tab                               | `filetab`                     | ✅          | Maintainability                                                        |
| Finacle                                | `finacle`                     | ⚠️          | Maintainability, Architecture                                          |
| Freeformat Cobol                       | `freeformatcobol`             | ⚠️          | Maintainability, Architecture                                          |
| Freemarker                             | `freemarker`                  | ✅          | Maintainability, Architecture                                          |
| FME                                    | `fme`                         | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| FORTRAN                                | `fortran`                     | ✅          | Maintainability, Architecture                                          |
| Gensym                                 | `gensym`                      | ✅          | Maintainability, Architecture                                          |
| gRPC                                   | `grpc`                        | ✅          | Maintainability, Architecture                                          |
| Go (AKA GoLang)                        | `go`                          | ✅          | Maintainability, Architecture, AI explanations                         |
| Gosu                                   | `gosu`                        | ⚠️          | Maintainability, Architecture, Security                                |
| Groovy                                 | `groovy`                      | ✅          | Maintainability, Architecture, Security, AI explanations               |
| GSP                                    | `gsp`                         | ✅          | Maintainability, Architecture                                          |
| GUI Definition                         | `guidefinition`               | ✅          | Maintainability                                                        | [(5)](#notes)                               |
| Gupta                                  | `gupta`                       | ✅          | Maintainability, Architecture                                          |
| Haml                                   | `haml`                        | ✅          | Maintainability, Architecture                                          |
| HTML                                   | `html`                        | ✅          | Maintainability, Architecture                                          | [(7)](#notes)                               |
| HQL                                    | `hql`                         | ✅          | Maintainability, Architecture                                          |
| IBM ACE                                | `ibmace`                      | ✅          | Maintainability                                                        |
| IBM BPM (BPD)                          | `ibmbpmbpd`                   | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| IBM BPM (Process)                      | `ibmbpmprocess`               | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Ideal                                  | `ideal`                       | ✅          | Maintainability, Architecture                                          |
| Informatica                            | `informatica`                 | ✅          | Maintainability                                                        |
| Informix 4GL                           | `informix4gl`                 | ✅          | Maintainability, Architecture                                          |
| Informix SQL                           | `informixsql`                 | ⚠️          | Maintainability, Architecture                                          |
| Ingres                                 | `ingres`                      | ⚠️          | Maintainability                                                        |
| Intershop (Pipeline)                   | `intershoppipeline`           | ⚠️          | Maintainability, Architecture                                          |
| Jasper Reports                         | `jasperreports`               | ✅          | Maintainability, Architecture                                          |
| Jade                                   | `jade`                        | ✅          | Maintainability, Architecture                                          |
| Java                                   | `java`                        | ✅          | Maintainability, Architecture, Security, AI explanations, AI detection |
| Java FX                                | `javafx`                      | ✅          | Maintainability, Architecture                                          |
| JavaScript (includes NodeJS)           | `javascript`                  | ✅          | Maintainability, Architecture, Security, AI explanations               | [(3)](#notes)                               | 
| JBC                                    | `jbc`                         | ✅          | Maintainability, Architecture                                          |
| jBPM                                   | `jbpm`                        | ✅          | Maintainability, Architecture                                          |
| JCL                                    | `jcl`                         | ✅          | Maintainability, Architecture                                          |
| JCS                                    | `jcs`                         | ✅          | Maintainability, Architecture                                          |
| JDE                                    | `jde`                         | ✅          | Maintainability                                                        |
| Jinja                                  | `jinja`                       | ✅          | Maintainability, Architecture                                          |
| JSF                                    | `jsf`                         | ✅          | Maintainability, Architecture                                          |
| JSON                                   | `json`                        | ✅          | Maintainability, Architecture                                          | [(5)](#notes)                               |
| JSP                                    | `jsp`                         | ✅          | Maintainability, Architecture, Security [(7)](#notes), AI explanations |
| Kotlin                                 | `kotlin`                      | ✅          | Maintainability, Architecture, Security, AI explanations, AI detection |
| Less                                   | `less`                        | ✅          | Maintainability, Architecture                                          |
| LINC                                   | `linc`                        | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Lion                                   | `lion`                        | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Lodestar                               | `lodestar`                    | ✅          | Maintainability, Architecture                                          |
| Logic Apps                             | `logicapps`                   | ⚠️          | Maintainability                                                        |
| LogicNets                              | `logicnets`                   | ✅          | Maintainability, Architecture                                          |
| LotusScript                            | `lotusscript`                 | ✅          | Maintainability, Architecture                                          |
| Lua                                    | `lua`                         | ✅          | Maintainability, Architecture, AI explanations                         |
| Magic                                  | `magic`                       | ✅          | Maintainability, Architecture                                          |
| Magik                                  | `magik`                       | ✅          | Maintainability, Architecture                                          |
| Magnum                                 | `magnum`                      | ✅          | Maintainability, Architecture                                          |
| Matlab                                 | `matlab`                      | ⚠️          | Maintainability, Architecture                                          |
| Mediation Flows                        | `mediationflows`              | ✅          | Maintainability, Architecture                                          |
| Mendix                                 | `mendix`                      | ✅          | Maintainability, Architecture, Security, AI explanations               | [(9)](#notes), [(4)](#notes)                |
| Mendix microflows/nanoflows            | `mendixflow`                  | ✅          | Maintainability, Architecture, Security                                | [(11)](#notes)                              |
| MessageBuilder                         | `messagebuilder`              | ✅          | Maintainability, Architecture                                          |
| MPS Behavior                           | `mpsbehavior`                 | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| MPS Class                              | `mpsclass`                    | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| MPS Translator                         | `mpstranslator`               | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| Mule                                   | `mule`                        | ✅          | Maintainability, Architecture                                          |
| MtWize                                 | `mtwize`                      | ✅          | Maintainability, Architecture                                          |
| Murex Data Dictionary                  | `murexdatadictionary`         | ✅          | Maintainability, Architecture                                          |
| Murex Lookup Table                     | `murexlookuptable`            | ✅          | Maintainability, Architecture                                          |
| Murex Script                           | `murexscript`                 | ✅          | Maintainability, Architecture                                          |
| Murex Workflow                         | `murexworkflow`               | ✅          | Maintainability, Architecture                                          |
| Mustache (includes Handlebars)         | `mustache`                    | ✅          | Maintainability, Architecture                                          |
| Nabsic                                 | `nabsic`                      | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| NavaScript                             | `navascript`                  | ✅          | Maintainability                                                        |
| Naviscript                             | `naviscript`                  | ⚠️          | Maintainability, Architecture                                          |
| Navision (AKA Dynamics NAV, AL)        | `navision`                    | ✅          | Maintainability, Architecture                                          |
| NetIQ IDM Policy                       | `netiqidmpolicy`              | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| NetIQ IDM Request                      | `netiqidmrequest`             | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| NetIQ IDM Workflow                     | `netiqidmworkflow`            | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| NetweaverIDM                           | `netweaveridm`                | ✅          | Maintainability, Architecture                                          |
| Nonstop SQL                            | `nonstopsql`                  | ✅          | Maintainability, Architecture                                          |
| Normalized Systems Java                | `normalizedsystemsjava`       | ✅          | Maintainability, Architecture                                          |
| Normalized Systems JavaScript          | `normalizedsystemsjavascript` | ✅          | Maintainability                                                        |
| Normalized Systems Model               | `normalizedsystemsmodel`      | ✅          | Maintainability, Architecture                                          |
| Normalized Systems TypeScript          | `normalizedsystemstypescript` | ✅          | Maintainability                                                        |
| Objective-C                            | `objectivec`                  | ✅          | Maintainability, Architecture, AI explanations                         |
| ODI                                    | `odi`                         | ⚠️          | Maintainability, Architecture                                          |
| ODM                                    | `odm`                         | ✅          | Maintainability, Architecture                                          |
| OMT                                    | `omt`                         | ✅          | Maintainability, Architecture                                          |
| OPA                                    | `opa`                         | ✅          | Maintainability, Architecture                                          |
| OPC                                    | `opc`                         | ✅          | Maintainability                                                        |
| OpenROAD 4GL                           | `openroad`                    | ⚠️          | Maintainability                                                        |
| Oracle BPM                             | `oraclebpm`                   | ✅          | Maintainability, Architecture                                          |
| Oracle OFSAA                           | `oracleofsaa`                 | ✅          | Maintainability, Architecture                                          |
| Oracle Workflow                        | `oracleworkflow`              | ✅          | Maintainability, Architecture                                          |
| ORDS                                   | `ords`                        | ⚠️          | Maintainability                                                        |
| OSB                                    | `osb`                         | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| OSB Proxy                              | `osbproxy`                    | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| OSM Process                            | `osmprocess`                  | ⚠️          | Maintainability, Architecture                                          |
| OSM Task                               | `osmtask`                     | ✅          | Maintainability, Architecture                                          |
| OutSystems                             | `outsystems`                  | ✅          | Maintainability, Architecture                                          | [(1)](#notes), [(4)](#notes), [(9)](#notes) |
| Pascal                                 | `pascal`                      | ⚠️          | Maintainability, Architecture                                          |
| Pega                                   | `pega`                        | ✅          | Maintainability                                                        | [(1)](#notes), [(9)](#notes)                |
| Perl                                   | `perl`                        | ✅          | Maintainability, Architecture, Security [(7)](#notes)                  |
| PHP                                    | `php`                         | ✅          | Maintainability, Architecture, Security, AI explanations, AI detection |
| PLC                                    | `plc`                         | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| PLC Functional Block Diagram           | `plcfbd`                      | ✅          | Maintainability                                                        |
| PLC Instruction List                   | `plcil`                       | ✅          | Maintainability                                                        |
| PLC Ladder Diagram                     | `plcld`                       | ✅          | Maintainability                                                        |
| PLC Sequential Function Chart          | `plcsfc`                      | ✅          | Maintainability                                                        |
| PLC Structured Text                    | `plcst`                       | ✅          | Maintainability                                                        |
| PL/I                                   | `pli`                         | ✅          | Maintainability, Architecture                                          |
| Oracle PL/SQL                          | `plsql`                       | ✅          | Maintainability, Architecture, AI explanations                         |
| Oracle PL/SQL Forms                    | `plsqlforms`                  | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| Oracle PL/SQL Reports                  | `plsqlreports`                | ✅          | Maintainability                                                        |
| PLUK                                   | `pluk`                        | ✅          | Maintainability, Architecture                                          |
| Polymer Templates                      | `polymertemplates`            | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Powerbuilder                           | `powerbuilder`                | ✅          | Maintainability, Architecture                                          |
| PowerCenter                            | `powercenter`                 | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Power Fx (AKA Microsoft Power Apps)    | `powerfx`                     | ✅          | Maintainability                                                        |
| Powershell                             | `powershell`                  | ✅          | Maintainability, Architecture, AI explanations                         |
| Progress (OpenEdge)                    | `progress`                    | ✅          | Maintainability, Architecture, Security, AI explanations               |
| PRT                                    | `prt`                         | ✅          | Maintainability                                                        |
| Puppet                                 | `puppet`                      | ✅          | Maintainability, Architecture                                          |
| Python                                 | `python`                      | ✅          | Maintainability, Architecture, Security, AI explanations, AI detection |
| R                                      | `r`                           | ✅          | Maintainability, Architecture                                          |
| Radience                               | `radience`                    | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Razor                                  | `razor`                       | ✅          | Maintainability, Architecture, AI explanations                         |
| ALEF Regelspraak                       | `regelspraak`                 | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| ALEF Regelspraak (HTML export)         | `regelspraakhtml`             | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Rexx                                   | `rexx`                        | ⚠️          | Maintainability, Architecture                                          |
| Robot                                  | `robot`                       | ✅          | Maintainability                                                        |
| RPG                                    | `rpg`                         | ✅          | Maintainability, Architecture                                          |
| Ruby (includes Ruby on Rails)          | `ruby`                        | ✅          | Maintainability, Architecture, Security, AI explanations               |
| Rust                                   | `rust`                        | ✅          | Maintainability, Architecture, AI explanations                         | [(4)](#notes), [(8)](#notes)                |
| Salesforce Apex                        | `salesforceapex`              | ✅          | Maintainability, Architecture                                          |
| Salesforce Flow                        | `salesforceflow`              | ✅          | Maintainability, Architecture                                          |
| Salesforce Process Builder             | `salesforceprocessbuilder`    | ✅          | Maintainability                                                        |
| SAP PO                                 | `sappo`                       | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| SAS                                    | `sas`                         | ✅          | Maintainability, Architecture                                          |
| SAS Flows                              | `sasflows`                    | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| Sass                                   | `sass`                        | ✅          | Maintainability, Architecture, AI explanations                         |
| Scala                                  | `scala`                       | ✅          | Maintainability, Architecture, Security, AI explanations               |
| SCL                                    | `scl`                         | ⚠️          | Maintainability, Architecture                                          |
| SCR                                    | `scr`                         | ✅          | Maintainability, Architecture                                          |
| Shell script                           | `script`                      | ✅          | Maintainability, Architecture                                          |
| ServiceNow                             | `servicenow`                  | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Siebel Declarative                     | `siebeldeclarative`           | ⚠️          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Siebel JS                              | `siebeljs`                    | ⚠️          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Siebel Scripted                        | `siebelscripted`              | ⚠️          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Siebel Workflow                        | `siebelworkflow`              | ⚠️          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Siebel TBUI                            | `siebeltbui`                  | ⚠️          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Slim                                   | `slim`                        | ✅          | Maintainability                                                        |
| Smalltalk                              | `smalltalk`                   | ⚠️          | Maintainability, Architecture                                          |
| Solidity                               | `solidity`                    | ✅          | Maintainability, Architecture                                          |
| Sonic ESB                              | `sonicesb`                    | ✅          | Maintainability, Architecture                                          |
| SPL                                    | `spl`                         | ✅          | Maintainability                                                        |
| SQLJ                                   | `sqlj`                        | ✅          | Maintainability, Architecture                                          |
| SQR                                    | `sqr`                         | ⚠️          | Maintainability, Architecture                                          |
| SSIS                                   | `ssis`                        | ✅          | Maintainability, Architecture                                          |
| StarLIMS                               | `starlimssql`                 | ✅          | Maintainability, Architecture                                          |
| StreamServe                            | `streamserve`                 | ✅          | Maintainability, Architecture                                          |
| Synapse                                | `synapse`                     | ⚠️          | Maintainability                                                        |
| Synon                                  | `synon`                       | ✅          | Maintainability, Architecture                                          |
| Swift                                  | `swift`                       | ✅          | Maintainability, Architecture, Security, AI explanations, AI detection |
| T4                                     | `t4`                          | ✅          | Maintainability                                                        |
| TACL                                   | `tacl`                        | ✅          | Maintainability, Architecture                                          |
| TAL                                    | `tal`                         | ✅          | Maintainability                                                        |
| Tandem                                 | `tandem`                      | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Tapestry                               | `tapestry`                    | ✅          | Maintainability, Architecture                                          |
| Terraform                              | `terraform`                   | ✅          | Maintainability, Architecture, Security, AI explanations               |
| Thrift                                 | `thrift`                      | ✅          | Maintainability, Architecture                                          |
| Thymeleaf                              | `thymeleaf`                   | ✅          | Maintainability, Architecture                                          |
| TIBCO BW                               | `tibco`                       | ✅          | Maintainability, Architecture                                          |
| TIBCO BE (XML)                         | `tibcobe`                     | ✅          | Maintainability, Architecture                                          |
| TIBCO BE (Java)                        | `tibcobejava`                 | ✅          | Maintainability, Architecture                                          |
| TIBCO BE (State Machine)               | `tibcobestatemachine`         | ✅          | Maintainability, Architecture                                          |
| TIBCO BW6                              | `tibcobw6`                    | ✅          | Maintainability, Architecture                                          |
| TriplEforms                            | `tripleforms`                 | ✅          | Maintainability                                                        |
| TRS                                    | `trs`                         | ✅          | Maintainability                                                        | [(4)](#notes), [(8)](#notes)                |
| T-SQL (Microsoft SQL Server, MS SQL))  | `tsql`                        | ✅          | Maintainability, Architecture, AI explanations                         |
| Turtle                                 | `turtle`                      | ✅          | Maintainability                                                        |
| Twig                                   | `twig`                        | ✅          | Maintainability                                                        |
| TypeScript (includes React/TypeScript) | `typescript`                  | ✅          | Maintainability, Architecture, Security, AI explanations, AI detection | [(10)](#notes)                              |
| UIL (Motif)                            | `uil`                         | ✅          | Maintainability, Architecture                                          |
| Uniface                                | `uniface`                     | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Until                                  | `until`                       | ⚠️          | Maintainability, Architecture                                          |
| Visual Age                             | `vag`                         | ✅          | Maintainability, Architecture                                          |
| Visual Age Record                      | `vagrecord`                   | ✅          | Maintainability, Architecture                                          |
| Visual Basic                           | `vb`                          | ✅          | Maintainability, Architecture, Security [(7)](#notes), AI explanations |
| Visual Basic .NET                      | `vbnet`                       | ✅          | Maintainability, Architecture, Security [(7)](#notes), AI explanations |
| Velocity                               | `velocity`                    | ✅          | Maintainability, Architecture                                          |
| VGL                                    | `vgl`                         | ✅          | Maintainability                                                        |
| VisualForce                            | `visualforce`                 | ✅          | Maintainability                                                        |
| Visual FoxPro                          | `visualfoxpro`                | ⚠️          | Maintainability                                                        |
| Visual RPG                             | `visualrpg`                   | ✅          | Maintainability, Architecture                                          |
| Visual Objects                         | `visualobjects`               | ⚠️          | Maintainability, Architecture                                          |
| Vue                                    | `vue`                         | ✅          | Maintainability, Architecture, Security, AI explanations, AI detection | [(2)](#notes)                               |
| Vulcan.NET                             | `vulcan`                      | ⚠️          | Maintainability, Architecture                                          |
| WebFocus                               | `webfocus`                    | ✅          | Maintainability, Architecture                                          |
| WebMethods                             | `webmethods`                  | ✅          | Maintainability, Architecture                                          |
| WebSmart                               | `websmart`                    | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| WebSmart Panels                        | `websmartpanels`              | ✅          | Maintainability                                                        |
| Wonderware                             | `wonderware`                  | ✅          | Maintainability                                                        |
| WSDL                                   | `wsdl`                        | ✅          | Maintainability, Architecture                                          |
| WTX                                    | `wtx`                         | ⚠️          | Maintainability                                                        |
| XAML                                   | `xaml`                        | ✅          | Maintainability, Architecture                                          |
| XML                                    | `xml`                         | ✅          | Maintainability, Architecture                                          | [(5)](#notes)                               |
| Tibco ActiveMatrix BPM                 | `xpdl`                        | ✅          | Maintainability                                                        |
| X++ AX                                 | `xpp`                         | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| X++ for Dynamics 365                   | `xpp365`                      | ✅          | Maintainability, Architecture                                          | [(4)](#notes), [(8)](#notes)                |
| Xquery                                 | `xquery`                      | ✅          | Maintainability, Architecture                                          |
| XSD                                    | `xsd`                         | ✅          | Maintainability, Architecture                                          |
| XSLT                                   | `xslt`                        | ✅          | Maintainability, Architecture                                          |
| XUL                                    | `xul`                         | ✅          | Maintainability                                                        |
| YAML                                   | `yaml`                        | ✅          | Maintainability, Architecture                                          | [(5)](#notes)                               |
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
