Technology support
==================

The table below describes all technologies that can be analyzed by Sigrid. The first column refers to how the technology should be named in the [configuration file](analysis-scope-configuration.md), specifically for setting languages in your scope file, [see the technology support section](../reference/analysis-scope-configuration.md#technology-support).

Technologies are sometimes referred to by multiple names. For example, some people call their code NodeJS instead of JavaScript. If we are being pedantic, JavaScript is the name of the programming language and NodeJS is the name of the runtime. However, in practice many people just use these names interchangeably, so both are listed to prevent confusion.

Finally, note the column "supported Sigrid capabilities" does not list Open Source Health. The reason is that Open Source Health is based on open source ecosystems, not specific technologies. Refer to the section on [supported technologies for Open Source Health](#supported-open-source-ecosystems) for more information.

<sig-toc></sig-toc>

## List of supported technologies

| Name in configuration file | Display name                                           | Also known as        | Supported Sigrid capabilities           | Notes |
|----------------------------|--------------------------------------------------------|----------------------|-----------------------------------------|-------|
| `abap`                     | ABAP                                                   | SAP                  | Maintainability                         |
| `abapsmartforms`           | ABAP SmartForms                                        |                      | Maintainability, Architecture           |
| `abl`                      | Abl                                                    | OpenEdge             | Maintainability, Architecture           |
| `acl`                      | ACL                                                    |                      | Maintainability                         |
| `accell`                   | Accell                                                 |                      | Maintainability, Architecture           |
| `actionscript`             | ActionScript                                           |                      | Maintainability, Architecture           |
| `actionscript3`            | ActionScript 3                                         |                      | Maintainability, Architecture           |
| `ada`                      | Ada                                                    |                      | Maintainability, Architecture           |
| `adabasnatural`            | Adabas Natural                                         |                      | Maintainability, Architecture           |
| `adfxml`                   | ADF XML                                                |                      | Maintainability,                        |
| `agilepoint`               | AgilePoint                                             |                      | Maintainability, Architecture           |
| `altovauml`                | Altova UML                                             |                      | Maintainability, Architecture           | (8) |
| `angularjstemplate`        | Angular Templates                                      |                      | Maintainability                         | (7) |
| `ansible`                  | Ansible                                                |                      | Maintainability, Security               |
| `apachecamel`              | Apache Camel                                           |                      | Maintainability, Architecture           |
| `apex`                     | Oracle APEX                                            |                      | Maintainability, Architecture           | (8) |
| `aps`                      | APS                                                    |                      | Maintainability, Architecture           |
| `applicationmaster`        | Application Master                                     |                      | Maintainability, Architecture           |
| `ash`                      | ArtosScript (ash)                                      |                      | Maintainability, Architecture           |
| `asp`                      | ASP                                                    |                      | Maintainability, Architecture           |
| `aspx`                     | ASP.NET                                                |                      | Maintainability, Architecture           |
| `assembly`                 | Assembly                                               |                      | Maintainability, Architecture           |
| `aura`                     | Aura                                                   |                      | Maintainability, Architecture           |
| `axway`                    | Axway                                                  |                      | Maintainability, Architecture           | (8) |
| `axystudio`                | AxyStudio functions                                    |                      | Maintainability                         | (8) |
| `axyworkflow`              | AxyStudio workflows                                    |                      | Maintainability, Architecture           |
| `baan`                     | Baan                                                   |                      | Maintainability                         | (8) |
| `basic`                    | BASIC                                                  |                      | Maintainability, Architecture           |
| `batch`                    | Batch                                                  |                      | Maintainability, Architecture           |
| `bea`                      | Bea Weblogic                                           |                      | Maintainability, Architecture           |
| `beanshell`                | BeanShell                                              |                      | Maintainability                         |
| `beinformed`               | Be Informed                                            |                      | Maintainability, Architecture           | (8) |
| `biztalk`                  | BizTalk                                                |                      | Maintainability, Architecture           |
| `biztalkrules`             | BizTalk Rules Engine                                   |                      | Maintainability                         |
| `blazerules`               | Blaze BRM                                              |                      | Maintainability                         | (8) |
| `blueprism`                | Blue Prism                                             |                      | Maintainability, Architecture           |
| `blueriq`                  | Blueriq flows/processes                                |                      | Maintainability, Architecture           | (8) |
| `blueriqexpressions`       | Blueriq expressions                                    |                      | Maintainability, Architecture           | (8) |
| `bpel`                     | BPEL                                                   |                      | Maintainability, Architecture           |
| `bpm`                      | BPMN                                                   |                      | Maintainability, Architecture           |
| `brail`                    | Brail                                                  |                      | Maintainability                         |
| `bsp`                      | Bsp                                                    |                      | Maintainability, Architecture           |
| `c`                        | C                                                      |                      | Maintainability, Architecture, Security | (1) |
| `cache`                    | Cache                                                  |                      | Maintainability, Architecture           |
| `cacheobjectscript`        | Cache ObjectScript                                     |                      | Maintainability, Architecture           |
| `ccl`                      | CCL                                                    |                      | Maintainability, Architecture           |
| `cgdc`                     | CGDC                                                   |                      | Maintainability, Architecture           |
| `cgt`                      | CGT                                                    |                      | Maintainability, Architecture           |
| `cicode`                   | Cicode                                                 |                      | Maintainability, Architecture           |
| `cl`                       | CL                                                     |                      | Maintainability, Architecture           |
| `clearbasic`               | Clearbasic                                             |                      | Maintainability, Architecture           |
| `cobol`                    | Cobol                                                  |                      | Maintainability, Architecture           |
| `coffeescript`             | CoffeeScript                                           |                      | Maintainability, Architecture           |
| `coldfusion`               | ColdFusion                                             |                      | Maintainability, Architecture           |
| `configuration`            | Configuration                                          |                      | Maintainability                         | (5) |
| `coolgenc`                 | CoolGen C                                              |                      | Maintainability, Architecture           |
| `coolgencobol`             | CoolGen Cobol                                          |                      | Maintainability, Architecture           |
| `cordysbpm`                | Cordys BPM                                             |                      | Maintainability, Architecture           |
| `cpp`                      | C++                                                    |                      | Maintainability, Architecture, Security | (1) |
| `csharp`                   | C#                                                     | .NET                 | Maintainability, Architecture, Security |
| `csp`                      | CSP                                                    |                      | Maintainability, Architecture           |
| `css`                      | CSS                                                    |                      | Maintainability, Architecture           |
| `cypher`                   | Cypher                                                 |                      | Maintainability, Architecture           |
| `cucumber`                 | Cucumber                                               |                      | Maintainability, Architecture           |
| `dart`                     | Dart                                                   | Flutter              | Maintainability, Architecture           |
| `datastage`                | Datastage                                              |                      | Maintainability, Architecture           |
| `datastageetl`             | DatastageETL                                           |                      | Maintainability, Architecture           |
| `datastageworkflow`        | DatastageWorkflow                                      |                      | Maintainability, Architecture           |
| `db2`                      | DB2                                                    |                      | Maintainability, Architecture           |
| `dcl`                      | Dcl                                                    |                      | Maintainability, Architecture           |
| `delphi`                   | Delphi                                                 |                      | Maintainability, Architecture           |
| `delphiforms`              | Delphi Forms                                           |                      | Maintainability, Architecture           |
| `deltacobol`               | Delta/Cobol                                            |                      | Maintainability, Architecture           |
| `djangotemplates`          | Django Templates                                       |                      | Maintainability, Architecture           |
| `docker`                   | Docker                                                 |                      | Maintainability, Architecture, Security |
| `documentumxcp`            | Documentum xCP                                         |                      | Maintainability, Architecture           |
| `drools`                   | Drools                                                 |                      | Maintainability                         |
| `dscript`                  | Dscript                                                |                      | Maintainability                         |
| `easytrieve`               | Easytrieve                                             |                      | Maintainability, Architecture           |
| `egl`                      | EGL                                                    |                      | Maintainability, Architecture           |
| `ejs`                      | EJS                                                    |                      | Maintainability, Architecture           |
| `elixir`                   | Elixir                                                 |                      | Maintainability, Architecture           |
| `embeddedsql`              | C++ Embedded SQL                                       |                      | Maintainability, Architecture           |
| `erb`                      | ERB                                                    |                      | Maintainability, Architecture           |
| `esql`                     | ESQL                                                   |                      | Maintainability, Architecture           |
| `filetab`                  | File Tab                                               |                      | Maintainability                         |
| `finacle`                  | Finacle                                                |                      | Maintainability, Architecture           |
| `freeformatcobol`          | Freeformat Cobol                                       |                      | Maintainability, Architecture           |
| `freemarker`               | Freemarker                                             |                      | Maintainability, Architecture           |
| `fme`                      | FME                                                    |                      | Maintainability, Architecture           | (8) |
| `fortran`                  | FORTRAN                                                |                      | Maintainability, Architecture           |
| `gensym`                   | Gensym                                                 |                      | Maintainability, Architecture           |
| `grpc`                     | gRPC                                                   |                      | Maintainability, Architecture           |
| `go`                       | Go                                                     | GoLang               | Maintainability, Architecture           |
| `gosu`                     | Gosu                                                   |                      | Maintainability, Architecture, Security |
| `groovy`                   | Groovy                                                 |                      | Maintainability, Architecture, Security |
| `gsp`                      | GSP                                                    |                      | Maintainability, Architecture           |
| `guidefinition`            | GUI Definition                                         |                      | Maintainability                         | (5) |
| `gupta`                    | Gupta                                                  |                      | Maintainability, Architecture           |
| `haml`                     | Haml                                                   |                      | Maintainability, Architecture           |
| `html`                     | HTML                                                   |                      | Maintainability, Architecture           | (7) |
| `hql`                      | HQL                                                    |                      | Maintainability, Architecture           |
| `ibmbpmbpd`                | IBM BPM (BPD)                                          |                      | Maintainability, Architecture           | (8) |
| `ibmbpmprocess`            | IBM BPM (Process)                                      |                      | Maintainability, Architecture           | (8) |
| `ideal`                    | Ideal                                                  |                      | Maintainability, Architecture           |
| `informatica`              | Informatica                                            |                      | Maintainability                         |
| `informix4gl`              | Informix 4GL                                           |                      | Maintainability, Architecture           |
| `informixsql`              | Informix SQL                                           |                      | Maintainability, Architecture           |
| `ingres`                   | Ingres                                                 |                      | Maintainability                         |
| `intershoppipeline`        | Intershop (Pipeline)                                   |                      | Maintainability, Architecture           |
| `jasperreports`            | Jasper Reports                                         |                      | Maintainability, Architecture           |
| `jade`                     | Jade                                                   |                      | Maintainability, Architecture           |
| `java`                     | Java                                                   |                      | Maintainability, Architecture, Security |
| `javafx`                   | Java FX                                                |                      | Maintainability, Architecture           |
| `javascript`               | JavaScript                                             | NodeJS               | Maintainability, Architecture, Security | (2) |
| `javascript`               | Google App Script                                      |                      | Maintainability, Architecture           |
| `jbc`                      | JBC                                                    |                      | Maintainability, Architecture           |
| `jbpm`                     | jBPM                                                   |                      | Maintainability, Architecture           |
| `jcl`                      | JCL                                                    |                      | Maintainability, Architecture           |
| `jcs`                      | JCS                                                    |                      | Maintainability, Architecture           |
| `jinja`                    | Jinja                                                  |                      | Maintainability, Architecture           |
| `jsf`                      | JSF                                                    |                      | Maintainability, Architecture           |
| `json`                     | JSON                                                   |                      | Maintainability, Architecture           | (5) |
| `jsp`                      | JSP                                                    |                      | Maintainability, Architecture           |
| `kotlin`                   | Kotlin                                                 |                      | Maintainability, Architecture, Security |
| `less`                     | Less                                                   |                      | Maintainability, Architecture           |
| `linc`                     | LINC                                                   |                      | Maintainability, Architecture           | (8) |
| `lion`                     | Lion                                                   |                      | Maintainability, Architecture           | (8) |
| `lodestar`                 | Lodestar                                               |                      | Maintainability, Architecture           |
| `logicapps`                | Logic Apps                                             |                      | Maintainability                         |
| `logicnets`                | LogicNets                                              |                      | Maintainability, Architecture           |
| `lotusscript`              | LotusScript                                            |                      | Maintainability, Architecture           |
| `lua`                      | Lua                                                    |                      | Maintainability, Architecture           |
| `magic`                    | Magic                                                  |                      | Maintainability, Architecture           |
| `magik`                    | Magik                                                  |                      | Maintainability, Architecture           |
| `magnum`                   | Magnum                                                 |                      | Maintainability, Architecture           |
| `matlab`                   | Matlab                                                 |                      | Maintainability, Architecture           |
| `mediationflows`           | Mediation Flows                                        |                      | Maintainability, Architecture           |
| `mendix`                   | Mendix                                                 |                      | Maintainability, Architecture, Security |
| `messagebuilder`           | MessageBuilder                                         |                      | Maintainability, Architecture           |
| `mpsbehavior`              | MPS Behavior                                           |                      | Maintainability                         | (8) |
| `mpsclass`                 | MPS Class                                              |                      | Maintainability                         | (8) |
| `mpstranslator`            | MPS Translator                                         |                      | Maintainability                         | (8) |
| `mule`                     | Mule                                                   |                      | Maintainability, Architecture           |
| `mtwize`                   | MtWize                                                 |                      | Maintainability, Architecture           |
| `murexdatadictionary`      | Murex Data Dictionary                                  |                      | Maintainability, Architecture           |
| `murexlookuptable`         | Murex Lookup Table                                     |                      | Maintainability, Architecture           |
| `murexscript`              | Murex Script                                           |                      | Maintainability, Architecture           |
| `murexworkflow`            | Murex Workflow                                         |                      | Maintainability, Architecture           |
| `mustache`                 | Mustache                                               | Handlebars           | Maintainability, Architecture           |
| `mysql`                    | MySQL                                                  |                      | Maintainability, Architecture           |
| `nabsic`                   | Nabsic                                                 |                      | Maintainability, Architecture           | (8) |
| `naviscript`               | Naviscript                                             |                      | Maintainability, Architecture           |
| `navision`                 | Navision                                               | Dynamics NAV, AL     | Maintainability, Architecture           |
| `netiqidmpolicy`           | NetIQ IDM Policy                                       |                      | Maintainability                         | (8) |
| `netiqidmrequest`          | NetIQ IDM Request                                      |                      | Maintainability                         | (8) |
| `netiqidmworkflow`         | NetIQ IDM Workflow                                     |                      | Maintainability                         | (8) |
| `netweaveridm`             | NetweaverIDM                                           |                      | Maintainability, Architecture           |
| `nonstopsql`               | Nonstop SQL                                            |                      | Maintainability, Architecture           |
| `normalizedsystemsjava`    | Normalized Systems Java                                |                      | Maintainability, Architecture           |
| `normalizedsystemsmodel`   | Normalized Systems Model                               |                      | Maintainability, Architecture           |
| `objectivec`               | Objective-C                                            |                      | Maintainability, Architecture           |
| `odi`                      | ODI                                                    |                      | Maintainability, Architecture           |
| `odm`                      | ODM                                                    |                      | Maintainability, Architecture           |
| `omt`                      | OMT                                                    |                      | Maintainability, Architecture           |
| `opa`                      | OPA                                                    |                      | Maintainability, Architecture           |
| `opc`                      | OPC                                                    |                      | Maintainability                         |
| `openroad`                 | OpenROAD 4GL                                           |                      | Maintainability                         |
| `oraclebpm`                | Oracle BPM                                             |                      | Maintainability, Architecture           |
| `oracleofsaa`              | Oracle OFSAA                                           |                      | Maintainability, Architecture           |
| `oracleworkflow`           | Oracle Workflow                                        |                      | Maintainability, Architecture           |
| `ords`                     | ORDS                                                   |                      | Maintainability                         |
| `osb`                      | OSB                                                    |                      | Maintainability, Architecture           | (8) |
| `osbproxy`                 | OSB Proxy                                              |                      | Maintainability, Architecture           | (8) |
| `osmprocess`               | OSM Process                                            |                      | Maintainability, Architecture           |
| `osmtask`                  | OSM Task                                               |                      | Maintainability, Architecture           |
| `outsystems`               | OutSystems                                             |                      | Maintainability, Architecture           | (8) |
| `pascal`                   | Pascal                                                 |                      | Maintainability, Architecture           |
| `pega`                     | Pega                                                   |                      | Maintainability                         | (8) |
| `pegajsp`                  | PEGA JSP                                               |                      | Maintainability                         | (8) |
| `perl`                     | Perl                                                   |                      | Maintainability, Architecture, Security |
| `php`                      | PHP                                                    |                      | Maintainability, Architecture, Security |
| `plc`                      | PLC - Structured Text - ABB                            |                      | Maintainability, Architecture           | (8) |
| `plc`                      | PLC - Structured Text - Schneider Electric/EcoStruxure |                      | Maintainability, Architecture           | (8) |
| `plc`                      | PLC - Structured Text - Siemens                        |                      | Maintainability, Architecture           |
| `plc`                      | PLC - Functional Block Diagram - ABB                   |                      | Maintainability, Architecture           |
| `plc`                      | PLC - Functional Block Diagram - Rockwell              |                      | Maintainability, Architecture           |
| `plc`                      | PLC - Functional Block Diagram - Siemens               |                      | Maintainability, Architecture           |
| `plc`                      | PLC - Ladder Logic - Rockwell                          |                      | Maintainability, Architecture           |
| `plc`                      | PLC - Structured Text - Rockwell                       |                      | Maintainability, Architecture           |
| `pli`                      | PL/I                                                   |                      | Maintainability, Architecture           |
| `plsql`                    | PL/SQL                                                 |                      | Maintainability, Architecture           |
| `plsqlforms`               | PL/SQL Forms                                           |                      | Maintainability                         | (8) |
| `plsqlreports`             | PL/SQL Reports                                         |                      | Maintainability                         |
| `pluk`                     | PLUK                                                   |                      | Maintainability, Architecture           |
| `polymertemplates`         | Polymer Templates                                      |                      | Maintainability, Architecture           | (8) |
| `postgresql`               | PostgreSQL                                             |                      | Maintainability, Architecture           |
| `powerbuilder`             | Powerbuilder                                           |                      | Maintainability, Architecture           |
| `powercenter`              | PowerCenter                                            |                      | Maintainability, Architecture           | (8) |
| `powerfx`                  | Power Fx                                               | Microsoft Power Apps | Maintainability                         |
| `powershell`               | Powershell                                             |                      | Maintainability, Architecture           |
| `progress`                 | Progress                                               | OpenEdge             | Maintainability, Architecture           |
| `pronto`                   | Pronto                                                 |                      | Maintainability, Architecture           |
| `prt`                      | PRT                                                    |                      | Maintainability                         |
| `puppet`                   | Puppet                                                 |                      | Maintainability, Architecture           |
| `python`                   | Python                                                 |                      | Maintainability, Architecture, Security |
| `r`                        | R                                                      |                      | Maintainability, Architecture           |
| `radience`                 | Radience                                               |                      | Maintainability, Architecture           | (8) |
| `razor`                    | Razor                                                  |                      | Maintainability, Architecture           |
| `react`                    | React                                                  |                      | Maintainability, Architecture, Security | (2) |
| `regelspraak`              | ALEF Regelspraak                                       |                      | Maintainability, Architecture           | (8) |
| `regelspraakhtml`          | ALEF Regelspraak (HTML export)                         |                      | Maintainability, Architecture           | (8) |
| `rexx`                     | Rexx                                                   |                      | Maintainability, Architecture           |
| `robot`                    | Robot                                                  |                      | Maintainability                         |
| `rpg`                      | RPG                                                    |                      | Maintainability, Architecture           |
| `ruby`                     | Ruby                                                   | Ruby on Rails, Rails | Maintainability, Architecture, Security |
| `rust`                     | Rust                                                   |                      | Maintainability, Architecture           |
| `salesforceapex`           | Salesforce Apex                                        |                      | Maintainability, Architecture           |
| `salesforceflow`           | Salesforce Flow                                        |                      | Maintainability, Architecture           |
| `sappo`                    | SAP PO                                                 |                      | Maintainability, Architecture           | (8) |
| `sapui5`                   | SapUI5                                                 |                      | Maintainability, Architecture           |
| `sas`                      | SAS                                                    |                      | Maintainability, Architecture           |
| `sasflows`                 | SAS Flows                                              |                      | Maintainability                         | (8) |
| `sass`                     | Sass                                                   |                      | Maintainability, Architecture           |
| `scala`                    | Scala                                                  |                      | Maintainability, Architecture, Security |
| `scl`                      | SCL                                                    |                      | Maintainability, Architecture           |
| `scr`                      | SCR                                                    |                      | Maintainability, Architecture           |
| `script`                   | Shell script                                           |                      | Maintainability, Architecture           |
| `servicenow`               | ServiceNow                                             |                      | Maintainability, Architecture           | (8) |
| `siebeldeclarative`        | Siebel Declarative                                     |                      | Maintainability, Architecture           | (8) |
| `siebeljs`                 | Siebel JS                                              |                      | Maintainability, Architecture           | (8) |
| `siebelscripted`           | Siebel Scripted                                        |                      | Maintainability, Architecture           | (8) |
| `siebelworkflow`           | Siebel Workflow                                        |                      | Maintainability, Architecture           | (8) |
| `siebeltbui`               | Siebel TBUI                                            |                      | Maintainability, Architecture           | (8) |
| `slim`                     | Slim                                                   |                      | Maintainability                         |
| `smalltalk`                | Smalltalk                                              |                      | Maintainability, Architecture           |
| `solidity`                 | Solidity                                               |                      | Maintainability, Architecture           |
| `sonicesb`                 | Sonic ESB                                              |                      | Maintainability, Architecture           |
| `spl`                      | SPL                                                    |                      | Maintainability                         |
| `sqlj`                     | SQLJ                                                   |                      | Maintainability, Architecture           |
| `sqlite`                   | SQLite                                                 |                      | Maintainability, Architecture           |
| `sqr`                      | SQR                                                    |                      | Maintainability, Architecture           |
| `ssis`                     | SSIS                                                   |                      | Maintainability, Architecture           |
| `starlimssql`              | StarLIMS                                               |                      | Maintainability, Architecture           |
| `streamserve`              | StreamServe                                            |                      | Maintainability, Architecture           |
| `synapse`                  | Synapse                                                |                      | Maintainability                         |
| `synon`                    | Synon                                                  |                      | Maintainability, Architecture           |
| `swift`                    | Swift                                                  |                      | Maintainability, Architecture, Security |
| `t4`                       | T4                                                     |                      | Maintainability                         |
| `tacl`                     | TACL                                                   |                      | Maintainability, Architecture           |
| `tal`                      | TAL                                                    |                      | Maintainability                         |
| `tandem`                   | Tandem                                                 |                      | Maintainability, Architecture           | (8) |
| `tapestry`                 | Tapestry                                               |                      | Maintainability, Architecture           |
| `terraform`                | Terraform                                              |                      | Maintainability, Architecture, Security |
| `thrift`                   | Thrift                                                 |                      | Maintainability, Architecture           |
| `thymeleaf`                | Thymeleaf                                              |                      | Maintainability, Architecture           |
| `tibco`                    | TIBCO BW                                               |                      | Maintainability, Architecture           |
| `tibcobe`                  | TIBCO BE (XML)                                         |                      | Maintainability, Architecture           |
| `tibcobejava`              | TIBCO BE (Java)                                        |                      | Maintainability, Architecture           |
| `tibcobestatemachine`      | TIBCO BE (State Machine)                               |                      | Maintainability, Architecture           |
| `tibcobw6`                 | TIBCO BW6                                              |                      | Maintainability, Architecture           |
| `tripleforms`              | TriplEforms                                            |                      | Maintainability                         |
| `tsql`                     | T-SQL                                                  |                      | Maintainability, Architecture           |
| `turtle`                   | Turtle                                                 |                      | Maintainability                         |
| `typescript`               | TypeScript                                             |                      | Maintainability, Architecture, Security | (3) |
| `uil`                      | UIL (Motif)                                            |                      | Maintainability, Architecture           |
| `uniface`                  | Uniface                                                |                      | Maintainability, Architecture           | (8) |
| `until`                    | Until                                                  |                      | Maintainability, Architecture           |
| `vag`                      | Visual Age                                             |                      | Maintainability, Architecture           |
| `vagrecord`                | Visual Age Record                                      |                      | Maintainability, Architecture           |
| `vb`                       | Visual Basic                                           |                      | Maintainability, Architecture, Security | (4) |
| `vbnet`                    | Visual Basic .NET                                      |                      | Maintainability, Architecture, Security | (4) |
| `velocity`                 | Velocity                                               |                      | Maintainability, Architecture           |
| `vgl`                      | VGL                                                    |                      | Maintainability                         |
| `visualforce`              | VisualForce                                            |                      | Maintainability                         |
| `visualrpg`                | Visual RPG                                             |                      | Maintainability, Architecture           |
| `visualobjects`            | Visual Objects                                         |                      | Maintainability, Architecture           |
| `vuejs`                    | VueJS                                                  |                      | Maintainability, Architecture, Security | (2) |
| `vuets`                    | VueTS                                                  |                      | Maintainability, Architecture, Security | (3) |
| `vulcan`                   | Vulcan.NET                                             |                      | Maintainability, Architecture           |
| `webfocus`                 | WebFocus                                               |                      | Maintainability, Architecture           |
| `webmethods`               | WebMethods                                             |                      | Maintainability, Architecture           |
| `webmethodsbpm`            | WebMethods BPM                                         |                      | Maintainability, Architecture           |
| `websmart`                 | WebSmart                                               |                      | Maintainability, Architecture           | (8) |
| `wonderware`               | Wonderware                                             |                      | Maintainability                         |
| `wsdl`                     | WSDL                                                   |                      | Maintainability, Architecture           |
| `wtx`                      | WTX                                                    |                      | Maintainability                         |
| `xaml`                     | XAML                                                   |                      | Maintainability, Architecture           |
| `xml`                      | XML                                                    |                      | Maintainability, Architecture           | (5) |
| `xpdl`                     | Tibco ActiveMatrix BPM                                 |                      | Maintainability                         |
| `xpp`                      | X++                                                    |                      | Maintainability, Architecture           | (8) |
| `xpp365`                   | X++ for Dynamics 365                                   |                      | Maintainability, Architecture           | (8) |
| `xquery`                   | Xquery                                                 |                      | Maintainability, Architecture           |
| `xsd`                      | XSD                                                    |                      | Maintainability, Architecture           |
| `xslt`                     | XSLT                                                   |                      | Maintainability, Architecture           |
| `xul`                      | XUL                                                    |                      | Maintainability                         |
| `yaml`                     | YAML                                                   |                      | Maintainability, Architecture           | (5) |

Notes:

1. Use either `c` or `cpp`, but not both.
  - Prefer `cpp` if your system contains a combination of C and C++ code.
2. Use one of `javascript`, `react`, `vuejs`, `sapui5`, but do not use multiple.
  - Prefer `vuejs` if your system contains [Vue.js](https://vuejs.org) components that use the `.vue` file extension.
  - Prefer `react` if your codebase contains [React](https://reactjs.org) and/or [JSX](https://reactjs.org/docs/introducing-jsx.html).
  - Only use `sapui5` if you are using [SAP UI](https://developers.sap.com/topics/ui-development.html).
  - Use `javascript` in all other cases.
3. Use either `typescript` or `vuets`, but not both.
  - Prefer `vuets` if you're using [Vue.js](https://vuejs.org) in combination with TypeScript code. 
  - Prefer `typescript` in all other cases.
4. Use either `vb` or `vbnet`, but not both.
  - Prefer `vbnet` for Visual Basic code running on the .NET platform, or when not sure.
  - Use `vb` for [classic Visual Basic](https://en.wikipedia.org/wiki/Visual_Basic_(classic)), which has been end-of-life since 2008.
5. In most cases, configuration files are not considered part of production code and are therefore not relevant for Sigrid's maintainability analysis. Only add these technologies if you consider them part of the system's production code.
6. "Unknown technology" will be shown in Sigrid when the technology cannot be detected.
7. Use either `html` or `angularjstemplate`, but not both.
  - Prefer `angularjstemplate` if you're using [Angular templates](https://angular.io/guide/template-syntax).
  - Use `html` for all other types of HTML files or templates.
8. Sigrid CI is not supported for this technology. You can still use Sigrid, but you will need to use one of the [alternative upload channels](../organization-integration/upload-instructions.md).

## Supported open source ecosystems

In addition to supporting 300+ technologies, Sigrid also supports various open source ecosystems for its Open Source Health capability. Note that different projects might use different open source ecosystems, even if they use the same technology. For example, there is no standardized way to manage open source dependencies in Java projects. Some Java projects use Maven, others use Gradle. This is why some technologies are listed multiple times in the table below.

| Open source ecosystem | Common technologies    |
|-----------------------|------------------------|
| Alpine Linux          | Alpine Linux           |
| Bower                 | JavaScript             |
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
| PyPi                  | Python                 |
| RubyGems              | Ruby                   |
| SBT                   | Scala                  |
| Unmanaged JAR files   | Java                   |
| Unmanaged DLL files   | C#                     |
| Unmanaged JS files    | JavaScript             |

## Supported security analyzers

These are the supported security analyzers as you may see them in your security findings overview. You can use the literal text in the `Display name` below to enable or disable specific analyzers, if deemed necessary. For such configuration, see the [Security/Third Party Findings section section on the system security page](../reference/analysis-scope-configuration.md#third-party-findings).

| Display name           | Technology                       | Note                       |
|------------------------|----------------------------------|----------------------------|
| Astree                 | C, C++                           |                            |
| FlawFinder             | C                                | Semgrep plugin             |
| ErrorProne.NET         | C#                               |                            |
| Microsoft Code Quality | C#                               | FxCop                      |
| MultithreadingAnalyzer | C#                               |                            |
| Puma Security          | C#                               |                            |
| SecurityCodeScan       | C#                               |                            |
| SonarQube (C#)         | C#                               |                            |
| KICS                   | Docker, Ansible, k8s, etc.       |                            |
| FB Contrib             | Java                             |                            |
| Facebook Infer         | Java                             | Disabled by default        |
| FindSecBugs            | Java                             |                            |
| Google ErrorProne      | Java                             |                            |
| SonarQube (Java)       | Java                             |                            |
| SpotBugs               | Java                             |                            |
| MobSF                  | Java-Android                     | Semgrep plugin             |
| SemGrep                | Java,Python,PHP,Ruby,JS,TS, etc. |                            |
| VMWare CSA             | Java, C#, configurations         | Cloud Suitability Analyzer |
| ESLint                 | JS,TS                            | Semgrep plugin             |
| NodeJS Scan            | JS,TS                            | Semgrep plugin             |
| Gosec                  | Go                               | Semgrep plugin             |
| Bandit                 | Python                           | Semgrep plugin             |

## Supported software quality standards

| Software quality standard | Relevant for capabilities |
|---------------------------|---------------------------|
| [ISO 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) | Maintainability, Architecture, Security, Reliability |
| [SIG Security Model](https://softwareimprovementgroup.com/wp-content/uploads/SIG-Evaluation-Criteria-Security.pdf) | Security |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | Security |
| [ISO 5055](https://www.iso.org/standard/80623.html) | Security, Reliability |
| [CWE Top 25](https://cwe.mitre.org/top25/) | Security |
| [PCI DSS 4.0](https://blog.pcisecuritystandards.org/pci-dss-v4-0-resource-hub) | Security |
| [OWASP ASVS 4.0](https://owasp.org/www-pdf-archive/OWASP_Application_Security_Verification_Standard_4.0-en.pdf) | Security |
| [OWASP Low-code/No-code Top 10](https://owasp.org/www-project-top-10-low-code-no-code-security-risks/) | Security |

## Requesting additional technology support

Even with 300+ supported technologies, we are still continuously working on adding support for new technologies and frameworks and updating our technology support for new technology versions. You can contact us using the information provided below if you believe we should extend technology support for your organization.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
