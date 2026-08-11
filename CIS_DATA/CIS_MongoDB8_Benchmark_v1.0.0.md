# CIS MongoDB 8 Benchmark 

v1.0.0 - 08-11-2025 

Internal Only - General 

## **Terms of Use** 

Please see the below link for our current terms of use: 

https://www.cisecurity.org/cis-securesuite/cis-securesuite-membership-terms-of-use/ 

For information on referencing and/or citing CIS Benchmarks in 3<sup>rd</sup> party documentation (including using portions of Benchmark Recommendations) please contact CIS Legal (legalnotices@cisecurity.org) and request guidance on copyright usage. 

**NOTE** :  It is **_NEVER_** acceptable to host a CIS Benchmark in **_ANY_** format (PDF, etc.) on a 3<sup>rd</sup> party (non-CIS owned) site. 

Page 1 

Internal Only - General 

## **Table of Contents** 

|**_Terms of Use .................................................................................................................. 1_**|
|---|
|**_Table of Contents ........................................................................................................... 2_**|
|**_Overview ......................................................................................................................... 4_**|
|**Important Usage Information .................................................................................................. 4**<br>|
|**Key Stakeholders .................................................................................................................................. 4**<br>|
|**Apply the Correct Version of a Benchmark ........................................................................................ 5**<br>|
|**Exceptions ............................................................................................................................................. 5**|
|**Remediation ........................................................................................................................................... 6**|
|**Summary ................................................................................................................................................ 6**|
|**Target Technology Details ....................................................................................................... 7**|
|**Intended Audience ................................................................................................................... 7**|
|**Consensus Guidance ............................................................................................................... 9**|
|**Typographical Conventions .................................................................................................. 10**|
|**_Recommendation Definitions ..................................................................................... 11_**|
|**Title .......................................................................................................................................... 11**|
|**Assessment Status ................................................................................................................ 11**|
|**Automated ............................................................................................................................................ 11**|
|**Manual .................................................................................................................................................. 11**|
|**Profile ...................................................................................................................................... 11**|
|**Description .............................................................................................................................. 11**|
|**Rationale Statement ............................................................................................................... 11**|
|**Impact Statement .................................................................................................................... 12**|
|**Audit Procedure ...................................................................................................................... 12**|
|**Remediation Procedure ......................................................................................................... 12**|
|**Default Value ........................................................................................................................... 12**|
|**References .............................................................................................................................. 12**|
|**CIS Critical Security Controls**<sup>**®**</sup>**(CIS Controls**<sup>**®**</sup>**) ................................................................... 12**|
|**Additional Information ........................................................................................................... 12**|
|**Profile Definitions ................................................................................................................... 13**|
|**Acknowledgements ................................................................................................................ 14**|
|**_Recommendations ....................................................................................................... 15_**|
|**1 Installation and Patching .................................................................................................... 15**|
|1.1 Ensure the appropriate MongoDB software version/patches are installed (Manual) ......... 16|
|**2 Authentication ..................................................................................................................... 18**<br>2.1 Ensure Authentication is configured (Automated) .............................................................. 19|



Page 2 

Internal Only - General 

|2.2 Ensure that MongoDB does not bypass authentication via the localhost exception|
|---|
|(Automated) .............................................................................................................................. 22|
|2.3 Ensure authentication is enabled in the sharded cluster (Automated) ............................... 24|
|**3 Authorization ....................................................................................................................... 28**|
|3.1 Ensure least privilege for database accounts (Manual) ..................................................... 29|
|3.2 Ensure that role-based access control is enabled and configured appropriately (Manual) 31<br>3.3 Ensure that MongoDB is run using a non-privileged, dedicated service account (Manual)33<br>|
|3.4 Ensure that each role for each MongoDB database is needed and grants only the<br>necessary privileges (Manual) .................................................................................................. 35|
|3.5 Review Superuser/Admin Roles (Manual) ......................................................................... 37|
|**4 Data Encryption ................................................................................................................... 39**|
|4.1 Ensure legacy TLS protocols are disabled (Automated) .................................................... 40|
|4.2 Ensure Weak Protocols are Disabled (Automated) ............................................................ 42|
|4.3 Ensure Encryption of Data in Transit TLS or SSL (Transport Encryption) (Automated) .... 44|
|4.4 Ensure Federal Information Processing Standard (FIPS) is enabled (Automated) ............ 47|
|4.5 Ensure Encryption of Data at Rest (Manual) ...................................................................... 49|
|**5 Audit Logging ...................................................................................................................... 51**<br>|
|5.1 Ensure that system activity is audited (Automated) ........................................................... 52|
|5.2 Ensure that audit filters are configured properly (Manual) ................................................. 54|
|5.3 Ensure that logging captures as much information as possible (Automated) .................... 56|
|5.4 Ensure that new entries are appended to the end of the log file (Automated) ................... 58|
|**6 Operating System Hardening ............................................................................................. 60**|
|6.1 Ensure that MongoDB uses a non-default port (Automated) ............................................. 61|
|6.2 Ensure that operating system resource limits are set for MongoDB (Manual) ................... 63|
|6.3 Ensure that server-side scripting is disabled if not needed (Manual) ................................. 65|
|**7 File Permissions .................................................................................................................. 67**|
|7.1 Ensure appropriate key file permissions are set (Manual) ................................................. 68|
|7.2 Ensure appropriate database file permissions are set. (Manual) ....................................... 70|
|**_Appendix: Summary Table .......................................................................................... 72_**|
|**_Appendix: CIS Controls v7 IG 1 Mapped Recommendations .................................. 74_**|
|**_Appendix: CIS Controls v7 IG 2 Mapped Recommendations .................................. 75_**|
|**_Appendix: CIS Controls v7 IG 3 Mapped Recommendations .................................. 77_**|
|**_Appendix: CIS Controls v7 Unmapped Recommendations ..................................... 79_**|
|**_Appendix: CIS Controls v8 IG 1 Mapped Recommendations .................................. 80_**|
|**_Appendix: CIS Controls v8 IG 2 Mapped Recommendations .................................. 81_**|
|**_Appendix: CIS Controls v8 IG 3 Mapped Recommendations .................................. 83_**|
|**_Appendix: CIS Controls v8 Unmapped Recommendations ..................................... 85_**|
|**_Appendix: Change History .......................................................................................... 86_**|



Page 3 

Internal Only - General 

## **Overview** 

All CIS Benchmarks™ (Benchmarks) focus on technical configuration settings used to maintain and/or increase the security of the addressed technology, and they should be used in **conjunction** with other essential cyber hygiene tasks like: 

- Monitoring the base operating system and applications for vulnerabilities and quickly updating with the latest security patches. 

- End-point protection (Antivirus software, Endpoint Detection and Response (EDR), etc.). 

- Logging and monitoring user and system activity. 

In the end, the Benchmarks are designed to be a key **component** of a comprehensive cybersecurity program. 

#### **Important Usage Information** 

All Benchmarks are available free for non-commercial use from the <u>CIS Website. They</u> can be used to manually assess and remediate systems and applications. In lieu of manual assessment and remediation, there are several tools available to assist with assessment: 

- <u>CIS Configuration Assessment Tool (CIS-CAT</u><sup>®</sup> <u>Pro Assessor)</u> 

- <u>CIS Benchmarks™ Certified 3rd Party Tooling</u> 

These tools make the hardening process much more scalable for large numbers of systems and applications. 

**NOTE** : Some tooling focuses only on the Benchmark Recommendations that can be fully automated (skipping ones marked **Manual** ). It is important that **_ALL_** Recommendations ( **Automated** and **Manual** ) be addressed since all are important for properly securing systems and are typically in scope for audits. 

##### **Key Stakeholders** 

Cybersecurity is a collaborative effort, and cross functional cooperation is imperative within an organization to discuss, test, and deploy Benchmarks in an effective and efficient way. The Benchmarks are developed to be best practice configuration guidelines applicable to a wide range of use cases. In some organizations, exceptions to specific Recommendations will be needed, and this team should work to prioritize the problematic Recommendations based on several factors like risk, time, cost, and labor. These exceptions should be properly categorized and documented for auditing purposes. 

Page 4 

Internal Only - General 

##### **Apply the Correct Version of a Benchmark** 

Benchmarks are developed and tested for a specific set of products and versions and applying an incorrect Benchmark to a system can cause the resulting pass/fail score to be incorrect. This is due to the assessment of settings that do not apply to the target systems. To assure the correct Benchmark is being assessed: 

- **Deploy the Benchmark applicable to the way settings are managed in the environment:** An example of this is the Microsoft Windows family of Benchmarks, which have separate Benchmarks for Group Policy, Intune, and Stand-alone systems based upon how system management is deployed. Applying the wrong Benchmark in this case will give invalid results. 

- **Use the most recent version of a Benchmark** : This is true for all Benchmarks, but especially true for cloud technologies. Cloud technologies change frequently and using an older version of a Benchmark may have invalid methods for auditing and remediation. 

##### **Exceptions** 

The guidance items in the Benchmarks are called recommendations and not requirements, and exceptions to some of them are expected and acceptable. The Benchmarks strive to be a secure baseline, or starting point, for a specific technology, with known issues identified during Benchmark development are documented in the Impact section of each Recommendation. In addition, organizational, system specific requirements, or local site policy may require changes as well, or an exception to a Recommendation or group of Recommendations (e.g. A Benchmark could Recommend that a Web server not be installed on the system, but if a system's primary purpose is to function as a Webserver, there should be a documented exception to this Recommendation for that specific server). 

In the end, exceptions to some Benchmark Recommendations are common and acceptable, and should be handled as follows: 

- The reasons for the exception should be reviewed cross-functionally and be well documented for audit purposes. 

- A plan should be developed for mitigating, or eliminating, the exception in the future, if applicable. 

- If the organization decides to accept the risk of this exception (not work toward mitigation or elimination), this should be documented for audit purposes. 

It is the responsibility of the organization to determine their overall security policy, and which settings are applicable to their unique needs based on the overall risk profile for the organization. 

Page 5 

Internal Only - General 

##### **Remediation** 

CIS has developed <u>Build Kits</u> for many technologies to assist in the automation of hardening systems. Build Kits are designed to correspond to Benchmark's “Remediation” section, which provides the manual remediation steps necessary to make that Recommendation compliant to the Benchmark. 

**When remediating systems (changing configuration settings on deployed systems as per the Benchmark's Recommendations), please approach this with caution and test thoroughly.** 

The following is a reasonable remediation approach to follow: 

- CIS Build Kits, or internally developed remediation methods should never be applied to production systems without proper testing. 

- Proper testing consists of the following: 

   - Understand the configuration (including installed applications) of the targeted systems. Various parts of the organization may need different configurations (e.g., software developers vs standard office workers). 

   - Read the Impact section of the given Recommendation to help determine if there might be an issue with the targeted systems. 

   - Test the configuration changes with representative lab system(s). If issues arise during testing, they can be resolved prior to deploying to any production systems. 

   - When testing is complete, initially deploy to a small sub-set of production systems and monitor closely for issues. If there are issues, they can be resolved prior to deploying more broadly. 

   - When the initial deployment above is completes successfully, iteratively deploy to additional systems and monitor closely for issues. Repeat this process until the full deployment is complete. 

##### **Summary** 

Using the Benchmarks Certified tools, working as a team with key stakeholders, being selective with exceptions, and being careful with remediation deployment, it is possible to harden large numbers of deployed systems in a cost effective, efficient, and safe manner. 

- **NOTE** : As previously stated, the PDF versions of the CIS Benchmarks™ are available for free, non-commercial use on the <u>CIS Website. All other formats</u> of the CIS Benchmarks™ (MS Word, Excel, and <u>Build Kits) are available for</u> CIS <u>SecureSuite</u><sup>®</sup> members. 

CIS-CAT<sup>®</sup> Pro is also available to CIS <u>SecureSuite</u><sup>®</sup> members. 

Page 6 

Internal Only - General 

#### **Target Technology Details** 

This document, CIS MongoDB 8.0 Benchmark, provides prescriptive guidance for establishing a secure configuration posture for MongoDB version/s 8.x. 

This guide was tested against MongoDB 8.0.0 running on Ubuntu Linux, Linux Red hat, and Windows but applies to other distributions as well. 

To obtain the latest version of this guide, please visit http://benchmarks.cisecurity.org. If you have questions, comments, or have identified ways to improve this guide, please write to us at <u>feedback@cisecurity.org.</u> 

**_Extracting Running Configuration File_** 

To verify the MongoDB running configuration file we need to connect MongoDB instance using MongoDB client with valid username/password and execute this command: 

```
db.runCommand( { getCmdLineOpts: 1 } )
```

The response will contain MongoDB running configuration file location. For example: 

```
"config" : "/etc/mongod.conf",
```

**MongoDB Configuration File Location 

** 

- For Windows: "\bin\mongod.cfg" 

- For macOS: "/usr/local/etc/mongod.conf" (Intel processors) and "/opt/homebrew/etc/mongod.conf" (Apple M1 processors) 

- For Linux: "/etc/mongod.conf" 

###### **Important Information** 

- Automated Assessment Content is provided for Linux platforms only and is set to look for mongod.conf in path /etc/mongod.conf. 

- Mongod: The primary daemon process for the MongoDB system. It handles data requests, manages data access, and performs background management operations. 

- Mongos: mongos is a routing service for MongoDB Sharded Clusters.mongos requires mongod config, which stores the metadata of the cluster.MongoDB Shard Utility, the controller and query router for sharded clusters. Sharding partitions the data-set into discrete parts. 

#### **Intended Audience** 

This document is intended for system and application administrators, security specialists, auditors, help desk, and platform deployment personnel who plan to develop, deploy, assess, or secure solutions that incorporate MongoDB. 

Page 7 

Internal Only - General 

Page 8 

Internal Only - General 

#### **Consensus Guidance** 

This CIS Benchmark™ was created using a consensus review process comprised of a global community of subject matter experts. The process combines real world experience with data-based information to create technology specific guidance to assist users to secure their environments. Consensus participants provide perspective from a diverse set of backgrounds including consulting, software development, audit and compliance, security research, operations, government, and legal. 

Each CIS Benchmark undergoes two phases of consensus review. The first phase occurs during initial Benchmark development. During this phase, subject matter experts convene to discuss, create, and test working drafts of the Benchmark. This discussion occurs until consensus has been reached on Benchmark recommendations. The second phase begins after the Benchmark has been published. During this phase, all feedback provided by the Internet community is reviewed by the consensus team for incorporation in the Benchmark. If you are interested in participating in the consensus process, please visit <u>https://workbench.cisecurity.org/.</u> 

Page 9 

Internal Only - General 

#### **Typographical Conventions** 

The following typographical conventions are used throughout this guide: 

|**Convention**|**Meaning**|
|---|---|
|`Stylized Monospace font`|Used for blocks of code, command, and<br>script examples. Text should be interpreted<br>exactly as presented.|
|Monospace font|Used for inline code, commands, UI/Menu<br>selections or examples. Text should be<br>interpreted exactly as presented.|
|<Monospace font in brackets>|Text set in angle brackets denote a variable<br>requiring substitution for a real value.|
|_Italic font_|Used to reference other relevant settings,<br>CIS Benchmarks and/or Benchmark<br>Communities. Also, used to denote the title<br>of a book, article, or other publication.|
|**Bold font**|Additional information or caveats things like<br>**Notes**,**Warnings**, or**Cautions**(usually just<br>the word itself and the rest of the text<br>normal).|



Page 10 

Internal Only - General 

## **Recommendation Definitions** 

The following defines the various components included in a CIS recommendation as applicable.  If any of the components are not applicable it will be noted, or the component will not be included in the recommendation. 

#### **Title** 

Concise description for the recommendation's intended configuration. 

#### **Assessment Status** 

An assessment status is included for every recommendation. The assessment status indicates whether the given recommendation can be automated or requires manual steps to implement. Both statuses are equally important and are determined and supported as defined below: 

##### **Automated** 

Represents recommendations for which assessment of a technical control can be fully automated and validated to a pass/fail state. Recommendations will include the necessary information to implement automation. 

##### **Manual** 

Represents recommendations for which assessment of a technical control cannot be fully automated and requires all or some manual steps to validate that the configured state is set as expected. The expected state can vary depending on the environment. 

#### **Profile** 

A collection of recommendations for securing a technology or a supporting platform. Most benchmarks include at least a Level 1 and Level 2 Profile. Level 2 extends Level 1 recommendations and is not a standalone profile. The Profile Definitions section in the benchmark provides the definitions as they pertain to the recommendations included for the technology. 

#### **Description** 

Detailed information pertaining to the setting with which the recommendation is concerned. In some cases, the description will include the recommended value. 

#### **Rationale Statement** 

Detailed reasoning for the recommendation to provide the user a clear and concise understanding on the importance of the recommendation. 

Page 11 

Internal Only - General 

#### **Impact Statement** 

Any security, functionality, or operational consequences that can result from following the recommendation. 

#### **Audit Procedure** 

Systematic instructions for determining if the target system complies with the recommendation. 

#### **Remediation Procedure** 

Systematic instructions for applying recommendations to the target system to bring it into compliance according to the recommendation. 

#### **Default Value** 

Default value for the given setting in this recommendation, if known. If not known, either not configured or not defined will be applied. 

#### **References** 

Additional documentation relative to the recommendation. 

#### **CIS Critical Security Controls**<sup>**®**</sup> **(CIS Controls**<sup>**®**</sup> **)** 

The mapping between a recommendation and the CIS Controls is organized by CIS Controls version, Safeguard, and Implementation Group (IG). The Benchmark in its entirety addresses the CIS Controls safeguards of (v7) “5.1 - Establish Secure Configurations” and (v8) '4.1 - Establish and Maintain a Secure Configuration Process” so individual recommendations will not be mapped to these safeguards. 

#### **Additional Information** 

Supplementary information that does not correspond to any other field but may be useful to the user. 

Page 12 

Internal Only - General 

#### **Profile Definitions** 

The following configuration profiles are defined by this Benchmark: 

- **Level 1- MongoDB** 

Items in this profile apply to MongoDB and intend to: 

   - be practical and prudent; 

   - provide a clear security benefit; and 

   - not inhibit the utility of the technology beyond acceptable means. 

- **Level 2 - MongoDB** 

This profile extends the “Level 1 - MongoDB” profile. Items in this profile apply to MongoDB and exhibit one or more of the following characteristics: 

- are intended for environments or use cases where security is paramount 

- acts as defense in depth measure 

- may negatively inhibit the utility or performance of the technology. 

Page 13 

Internal Only - General 

#### **Acknowledgements** 

This Benchmark exemplifies the great things a community of users, vendors, and subject matter experts can accomplish through consensus collaboration. The CIS community thanks the entire consensus team with special recognition to the following individuals who contributed greatly to the creation of this guide: 

Special thanks to: 

**Author/s** Vinesh Redkar Pralhad Chaskar 

**Editor/s** Randall Mowen Matthew Reagan 

**Contributor/s** Tony Wilwerding James Scott Mark larinde 

Page 14 

Internal Only - General 

## **Recommendations** 

#### **1 Installation and Patching** 

This section provides guidance on ensuring that the MongoDB software is up to date to eliminate easily avoidable vulnerabilities. 

Page 15 

Internal Only - General 

_1.1 Ensure the appropriate MongoDB software version/patches are installed (Manual)_ 

###### **Profile Applicability:** 

- Level 1- MongoDB 

###### **Description:** 

The MongoDB installation version, along with the patch level, should be the most recent that is compatible with the organization's operational needs. In addition, regularly view latest minor security patch updates for security vulnerability fixes (CVE Related) from MongoDB website: https://www.mongodb.com/alerts 

###### **Rationale:** 

Using the most recent MongoDB software version along with all applicable patches, helps limit the possibilities for vulnerabilities in the software. The installation version and/or patches applied should be selected according to the needs of the organization. At a minimum, the software version should be supported. 

###### **Audit:** 

On Ubuntu: 

Run the following command from within the MongoDB shell to determine if the MongoDB software version complies with your organization’s operational needs: 

```
mongo --version
db.version() #Inside mongo console
```

On Windows: 

Navigate to the Installation directory of Mongo DB on the server and run below command 

```
mongod.exe --version
```

###### **Remediation:** 

Upgrade to the latest version of the MongoDB software: 

1. Backup the data set. 

2. Download the binaries for the latest MongoDB revision from the MongoDB Download Page and store the binaries in a temporary location. The binaries download as compressed files that extract to the directory structure used by the MongoDB installation. 

3. Shutdown the MongoDB instance. 4. Replace the existing MongoDB binaries with the downloaded binaries. 5. Restart the MongoDB instance. 

Page 16 

Internal Only - General 

###### **Default Value:** 

###### Patches are not installed by default. 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/installation/</u> 2. <u>https://www.mongodb.com/docs/v7.0/release-notes/7.0/#std-label-release-notes7.0</u> 

3. <u>https://www.mongodb.com/download-center#community</u> 4. <u>https://www.mongodb.com/support-policy</u> 5. <u>https://www.mongodb.com/alerts</u> 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|2.3Address Unauthorized Software<br>Ensure that unauthorized software is either removed from use on enterprise<br>assets or receives a documented exception. Review monthly, or more frequently.|●|●|●|
|v7|2.2Ensure Software is Supported by Vendor<br>Ensure that only software applications or operating systems currently supported<br>by the software's vendor are added to the organization's authorized software<br>inventory. Unsupported software should be tagged as unsupported in the inventory<br>system.|●|●|●|



Page 17 

Internal Only - General 

#### **2 Authentication** 

This section contains recommendations for requiring authentication before allowing access to the MongoDB database. 

Page 18 

Internal Only - General 

#### _2.1 Ensure Authentication is configured (Automated)_ 

###### **Profile Applicability:** 

- Level 1- MongoDB 

###### **Description:** 

This setting ensures that all clients, users, servers are required to authenticate before being granted access to the MongoDB database. 

Authentication is the process of verifying the identity of a client. When access control, i.e. authorization, is enabled, MongoDB requires all clients to authenticate themselves in order to determine their access. 

from MongoDB documentation 

###### Authentication Mechanisms 

MongoDB supports a number of authentication mechanisms that clients can use to verify their identity. These mechanisms allow MongoDB to integrate into your existing authentication system. 

MongoDB supports multiple authentication mechanisms: 

- SCRAM (Default) 

- x.509 Certificate Authentication. 

###### Certificate Authority 

For production use, your MongoDB deployment should use valid certificates generated and signed by a certificate authority. You or your organization can generate and maintain an independent certificate authority, or use certificates generated by third-party TLS/SSL vendors. 

In addition to supporting the aforementioned mechanisms, MongoDB Enterprise also supports the following mechanisms: 

- LDAP proxy authentication 

- Kerberos authentication. 

###### **Rationale:** 

Failure to authenticate clients, users, servers can enable unauthorized access to the MongoDB database and can prevent tracing actions back to their sources. 

It's highly recommended that password length and complexity also be in-place. When performing the traditional user/password authentication against MongoDB there is not in-place intrinsic password complexity check and there is no LOCKING mechanism with multiple failure logins. So, MongoDB is prone to brute force attacks compared to other database systems. 

Page 19 

Internal Only - General 

###### **Audit:** 

Run the following command to verify whether an authorization is enabled on the MongoDB server. On Ubuntu: 

```
cat /etc/mongod.conf | grep “authorization”
```

On Windows: 

```
type mongod.conf | findstr “authorization”
```

The value for authorization must be set to enabled. 

To authenticate using the mongo shell use the following approach 

- Use the mongo command-line authentication options (--username, --password, and --authenticationDatabase) when connecting to the mongod or mongos instance Or 

- Connect first to the mongod or mongos instance, and then run the authenticate command or the db.auth() method against the authentication database. 

###### **Remediation:** 

The authentication mechanism should be implemented before anyone accesses the MongoDB Server. 

To enable the authentication mechanism: 

- Start the MongoDB instance without authentication. 

```
mongod --port 27017 --dbpath /data/db1
```

###### Or 

```
mongod.exe --port 27017 --dbpath db1
```

- Create the system user administrator, ensuring that its password meets organizationally-defined password in terms of length and complexity requirements as there is no in-place locking mechanism for multiple failed login attempts against MongoDB. 

Page 20 

Internal Only - General 

```
use admin
db.createUser(
  {
    user: "MongoAdmin",
    pwd: "password",
    roles: [ { role: "root", db: "admin" } ]
  }
)
```

- Open mongod.conf and change for authorization value to enabled: 

```
security:
    authorization: "enabled"
```

- Restart the MongoDB instance 

```
service mongod restart
```

###### **Default Value:** 

By default, authorization is set to disable. 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/core/authentication/</u> 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.2Use Unique Passwords<br>Use unique passwords for all enterprise assets. Best practice implementation<br>includes, at a minimum, an 8-character password for accounts using MFA and a<br>14-character password for accounts not using MFA.|●|●|●|
|v8|6.3Require MFA for Externally-Exposed Applications<br>Require all externally-exposed enterprise or third-party applications to enforce<br>MFA, where supported. Enforcing MFA through a directory service or SSO<br>provider is a satisfactory implementation of this Safeguard.||●|●|
|v7|16.3Require Multi-factor Authentication<br>Require multi-factor authentication for all user accounts, on all systems,<br>whether managed onsite or by a third-party provider.||●|●|



Page 21 

Internal Only - General 

_2.2 Ensure that MongoDB does not bypass authentication via the localhost exception (Automated)_ 

###### **Profile Applicability:** 

•  Level 1- MongoDB 

###### **Description:** 

MongoDB should not be set to bypass authentication via the localhost exception. The localhost exception allows the user to enable authorization before creating the first user in the system. When active, the localhost exception allows all connections from the localhost interface to have full access to that instance. The exception applies only when there are no users created in the MongoDB instance. 

**Note:** This recommendation only applies when there are no users created in the MongoDB instance. 

###### **Rationale:** 

Disabling this exception will prevent unauthorized local access to the MongoDB database. It will also ensure the traceability of each database activity to a specific user. Localhost Exception allows direct connect to Mongod’s without any UN/PW. 

###### **Audit:** 

Run the following command to extract the information about enableLocalhostAuthBypass setting on Configuration File. On Ubuntu: 

```
cat /etc/mongod.conf |grep "enableLocalhostAuthBypass"
```

On Windows: 

```
type mongod.conf | findstr "enableLocalhostAuthBypass"
```

The value for enableLocalhostAuthBypass must be false. 

###### **Remediation:** 

To disable local authentication on the MongoDB database. Type OS Console Command 

```
mongod --setParameter enableLocalhostAuthBypass=0
```

**or** 

To manually configure use the setParameter option in the mongo configuration file to set it to false. 

Page 22 

Internal Only - General 

```
setParameter:
  enableLocalhostAuthBypass: false
```

###### **Default Value:** 

By default, localhost exception value (enableLocalhostAuthBypass) is true. 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/core/localhost-exception/</u> 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|6.3Require MFA for Externally-Exposed Applications<br>Require all externally-exposed enterprise or third-party applications to enforce<br>MFA, where supported. Enforcing MFA through a directory service or SSO<br>provider is a satisfactory implementation of this Safeguard.||●|●|
|v7|16.3Require Multi-factor Authentication<br>Require multi-factor authentication for all user accounts, on all systems,<br>whether managed onsite or by a third-party provider.||●|●|



Page 23 

Internal Only - General 

_2.3 Ensure authentication is enabled in the sharded cluster (Automated)_ 

###### **Profile Applicability:** 

- Level 2 - MongoDB 

###### **Description:** 

Authentication is enabled in a sharded cluster when the certificate or key files are created and configured for all components. This ensures that every client that accesses the cluster must provide credentials, to include MongoDB instances that access each other within the cluster. 

With keyfile authentication, each mongod or mongos instance in the sharded cluster uses the contents of the keyfile as the shared password for authenticating other members in the deployment. Only mongod or mongos instances with the correct keyfile can join the sharded cluster. 

**For Production Environment** : x.509 certificate authentication with secure TSL/SSL connection must be used for authentication. 

**For Development Purpose** : Key file can be used as an authentication mechanism between the shared cluster. Keyfiles are bare-minimum forms of security and are best suited for testing or development environments. 

###### **Rationale:** 

Enforcing a key or certificate on a sharded cluster prevents unauthorized access to the MongoDB database and provides traceability of database activities to a specific user or component. A MongoDB sharded cluster can enforce user authentication as well as internal authentication of its components to secure against unauthorized access. 

###### **Audit:** 

Based on recommendations 

- PEMKeyFile, clusterFile, CAFile must be configured. 

- clusterAuthMode should be set to x509 

- authenticationMechanisms should be set to MONGODB-X509. 

To Check That your Current MongoDB is configured for sharding setup, execute the 

<u>following command:</u> 

```
sh.status()
```

OR 

Page 24 

Internal Only - General 

```
db.printShardingStatus()
```

Run the following command to verify that the certificate-based authentication is configured: On Ubuntu: 

```
cat /etc/mongod.conf | grep "clusterAuthMode"
```

On Windows: 

```
type mongod.conf | findstr “clusterAuthMode”
```

Run the following command to verify that the key file-based authentication is configured: ( _Only for Development Purpose_ ) On Ubuntu: 

```
cat /etc/mongod.conf | grep “keyFile”
```

On Windows: 

```
type mongod.conf | findstr “keyFile”
```

###### **Remediation:** 

To authenticate to servers, clients can use x.509 certificates instead of usernames and passwords. 

MongoDB supports x.509 certificate authentication for use with a secure TLS/SSL connection. The x.509 client authentication allows clients to authenticate to servers with certificates rather than with a username and password. 

Change the configuration file /etc/mongod.conf on each host, adding the following rows: 

Page 25 

Internal Only - General 

```
net:
   port: 27017
   tls:
      mode: requireSSL
      PEMKeyFile: /etc/mongodb/ssl/server1.pem
      CAFile: /etc/mongodb/ssl/mongoCA.crt
      clusterFile: /etc/mongodb/ssl/server1.pem
   security:
      authorization: enabled
      clusterAuthMode: x509
security:
   authorization: enabled
   clusterAuthMode: x509
net:
   tls:
      mode: requireTLS
      certificateKeyFile: <path to its TLS/SSL certificate and key file>
      CAFile: <path to root CA PEM file to verify received certificate>
      clusterFile: <path to its certificate key file for membership
authentication>
   bindIp: localhost,<hostname(s)|ip address(es)>
```

###### Restart the daemon 

```
sudo service mongodb restart
```

To enable authentication in the sharded cluster, perform the following steps:( _Only for Development Purpose_ ) 

- <u>Generate A Key File</u> 

- On each component in the shared cluster, enable authentication by editing the configuration file /etc/mongod.conf. Set the keyFile option to the key file’s path and then start the component with this command: 

```
keyFile = /srv/mongodb/keyfile
```

- When starting the component, set --keyFile option, which is an option for both mongos instances and mongod instances. Set the --keyFile to the key file’s path. 

###### **Default Value:** 

Not configured 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/core/security-transport-encryption/#stdlabel-transport-encryption</u> 

2. <u>https://www.mongodb.com/docs/v7.0/reference/security/</u> 

Page 26 

Internal Only - General 

3. <u>https://www.mongodb.com/docs/v7.0/tutorial/deploy-shard-cluster/</u> 4. <u>https://www.mongodb.com/docs/manual/tutorial/configure-x509-memberauthentication/</u> 

5. <u>https://www.mongodb.com/docs/manual/tutorial/deploy-sharded-cluster-withkeyfile-accesscontrol/#:~:text=With%20keyfile%20authentication%2C%20each%20mongod,ca n%20join%20the%20sharded%20cluster.</u> 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|6.6Establish and Maintain an Inventory of Authentication<br>and Authorization Systems<br>Establish and maintain an inventory of the enterprise’s authentication and<br>authorization systems, including those hosted on-site or at a remote service<br>provider. Review and update the inventory, at a minimum, annually, or more<br>frequently.||●|●|
|v7|1.8Utilize Client Certificates to Authenticate Hardware<br>Assets<br>Use client certificates to authenticate hardware assets connecting to the<br>organization's trusted network.|||●|



Page 27 

Internal Only - General 

#### **3 Authorization** 

MongoDB grants access to data and commands through "role-based" approach , MongoDB is shipped with built-in roles that provide the different levels of access commonly needed in a database system. In addition, you can create custom-roles. 

Page 28 

Internal Only - General 

- _3.1 Ensure least privilege for database accounts (Manual)_ 

###### **Profile Applicability:** 

- Level 1- MongoDB 

###### **Description:** 

MongoDB grants access to data and commands through "role-based" approach, MongoDB is shipped with built-in roles that provide the different levels of access commonly needed in a database system. In addition, you can create custom-roles. 

The following roles provide the ability to assign any user any privilege on any database, which means that users with one of these roles can assign themselves any privilege on any database: 

dbOwner role, when scoped to the admin database userAdmin role, when scoped to the admin database userAdminAnyDatabase role 

###### **Rationale:** 

Ensuring highly privileged Roles are granted only for database administrators, and roles are not scoped to "admin" databases will reduce attack surface and follows the least privilege principle. 

###### **Audit:** 

To check accounts with database roles scoped in "admin" database, use the following query: 

```
db.system.users.find(
{"roles.role":{$in:["dbOwner","userAdmin","userAdminAnyDatabase"]},"roles.db"
: "admin" } )
```

**Remediation:** 

If any accounts were listed with built in-roles: 

```
dbOwner
userAdmin
userAdminAnyDatabase
```

in "admin" database role then drop them. 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/reference/built-in-roles/</u> 

Page 29 

Internal Only - General 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet<br>browsing, email, and productivity suite use, from the user’s primary, non-privileged<br>account.|●|●|●|
|v7|4.3Ensure the Use of Dedicated Administrative Accounts<br>Ensure that all users with administrative account access use a dedicated or<br>secondary account for elevated activities. This account should only be used for<br>administrative activities and not internet browsing, email, or similar activities.|●|●|●|



Page 30 

Internal Only - General 

- _3.2 Ensure that role-based access control is enabled and configured appropriately (Manual)_ 

###### **Profile Applicability:** 

- Level 1- MongoDB 

###### **Description:** 

Role-based access control (RBAC) is a method of regulating access to resources based on the roles of individual users within an enterprise. A user is granted one or more roles that determine the user’s access to database resources and operations. Outside of role assignments, the user has no access to the system. MongoDB can use RBAC to govern access to MongoDB systems. MongoDB does not enable authorization by default. 

###### **Rationale:** 

When properly implemented, RBAC enables users to carry out a wide range of authorized tasks by dynamically regulating their actions according to flexible functions. This allows an organization to control employees’ access to all database tables through RBAC. 

###### **Audit:** 

Connect to MongoDB with the appropriate privileges and run the following command: 

Identify users' roles and privileges: 

```
> db.getUser()
```

```
> db.getRole()
```

Verify that the appropriate role or roles have been configured for each user. 

###### **Remediation:** 

1. Establish roles for MongoDB. 2. Assign the appropriate privileges to each role. 3. Assign the appropriate users to each role. 4. Remove any individual privileges assigned to users that are now addressed by the roles. 

5. See the reference below for more Information. 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/tutorial/manage-users-and-roles/</u> 

Page 31 

Internal Only - General 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|6.8Define and Maintain Role-Based Access Control<br>Define and maintain role-based access control, through determining and<br>documenting the access rights necessary for each role within the enterprise to<br>successfully carry out its assigned duties. Perform access control reviews of<br>enterprise assets to validate that all privileges are authorized, on a recurring<br>schedule at a minimum annually, or more frequently.|||●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share, claims,<br>application, or database specific access control lists. These controls will enforce the<br>principle that only authorized individuals should have access to the information<br>based on their need to access the information as a part of their responsibilities.|●|●|●|



Page 32 

Internal Only - General 

_3.3 Ensure that MongoDB is run using a non-privileged, dedicated service account (Manual)_ 

###### **Profile Applicability:** 

- Level 1- MongoDB 

###### **Description:** 

The MongoDB service should not be run using a privileged account such as 'root' because this unnecessarily exposes the operating system to high risk. 

###### **Rationale:** 

Using a non-privileged, dedicated service account restricts the database from accessing the critical areas of the operating system which are not required by the MongoDB. This will also mitigate the potential for unauthorized access via a compromised, privileged account on the operating system. 

###### **Audit:** 

Run the following command to get listing of all mongo instances, the PID number, and the PID owner. 

```
ps -ef | grep -E "mongos|mongod"
```

**Remediation:** 

1. Create a dedicated user for performing MongoDB database activity. 2. Set the Database data files, the keyfile, and the SSL private key files to only be readable by the mongod/mongos user. 

3. Set the log files to only be writable by the mongod/mongos user and readable only by root. 

###### **Default Value:** 

Not configured 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/tutorial/manage-users-and-roles/</u> 

Page 33 

Internal Only - General 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.5Establish and Maintain an Inventory of Service<br>Accounts<br>Establish and maintain an inventory of service accounts. The inventory, at a<br>minimum, must contain department owner, review date, and purpose. Perform<br>service account reviews to validate that all active accounts are authorized, on a<br>recurring schedule at a minimum quarterly, or more frequently.||●|●|
|v7|4.3Ensure the Use of Dedicated Administrative Accounts<br>Ensure that all users with administrative account access use a dedicated or<br>secondary account for elevated activities. This account should only be used for<br>administrative activities and not internet browsing, email, or similar activities.|●|●|●|



Page 34 

Internal Only - General 

- _3.4 Ensure that each role for each MongoDB database is needed and grants only the necessary privileges (Manual)_ 

###### **Profile Applicability:** 

- Level 1- MongoDB 

###### **Description:** 

Reviewing all roles periodically and eliminating unneeded roles as well as unneeded privileges from necessary roles helps minimize the privileges that each user has. 

###### **Rationale:** 

Although role-based access control (RBAC) has many advantages for regulating access to resources, over time some roles may no longer be needed, and some roles may grant privileges that are no longer needed. 

###### **Audit:** 

Perform the following command to view all roles on the database on which the command runs, including both built-in and user-defined roles, as well as the privileges granted by each role. Ensure that only necessary roles are listed and only the necessary privileges are listed for each role. 

```
db.runCommand(
   {
      rolesInfo: 1,
      showPrivileges: true,
      showBuiltinRoles: true
   }
)
```

###### **Remediation:** 

To revoke specified privileges from the user-defined role on the database where the command is run. The revokePrivilegesFromRole command has the following syntax: 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/reference/privilege-actions/#mongodbauthaction-revokeRole</u> 

2. <u>https://www.mongodb.com/docs/v7.0/core/authorization/#std-label-privileges</u> 

###### **Additional Information:** 

You must have the dropRole action on a database to drop a role from that database. 

Page 35 

Internal Only - General 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet browsing,<br>email, and productivity suite use, from the user’s primary, non-privileged account.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 36 

Internal Only - General 

#### _3.5 Review Superuser/Admin Roles (Manual)_ 

###### **Profile Applicability:** 

- Level 2 - MongoDB 

###### **Description:** 

Roles provide several advantages that make it easier to manage privileges in a database system. Security administrators can control access to their databases in a way that mirrors the structure of their organizations (they can create roles in the database that map directly to the job functions in their organizations). The assignment of privileges is simplified. Instead of granting the same set of privileges to each individual user in a particular job function, the administrator can grant this set of privileges to a role representing that job function and then grant that role to each user in that job function. 

###### **Rationale:** 

Reviewing the Superuser/Admin roles within a database helps minimize the possibility of privileged unwanted access. 

###### **Audit:** 

**Superuser roles** provide the ability to assign any user any privilege on any database, which means that users with one of these roles can assign themselves any privilege on any database: 

```
db.runCommand( { rolesInfo: "dbOwner" } )
db.runCommand( { rolesInfo: "userAdmin" } )
db.runCommand( { rolesInfo: "userAdminAnyDatabase" } )
```

**Root role** provides access to the operations and all the resources of the readWriteAnyDatabase, dbAdminAnyDatabase, userAdminAnyDatabase, clusterAdmin roles, restore combined. 

```
db.runCommand( { rolesInfo: "readWriteAnyDatabase" } )
db.runCommand( { rolesInfo: "dbAdminAnyDatabase" } )
db.runCommand( { rolesInfo: "userAdminAnyDatabase" } )
db.runCommand( { rolesInfo: "clusterAdmin" } )
```

**Cluster Administration Roles** are used for administering the whole system rather than just a single database. 

```
db.runCommand( { rolesInfo: "hostManager" } )
```

###### **Remediation:** 

To remove a user from one or more roles on the current database. 

Page 37 

Internal Only - General 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/core/security-user-defined-roles/</u> 

2. <u>https://www.mongodb.com/docs/v7.0/reference/method/#std-label-rolemanagement-methods</u> 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet<br>browsing, email, and productivity suite use, from the user’s primary, non-privileged<br>account.|●|●|●|
|v7|4.3Ensure the Use of Dedicated Administrative Accounts<br>Ensure that all users with administrative account access use a dedicated or<br>secondary account for elevated activities. This account should only be used for<br>administrative activities and not internet browsing, email, or similar activities.|●|●|●|
|v7|16.8Disable Any Unassociated Accounts<br>Disable any account that cannot be associated with a business process or<br>business owner.|●|●|●|



Page 38 

Internal Only - General 

#### **4 Data Encryption** 

This section contains recommendations for securing data at rest (stored) and data in motion (transiting) for MongoDB. 

Page 39 

Internal Only - General 

- _4.1 Ensure legacy TLS protocols are disabled (Automated)_ 

###### **Profile Applicability:** 

- Level 2 - MongoDB 

###### **Description:** 

Only modern TLS protocols should be enabled in MongoDB for all client connections and upstream connections. Removing legacy TLS and SSL protocols (SSL 3.0, TLS 1.0 and 1.1), and enabling emerging and stable TLS protocols (TLS 1.2, and TLS 1.3), ensures users are able to take advantage of strong security capabilities and protects them from insecure legacy protocols. 

###### **Rationale:** 

**Why disable TLS 1.0:** TLS 1.0 was deprecated from use when PCI DSS Compliance mandated that it not be used for any applications processing credit card numbers in June 2018. 

**Why disable TLS 1.1:** Because of the increased security associated with higher versions of TLS, TLS 1.0 should be disabled. 

###### **Audit:** 

To verify that the server uses disables legacy TLS protocols you should check the disabledProtocols directive, run the following commands: 

```
mongod --config /etc/mongod.conf
```

Review for disabledProtocols as part of the output shown below: 

```
net:
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/ssl/mongodb.pem
    CAFile: /etc/ssl/caToValidateClientCertificates.pem
    disabledProtocols: TLS1_0,TLS1_1
```

###### **Remediation:** 

Make changes to configuration file, to configure your mongod or mongos instance to disable legacy protocols, shut down the instance and update the configuration file with the following setting: 

```
net:
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/ssl/mongodb.pem
    CAFile: /etc/ssl/caToValidateClientCertificates.pem
    disabledProtocols: TLS1_0,TLS1_1
```

Start mongod or mongos instance with the configuration file. 

Page 40 

Internal Only - General 

```
mongod --config /etc/mongod.conf
```

**Default Value:** 

TLS1_0, TLS1_1, TLS1_2 

**Note:** Starting in version 4.0.4 (and 3.6.9)TLS1_3 is added to the default value. 

**References:** 

1. <u>https://www.mongodb.com/docs/v7.0/core/security-transport-encryption/</u> 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|4.1Establish and Maintain a Secure Configuration Process<br>Establish and maintain a secure configuration process for enterprise assets<br>(end-user devices, including portable and mobile, non-computing/IoT devices, and<br>servers) and software (operating systems and applications). Review and update<br>documentation annually, or when significant enterprise changes occur that could<br>impact this Safeguard.|●|●|●|
|v7|18.11Use Standard Hardening Configuration Templates<br>for Databases<br>For applications that rely on a database, use standard hardening configuration<br>templates. All systems that are part of critical business processes should also be<br>tested.||●|●|



Page 41 

Internal Only - General 

#### _4.2 Ensure Weak Protocols are Disabled (Automated)_ 

###### **Profile Applicability:** 

- Level 1- MongoDB 

###### **Description:** 

Servers can be configured to disable specific TLS/SSL protocol versions which may be vulnerable to exploitation and/or lack features which improve the level of security as provided by newer versions of the protocol. 

###### **Rationale:** 

The TLSv1.0 protocol is vulnerable to the BEAST attack when used in CBC mode (October 2011). Unfortunately, the TLSv1.0 uses CBC modes for all of the block mode ciphers, which only leaves the RC4 streaming cipher which is also weak and is not recommended. Therefore, it is recommended that the TLSv1.0 protocol be disabled. The TLSv1.1 protocol does not support Authenticated Encryption with Associated Data (AEAD) which is designed to simultaneously provide confidentiality, integrity, and authenticity. 

The NIST SP 800-52r2 guidelines for TLS configuration require that TLS 1.2 is configured with FIPS-based cipher suites be supported by all government TLS servers and clients and requires support of TLS 1.3 by January 1, 2024. A September 2018 IETF draft also depreciates the usage of TLSv1.0 and TLSv1.1 as shown in the references. 

###### **Impact:** 

If an attempt to connect using a disabled protocol is made the connection attempt will fail and may have unanticipated impact on clients attempting to establish the connection. 

###### **Audit:** 

To verify that the server disable TLS v1.0 and v1.1, run one of the following commands: 

- On Ubuntu: 

```
cat /etc/mongod.conf | grep –A20 ‘net’ | grep –A10 ‘ssl’ | grep
‘disabledProtocols’
```

- On Windows: 

```
type mongod.conf | findstr –A20 ‘net’ | findstr –A10 ‘ssl’ | findstr
‘disabledProtocols’
```

If TLS1_0,TLS1_1 is not included in the string returned by either of these commands this is a fail. 

Page 42 

Internal Only - General 

###### **Remediation:** 

**For mongod (“Primary daemon process for the MongoDB system”)** In the configuration file /etc/mongod.conf, set the disabledProtocols option to to include TLS1_0,TLS1_1: 

```
net:
  ssl:
    mode: requireSSL
    PEMKeyFile: /etc/ssl/mongodb.pem
    CAFile: /etc/ssl/caToValidateClientCertificates.pem
    disabledProtocols: TLS1_0,TLS1_1
```

And restart monogdb instance with 

```
mongod --config /etc/mongod.conf
```

Or 

```
mongod --sslDisabledProtocols `TLS1_0,TLS1_1
```

###### **Default Value:** 

TLS1_0 if TLS 1.1+ is available on the system. 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/reference/configuration-options/#mongodbsetting-net.ssl.disabledProtocols</u> 

###### **Additional Information:** 

On macOS, you cannot disable TLS1_1 and leave both TLS1_0 and TLS1_2 enabled. You must also disable at least one of the other two; for example, TLS1_0,TLS1_1. 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).||●|●|
|v7|14.4Encrypt All Sensitive Information in Transit<br>Encrypt all sensitive information in transit.||●|●|



Page 43 

Internal Only - General 

_4.3 Ensure Encryption of Data in Transit TLS or SSL (Transport Encryption) (Automated)_ 

###### **Profile Applicability:** 

- Level 1- MongoDB 

###### **Description:** 

Use TLS or SSL to protect all incoming and outgoing connections. This should include using TLS or SSL to encrypt communication between the mongod and mongos components of a MongoDB client as well as between all applications and MongoDB. 

MongoDB supports TLS/SSL (Transport Layer Security/Secure Sockets Layer) to encrypt all of MongoDB’s network traffic. TLS/SSL ensures that MongoDB network traffic is only readable by the intended client. 

Please note: As of MongoDB version 4.2 SSL has been deprecated. 

Also, starting in MongoDB version 4.0, MongoDB disables support for TLS 1.0 encryption on systems where TLS 1.1+ is available. 

###### **Rationale:** 

This prevents sniffing of cleartext traffic between MongoDB components or performing a man-in-the-middle attack for MongoDB. 

###### **Audit:** 

To verify that the server requires SSL or TLS (net.tls.mode value set to requireTLS), run one of the following commands: On Ubuntu: 

```
cat /etc/mongod.conf | grep –A20 ‘net’ | grep –A10 ‘tls’ | grep ‘mode’
```

On Windows: 

```
type mongod.conf | findstr –A20 ‘net’ | findstr –A10 ‘tls’ | findstr ‘mode’
```

###### **Remediation:** 

Configure MongoDB servers to require the use of SSL or TLS to encrypt all MongoDB network communications. 

To implement SSL or TLS to encrypt all MongoDB network communication, perform the following steps: 

**For mongod (“Primary daemon process for the MongoDB system”)** 

In the configuration file /etc/mongod.conf, set the PEMKeyFile option to the certificate file’s path and then start the component with this command: 

Page 44 

Internal Only - General 

```
net:
   tls:
      mode: requireTLS
      certificateKeyFile: /etc/ssl/mongodb.pem
      CAFile: /etc/ssl/caToValidateClientCertificates.pem
```

And restart monogdb instance with 

```
mongod --config /etc/mongod.conf
```

###### **Default Value:** 

Not configured 

**References:** 

1. <u>https://www.mongodb.com/docs/v7.0/tutorial/configure-ssl/</u> 

2. <u>https://www.mongodb.com/docs/v7.0/tutorial/configure-ssl-clients/</u> 

3. <u>https://www.mongodb.com/docs/v7.0/tutorial/upgrade-cluster-to-ssl/</u> 

4. <u>https://www.mongodb.com/docs/v7.0/reference/configuration-options/#mongodbsetting-net.tls.clusterAuthX509.attributes</u> 

###### **Additional Information:** 

|`-------------`<br>`Value    |`<br>`------------+`|`----------------------`<br> <br>`----------------------`|`------------------------------------------`<br>`Description`<br>`------------------------------------------`|
|---|---|---|
|<br>`disabled    |`<br>`------------+`|<br>`The server does not`<br>`----------------------`|<br>`use TLS.`<br>`------------------------------------------`|
|<br>`allowTLS    |`<br>`connections,`<br>`|`<br>`|`<br>`|`|<br>`Connections between`<br> <br>`the server accepts`<br> <br>|<br>`servers do not use TLS. For incoming`<br>`both TLS and non-TLS.`|
|<br>`------------+`<br>`preferTLS   |`<br>`the server`<br>`|`<br>`|`<br>`|`|<br>`----------------------`<br>`Connections between`<br>`accepts both TLS and`<br> <br>|`------------------------------------------`<br>`servers use TLS. For incoming connections,`<br>`non-TLS.`|
|<br>`------------+`<br>`requireTLS  |`<br>`|`<br>`-------------`|<br>`----------------------`<br>`The server uses and`<br> <br>`----------------------`|`------------------------------------------`<br>`accepts only TLS encrypted connections.`<br>`------------------------------------------`|



###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).||●|●|



Page 45 

Internal Only - General 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v7|14.4Encrypt All Sensitive Information in Transit<br>Encrypt all sensitive information in transit.||●|●|
|v6|14.2Encrypt All Sensitive Information Over Less-trusted<br>Networks<br>All communication of sensitive information over less-trusted networks should<br>be encrypted. Whenever information flows over a network with a lower trust level,<br>the information should be encrypted.||||



Page 46 

Internal Only - General 

_4.4 Ensure Federal Information Processing Standard (FIPS) is enabled (Automated)_ 

###### **Profile Applicability:** 

- Level 2 - MongoDB 

###### **Description:** 

The Federal Information Processing Standard (FIPS) is a computer security standard used to certify software modules and libraries that encrypt and decrypt data securely. You can configure MongoDB to run with a FIPS 140-2 certified library for OpenSSL. 

FIPS is a property of the encryption system and not the access control system. However, the environment requires FIPS compliant encryption and access control. Organizations must ensure that the access control system uses only FIPS-compliant encryption. 

###### **Rationale:** 

FIPS is an industry standard which dictates how data should be encrypted at rest and during transmission. 

###### **Audit:** 

On Ubuntu: 

To verify that the server uses FIPS Mode (net.tls.FIPSMode value set to true), run following commands: 

```
mongod --config /etc/mongod.conf
net:
 tls:
 FIPSMode: true
```

Or 

To verify FIPS mode is running, check the server log file for a message that FIPS is active: 

```
FIPS 140-2 mode activated
```

On Windows: 

Check FIPSMode is true 

```
type mongod.conf | findstr “FIPSMode"
```

###### **Remediation:** 

Configuring FIPS mode, ensure that your certificate is FIPS compliant. Run mongod or mongos instance in FIPS mode. 

Make changes to configuration file, to configure your mongod or mongos instance to use FIPS mode, shut down the instance and update the configuration file with the following setting: 

Page 47 

Internal Only - General 

```
net:
   tls:
      FIPSMode: true
```

Start mongod or mongos instance with a configuration file. 

```
mongod --config /etc/mongod.conf
```

**Default Value:** 

Not configured 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/tutorial/configure-fips/</u> 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).|●|●|
|v7|14.4Encrypt All Sensitive Information in Transit<br>Encrypt all sensitive information in transit.|●|●|
|v7|14.8Encrypt Sensitive Information at Rest<br>Encrypt all sensitive information at rest using a tool that requires a secondary<br>authentication mechanism not integrated into the operating system, in order to<br>access the information.||●|



Page 48 

Internal Only - General 

#### _4.5 Ensure Encryption of Data at Rest (Manual)_ 

###### **Profile Applicability:** 

- Level 2 - MongoDB 

###### **Description:** 

Encryption of data at rest must be enabled to ensure compliance with security and privacy standards including HIPAA, PCI-DSS, and FERPA. 

Encryption at rest, when used in conjunction with transport encryption and good security policies that protect relevant accounts, passwords, and encryption keys. 

###### **Rationale:** 

Unauthorized users, such as intruders who are attempting security attacks, cannot read the data from storage and back up media unless they have the master encryption key to decrypt it. 

###### **Audit:** 

To verify that the server requires TLS (net.tls.mode value set to requireTLS), run one of the following commands: 

On Ubuntu: 

```
cat /etc/mongod.conf | grep --enableEncryption 'yes' | grep --
encryptionKeyFile '<path to keyfile>'
```

On Windows: 

```
type mongod.conf | findstr --enableEncryption 'yes' | findstr --
encryptionKeyFile '<path to keyfile>'
```

###### **Remediation:** 

It is recommended to enable the data at rest encryption to protect the data. Protecting Data at Rest Including following steps. 

- Generating a master key. 

- Generating keys for each database. 

- Encrypting data with the database keys. 

- Encrypting the database keys with the master key. 

Only the master key is external to the server and requires external management. To manage the master key, MongoDB’s encrypted storage engine supports two key management options: 

- Integration with a third-party key management appliance via the Key Management Interoperability Protocol (KMIP). Recommended 

- Use of local key management via a keyfile. 

Page 49 

Internal Only - General 

The encryption occurs transparently in the storage layer; i.e. all data files are fully encrypted from a filesystem perspective, and data only exists in an unencrypted state in memory and during transmission. 

**To enable Encryption on Database follow below step mentioned in below Link** <u>https://docs.mongodb.com/manual/tutorial/configure-encryption/</u> **Rotation of Key is also important. This can be enabled by following mentioned steps in below link.** <u>https://docs.mongodb.com/manual/tutorial/rotate-encryption-key/</u> 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/core/security-encryption-at-rest/</u> 

###### **Additional Information:** 

Available in MongoDB Enterprise only. 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.11Encrypt Sensitive Data at Rest<br>Encrypt sensitive data at rest on servers, applications, and databases containing<br>sensitive data. Storage-layer encryption, also known as server-side encryption,<br>meets the minimum requirement of this Safeguard. Additional encryption methods<br>may include application-layer encryption, also known as client-side encryption,<br>where access to the data storage device(s) does not permit access to the plain-text<br>data.||●|●|
|v7|14.8Encrypt Sensitive Information at Rest<br>Encrypt all sensitive information at rest using a tool that requires a secondary<br>authentication mechanism not integrated into the operating system, in order to<br>access the information.|||●|



Page 50 

Internal Only - General 

#### **5 Audit Logging** 

This section contains recommendations related to configuring audit logging in MongoDB. 

Page 51 

Internal Only - General 

- _5.1 Ensure that system activity is audited (Automated)_ 

###### **Profile Applicability:** 

- Level 1- MongoDB 

###### **Description:** 

Track access and changes to database configurations and data. MongoDB Enterprise includes a system auditing facility that can record system events (e.g. user operations, connection events) on a MongoDB instance. These audit records permit forensic analysis and allow administrators to verify proper controls. 

###### **Rationale:** 

System level logs can be handy while troubleshooting an operational problem or handling a security incident. 

###### **Audit:** 

To verify that system activity is being audited for MongoDB, run the following command to confirm the auditLog.destination value is set correctly: On Ubuntu: 

```
cat /etc/mongod.conf |grep –A4 "auditLog" | grep "destination"
```

On Windows: 

```
type mongod.conf | findstr –A4 "auditLog" | findstr "destination"
```

**Remediation:** 

Set the value of auditLog.destination to the appropriate value from the following options: 

syslog 

To enable auditing and print audit events to syslog 

```
mongod --dbpath data/db --auditDestination syslog
```

console 

To enable auditing and print audit events to standard output (i.e., stdout) 

```
mongod --dbpath data/db --auditDestination console
```

Json File 

To enable auditing and print audit events to a file in JSON format. Printing audit events to file in JSON format degrades server performance more than printing to a file in BSON format. 

Page 52 

Internal Only - General 

```
mongod --dbpath data/db --auditDestination file --auditFormat JSON --
auditPath data/db/auditLog.json
```

###### Bson File 

To enable auditing and print audit events to a file in BSON binary format 

```
mongod --dbpath data/db --auditDestination file --auditFormat BSON --
auditPath data/db/auditLog.bson
```

###### **Default Value:** 

Not configured 

###### **References:** 

1. <u>http://docs.mongodb.org/manual/tutorial/configure-auditing/</u> 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|8.2Collect Audit Logs<br>Collect audit logs. Ensure that logging, per the enterprise’s audit log<br>management process, has been enabled across enterprise assets.|●|●|●|
|v7|6.2Activate audit logging<br>Ensure that local logging has been enabled on all systems and networking<br>devices.|●|●|●|
|v7|6.3Enable Detailed Logging<br>Enable system logging to include detailed information such as an event<br>source, date, user, timestamp, source addresses, destination addresses, and<br>other useful elements.||●|●|



Page 53 

Internal Only - General 

#### _5.2 Ensure that audit filters are configured properly (Manual)_ 

###### **Profile Applicability:** 

- Level 2 - MongoDB 

###### **Description:** 

MongoDB Enterprise supports auditing of various operations. When enabled, the audit facility, by default, records all auditable operations as detailed in Audit Event Actions, Details, and Results. To specify which events to record, the audit feature includes the - -auditFilter option. This check is only for Enterprise editions. 

###### **Rationale:** 

All operations carried out on the database are logged. This helps in backtracking and tracing any incident that occurs. 

###### **Audit:** 

To verify that audit filters are configured on MongoDB as per the organization’s requirements, run the following command: On Ubuntu: 

```
cat /etc/mongod.conf |grep –A10 "auditLog" | grep "filter"
```

On Windows: 

```
type mongod.conf | findstr –A10 "auditLog" | findstr "filter"
```

**Remediation:** 

Set the audit filters based on the organization’s requirements. 

###### **Default Value:** 

Not configured 

###### **References:** 

1. <u>https://docs.mongodb.com/manual/reference/audit-message/</u> 

2. <u>https://docs.mongodb.com/manual/tutorial/configure-audit-filters/</u> 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|8.2Collect Audit Logs<br>Collect audit logs. Ensure that logging, per the enterprise’s audit log<br>management process, has been enabled across enterprise assets.|●|●|●|



Page 54 

Internal Only - General 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|8.5Collect Detailed Audit Logs<br>Configure detailed audit logging for enterprise assets containing sensitive data.<br>Include event source, date, username, timestamp, source addresses, destination<br>addresses, and other useful elements that could assist in a forensic investigation.||●|●|
|v7|6.2Activate audit logging<br>Ensure that local logging has been enabled on all systems and networking<br>devices.|●|●|●|
|v7|6.3Enable Detailed Logging<br>Enable system logging to include detailed information such as an event source,<br>date, user, timestamp, source addresses, destination addresses, and other useful<br>elements.||●|●|



Page 55 

Internal Only - General 

_5.3 Ensure that logging captures as much information as possible (Automated)_ 

###### **Profile Applicability:** 

- Level 2 - MongoDB 

###### **Description:** 

The SystemLog.quiet option stops logging of information such as: 

- connection events 

- authentication events 

- replication sync activities 

- evidence of some potentially impactful commands being run (eg: drop, dropIndexes, validate) 

This information should be logged whenever possible. This check is only for Enterprise editions. 

###### **Rationale:** 

The use of SystemLog.quiet makes troubleshooting problems and investigating possible security incidents much more difficult. 

###### **Audit:** 

To verify that the SystemLog: quiet=false option is disabled (value of false), run the following command: On Ubuntu: 

```
cat /etc/mongod.conf |grep "quiet"
```

On Windows: 

```
type mongod.conf | findstr "quiet"
```

**Remediation:** 

Set 

```
`SystemLog:
quiet: false`
```

to false in the /etc/mongod.conf file to disable it. 

###### **References:** 

1. <u>https://docs.mongodb.com/manual/reference/configurationoptions/#systemLog.quiet</u> 

Page 56 

Internal Only - General 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|8.2Collect Audit Logs<br>Collect audit logs. Ensure that logging, per the enterprise’s audit log<br>management process, has been enabled across enterprise assets.|●|●|●|
|v8|8.5Collect Detailed Audit Logs<br>Configure detailed audit logging for enterprise assets containing sensitive data.<br>Include event source, date, username, timestamp, source addresses, destination<br>addresses, and other useful elements that could assist in a forensic investigation.||●|●|
|v7|6.2Activate audit logging<br>Ensure that local logging has been enabled on all systems and networking<br>devices.|●|●|●|
|v7|6.3Enable Detailed Logging<br>Enable system logging to include detailed information such as an event source,<br>date, user, timestamp, source addresses, destination addresses, and other useful<br>elements.||●|●|



Page 57 

Internal Only - General 

_5.4 Ensure that new entries are appended to the end of the log file (Automated)_ 

###### **Profile Applicability:** 

- Level 2 - MongoDB 

###### **Description:** 

By default, new log entries will overwrite old entries after a restart of the mongod or Mongols service. Enabling the systemLog.logAppend setting causes new entries to be appended to the end of the log file rather than overwriting the existing content of the log when the mongos or mongod instance restarts. 

###### **Rationale:** 

Allowing old entries to be overwritten by new entries instead of appending new entries to the end of the log may destroy old log data that is needed for a variety of purposes. 

###### **Audit:** 

To verify that new log entries will be appended to the end of the log file after a restart (systemLog: logAppend: true value set to true), run the following command: On Ubuntu: 

```
cat /etc/mongod.conf | grep "logAppend"
```

On Windows: 

```
type mongod.conf | findstr "logAppend"
```

**Remediation:** 

Set 

```
`systemLog:
    logAppend: true`
```

to true in the /etc/mongod.conf file. 

###### **References:** 

1. <u>https://docs.mongodb.com/manual/reference/configurationoptions/#systemLog.logAppend</u> 

Page 58 

Internal Only - General 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|8.10Retain Audit Logs<br>Retain audit logs across enterprise assets for a minimum of 90 days.||●|●|
|v7|6.4Ensure adequate storage for logs<br>Ensure that all systems that store logs have adequate storage space for<br>the logs generated.||●|●|



Page 59 

Internal Only - General 

#### **6 Operating System Hardening** 

This section contains recommendations related to hardening the operating system running below MongoDB. 

Page 60 

Internal Only - General 

- _6.1 Ensure that MongoDB uses a non-default port (Automated)_ 

###### **Profile Applicability:** 

- Level 1- MongoDB 

###### **Description:** 

Changing the default port used by MongoDB makes it harder for attackers to find the database and target it. 

###### **Rationale:** 

Standard ports are used in automated attacks and by attackers to verify which applications are running on a server. 

###### **Impact:** 

Hackers frequently scan IP addresses for commonly used ports, so it's not uncommon to use a different port to "fly under the radar". This is just to avoid detection, other than that there is no added safety by using a different port. 

###### **Audit:** 

To verify the port number used by MongoDB, execute the following command and ensure that the port number is not 27017: On Ubuntu: 

```
cat /etc/mongod.conf |grep “port”
```

On Windows: 

```
type mongod.conf | findstr “port”
```

**Remediation:** 

Change the port for MongoDB server to a number other than 27017. In mongod.conf edit the below lines 

```
# network interfaces
net:
  port: $Orginasation Defined port
  bindIp: $Orginasation Defined IP
```

**References:** 

1. <u>https://docs.mongodb.com/v5.0/reference/default-mongodb-port/</u> 

Page 61 

Internal Only - General 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|4.8Uninstall or Disable Unnecessary Services on<br>Enterprise Assets and Software<br>Uninstall or disable unnecessary services on enterprise assets and software,<br>such as an unused file sharing service, web application module, or service<br>function.||●|●|
|v7|9.2Ensure Only Approved Ports, Protocols and Services<br>Are Running<br>Ensure that only network ports, protocols, and services listening on a system<br>with validated business needs, are running on each system.||●|●|



Page 62 

Internal Only - General 

#### _6.2 Ensure that operating system resource limits are set for MongoDB (Manual)_ 

###### **Profile Applicability:** 

- Level 2 - MongoDB 

###### **Description:** 

Operating systems provide ways to limit and control the usage of system resources such as threads, files, and network connections on a per-process and per-user basis 

###### **Rationale:** 

These ulimits prevent a single user from consuming too many system resources. 

###### **Audit:** 

To verify the resource limits set for MongoDB, run the following commands. Extract the process ID for MongoDB: 

```
ps -ef | grep mongod
```

View the limits associated with that process number: 

```
cat /proc/1322/limits
```

###### **Remediation:** 

Every deployment may have unique requirements and settings. Recommended thresholds and settings are particularly important for MongoDB deployments: 

- f (file size): unlimited 

- t (cpu time): unlimited 

- v (virtual memory): unlimited [1] 

- n (open files): 64000 

- m (memory size): unlimited [1] [2] 

- u (processes/threads): 64000 

Restart the mongod and mongos instances after changing the ulimit settings to ensure that the changes take effect. 

###### **Default Value:** 

Not configured 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/reference/ulimit/</u> 

2. <u>https://docs.mongodb.com/manual/reference/ulimit/</u> 

Page 63 

Internal Only - General 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|16.7Use Standard Hardening Configuration Templates for<br>Application Infrastructure<br>Use standard, industry-recommended hardening configuration templates for<br>application infrastructure components. This includes underlying servers, databases,<br>and web servers, and applies to cloud containers, Platform as a Service (PaaS)<br>components, and SaaS components. Do not allow in-house developed software to<br>weaken configuration hardening.||●|●|
|v7|8.3Enable Operating System Anti-Exploitation Features/<br>Deploy Anti-Exploit Technologies<br>Enable anti-exploitation features such as Data Execution Prevention (DEP) or<br>Address Space Layout Randomization (ASLR) that are available in an operating<br>system or deploy appropriate toolkits that can be configured to apply protection to a<br>broader set of applications and executables.||●|●|



Page 64 

Internal Only - General 

_6.3 Ensure that server-side scripting is disabled if not needed (Manual)_ 

###### **Profile Applicability:** 

- Level 2 - MongoDB 

###### **Description:** 

MongoDB supports the execution of JavaScript code for certain server-side operations: mapReduce, group, $where, $accumulator, and $function aggregation operations that allow users to define custom aggregation expressions. If you do not use these operations, server-side scripting should be disabled. 

###### **Rationale:** 

If server-side scripting is not needed and is not disabled, this introduces unnecessary risk which may allow an attacker to take advantage of insecure coding. 

###### **Impact:** 

Disabling server-side scripting will block all server-side scripts from executing. 

###### **Audit:** 

If server-side scripting is not required, verify that it is disabled (javascriptEnabled value of false) using the following command: On Ubuntu: 

```
cat /etc/mongod.conf | grep –A10 "security" | grep "javascriptEnabled"
```

On Windows: 

```
type mongod.conf | findstr –A10 "security" | findstr "javascriptEnabled"
```

###### **Remediation:** 

If server-side scripting is not required, for mongod instance disable it by using the -- noscripting option on the command line, or setting security.javascriptEnabled to false in the configuration file. 

Starting in MongoDB 4.4 this is also applicable to mongos. 

###### **Default Value:** 

Enabled 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/core/server-side-javascript/</u> 

2. <u>https://docs.mongodb.com/manual/core/server-side-javascript/#disable-serverside-js</u> 

Page 65 

Internal Only - General 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|2.7Allowlist Authorized Scripts<br>Use technical controls, such as digital signatures and version control, to ensure<br>that only authorized scripts, such as specific .ps1, .py, etc., files, are allowed to<br>execute. Block unauthorized scripts from executing. Reassess bi-annually, or more<br>frequently.|||●|
|v7|2.9Implement Application Whitelisting of Scripts<br>The organization's application whitelisting software must ensure that only<br>authorized, digitally signed scripts (such as *.ps1, *.py, macros, etc) are allowed to<br>run on a system.|||●|
|v7|4.7Limit Access to Script Tools<br>Limit access to scripting tools (such as Microsoft PowerShell and Python) to<br>only administrative or development users with the need to access those<br>capabilities.||●|●|
|v7|7.3Limit Use of Scripting Languages in Web Browsers<br>and Email Clients<br>Ensure that only authorized scripting languages are able to run in all web<br>browsers and email clients.||●|●|



Page 66 

Internal Only - General 

#### **7 File Permissions** 

This section provides recommendations for setting permissions for the key file and the database file. 

Page 67 

Internal Only - General 

- _7.1 Ensure appropriate key file permissions are set (Manual)_ 

###### **Profile Applicability:** 

- Level 1- MongoDB 

###### **Description:** 

In the Shared Cluster, the certificate or keyfile is utilized for authentications. Implementing proper file permissions on the certificate or keyfile will prevent unauthorized access to it. 

###### **Rationale:** 

Protecting the certificate/keyfile strengthens authentication in the sharded cluster and prevents unauthorized access to the MongoDB database. 

###### **Audit:** 

Find the location of certificate/keyfile using the following commands: On Ubuntu: 

```
cat /etc/mongod.conf | grep “keyFile:”
cat /etc/mongod.conf | grep “PEMKeyFile:”
cat /etc/mongod.conf | grep “CAFile:”
```

On Windows: 

```
type mongod.conf | findstr “keyFile:”
type mongod.conf | findstr “PEMKeyFile:”
type mongod.conf | findstr “CAFile:”
```

Check the permission of the file using: 

```
ls -l certificate_file_locations
ls -l keyfile_locations
```

###### **Remediation:** 

Set the keyFile ownership to mongodb user and remove other permissions by executing these commands: 

```
chmod 600 /keyfile
sudo chown mongodb:mongodb /keyfile
```

###### **Default Value:** 

Not configured 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/tutorial/deploy-replica-set-with-keyfileaccess-control/</u> 

Page 68 

Internal Only - General 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.11Encrypt Sensitive Data at Rest<br>Encrypt sensitive data at rest on servers, applications, and databases containing<br>sensitive data. Storage-layer encryption, also known as server-side encryption,<br>meets the minimum requirement of this Safeguard. Additional encryption methods<br>may include application-layer encryption, also known as client-side encryption,<br>where access to the data storage device(s) does not permit access to the plain-text<br>data.||●|●|
|v7|16.4Encrypt or Hash all Authentication Credentials<br>Encrypt or hash with a salt all authentication credentials when stored.||●|●|



Page 69 

Internal Only - General 

_7.2 Ensure appropriate database file permissions are set. (Manual)_ 

###### **Profile Applicability:** 

•  Level 1- MongoDB 

###### **Description:** 

MongoDB database files need to be protected using file permissions. 

###### **Rationale:** 

This will restrict unauthorized users from accessing the database. 

###### **Audit:** 

To verify that the permissions for the MongoDB database file are configured securely, run the following commands. 

Find out the database location using the following command: On Ubuntu: 

```
cat /etc/mongod.conf |grep "dbpath"
or
cat /etc/mongod.conf | grep "dbPath"
```

Use the database location as part of the following command to view and verify the permissions set for the database file: Example: 

```
$ stat -c '%a' /var/lib/mongodb
```

On Windows: 

```
type mongod.conf | findstr "dbpath"
```

Use the database location as part of the following command to view and verify the permissions set for the database file: 

```
icacls "dbpath"
```

###### **Remediation:** 

Set ownership of the database file to mongodb user and remove other permissions using the following commands: 

```
chmod 770 /var/lib/mongodb
chown mongodb:mongodb /var/lib/mongodb
```

###### **Default Value:** 

Not configured 

Page 70 

Internal Only - General 

###### **References:** 

1. <u>https://www.mongodb.com/docs/v7.0/reference/configuration-options/#mongodbsetting-storage.dbPath</u> 

###### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 71 

Internal Only - General 

## **Appendix: Summary Table** 

||**CIS Benchmark Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|---|
|||Yes|No|
|**1**|**Installation and Patching**|||
|1.1|Ensure the appropriate MongoDB software<br>version/patches are installed (Manual)|o|o|
|**2**|**Authentication**|||
|2.1|Ensure Authentication is configured (Automated)|o|o|
|2.2|Ensure that MongoDB does not bypass authentication<br>via the localhost exception (Automated)|o|o|
|2.3|Ensure authentication is enabled in the sharded cluster<br>(Automated)|o|o|
|**3**|**Authorization**|||
|3.1|Ensure least privilege for database accounts (Manual)|o|o|
|3.2|Ensure that role-based access control is enabled and<br>configured appropriately (Manual)|o|o|
|3.3|Ensure that MongoDB is run using a non-privileged,<br>dedicated service account (Manual)|o|o|
|3.4|Ensure that each role for each MongoDB database is<br>needed and grants only the necessary privileges<br>(Manual)|o|o|
|3.5|Review Superuser/Admin Roles (Manual)|o|o|
|**4**|**Data Encryption**|||
|4.1|Ensure legacy TLS protocols are disabled (Automated)|o|o|
|4.2|Ensure Weak Protocols are Disabled (Automated)|o|o|
|4.3|Ensure Encryption of Data in Transit TLS or SSL<br>(Transport Encryption) (Automated)|o|o|



Page 72 

Internal Only - General 

||**CIS Benchmark Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|---|
|||Yes|No|
|4.4|Ensure Federal Information Processing Standard (FIPS)<br>is enabled (Automated)|o|o|
|4.5|Ensure Encryption of Data at Rest (Manual)|o|o|
|**5**|**Audit Logging**|||
|5.1|Ensure that system activity is audited (Automated)|o|o|
|5.2|Ensure that audit filters are configured properly (Manual)|o|o|
|5.3|Ensure that logging captures as much information as<br>possible (Automated)|o|o|
|5.4|Ensure that new entries are appended to the end of the<br>log file (Automated)|o|o|
|**6**|**Operating System Hardening**|||
|6.1|Ensure that MongoDB uses a non-default port<br>(Automated)|o|o|
|6.2|Ensure that operating system resource limits are set for<br>MongoDB (Manual)|o|o|
|6.3|Ensure that server-side scripting is disabled if not<br>needed (Manual)|o|o|
|**7**|**File Permissions**|||
|7.1|Ensure appropriate key file permissions are set (Manual)|o|o|
|7.2|Ensure appropriate database file permissions are set.<br>(Manual)|o|o|



Page 73 

Internal Only - General 

### **Appendix: CIS Controls v7 IG 1 Mapped Recommendations** 

||**Recommendation**|**Se**<br>**Corr**|**t**<br>**ectly**|
|---|---|---|---|
|||**Yes**|**No**|
|1.1|Ensure the appropriate MongoDB software<br>version/patches areinstalled|o|o|
|3.1|Ensureleastprivilegefordatabase accounts|o|o|
|3.2|Ensure that role-based access control is enabled and<br>configured appropriately|o|o|
|3.3|Ensure that MongoDB is run using a non-privileged,<br>dedicated service account|o|o|
|3.4|Ensure that each role for each MongoDB database is<br>needed and grants onlythenecessary privileges|o|o|
|3.5|ReviewSuperuser/Admin Roles|o|o|
|5.1|Ensurethatsystemactivityis audited|o|o|
|5.2|Ensure that audit filters are configuredproperly|o|o|
|5.3|Ensure that logging captures as much information as<br>possible|o|o|
|7.2|Ensure appropriate databasefile permissions are set.|o|o|



Page 74 

Internal Only - General 

### **Appendix: CIS Controls v7 IG 2 Mapped Recommendations** 

||**Recommendation**|**Se**<br>**Corr**|**t**<br>**ectly**|
|---|---|---|---|
|||**Yes**|**No**|
|1.1|Ensure the appropriate MongoDB software<br>version/patches areinstalled|o|o|
|2.1|EnsureAuthentication is configured|o|o|
|2.2|Ensure that MongoDB does not bypass authentication<br>viathelocalhostexception|o|o|
|3.1|Ensureleastprivilegefordatabase accounts|o|o|
|3.2|Ensure that role-based access control is enabled and<br>configured appropriately|o|o|
|3.3|Ensure that MongoDB is run using a non-privileged,<br>dedicated service account|o|o|
|3.4|Ensure that each role for each MongoDB database is<br>needed and grants onlythenecessary privileges|o|o|
|3.5|ReviewSuperuser/Admin Roles|o|o|
|4.1|EnsurelegacyTLS protocols are disabled|o|o|
|4.2|EnsureWeak Protocols areDisabled|o|o|
|4.3|Ensure Encryption of Data in Transit TLS or SSL<br>(Transport Encryption)|o|o|
|4.4|Ensure Federal Information Processing Standard (FIPS)<br>is enabled|o|o|
|5.1|Ensurethatsystemactivityis audited|o|o|
|5.2|Ensurethataudit filters are configured properly|o|o|
|5.3|Ensure that logging captures as much information as<br>possible|o|o|
|5.4|Ensure that new entries are appended to the end of the<br>logfile|o|o|
|6.1|Ensurethat MongoDBuses anon-defaultport|o|o|
|6.2|Ensure that operating system resource limits are set for<br>MongoDB|o|o|
|6.3|Ensurethatserver-side scriptingis disabledif not needed|o|o|
|7.1|Ensure appropriate keyfilepermissions are set|o|o|



Page 75 

Internal Only - General 

||**Recommendation**|**S**|**et**|
|---|---|---|---|
|||**Corr**|**ectly**|
|||**Yes**|**No**|
|7.2|Ensure appropriate database filepermissions are set.|o|o|



Page 76 

Internal Only - General 

### **Appendix: CIS Controls v7 IG 3 Mapped Recommendations** 

||**Recommendation**|**Se**<br>**Corr**|**t**<br>**ectly**|
|---|---|---|---|
|||**Yes**|**No**|
|1.1|Ensure the appropriate MongoDB software<br>version/patches areinstalled|o|o|
|2.1|EnsureAuthentication is configured|o|o|
|2.2|Ensure that MongoDB does not bypass authentication<br>viathelocalhostexception|o|o|
|2.3|Ensure authentication is enabledin the sharded cluster|o|o|
|3.1|Ensure leastprivilege for database accounts|o|o|
|3.2|Ensure that role-based access control is enabled and<br>configured appropriately|o|o|
|3.3|Ensure that MongoDB is run using a non-privileged,<br>dedicated service account|o|o|
|3.4|Ensure that each role for each MongoDB database is<br>needed and grants only the necessary privileges|o|o|
|3.5|ReviewSuperuser/Admin Roles|o|o|
|4.1|EnsurelegacyTLS protocols are disabled|o|o|
|4.2|EnsureWeak Protocols areDisabled|o|o|
|4.3|Ensure Encryption of Data in Transit TLS or SSL<br>(Transport Encryption)|o|o|
|4.4|Ensure Federal Information Processing Standard (FIPS)<br>is enabled|o|o|
|4.5|EnsureEncryptionof Data at Rest|o|o|
|5.1|Ensurethatsystemactivityis audited|o|o|
|5.2|Ensure that audit filters are configuredproperly|o|o|
|5.3|Ensure that logging captures as much information as<br>possible|o|o|
|5.4|Ensure that new entries are appended to the end of the<br>log file|o|o|
|6.1|Ensure that MongoDB uses a non-defaultport|o|o|
|6.2|Ensure that operating system resource limits are set for<br>MongoDB|o|o|



Page 77 

Internal Only - General 

||**Recommendation**|**S**<br>**Corr**<br>**Yes**|**et**<br>**ectly**<br>**No**|
|---|---|---|---|
|6.3|Ensurethatserver-side scriptingis disabledif not needed|o|o|
|7.1|Ensure appropriatekeyfile permissions are set|o|o|
|7.2|Ensure appropriate databasefile permissions are set.|o|o|



Page 78 

Internal Only - General 

### **Appendix: CIS Controls v7 Unmapped Recommendations** 

|**Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|
||**Yes**|**No**|
|No unmappedrecommendationsto CIS Controlsv7|o|o|



Page 79 

Internal Only - General 

### **Appendix: CIS Controls v8 IG 1 Mapped Recommendations** 

||**Recommendation**|**Se**<br>**Corr**|**t**<br>**ectly**|
|---|---|---|---|
|||**Yes**|**No**|
|1.1|Ensure the appropriate MongoDB software<br>version/patches areinstalled|o|o|
|2.1|EnsureAuthentication is configured|o|o|
|3.1|Ensureleastprivilegefordatabase accounts|o|o|
|3.4|Ensure that each role for each MongoDB database is<br>needed and grants only the necessary privileges|o|o|
|3.5|Review Superuser/Admin Roles|o|o|
|4.1|EnsurelegacyTLS protocols are disabled|o|o|
|5.1|Ensurethatsystemactivityis audited|o|o|
|5.2|Ensure that audit filters are configuredproperly|o|o|
|5.3|Ensure that logging captures as much information as<br>possible|o|o|
|7.2|Ensure appropriate databasefile permissions are set.|o|o|



Page 80 

Internal Only - General 

### **Appendix: CIS Controls v8 IG 2 Mapped Recommendations** 

||**Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|---|
|||**Yes**|**No**|
|1.1|Ensure the appropriate MongoDB software<br>version/patches areinstalled|o|o|
|2.1|EnsureAuthentication is configured|o|o|
|2.2|Ensure that MongoDB does not bypass authentication<br>viathelocalhostexception|o|o|
|2.3|Ensure authentication is enabledin the sharded cluster|o|o|
|3.1|Ensure leastprivilege for database accounts|o|o|
|3.3|Ensure that MongoDB is run using a non-privileged,<br>dedicated service account|o|o|
|3.4|Ensure that each role for each MongoDB database is<br>needed and grants only the necessary privileges|o|o|
|3.5|Review Superuser/Admin Roles|o|o|
|4.1|EnsurelegacyTLS protocols are disabled|o|o|
|4.2|EnsureWeak Protocols areDisabled|o|o|
|4.3|Ensure Encryption of Data in Transit TLS or SSL<br>(Transport Encryption)|o|o|
|4.4|Ensure Federal Information Processing Standard (FIPS)<br>is enabled|o|o|
|4.5|EnsureEncryptionof Data at Rest|o|o|
|5.1|Ensure that system activityis audited|o|o|
|5.2|Ensurethataudit filters are configured properly|o|o|
|5.3|Ensure that logging captures as much information as<br>possible|o|o|
|5.4|Ensure that new entries are appended to the end of the<br>log file|o|o|
|6.1|Ensurethat MongoDBuses anon-defaultport|o|o|
|6.2|Ensure that operating system resource limits are set for<br>MongoDB|o|o|
|7.1|Ensure appropriatekeyfile permissions are set|o|o|



Page 81 

Internal Only - General 

||**Recommendation**|**S**|**et**|
|---|---|---|---|
|||**Corr**|**ectly**|
|||**Yes**|**No**|
|7.2|Ensure appropriate database filepermissions are set.|o|o|



Page 82 

Internal Only - General 

### **Appendix: CIS Controls v8 IG 3 Mapped Recommendations** 

||**Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|---|
|||**Yes**|**No**|
|1.1|Ensure the appropriate MongoDB software<br>version/patches areinstalled|o|o|
|2.1|EnsureAuthentication is configured|o|o|
|2.2|Ensure that MongoDB does not bypass authentication<br>viathelocalhostexception|o|o|
|2.3|Ensure authentication is enabledin the sharded cluster|o|o|
|3.1|Ensure leastprivilege for database accounts|o|o|
|3.2|Ensure that role-based access control is enabled and<br>configured appropriately|o|o|
|3.3|Ensure that MongoDB is run using a non-privileged,<br>dedicated service account|o|o|
|3.4|Ensure that each role for each MongoDB database is<br>needed and grants only the necessary privileges|o|o|
|3.5|ReviewSuperuser/Admin Roles|o|o|
|4.1|EnsurelegacyTLS protocols are disabled|o|o|
|4.2|EnsureWeak Protocols areDisabled|o|o|
|4.3|Ensure Encryption of Data in Transit TLS or SSL<br>(Transport Encryption)|o|o|
|4.4|Ensure Federal Information Processing Standard (FIPS)<br>is enabled|o|o|
|4.5|EnsureEncryptionof Data at Rest|o|o|
|5.1|Ensurethatsystemactivityis audited|o|o|
|5.2|Ensure that audit filters are configuredproperly|o|o|
|5.3|Ensure that logging captures as much information as<br>possible|o|o|
|5.4|Ensure that new entries are appended to the end of the<br>log file|o|o|
|6.1|Ensure that MongoDB uses a non-defaultport|o|o|
|6.2|Ensure that operating system resource limits are set for<br>MongoDB|o|o|



Page 83 

Internal Only - General 

||**Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|---|
|||**Yes**|**No**|
|6.3|Ensurethatserver-side scriptingis disabledif not needed|o|o|
|7.1|Ensure appropriatekeyfile permissions are set|o|o|
|7.2|Ensure appropriate databasefile permissions are set.|o|o|



Page 84 

Internal Only - General 

### **Appendix: CIS Controls v8 Unmapped Recommendations** 

|**Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|
||**Yes**|**No**|
|No unmappedrecommendationsto CIS Controlsv8|o|o|



Page 85 

Internal Only - General 

## **Appendix: Change History** 

|**Date**|**Version**|**Changes for this version**|
|---|---|---|
|8/1/2025|1.0.0|New technology release<br>support for MongoDB 8|



Page 86 

Internal Only - General 

