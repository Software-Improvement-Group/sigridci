Technology support
==================

The table below describes all technologies that can be analyzed by Sigrid. The first column refers to how the technology should be named in the [configuration file](analysis-scope-configuration.md). 

Technologies are sometimes referred to by multiple names. For example, some people call their code NodeJS instead of JavaScript. If we're being pedantic, JavaScript is the name of the programming language and NodeJS is the name of the runtime. However, in practice many people just use these names interchangeably, so both are listed to prevent confusion.

Finally, note the column "supported Sigrid capabilities" does not list Open Source Health. The reason is that Open Source Health is based on open source ecosystems, not specific technologies. Refer to the section on [supported technologies for Open Source Health](#supported-open-source-ecosystems) for more information.

| Name in configuration file     | Display name                   | Also known as | Supported Sigrid capabilities | Notes |
|--------------------------------|--------------------------------|---------------|-------------------------------|-------|
| `abap`                         | ABAP                           | SAP | Maintainability |
| `abapsmartforms`               | ABAP SmartForms                | | Maintainability |
| `abl`                          | Abl                            | OpenEdge | Maintainability |
| `acl`                          | ACL                            | | Maintainability |
| `accell`                       | Accell                         | | Maintainability |
| `actionscript`                 | ActionScript                   | | Maintainability |
| `actionscript3`                | ActionScript 3                 | | Maintainability |
| `ada`                          | Ada                            | | Maintainability |
| `adabasnatural`                | Adabas Natural                 | | Maintainability |
| `adfxml`                       | ADF XML                        | | Maintainability |
| `agilepoint`                   | AgilePoint                     | | Maintainability |
| `altovauml`                    | Altova UML                     | | Maintainability |
| `angularjstemplate`            | Angular Templates              | | Maintainability |
| `ansible`                      | Ansible                        | | Maintainability, Security |
| `apachecamel`                  | Apache Camel                   | | Maintainability |
| `apex`                         | APEX                           | | Maintainability |
| `aps`                          | APS                            | | Maintainability |
| `applicationmaster`            | Application Master             | | Maintainability |
| `ash`                          | ArtosScript (ash)              | | Maintainability |
| `asp`                          | ASP                            | | Maintainability |
| `aspx`                         | ASP.NET                        | | Maintainability |
| `assembly`                     | Assembly                       | | Maintainability |
| `aura`                         | Aura                           | | Maintainability |
| `axway`                        | Axway                          | | Maintainability |
| `axystudio`                    | AxyStudio functions            | | Maintainability |
| `axyworkflow`                  | AxyStudio workflows            | | Maintainability |
| `basic`                        | BASIC                          | | Maintainability |
| `batch`                        | Batch                          | | Maintainability |
| `bea`                          | Bea Weblogic                   | | Maintainability |
| `beanshell`                    | BeanShell                      | | Maintainability |
| `beinformed`                   | Be Informed                    | | Maintainability |
| `biztalk`                      | BizTalk                        | | Maintainability |
| `biztalkrules`                 | BizTalk Rules Engine           | | Maintainability |
| `blazerules`                   | Blaze BRM                      | | Maintainability |
| `blueprism`                    | Blue Prism                     | | Maintainability |
| `blueriq`                      | Blueriq flows/processes        | | Maintainability |
| `blueriqexpressions`           | Blueriq expressions            | | Maintainability |
| `bpel`                         | BPEL                           | | Maintainability |
| `bpm`                          | BPMN                           | | Maintainability |
| `brail`                        | Brail                          | | Maintainability |
| `bsp`                          | Bsp                            | | Maintainability |
| `c`                            | C                              | | Maintainability, Security | (1) |
| `cache`                        | Cache                          | | Maintainability |
| `cacheobjectscript`            | Cache ObjectScript             | | Maintainability |
| `ccl`                          | CCL                            | | Maintainability |
| `cgdc`                         | CGDC                           | | Maintainability |
| `cgt`                          | CGT                            | | Maintainability |
| `cicode`                       | Cicode                         | | Maintainability |
| `cl`                           | CL                             | | Maintainability |
| `clearbasic`                   | Clearbasic                     | | Maintainability |
| `cobol`                        | Cobol                          | | Maintainability |
| `coffeescript`                 | CoffeeScript                   | | Maintainability |
| `coldfusion`                   | ColdFusion                     | | Maintainability |
| `configuration`                | Configuration                  | | Maintainability | (5) |
| `coolgenc`                     | CoolGen C                      | | Maintainability |
| `coolgencobol`                 | CoolGen Cobol                  | | Maintainability |
| `cordysbpm`                    | Cordys BPM                     | | Maintainability |
| `cpp`                          | C++                            | | Maintainability, Security | (1) |
| `csharp`                       | C#                             | .NET | Maintainability, Security |
| `csp`                          | CSP                            | | Maintainability |
| `css`                          | CSS                            | | Maintainability |
| `cypher`                       | Cypher                         | | Maintainability |
| `cucumber`                     | Cucumber                       | | Maintainability |
| `datastage`                    | Datastage                      | | Maintainability |
| `datastageetl`                 | DatastageETL                   | | Maintainability |
| `datastageworkflow`            | DatastageWorkflow              | | Maintainability |
| `db2`                          | DB2                            | | Maintainability |
| `dcl`                          | Dcl                            | | Maintainability |
| `delphi`                       | Delphi                         | | Maintainability |
| `delphiforms`                  | Delphi Forms                   | | Maintainability |
| `deltacobol`                   | Delta/Cobol                    | | Maintainability |
| `djangotemplates`              | Django Templates               | | Maintainability |
| `docker`                       | Docker                         | | Maintainability, Security |
| `documentumxcp`                | Documentum xCP                 | | Maintainability |
| `drools`                       | Drools                         | | Maintainability |
| `dscript`                      | Dscript                        | | Maintainability |
| `easytrieve`                   | Easytrieve                     | | Maintainability |
| `egl`                          | EGL                            | | Maintainability |
| `ejs`                          | EJS                            | | Maintainability |
| `embeddedsql`                  | C++ Embedded SQL               | | Maintainability |
| `erb`                          | ERB                            | | Maintainability |
| `esql`                         | ESQL                           | | Maintainability |
| `filetab`                      | File Tab                       | | Maintainability |
| `finacle`                      | Finacle                        | | Maintainability |
| `freeformatcobol`              | Freeformat Cobol               | | Maintainability |
| `freemarker`                   | Freemarker                     | | Maintainability |
| `fme`                          | FME                            | | Maintainability |
| `fortran`                      | FORTRAN                        | | Maintainability |
| `generated`                    | Generated                      | | Maintainability |
| `gensym`                       | Gensym                         | | Maintainability |
| `grpc`                         | [gRPC](https://grpc.io)        | | Maintainability |
| `go`                           | Go                             | GoLang | Maintainability |
| `gosu`                         | Gosu                           | | Maintainability, Security |
| `groovy`                       | Groovy                         | | Maintainability, Security |
| `gsp`                          | GSP                            | | Maintainability |
| `guidefinition`                | GUI Definition                 | | Maintainability | (5) |
| `gupta`                        | Gupta                          | | Maintainability |
| `haml`                         | Haml                           | | Maintainability |
| `html`                         | HTML                           | | Maintainability |
| `hql`                          | HQL                            | | Maintainability |
| `ibmbpmbpd`                    | IBM BPM (BPD)                  | | Maintainability |
| `ibmbpmprocess`                | IBM BPM (Process)              | | Maintainability |
| `ideal`                        | Ideal                          | | Maintainability |
| `informatica`                  | Informatica                    | | Maintainability |
| `informix4gl`                  | Informix 4GL                   | | Maintainability |
| `informixsql`                  | Informix SQL                   | | Maintainability |
| `ingres`                       | Ingres                         | | Maintainability |
| `intershoppipeline`            | Intershop (Pipeline)           | | Maintainability |
| `jasperreports`                | Jasper Reports                 | | Maintainability |
| `jade`                         | Jade                           | | Maintainability |
| `java`                         | Java                           | | Maintainability, Security |
| `javafx`                       | Java FX                        | | Maintainability |
| `javascript`                   | JavaScript                     | NodeJS | Maintainability, Security | (2) |
| `javascript`                   | Google App Script              | | Maintainability |
| `jbc`                          | JBC                            | | Maintainability |
| `jbpm`                         | jBPM                           | | Maintainability |
| `jcl`                          | JCL                            | | Maintainability |
| `jcs`                          | JCS                            | | Maintainability |
| `jinja`                        | Jinja                          | | Maintainability |
| `jsf`                          | JSF                            | | Maintainability |
| `json`                         | JSON                           | | Maintainability | (5) |
| `jsp`                          | JSP                            | | Maintainability |
| `kotlin`                       | Kotlin                         | | Maintainability, Security |
| `less`                         | Less                           | | Maintainability |
| `linc`                         | LINC                           | | Maintainability |
| `lion`                         | Lion                           | | Maintainability |
| `lodestar`                     | Lodestar                       | | Maintainability |
| `logicapps`                    | Logic Apps                     | | Maintainability |
| `logicnets`                    | LogicNets                      | | Maintainability |
| `lotusscript`                  | LotusScript                    | | Maintainability |
| `lua`                          | Lua                            | | Maintainability |
| `magic`                        | Magic                          | | Maintainability |
| `magik`                        | Magik                          | | Maintainability |
| `magnum`                       | Magnum                         | | Maintainability |
| `matlab`                       | Matlab                         | | Maintainability |
| `mediationflows`               | Mediation Flows                | | Maintainability |
| `mendix`                       | Mendix                         | | Maintainability, Security |
| `messagebuilder`               | MessageBuilder                 | | Maintainability |
| `mpsbehavior`                  | MPS Behavior                   | | Maintainability |
| `mpsclass`                     | MPS Class                      | | Maintainability |
| `mpstranslator`                | MPS Translator                 | | Maintainability |
| `mule`                         | Mule                           | | Maintainability |
| `mtwize`                       | MtWize                         | | Maintainability |
| `murexdatadictionary`          | Murex Data Dictionary          | | Maintainability |
| `murexlookuptable`             | Murex Lookup Table             | | Maintainability |
| `murexscript`                  | Murex Script                   | | Maintainability |
| `murexworkflow`                | Murex Workflow                 | | Maintainability |
| `mustache`                     | Mustache                       | Handlebars | Maintainability |
| `mysql`                        | MySQL                          | | Maintainability |
| `naviscript`                   | Naviscript                     | | Maintainability |
| `navision`                     | Navision                       | | Maintainability |
| `netiqidmpolicy`               | NetIQ IDM Policy               | | Maintainability |
| `netiqidmrequest`              | NetIQ IDM Request              | | Maintainability |
| `netiqidmworkflow`             | NetIQ IDM Workflow             | | Maintainability |
| `netweaveridm`                 | NetweaverIDM                   | | Maintainability |
| `nonstopsql`                   | Nonstop SQL                    | | Maintainability |
| `normalizedsystemsjava`        | Normalized Systems Java        | | Maintainability |
| `normalizedsystemsmodel`       | Normalized Systems Model       | | Maintainability |
| `objectivec`                   | Objective-C                    | | Maintainability |
| `odi`                          | ODI                            | | Maintainability |
| `odm`                          | ODM                            | | Maintainability |
| `omt`                          | OMT                            | | Maintainability |
| `opa`                          | OPA                            | | Maintainability |
| `opc`                          | OPC                            | | Maintainability |
| `openroad`                     | OpenROAD 4GL                   | | Maintainability |
| `oraclebpm`                    | Oracle BPM                     | | Maintainability |
| `oracleofsaa`                  | Oracle OFSAA                   | | Maintainability |
| `oracleworkflow`               | Oracle Workflow                | | Maintainability |
| `ords`                         | ORDS                           | | Maintainability |
| `osb`                          | OSB                            | | Maintainability |
| `osbproxy`                     | OSB Proxy                      | | Maintainability |
| `osmprocess`                   | OSM Process                    | | Maintainability |
| `osmtask`                      | OSM Task                       | | Maintainability |
| `outsystems`                   | OutSystems                     | | Maintainability |
| `pascal`                       | Pascal                         | | Maintainability |
| `pega`                         | Pega                           | | Maintainability |
| `pegajsp`                      | PEGA JSP                       | | Maintainability |
| `performance`                  | Performance                    | | Maintainability |
| `perl`                         | Perl                           | | Maintainability, Security |
| `php`                          | PHP                            | | Maintainability, Security |
| `plc`                          | PLC - Structured Text - ABB    | | Maintainability |
| `plc`                          | PLC - Structured Text - Schneider Electric - EcoStruxure | | Maintainability |
| `plc`                          | PLC - Structured Text - Siemens | | Maintainability |
| `plc`                          | PLC - Functional Block Diagram - ABB | | Maintainability |
| `plc`                          | PLC - Functional Block Diagram - Rockwell | | Maintainability |
| `plc`                          | PLC - Functional Block Diagram - Siemens | | Maintainability |
| `plc`                          | PLC - Ladder Logic - Rockwell | | Maintainability |
| `plc`                          | PLC - Structured Text - Rockwell | | Maintainability |
| `pli`                          | PL/I                           | | Maintainability |
| `plsql`                        | PL/SQL                         | | Maintainability |
| `plsqlforms`                   | PL/SQL Forms                   | | Maintainability |
| `plsqlreports`                 | PL/SQL Reports                 | | Maintainability |
| `pluk`                         | PLUK                           | | Maintainability |
| `polymertemplates`             | Polymer Templates              | | Maintainability |
| `postgresql`                   | PostgreSQL                     | | Maintainability |
| `powerbuilder`                 | Powerbuilder                   | | Maintainability |
| `powercenter`                  | PowerCenter                    | | Maintainability |
| `powerfx`                      | Power Fx                       | Microsoft Power Apps | Maintainability |
| `powershell`                   | Powershell                     | | Maintainability |
| `production`                   | Production code                | | Maintainability |
| `progress`                     | Progress                       | OpenEdge | Maintainability |
| `progressstrict`               | Progress (Strict)              | | Maintainability |
| `pronto`                       | Pronto                         | | Maintainability |
| `prt`                          | PRT                            | | Maintainability |
| `puppet`                       | Puppet                         | | Maintainability |
| `python`                       | Python                         | | Maintainability, Security |
| `r`                            | R                              | | Maintainability |
| `radience`                     | Radience                       | | Maintainability |
| `razor`                        | Razor                          | | Maintainability |
| `react`                        | React                          | | Maintainability, Security | (2) |
| `regelspraak`                  | ALEF Regelspraak               | | Maintainability |
| `regelspraakhtml`              | ALEF Regelspraak (HTML export) | | Maintainability |
| `rexx`                         | Rexx                           | | Maintainability |
| `robot`                        | Robot                          | | Maintainability |
| `rpg`                          | RPG                            | | Maintainability |
| `ruby`                         | Ruby                           | Ruby on Rails, Rails | Maintainability, Security |
| `rust`                         | Rust                           | | Maintainability |
| `salesforceapex`               | Salesforce Apex                | | Maintainability |
| `salesforceflow`               | Salesforce Flow                | | Maintainability |
| `sappo`                        | SAP PO                         | | Maintainability |
| `sapui5`                       | SapUI5                         | | Maintainability |
| `sas`                          | SAS                            | | Maintainability |
| `sasflows`                     | SAS Flows                      | | Maintainability |
| `sass`                         | Sass                           | | Maintainability |
| `scala`                        | Scala                          | | Maintainability, Security |
| `scl`                          | SCL                            | | Maintainability |
| `scr`                          | SCR                            | | Maintainability |
| `script`                       | Shell script                   | | Maintainability |
| `servicenow`                   | ServiceNow                     | | Maintainability |
| `siebeldeclarative`            | Siebel Declarative             | | Maintainability |
| `siebeljs`                     | Siebel JS                      | | Maintainability |
| `siebelscripted`               | Siebel Scripted                | | Maintainability |
| `siebelworkflow`               | Siebel Workflow                | | Maintainability |
| `siebeltbui`                   | Siebel TBUI                    | | Maintainability |
| `slim`                         | Slim                           | | Maintainability |
| `smalltalk`                    | Smalltalk                      | | Maintainability |
| `solidity`                     | Solidity                       | | Maintainability |
| `sonicesb`                     | Sonic ESB                      | | Maintainability |
| `spl`                          | SPL                            | | Maintainability |
| `sqlj`                         | SQLJ                           | | Maintainability |
| `sqlite`                       | SQLite                         | | Maintainability |
| `sqr`                          | SQR                            | | Maintainability |
| `ssis`                         | SSIS                           | | Maintainability |
| `starlimssql`                  | StarLIMS                       | | Maintainability |
| `streamserve`                  | StreamServe                    | | Maintainability |
| `synapse`                      | Synapse                        | | Maintainability |
| `synon`                        | Synon                          | | Maintainability |
| `swift`                        | Swift                          | | Maintainability, Security |
| `t4`                           | T4                             | | Maintainability |
| `tacl`                         | TACL                           | | Maintainability |
| `tal`                          | TAL                            | | Maintainability |
| `tandem`                       | Tandem                         | | Maintainability |
| `tapestry`                     | Tapestry                       | | Maintainability |
| `terraform`                    | Terraform                      | | Maintainability, Security |
| `test`                         | Testcode                       | | Maintainability |
| `thrift`                       | Thrift                         | | Maintainability |
| `thymeleaf`                    | Thymeleaf                      | | Maintainability |
| `tibco`                        | TIBCO BW                       | | Maintainability |
| `tibcobe`                      | TIBCO BE (XML)                 | | Maintainability |
| `tibcobejava`                  | TIBCO BE (Java)                | | Maintainability |
| `tibcobestatemachine`          | TIBCO BE (State Machine)       | | Maintainability |
| `tibcobw6`                     | TIBCO BW6                      | | Maintainability |
| `tripleforms`                  | TriplEforms                    | | Maintainability |
| `tsql`                         | T-SQL                          | | Maintainability |
| `turtle`                       | Turtle                         | | Maintainability |
| `typescript`                   | TypeScript                     | | Maintainability, Security | (3) |
| `uil`                          | UIL (Motif)                    | | Maintainability |
| `uniface`                      | Uniface                        | | Maintainability |
| `until`                        | Until                          | | Maintainability |
| `vag`                          | Visual Age                     | | Maintainability |
| `vagrecord`                    | Visual Age Record              | | Maintainability |
| `vb`                           | Visual Basic                   | | Maintainability, Security | (4) |
| `vbnet`                        | Visual Basic .NET              | | Maintainability, Security | (4) |
| `velocity`                     | Velocity                       | | Maintainability |
| `vgl`                          | VGL                            | | Maintainability |
| `visualforce`                  | VisualForce                    | | Maintainability |
| `visualrpg`                    | Visual RPG                     | | Maintainability |
| `visualobjects`                | Visual Objects                 | | Maintainability |
| `vuejs`                        | VueJS                          | | Maintainability, Security | (2) |
| `vuets`                        | VueTS                          | | Maintainability, Security | (3) |
| `vulcan`                       | Vulcan.NET                     | | Maintainability |
| `webfocus`                     | WebFocus                       | | Maintainability |
| `webmethods`                   | WebMethods                     | | Maintainability |
| `webmethodsbpm`                | WebMethods BPM                 | | Maintainability |
| `websmart`                     | WebSmart                       | | Maintainability |
| `wonderware`                   | Wonderware                     | | Maintainability |
| `wsdl`                         | WSDL                           | | Maintainability |
| `wtx`                          | WTX                            | | Maintainability |
| `xaml`                         | XAML                           | | Maintainability |
| `xml`                          | XML                            | | Maintainability | (5) |
| `xpdl`                         | Tibco ActiveMatrix BPM         | | Maintainability |
| `xpp`                          | X++                            | | Maintainability |
| `xquery`                       | Xquery                         | | Maintainability |
| `xsd`                          | XSD                            | | Maintainability |
| `xslt`                         | XSLT                           | | Maintainability |
| `xul`                          | XUL                            | | Maintainability |
| `yaml`                         | YAML                           | | Maintainability | (5) |
| `unknown`                      | Unknown technology             | | Maintainability | (6) |

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
  - Use `vb` for [classic Visual Basic](https://en.wikipedia.org/wiki/Visual_Basic_(classic), which has been end-of-life since 2008.
5. In most cases, configuration files are not considered part of production code and are therefore not relevant for Sigrid's maintainability analysis. Only add these technologies if you consider them part of the system's production code.
6. "Unknown technology" will be shown in Sigrid when the technology cannot be detected.

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
| PyPi                  | Python                 |
| RubyGems              | Ruby                   |
| SBT                   | Scala                  |
| Unmanaged JAR files   | Java                   |
| Unmanaged DLL files   | C#                     |
| Unmanaged JS files    | JavaScript             |

## Requesting additional technology support

Even with 300+ supported technologies, we are still continuously working on adding support for new technologies and frameworks, and updating our technology suport for new technology versions. You can contact us using the information provided below if you believe we should extend technology support for your organization.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
