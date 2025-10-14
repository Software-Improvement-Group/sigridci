Technology support
==================

This page provides an overview of all technologies that can be analyzed by Sigrid for its various capabilities. 

## List of supported technologies

- The first column refers to how the technology is named in Sigrid's [scope configuration file](../reference/analysis-scope-configuration.md#technology-support).
- The column "supported Sigrid capabilities" does *not* list Open Source Health. The reason is that Open Source Health is based on open source ecosystems, not specific technologies. Refer to the section on [supported technologies for Open Source Health](#supported-open-source-ecosystems) for more information.
- In the list of supported capabilities, "AI" indicates Sigrid offer AI-generated explanations related to findings, which makes them more actionable and easier to understand.

<a>Sigrid</a> \| <a>On-premise Sigrid</a> \| <a>Sigrid Local</a>
{: .technologySupportCategories }

| Name in configuration file    | Technology name(s)                     | Supported Sigrid capabilities               | Notes                                       |
|-------------------------------|----------------------------------------|---------------------------------------------|---------------------------------------------|
| `abap`                        | ABAP (SAP)                             | Maintainability, AI                         |
| `abapcds`                     | ABAP Core Data Services                | Maintainability                             |
| `abapsmartforms`              | ABAP SmartForms                        | Maintainability, Architecture               |
| `abl`                         | Abl (OpenEdge)                         | Maintainability, Architecture, AI           |
| `acl`                         | ACL                                    | Maintainability                             |
| `accell`                      | Accell                                 | Maintainability, Architecture               |
| `actionscript`                | ActionScript                           | Maintainability, Architecture               |
| `actionscript3`               | ActionScript 3                         | Maintainability, Architecture               |
| `ada`                         | Ada                                    | Maintainability, Architecture               |
| `adabasnatural`               | Adabas Natural                         | Maintainability, Architecture               |
| `adfxml`                      | ADF XML                                | Maintainability,                            |
| `agilepoint`                  | AgilePoint                             | Maintainability, Architecture               |
| `altovauml`                   | Altova UML                             | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `angularjstemplate`           | Angular Templates                      | Maintainability, AI                         | [(7)](#notes)                               |
| `ansible`                     | Ansible                                | Maintainability, Security                   |
| `apachecamel`                 | Apache Camel                           | Maintainability, Architecture               |
| `apex`                        | Oracle APEX                            | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `aps`                         | APS                                    | Maintainability, Architecture               |
| `applicationmaster`           | Application Master                     | Maintainability, Architecture               |
| `ash`                         | ArtosScript (ash)                      | Maintainability, Architecture               |
| `asp`                         | ASP                                    | Maintainability, Architecture               |
| `aspx`                        | ASP.NET                                | Maintainability, Architecture, AI           |
| `assembly`                    | Assembly                               | Maintainability, Architecture               |
| `aura`                        | Aura                                   | Maintainability, Architecture               |
| `axway`                       | Axway                                  | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `axystudio`                   | AxyStudio functions                    | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `axyworkflow`                 | AxyStudio workflows                    | Maintainability, Architecture               |
| `baan`                        | Baan                                   | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `basic`                       | BASIC                                  | Maintainability, Architecture               |
| `batch`                       | Batch                                  | Maintainability, Architecture               |
| `beanshell`                   | BeanShell                              | Maintainability                             |
| `beinformed`                  | Be Informed case management            | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `beinformedknowledgemodels`   | Be Informed knowledge models           | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `biztalk`                     | BizTalk                                | Maintainability, Architecture               |
| `biztalkrules`                | BizTalk Rules Engine                   | Maintainability                             |
| `blazerules`                  | Blaze BRM                              | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `blueprism`                   | Blue Prism                             | Maintainability, Architecture               |
| `blueriq`                     | Blueriq flows/processes                | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `blueriqexpressions`          | Blueriq expressions                    | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `bpel`                        | BPEL                                   | Maintainability, Architecture               |
| `bpm`                         | BPMN                                   | Maintainability, Architecture               |
| `brail`                       | Brail                                  | Maintainability                             |
| `bsp`                         | Bsp                                    | Maintainability, Architecture               |
| `c`                           | C                                      | Maintainability, Architecture, Security, AI |
| `cache`                       | Cache                                  | Maintainability, Architecture               |
| `cacheobjectscript`           | Cache ObjectScript                     | Maintainability, Architecture               |
| `ccl`                         | CCL                                    | Maintainability, Architecture               |
| `cgdc`                        | CGDC                                   | Maintainability, Architecture               |
| `cgt`                         | CGT                                    | Maintainability, Architecture               |
| `cicode`                      | Cicode                                 | Maintainability, Architecture               |
| `cl`                          | CL                                     | Maintainability, Architecture               |
| `clearbasic`                  | Clearbasic                             | Maintainability, Architecture               |
| `cobol`                       | Cobol                                  | Maintainability, Architecture. AI           |
| `coffeescript`                | CoffeeScript                           | Maintainability, Architecture               |
| `coldfusion`                  | ColdFusion                             | Maintainability, Architecture               |
| `configuration`               | Configuration                          | Maintainability                             | [(5)](#notes)                               |
| `coolgenc`                    | CoolGen C                              | Maintainability, Architecture               |
| `coolgencobol`                | CoolGen Cobol                          | Maintainability, Architecture               |
| `cpp`                         | C++                                    | Maintainability, Architecture, Security, AI |
| `csharp`                      | C#                                     | Maintainability, Architecture, Security, AI |
| `csp`                         | CSP                                    | Maintainability, Architecture               |
| `css`                         | CSS                                    | Maintainability, Architecture               |
| `cypher`                      | Cypher                                 | Maintainability, Architecture               |
| `cucumber`                    | Cucumber                               | Maintainability, Architecture               |
| `dart`                        | Dart (includes Flutter)                | Maintainability, Architecture, AI           |
| `datastage`                   | Datastage                              | Maintainability, Architecture               |
| `datastageetl`                | DatastageETL                           | Maintainability, Architecture               |
| `datastageworkflow`           | DatastageWorkflow                      | Maintainability, Architecture               |
| `db2`                         | DB2                                    | Maintainability, Architecture               |
| `dcl`                         | Dcl                                    | Maintainability, Architecture               |
| `delphi`                      | Delphi                                 | Maintainability, Architecture, AI           |
| `delphiforms`                 | Delphi Forms                           | Maintainability, Architecture               |
| `deltacobol`                  | Delta/Cobol                            | Maintainability, Architecture               |
| `djangotemplates`             | Django Templates                       | Maintainability, Architecture               |
| `docker`                      | Docker                                 | Maintainability, Architecture, Security     |
| `documentumxcp`               | Documentum xCP                         | Maintainability, Architecture               |
| `drools`                      | Drools                                 | Maintainability                             |
| `dscript`                     | Dscript                                | Maintainability                             |
| `easytrieve`                  | Easytrieve                             | Maintainability, Architecture               |
| `egl`                         | EGL                                    | Maintainability, Architecture               |
| `ejs`                         | EJS                                    | Maintainability, Architecture               |
| `elixir`                      | Elixir                                 | Maintainability, Architecture, AI           |
| `embeddedsql`                 | C++ Embedded SQL                       | Maintainability, Architecture               |
| `erb`                         | ERB                                    | Maintainability, Architecture               |
| `esql`                        | ESQL                                   | Maintainability, Architecture               |
| `filetab`                     | File Tab                               | Maintainability                             |
| `finacle`                     | Finacle                                | Maintainability, Architecture               |
| `freeformatcobol`             | Freeformat Cobol                       | Maintainability, Architecture               |
| `freemarker`                  | Freemarker                             | Maintainability, Architecture               |
| `fme`                         | FME                                    | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `fortran`                     | FORTRAN                                | Maintainability, Architecture               |
| `gensym`                      | Gensym                                 | Maintainability, Architecture               |
| `grpc`                        | gRPC                                   | Maintainability, Architecture               |
| `go`                          | Go (AKA GoLang)                        | Maintainability, Architecture, AI           |
| `gosu`                        | Gosu                                   | Maintainability, Architecture, Security     |
| `groovy`                      | Groovy                                 | Maintainability, Architecture, Security, AI |
| `gsp`                         | GSP                                    | Maintainability, Architecture               |
| `guidefinition`               | GUI Definition                         | Maintainability                             | [(5)](#notes)                               |
| `gupta`                       | Gupta                                  | Maintainability, Architecture               |
| `haml`                        | Haml                                   | Maintainability, Architecture               |
| `html`                        | HTML                                   | Maintainability, Architecture               | [(7)](#notes)                               |
| `hql`                         | HQL                                    | Maintainability, Architecture               |
| `ibmace`                      | IBM ACE                                | Maintainability                             |
| `ibmbpmbpd`                   | IBM BPM (BPD)                          | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `ibmbpmprocess`               | IBM BPM (Process)                      | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `ideal`                       | Ideal                                  | Maintainability, Architecture               |
| `informatica`                 | Informatica                            | Maintainability                             |
| `informix4gl`                 | Informix 4GL                           | Maintainability, Architecture               |
| `informixsql`                 | Informix SQL                           | Maintainability, Architecture               |
| `ingres`                      | Ingres                                 | Maintainability                             |
| `intershoppipeline`           | Intershop (Pipeline)                   | Maintainability, Architecture               |
| `jasperreports`               | Jasper Reports                         | Maintainability, Architecture               |
| `jade`                        | Jade                                   | Maintainability, Architecture               |
| `java`                        | Java                                   | Maintainability, Architecture, Security, AI |
| `javafx`                      | Java FX                                | Maintainability, Architecture               |
| `javascript`                  | JavaScript (includes NodeJS)           | Maintainability, Architecture, Security     | [(2)](#notes)                               |
| `javascript`                  | Google App Script                      | Maintainability, Architecture, AI           |
| `jbc`                         | JBC                                    | Maintainability, Architecture               |
| `jbpm`                        | jBPM                                   | Maintainability, Architecture               |
| `jcl`                         | JCL                                    | Maintainability, Architecture               |
| `jcs`                         | JCS                                    | Maintainability, Architecture               |
| `jde`                         | JDE                                    | Maintainability                             |
| `jinja`                       | Jinja                                  | Maintainability, Architecture               |
| `jsf`                         | JSF                                    | Maintainability, Architecture               |
| `json`                        | JSON                                   | Maintainability, Architecture               | [(5)](#notes)                               |
| `jsp`                         | JSP                                    | Maintainability, Architecture               |
| `kotlin`                      | Kotlin                                 | Maintainability, Architecture, Security, AI |
| `less`                        | Less                                   | Maintainability, Architecture               |
| `linc`                        | LINC                                   | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `lion`                        | Lion                                   | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `lodestar`                    | Lodestar                               | Maintainability, Architecture               |
| `logicapps`                   | Logic Apps                             | Maintainability                             |
| `logicnets`                   | LogicNets                              | Maintainability, Architecture               |
| `lotusscript`                 | LotusScript                            | Maintainability, Architecture               |
| `lua`                         | Lua                                    | Maintainability, Architecture, AI           |
| `magic`                       | Magic                                  | Maintainability, Architecture               |
| `magik`                       | Magik                                  | Maintainability, Architecture               |
| `magnum`                      | Magnum                                 | Maintainability, Architecture               |
| `matlab`                      | Matlab                                 | Maintainability, Architecture               |
| `mediationflows`              | Mediation Flows                        | Maintainability, Architecture               |
| `mendix`                      | Mendix                                 | Maintainability, Architecture, Security     | [(9)](#notes), [(4)](#notes)                |
| `mendixflow`                  | Mendix microflows/nanoflows *(Beta)*   | Maintainability, Architecture, Security     | [(11)](#notes), [(4)](#notes)               |
| `messagebuilder`              | MessageBuilder                         | Maintainability, Architecture               |
| `mpsbehavior`                 | MPS Behavior                           | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `mpsclass`                    | MPS Class                              | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `mpstranslator`               | MPS Translator                         | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `mule`                        | Mule                                   | Maintainability, Architecture               |
| `mtwize`                      | MtWize                                 | Maintainability, Architecture               |
| `murexdatadictionary`         | Murex Data Dictionary                  | Maintainability, Architecture               |
| `murexlookuptable`            | Murex Lookup Table                     | Maintainability, Architecture               |
| `murexscript`                 | Murex Script                           | Maintainability, Architecture               |
| `murexworkflow`               | Murex Workflow                         | Maintainability, Architecture               |
| `mustache`                    | Mustache (includes Handlebars)         | Maintainability, Architecture               |
| `mysql`                       | MySQL                                  | Maintainability, Architecture               |
| `nabsic`                      | Nabsic                                 | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `naviscript`                  | Naviscript                             | Maintainability, Architecture               |
| `navision`                    | Navision (AKA Dynamics NAV, AL)        | Maintainability, Architecture               |
| `netiqidmpolicy`              | NetIQ IDM Policy                       | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `netiqidmrequest`             | NetIQ IDM Request                      | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `netiqidmworkflow`            | NetIQ IDM Workflow                     | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `netweaveridm`                | NetweaverIDM                           | Maintainability, Architecture               |
| `nonstopsql`                  | Nonstop SQL                            | Maintainability, Architecture               |
| `normalizedsystemsjava`       | Normalized Systems Java                | Maintainability, Architecture               |
| `normalizedsystemsjavascript` | Normalized Systems JavaScript          | Maintainability                             |
| `normalizedsystemsmodel`      | Normalized Systems Model               | Maintainability, Architecture               |
| `normalizedsystemstypescript` | Normalized Systems TypeScript          | Maintainability                             |
| `objectivec`                  | Objective-C                            | Maintainability, Architecture, AI           |
| `odi`                         | ODI                                    | Maintainability, Architecture               |
| `odm`                         | ODM                                    | Maintainability, Architecture               |
| `omt`                         | OMT                                    | Maintainability, Architecture               |
| `opa`                         | OPA                                    | Maintainability, Architecture               |
| `opc`                         | OPC                                    | Maintainability                             |
| `openroad`                    | OpenROAD 4GL                           | Maintainability                             |
| `oraclebpm`                   | Oracle BPM                             | Maintainability, Architecture               |
| `oracleofsaa`                 | Oracle OFSAA                           | Maintainability, Architecture               |
| `oracleworkflow`              | Oracle Workflow                        | Maintainability, Architecture               |
| `ords`                        | ORDS                                   | Maintainability                             |
| `osb`                         | OSB                                    | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `osbproxy`                    | OSB Proxy                              | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `osmprocess`                  | OSM Process                            | Maintainability, Architecture               |
| `osmtask`                     | OSM Task                               | Maintainability, Architecture               |
| `outsystems`                  | OutSystems                             | Maintainability, Architecture               | [(1)](#notes), [(4)](#notes), [(9)](#notes) |
| `pascal`                      | Pascal                                 | Maintainability, Architecture               |
| `pega`                        | Pega                                   | Maintainability                             | [(1)](#notes), [(9)](#notes)                |
| `pegajsp`                     | PEGA JSP                               | Maintainability                             | [(9)](#notes)                               |
| `perl`                        | Perl                                   | Maintainability, Architecture, Security     |
| `php`                         | PHP                                    | Maintainability, Architecture, Security     |
| `plc`                         | PLC                                    | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `plcfbd`                      | PLC Functional Block Diagram           | Maintainability                             |
| `plcil`                       | PLC Instruction List                   | Maintainability                             |
| `plcld`                       | PLC Ladder Diagram                     | Maintainability                             |
| `plcsfc`                      | PLC Sequential Function Chart          | Maintainability                             |
| `plcst`                       | PLC Structured Text                    | Maintainability                             |
| `pli`                         | PL/I                                   | Maintainability, Architecture               |
| `plsql`                       | Oracle PL/SQL                          | Maintainability, Architecture, AI           |
| `plsqlforms`                  | Oracle PL/SQL Forms                    | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `plsqlreports`                | Oracle PL/SQL Reports                  | Maintainability                             |
| `pluk`                        | PLUK                                   | Maintainability, Architecture               |
| `polymertemplates`            | Polymer Templates                      | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `postgresql`                  | PostgreSQL                             | Maintainability, Architecture               |
| `powerbuilder`                | Powerbuilder                           | Maintainability, Architecture               |
| `powercenter`                 | PowerCenter                            | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `powerfx`                     | Power Fx (AKA Microsoft Power Apps)    | Maintainability                             |
| `powershell`                  | Powershell                             | Maintainability, Architecture               |
| `progress`                    | Progress (OpenEdge)                    | Maintainability, Architecture, Security, AI |
| `prt`                         | PRT                                    | Maintainability                             |
| `puppet`                      | Puppet                                 | Maintainability, Architecture               |
| `python`                      | Python                                 | Maintainability, Architecture, Security, AI |
| `r`                           | R                                      | Maintainability, Architecture               |
| `radience`                    | Radience                               | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `razor`                       | Razor                                  | Maintainability, Architecture, AI           |
| `regelspraak`                 | ALEF Regelspraak                       | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `regelspraakhtml`             | ALEF Regelspraak (HTML export)         | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `rexx`                        | Rexx                                   | Maintainability, Architecture               |
| `robot`                       | Robot                                  | Maintainability                             |
| `rpg`                         | RPG                                    | Maintainability, Architecture               |
| `ruby`                        | Ruby (includes Ruby on Rails)          | Maintainability, Architecture, Security, AI |
| `rust`                        | Rust                                   | Maintainability, Architecture, AI           | [(4)](#notes), [(8)](#notes)                |
| `salesforceapex`              | Salesforce Apex                        | Maintainability, Architecture               |
| `salesforceflow`              | Salesforce Flow                        | Maintainability, Architecture               |
| `salesforceprocessbuilder`    | Salesforce Process Builder             | Maintainability                             |
| `sappo`                       | SAP PO                                 | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `sapui5`                      | SapUI5                                 | Maintainability, Architecture               |
| `sas`                         | SAS                                    | Maintainability, Architecture               |
| `sasflows`                    | SAS Flows                              | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `sass`                        | Sass                                   | Maintainability, Architecture               |
| `scala`                       | Scala                                  | Maintainability, Architecture, Security, AI |
| `scl`                         | SCL                                    | Maintainability, Architecture               |
| `scr`                         | SCR                                    | Maintainability, Architecture               |
| `script`                      | Shell script                           | Maintainability, Architecture               |
| `servicenow`                  | ServiceNow                             | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `siebeldeclarative`           | Siebel Declarative                     | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `siebeljs`                    | Siebel JS                              | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `siebelscripted`              | Siebel Scripted                        | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `siebelworkflow`              | Siebel Workflow                        | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `siebeltbui`                  | Siebel TBUI                            | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `slim`                        | Slim                                   | Maintainability                             |
| `smalltalk`                   | Smalltalk                              | Maintainability, Architecture               |
| `solidity`                    | Solidity                               | Maintainability, Architecture               |
| `sonicesb`                    | Sonic ESB                              | Maintainability, Architecture               |
| `spl`                         | SPL                                    | Maintainability                             |
| `sqlj`                        | SQLJ                                   | Maintainability, Architecture               |
| `sqlite`                      | SQLite                                 | Maintainability, Architecture               |
| `sqr`                         | SQR                                    | Maintainability, Architecture               |
| `ssis`                        | SSIS                                   | Maintainability, Architecture               |
| `starlimssql`                 | StarLIMS                               | Maintainability, Architecture               |
| `streamserve`                 | StreamServe                            | Maintainability, Architecture               |
| `synapse`                     | Synapse                                | Maintainability                             |
| `synon`                       | Synon                                  | Maintainability, Architecture               |
| `swift`                       | Swift                                  | Maintainability, Architecture, Security, AI |
| `t4`                          | T4                                     | Maintainability                             |
| `tacl`                        | TACL                                   | Maintainability, Architecture               |
| `tal`                         | TAL                                    | Maintainability                             |
| `tandem`                      | Tandem                                 | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `tapestry`                    | Tapestry                               | Maintainability, Architecture               |
| `terraform`                   | Terraform                              | Maintainability, Architecture, Security     |
| `thrift`                      | Thrift                                 | Maintainability, Architecture               |
| `thymeleaf`                   | Thymeleaf                              | Maintainability, Architecture               |
| `tibco`                       | TIBCO BW                               | Maintainability, Architecture               |
| `tibcobe`                     | TIBCO BE (XML)                         | Maintainability, Architecture               |
| `tibcobejava`                 | TIBCO BE (Java)                        | Maintainability, Architecture               |
| `tibcobestatemachine`         | TIBCO BE (State Machine)               | Maintainability, Architecture               |
| `tibcobw6`                    | TIBCO BW6                              | Maintainability, Architecture               |
| `tripleforms`                 | TriplEforms                            | Maintainability                             |
| `trs`                         | TRS                                    | Maintainability                             | [(4)](#notes), [(8)](#notes)                |
| `tsql`                        | T-SQL (Microsoft SQL Server, MS SQL))  | Maintainability, Architecture, AI           |
| `turtle`                      | Turtle                                 | Maintainability                             |
| `twig`                        | Twig                                   | Maintainability                             |
| `typescript`                  | TypeScript (includes React/TypeScript) | Maintainability, Architecture, Security, AI | [(3, 10)](#notes)                           |
| `uil`                         | UIL (Motif)                            | Maintainability, Architecture               |
| `uniface`                     | Uniface                                | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `until`                       | Until                                  | Maintainability, Architecture               |
| `vag`                         | Visual Age                             | Maintainability, Architecture               |
| `vagrecord`                   | Visual Age Record                      | Maintainability, Architecture               |
| `vb`                          | Visual Basic                           | Maintainability, Architecture, Security     |
| `vbnet`                       | Visual Basic .NET                      | Maintainability, Architecture, Security     |
| `velocity`                    | Velocity                               | Maintainability, Architecture               |
| `vgl`                         | VGL                                    | Maintainability                             |
| `visualforce`                 | VisualForce                            | Maintainability                             |
| `visualrpg`                   | Visual RPG                             | Maintainability, Architecture               |
| `visualobjects`               | Visual Objects                         | Maintainability, Architecture               |
| `vuejs`                       | VueJS                                  | Maintainability, Architecture, Security, AI | [(2)](#notes)                               |
| `vuets`                       | VueTS                                  | Maintainability, Architecture, Security     | [(3)](#notes)                               |
| `vulcan`                      | Vulcan.NET                             | Maintainability, Architecture               |
| `webfocus`                    | WebFocus                               | Maintainability, Architecture               |
| `webmethods`                  | WebMethods                             | Maintainability, Architecture               |
| `websmart`                    | WebSmart                               | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `websmartpanels`              | WebSmart Panels                        | Maintainability                             |
| `wonderware`                  | Wonderware                             | Maintainability                             |
| `wsdl`                        | WSDL                                   | Maintainability, Architecture               |
| `wtx`                         | WTX                                    | Maintainability                             |
| `xaml`                        | XAML                                   | Maintainability, Architecture               |
| `xml`                         | XML                                    | Maintainability, Architecture               | [(5)](#notes)                               |
| `xpdl`                        | Tibco ActiveMatrix BPM                 | Maintainability                             |
| `xpp`                         | X++ AX                                 | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `xpp365`                      | X++ for Dynamics 365                   | Maintainability, Architecture               | [(4)](#notes), [(8)](#notes)                |
| `xquery`                      | Xquery                                 | Maintainability, Architecture               |
| `xsd`                         | XSD                                    | Maintainability, Architecture               |
| `xslt`                        | XSLT                                   | Maintainability, Architecture               |
| `xul`                         | XUL                                    | Maintainability                             |
| `yaml`                        | YAML                                   | Maintainability, Architecture               | [(5)](#notes)                               |
{: .technologySupportTable }

### Notes

1. Not supported by [on-premise Sigrid](../organization-integration/onpremise-integration.md).
2. Use one of `javascript`, `vuejs`, `sapui5`, but do not use multiple.
  - Prefer `vuejs` if your system contains [Vue.js](https://vuejs.org) components that use the `.vue` file extension.
  - Only use `sapui5` if you are using [SAP UI](https://developers.sap.com/topics/ui-development.html).
  - Use `javascript` in all other cases.
3. Use either `typescript` or `vuets`, but not both.
  - Prefer `vuets` if you're using [Vue.js](https://vuejs.org) in combination with TypeScript code. 
  - Prefer `typescript` in all other cases.
4. Not supported by the [Sigrid Local](../organization-integration/sigrid-local.md).
5. In most cases, configuration files are not considered part of production code and are therefore not relevant for Sigrid's maintainability analysis. Only add these technologies if you consider them part of the system's production code.
6. "Unknown technology" will be shown in Sigrid when the technology cannot be detected.
7. Use either `html` or `angularjstemplate`, but not both.
  - Prefer `angularjstemplate` if you're using [Angular templates](https://angular.io/guide/template-syntax).
  - Use `html` for all other types of HTML files or templates.
8. You can use Sigrid CI for this technology, but you will need to use a special option. See instructions on how to [technology conversion configuration](#technology-conversion-configuration) below.
9. Sigrid CI is not supported for this technology. You can still use Sigrid, but you will need to use one of the [alternative upload channels](../organization-integration/upload-instructions.md).
10. `typescript` should also be used with React and/or JSX files with Typescript that use the `.ts` or `.tsx` file extensions.
11. Technology support is currently in beta, and not yet generally available. Contact SIG if you want to participate in this beta program.

### Framework-specific support

The [list of supported technologies](#list-of-supported-technologies) refers to the *base* technologies. 
For many modern technologies, the choice of frameworks has a significant impact on your system structure and architecture.
Sigrid therefore also provides support for framework-specific constructs, for the following frameworks:

Android,
Angular,
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
Spring,
Spring Boot,
Spring Cloud,
Spring Data,
Spring Kafka,
Styled Components,
Swing,
Svelte,
WPF
VueJS,
Yii.

## Technology conversion configuration

For the vast majority of technologies, you can simply publish your repository and have your code analyzed by Sigrid. However, a small number of technologies cannot be analyzed by Sigrid in its "native" format. In those situations, Sigrid needs to convert these technologies to another format before it can be analyzed.

This configuration can be managed using the `--convert` [option in Sigrid CI](client-script-usage.md#command-line-options). This is only applicable for the following technologies:

| Technology          | Value of the `--convert` option                                         |
|---------------------|-------------------------------------------------------------------------|
| ABB Control Builder | `ABBControlBuilder`                                                     |
| Altova UML          | `AltovaUML`                                                             |
| Oracle APEX         | `Apex`                                                                  |
| Axway               | `Axway`                                                                 |
| Axystudio           | `Axystudio`                                                             |
| BRM                 | `BRM`                                                                   |
| Be Informed         | `Beinformed`                                                            |
| Blueriq             | `Blueriq`                                                               |
| Data Bricks         | `Databricks`                                                            |
| Ecostruxure         | `Ecostruxure`                                                           |
| FME                 | `FME`                                                                   |
| IBM BPM             | `IbmBpm`                                                                |
| Infinite Blue       | `Infiniteblue`                                                          |
| JDE                 | `JDE`                                                                   |
| Linc                | `Linc`                                                                  |
| Lion                | `Lion`                                                                  |
| Lion/COBOL          | `LionCobol`                                                             |
| MicroFocus COBOL    | `MicroFocusCobol`                                                       |
| MPS                 | `MPSLanguage`                                                           |
| Nabsic              | `Nabsic`                                                                |
| NetIQ IDM           | `NetIQIDM`                                                              |
| OSB Pipeline        | `OSBPipeline`                                                           |
| OutSystems          | `Outsystems` or `OutsystemsExporter` (contact SIG support for details)  |
| PEGA                | `Pega` or `PegaFilter` (contact SIG support for details)                |
| PL/SQL Headstart    | `PlsqlHeadstart`                                                        |
| PL/SQL Forms        | `Plsqlforms`                                                            |
| Polymer             | `Polymer`                                                               |
| PowerCenter         | `Powercenter`                                                           |
| Radience            | `Radience`                                                              |
| Regelspraak         | `Regelspraak` or `Regelspraakhtml` (contact SIG support for details)    |
| Rust                | `Rust`                                                                  |
| Sailpoint BeanShell | `Sailpointbeanshell`                                                    |
| SAP PO              | `Sappo`                                                                 |
| SAS Flows           | `Sasflows`                                                              |
| ServiceNow          | `ServiceNow`                                                            |
| Siebel              | `SiebelProject` or `SiebelRepository` (contact SIG support for details) |
| Svelte              | `Svelte`                                                                |
| Uniface             | `Ssduniface` or `Unifacexml` (contact SIG support for details)          |
| Tandem              | `Tandem`                                                                |
| TRS                 | `Trs`                                                                   |
| USoft               | `Usoft` or `UsoftEsi` (contact SIG support for details)                 |
| WebSmart            | `Websmart`                                                              |
| X++                 | `Xpp`                                                                   |
| X++ 365             | `Axmodel`                                                               |

## Supported open source ecosystems

In addition to supporting 300+ technologies, Sigrid also supports various open source ecosystems for its Open Source Health capability. Note that different projects might use different open source ecosystems, even if they use the same technology. For example, there is no standardized way to manage open source dependencies in Java projects. Some Java projects use Maven, others use Gradle. This is why some technologies are listed multiple times in the table below.

| Open source ecosystem | Common technologies    |
|-----------------------|------------------------|
| Bower                 | JavaScript             |
| Cargo                 | Rust                   |
| CocoaPods             | Swift, Objective-C     |
| Composer              | PHP                    |
| Go Modules            | Go                     |
| Gradle                | Java, Kotlin, Groovy   |
| Ivy                   | Java                   |
| LibMan                | JavaScript             |
| Maven                 | Java                   |
| NPM                   | JavaScript, TypeScript |
| NuGet                 | C#                     |
| PuppetForge           | Puppet                 |
| Poetry                | Python                 |
| pub.dev               | Dart, Flutter          |
| PyPi                  | Python                 |
| RubyGems              | Ruby                   |
| SBT                   | Scala                  |
| SwiftPM               | Swift                  |
| Unmanaged JAR files   | Java                   |
| Unmanaged DLL files   | C#                     |
| Unmanaged JS files    | JavaScript             |

## Supported security analyzers

These are the supported security analyzers as you may see them in your security findings overview. You can use the literal text in the `Display name` below to enable or disable specific analyzers, if deemed necessary. For such configuration, see the [Security/Third Party Findings section section on the system security page](../reference/analysis-scope-configuration.md#third-party-findings).

Note this section only described *third party* security analysis analyzers. The results from these analyzers are then combined with the results from Sigrid's own security ruleset before being displayed.

| Display name           | Technologies                      | Notes                                                    |
|------------------------|-----------------------------------|----------------------------------------------------------|
| Astrée                 | C, C++                            | Requires *Sigrid Security for Embedded Systems* license. |
| Bandit                 | Python                            |
| Checkmarx              | (many)                            | Requires *Sigrid Security Checkmarx* license.            |
| ErrorProne.NET         | C#                                | Requires compiling code.                                 |
| ESLint                 | JavaScript, TypeScript            |
| FB Contrib             | Java                              |
| FindSecBugs            | Java                              |
| FlawFinder             | C                                 |
| Google ErrorProne      | Java                              | Requires compiling code.                                 |
| Gosec                  | Go                                |
| KICS                   | Docker, Ansible, Kubernetes, etc. |
| Microsoft Code Quality | C#                                | Requires compiling code.                                 |
| MobSF                  | Android                           |
| MultithreadingAnalyzer | C#                                | Requires compiling code.                                 |
| NodeJS Scan            | JavaScript, TypeScript            |
| Puma Security          | C#                                | Requires compiling code.                                 |
| SecurityCodeScan       | C#                                | Requires compiling code.                                 |
| SonarQube (C#)         | C#                                | Requires compiling code.                                 |
| SonarQube (Java)       | Java                              | Requires compiling code.                                 | 
| SpotBugs               | Java                              |
| SemGrep                | (many)                            |
| VMWare CSA             | Java, C#, configuration           | Cloud Suitability Analyzer.                              |

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

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
