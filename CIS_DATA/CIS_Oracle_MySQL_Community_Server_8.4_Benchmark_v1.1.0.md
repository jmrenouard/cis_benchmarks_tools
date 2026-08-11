# CIS Oracle MySQL Community Server 8.4 Benchmark 

v1.1.0 - 11-28-2025 

Internal Only - General 

## **Terms of Use** 

Please see the below link for our current terms of use: 

https://www.cisecurity.org/cis-securesuite/cis-securesuite-membership-terms-of-use/ 

For information on referencing and/or citing CIS Benchmarks in 3<sup>rd</sup> party documentation (including using portions of Benchmark Recommendations) please contact CIS Legal (legalnotices@cisecurity.org) and request guidance on copyright usage. 

**NOTE** :  It is **_NEVER_** acceptable to host a CIS Benchmark in **_ANY_** format (PDF, etc.) on a 3<sup>rd</sup> party (non-CIS owned) site. 

Page 1 

Internal Only - General 

## **Table of Contents** 

|**_Terms of Use ..................................................................................................................... 1_**|
|---|
|**_Table of Contents ............................................................................................................. 2_**|
|**_Overview ............................................................................................................................ 5_**|
|**Important Usage Information .................................................................................................... 5**<br>|
|**Key Stakeholders.................................................................................................................................... 5**<br>|
|**Apply the Correct Version of a Benchmark ......................................................................................... 6**<br>|
|**Exceptions ............................................................................................................................................... 6**<br>|
|**Remediation ............................................................................................................................................ 7**|
|**Summary.................................................................................................................................................. 7**|
|**Target Technology Details ........................................................................................................ 8**|
|**Intended Audience ..................................................................................................................... 8**|
|**Consensus Guidance ................................................................................................................. 9**|
|**Typographical Conventions .................................................................................................... 10**|
|**_Recommendation Definitions ....................................................................................... 11_**|
|**Title ............................................................................................................................................. 11**|
|**Assessment Status .................................................................................................................. 11**|
|**Automated ............................................................................................................................................. 11**|
|**Manual.................................................................................................................................................... 11**|
|**Profile ......................................................................................................................................... 11**|
|**Description ................................................................................................................................ 11**|
|**Rationale Statement ................................................................................................................. 11**|
|**Impact Statement...................................................................................................................... 12**|
|**Audit Procedure ........................................................................................................................ 12**|
|**Remediation Procedure ........................................................................................................... 12**|
|**Default Value ............................................................................................................................. 12**|
|**References ................................................................................................................................ 12**|
|**CIS Critical Security Controls**<sup>**®**</sup>**(CIS Controls**<sup>**®**</sup>**) .................................................................... 12**|
|**Additional Information ............................................................................................................. 12**|
|**Profile Definitions ..................................................................................................................... 13**|
|**Acknowledgements .................................................................................................................. 15**|
|**_Recommendations ......................................................................................................... 16_**|
|**1 Operating System Level Configuration .............................................................................. 16**|
|1.1 Place Databases on Non-System Partitions (Manual) ........................................................ 17|
|1.2 Use Dedicated Least Privileged Account for MySQL Daemon/Service (Automated) ......... 20<br>1.3 Disable MySQL Command History (Automated)................................................................. 22<br>1.4 Verify That the MYSQL_PWD Environment Variable is Not in Use (Automated) ............... 24|



Page 2 

Internal Only - General 

|1.5 Ensure Interactive Login is Disabled (Automated) .............................................................. 26<br>1.6 Verify That 'MYSQLPWD' is Not Set in Users' Profiles (Automated) ................................ 28|
|---|
|_<br>1.7 Ensure MySQL is Run Under a Sandbox Environment (Manual) ....................................... 30|
|**2 Installation and Planning ...................................................................................................... 34**|
|**2.1 Backup and Disaster Recovery ..................................................................................................... 35**<br>|
|2.1.1 Backup Policy in Place (Manual) ...................................................................................... 36<br>|
|2.1.2 Verify Backups are Good (Manual) .................................................................................. 37<br>|
|2.1.3 Secure Backup Credentials (Manual) .............................................................................. 38|
|<br>2.1.4 Point-in-Time Recovery (Automated) ............................................................................... 39|
|2.1.5 Disaster Recovery (DR) Plan (Manual) ............................................................................ 41|
|2.1.6 Backup of Configuration and Related Files (Manual) ...................................................... 43<br>|
|**2.2 Data Encryption .............................................................................................................................. 44**<br>|
|2.2.1 Ensure Binary and Relay Logs are Encrypted (Automated) ............................................ 45|
|2.3 Dedicate the Machine Running MySQL (Manual) ............................................................... 47|
|2.4 Do Not Specify Passwords in the Command Line (Manual) ............................................... 49|
|2.5 Do Not Reuse Usernames (Manual) ................................................................................... 51<br>|
|2.6 Ensure Non-Default, Unique Cryptographic Material is in Use (Manual) ............................ 53|
|<br>2.7 Ensure 'password_lifetime' is Less Than or Equal to '365' (Automated) ............................ 54|
|2.8 Ensure Password Resets Require Strong Passwords (Automated) ................................... 56|
|2.9 Require Current Password for Password Reset (Automated) ............................................ 58|
|2.10 Use Dual Passwords to Enable Higher Frequency Password Rotation (Manual) ............ 59|
|<br>2.11 Lock Out Accounts if Not Currently in Use (Manual) ........................................................ 61|
|<br>2.12 Ensure AES Encryption Mode for AES_ENCRYPT/AES_DECRYPT is Configured<br>Correctly (Automated) ............................................................................................................... 63|
|213 Ensure Socket Peer-Credential Authentication is Used Appropriately (Manual)  65|
|.         ..............<br>2.14 Ensure MySQL is Bound to an IP Address (Automated) .................................................. 67|
|<br>2.15 Limit Accepted Transport Layer Security (TLS) Versions (Automated) ............................ 69<br>2.16 Require Client-Side Certificates (X.509) (Automated) ...................................................... 71|
|2.17 Ensure Only Approved Ciphers are Used (Automated) .................................................... 73<br>2.18 Implement Connection Delays to Limit Failed Login Attempts (Automated) .................... 75<br>|
|2.19 Ensure FIPS 140-2 OpenSSL Cryptography Is Used (Manual) ........................................ 77|
|**3 File Permissions .................................................................................................................... 82**|
|3.1 Ensure 'datadir' Has Appropriate Permissions (Automated) ............................................... 83|
|3.2 Ensure 'log_bin_basename' Files Have Appropriate Permissions (Automated) ................ 85|
|3.3 Ensure 'log_error' Has Appropriate Permissions (Automated) ........................................... 87|
|3.4 Ensure 'slowquerylog' Has Appropriate Permissions (Automated) ................................. 89|
|__<br>3.5 Ensure 'relay_log_basename' Files Have Appropriate Permissions (Automated) ............. 91|
|3.6 Ensure 'general_log_file' Has Appropriate Permissions (Automated) ................................ 93|
|3.7 Ensure SSL Key Files Have Appropriate Permissions (Automated) .................................. 95|
|3.8 Ensure Plugin Directory Has Appropriate Permissions (Automated) .................................. 97|
|**4 General ................................................................................................................................... 99**<br>|
|4.1 Ensure the Latest Security Patches are Applied (Manual) ............................................... 100|
|<br>4.2 Ensure Example or Test Databases are Not Installed on Production Servers (Automated)<br>................................................................................................................................................. 102|
|4.3 Ensure 'allow-suspicious-udfs' is Set to 'OFF' (Automated) .............................................. 104<br>|
|4.4 Harden Usage for 'localinfile' on MySQL Clients (Automated) ....................................... 106|
|_<br>4.5 Ensure 'mysqld' is Not Started With '--skip-grant-tables' (Automated) ............................. 108|
|<br>4.6 Ensure Symbolic Links are Disabled (Automated) ............................................................ 110|
|4.7 Ensure the 'secure_file_priv' is Configured Correctly (Automated) .................................. 112|
|4.8 Ensure 'sql_mode' Contains 'STRICT_ALL_TABLES' (Automated) ................................. 114<br>|
|4.9 Use MySQL TDE for At-Rest Data Encryption (Automated) ............................................. 116|
|**5 MySQL Permissions ............................................................................................................ 119**|
|<br>5.1 Ensure Only Administrative Users Have Full Database Access (Manual)........................ 120|



Page 3 

Internal Only - General 

|5.2 Ensure 'FILE' is Not Granted to Non-Administrative Users (Manual) ............................... 122|
|---|
|5.3 Ensure 'PROCESS' is Not Granted to Non-Administrative Users (Manual) ..................... 124|
|5.4 Ensure 'SUPER' is Not Granted to Non-Administrative Users (Manual) .......................... 126|
|5.5 Ensure 'SHUTDOWN' is Not Granted to Non-Administrative Users (Manual).................. 128<br>|
|5.6 Ensure 'CREATE USER' is Not Granted to Non-Administrative Users (Manual) ............. 130<br>|
|5.7 Ensure 'GRANT OPTION' is Not Granted to Non-Administrative Users (Manual) ........... 132<br>|
|5.8 Ensure 'REPLICATION SLAVE' is Not Granted to Non-Administrative Users (Manual) .. 134<br>5.9 Ensure DML/DDL Grants are Limited to Specific Databases and Users (Manual) .......... 136<br>5.10 Securely Define Stored Procedures and Functions DEFINER and INVOKER (Manual)138|
|5.11 Ensure Proper Use Of 'SET_ANY_DEFINER' (Manual) ................................................. 140|
|5.12 Ensure Proper Use Of ALLOW_NONEXISTENT_DEFINER (Manual) .......................... 142|
|**6 Auditing and Logging ......................................................................................................... 144**|
|6.1 Ensure 'log_error' is configured correctly (Automated) ..................................................... 145|
|6.2 Ensure Log Files are Stored on a Non-System Partition (Automated) ............................. 147|
|6.3 Ensure 'log_error_verbosity' is Set to '2' (Automated) ...................................................... 149|
|6.4 Ensure 'log-raw' is Set to 'OFF' (Automated) .................................................................... 151|
|**7 Authentication ..................................................................................................................... 153**<br>|
|7.1 Ensure your authentication_policy is Set to a Secure Option (Automated) ...................... 154|
|7.2 Ensure Passwords are Not Stored in the Global Configuration (Automated) ................... 157|
|7.3 Ensure Passwords are Set for All MySQL Accounts (Automated) ................................... 159|
|7.4 Set 'default_password_lifetime' to Require a Yearly Password Change (Automated) ..... 161|
|7.5 Ensure Password Complexity Policies are in Place (Automated) ..................................... 163|
|7.6 Ensure No Users Have Wildcard Hostnames (Automated) .............................................. 166|
|7.7 Ensure No Anonymous Accounts Exist (Automated) ........................................................ 167|
|**8 Network ................................................................................................................................. 169**<br>|
|8.1 Ensure 'require_secure_transport' is Set to 'ON' (Automated) ......................................... 170|
|8.2 Ensure 'ssl_type' is Set to 'ANY', 'X509', or 'SPECIFIED' for All Remote Users (Automated)<br>................................................................................................................................................. 172|
|8.3 Set Maximum Connection Limits for Server and per User (Manual) ................................ 174|
|**9 Replication ........................................................................................................................... 176**|
|9.1 Ensure Replication Traffic is Secured (Manual) ................................................................ 177|
|9.2 Ensure 'SOURCE_SSL_VERIFY_SERVER_CERT' is Set to 'YES' or '1' (Automated) ... 179<br>9.3 Ensure 'super_priv' is Not Set to 'Y' for Replication Users (Automated) ........................... 181|
|**10 MySQL InnoDB Cluster / Group Replication .................................................................. 184**|
|<br>10.1 Ensure All Group Replication Traffic is Secured (Manual).............................................. 185|
|10.2 Allowlist Approved Servers Belonging to a MySQL InnoDB Cluster (Manual) ............... 187|
|**_Appendix: Summary Table .......................................................................................... 189_**|
|**_Appendix: Change History .......................................................................................... 195_**|



Page 4 

Internal Only - General 

## **Overview** 

All CIS Benchmarks™ (Benchmarks) focus on technical configuration settings used to maintain and/or increase the security of the addressed technology, and they should be used in **conjunction** with other essential cyber hygiene tasks like: 

- Monitoring the base operating system and applications for vulnerabilities and quickly updating with the latest security patches. 

- End-point protection (Antivirus software, Endpoint Detection and Response (EDR), etc.). 

- Logging and monitoring user and system activity. 

In the end, the Benchmarks are designed to be a key **component** of a comprehensive cybersecurity program. 

### **Important Usage Information** 

All Benchmarks are available free for non-commercial use from the CIS Website. They can be used to manually assess and remediate systems and applications. In lieu of manual assessment and remediation, there are several tools available to assist with assessment: 

- <u>CIS Configuration Assessment Tool (CIS-CAT</u><sup>®</sup> <u>Pro Assessor)</u> 

- <u>CIS Benchmarks™ Certified 3rd Party Tooling</u> 

These tools make the hardening process much more scalable for large numbers of systems and applications. 

**NOTE** : Some tooling focuses only on the Benchmark Recommendations that can be fully automated (skipping ones marked **Manual** ). It is important that **_ALL_** Recommendations ( **Automated** and **Manual** ) be addressed since all are important for properly securing systems and are typically in scope for audits. 

#### **Key Stakeholders** 

Cybersecurity is a collaborative effort, and cross functional cooperation is imperative within an organization to discuss, test, and deploy Benchmarks in an effective and efficient way. The Benchmarks are developed to be best practice configuration guidelines applicable to a wide range of use cases. In some organizations, exceptions to specific Recommendations will be needed, and this team should work to prioritize the problematic Recommendations based on several factors like risk, time, cost, and labor. These exceptions should be properly categorized and documented for auditing purposes. 

Page 5 

Internal Only - General 

#### **Apply the Correct Version of a Benchmark** 

Benchmarks are developed and tested for a specific set of products and versions and applying an incorrect Benchmark to a system can cause the resulting pass/fail score to be incorrect. This is due to the assessment of settings that do not apply to the target systems. To assure the correct Benchmark is being assessed: 

- **Deploy the Benchmark applicable to the way settings are managed in the environment:** An example of this is the Microsoft Windows family of Benchmarks, which have separate Benchmarks for Group Policy, Intune, and Stand-alone systems based upon how system management is deployed. Applying the wrong Benchmark in this case will give invalid results. 

- **Use the most recent version of a Benchmark** : This is true for all Benchmarks, but especially true for cloud technologies. Cloud technologies change frequently and using an older version of a Benchmark may have invalid methods for auditing and remediation. 

#### **Exceptions** 

The guidance items in the Benchmarks are called recommendations and not requirements, and exceptions to some of them are expected and acceptable. The Benchmarks strive to be a secure baseline, or starting point, for a specific technology, with known issues identified during Benchmark development are documented in the Impact section of each Recommendation. In addition, organizational, system specific requirements, or local site policy may require changes as well, or an exception to a Recommendation or group of Recommendations (e.g. A Benchmark could Recommend that a Web server not be installed on the system, but if a system's primary purpose is to function as a Webserver, there should be a documented exception to this Recommendation for that specific server). 

In the end, exceptions to some Benchmark Recommendations are common and acceptable, and should be handled as follows: 

- The reasons for the exception should be reviewed cross-functionally and be well documented for audit purposes. 

- A plan should be developed for mitigating, or eliminating, the exception in the future, if applicable. 

- If the organization decides to accept the risk of this exception (not work toward mitigation or elimination), this should be documented for audit purposes. 

It is the responsibility of the organization to determine their overall security policy, and which settings are applicable to their unique needs based on the overall risk profile for the organization. 

Page 6 

Internal Only - General 

#### **Remediation** 

CIS has developed Build Kits for many technologies to assist in the automation of hardening systems. Build Kits are designed to correspond to Benchmark's “Remediation” section, which provides the manual remediation steps necessary to make that Recommendation compliant to the Benchmark. 

#### **When remediating systems (changing configuration settings on deployed systems as per the Benchmark's Recommendations), please approach this with caution and test thoroughly.** 

The following is a reasonable remediation approach to follow: 

- CIS Build Kits, or internally developed remediation methods should never be applied to production systems without proper testing. 

- Proper testing consists of the following: 

   - Understand the configuration (including installed applications) of the targeted systems. Various parts of the organization may need different configurations (e.g., software developers vs standard office workers). 

   - Read the Impact section of the given Recommendation to help determine if there might be an issue with the targeted systems. 

   - Test the configuration changes with representative lab system(s). If issues arise during testing, they can be resolved prior to deploying to any production systems. 

   - When testing is complete, initially deploy to a small sub-set of production systems and monitor closely for issues. If there are issues, they can be resolved prior to deploying more broadly. 

   - When the initial deployment above is completes successfully, iteratively deploy to additional systems and monitor closely for issues. Repeat this process until the full deployment is complete. 

#### **Summary** 

Using the Benchmarks Certified tools, working as a team with key stakeholders, being selective with exceptions, and being careful with remediation deployment, it is possible to harden large numbers of deployed systems in a cost effective, efficient, and safe manner. 

- **NOTE** : As previously stated, the PDF versions of the CIS Benchmarks™ are available for free, non-commercial use on the CIS Website. All other formats of the CIS Benchmarks™ (MS Word, Excel, and Build Kits) are available for CIS <u>SecureSuite</u><sup>®</sup> members. 

CIS-CAT<sup>®</sup> Pro is also available to CIS SecureSuite<sup>®</sup> members. 

Page 7 

Internal Only - General 

### **Target Technology Details** 

This document, CIS Oracle MySQL Community Server 8.4 Benchmark, provides prescriptive guidance for establishing a secure configuration posture for MySQL Community Server 8.4. This guide was tested against MySQL Community Server 8.4 running on Oracle Linux, but applies to other Linux distributions as well. To obtain the latest version of this guide, please visit http://benchmarks.cisecurity.org. If you have questions, comments, or have identified ways to improve this guide, please write us at <u>feedback@cisecurity.org.</u> 

### **Intended Audience** 

This document is intended for system and application administrators, security specialists, auditors, help desk, and platform deployment personnel who plan to develop, deploy, assess, or secure solutions that incorporate Oracle MySQL Community Server 8.4. 

Page 8 

Internal Only - General 

### **Consensus Guidance** 

This CIS Benchmark™ was created using a consensus review process comprised of a global community of subject matter experts. The process combines real world experience with data-based information to create technology specific guidance to assist users to secure their environments. Consensus participants provide perspective from a diverse set of backgrounds including consulting, software development, audit and compliance, security research, operations, government, and legal. 

Each CIS Benchmark undergoes two phases of consensus review. The first phase occurs during initial Benchmark development. During this phase, subject matter experts convene to discuss, create, and test working drafts of the Benchmark. This discussion occurs until consensus has been reached on Benchmark recommendations. The second phase begins after the Benchmark has been published. During this phase, all feedback provided by the Internet community is reviewed by the consensus team for incorporation in the Benchmark. If you are interested in participating in the consensus process, please visit https://workbench.cisecurity.org/. 

Page 9 

Internal Only - General 

### **Typographical Conventions** 

The following typographical conventions are used throughout this guide: 

|**Convention**|**Meaning**|
|---|---|
|`Stylized Monospace font`|Used for blocks of code, command, and<br>script examples. Text should be interpreted<br>exactly as presented.|
|`Monospace font`|Used for inline code, commands, UI/Menu<br>selections or examples. Text should be<br>interpreted exactly as presented.|
|`<Monospace font in brackets>`|Text set in angle brackets denote a variable<br>requiring substitution for a real value.|
|_Italic font_|Used to reference other relevant settings,<br>CIS Benchmarks and/or Benchmark<br>Communities. Also, used to denote the title<br>of a book, article, or other publication.|
|**Bold font**|Additional information or caveats things like<br>**Notes**,**Warnings**, or**Cautions**(usually just<br>the word itself and the rest of the text<br>normal).|



Page 10 

Internal Only - General 

## **Recommendation Definitions** 

The following defines the various components included in a CIS recommendation as applicable.  If any of the components are not applicable it will be noted, or the component will not be included in the recommendation. 

### **Title** 

Concise description for the recommendation's intended configuration. 

### **Assessment Status** 

An assessment status is included for every recommendation. The assessment status indicates whether the given recommendation can be automated or requires manual steps to implement. Both statuses are equally important and are determined and supported as defined below: 

#### **Automated** 

Represents recommendations for which assessment of a technical control can be fully automated and validated to a pass/fail state. Recommendations will include the necessary information to implement automation. 

**Manual** 

Represents recommendations for which assessment of a technical control cannot be fully automated and requires all or some manual steps to validate that the configured state is set as expected. The expected state can vary depending on the environment. 

### **Profile** 

A collection of recommendations for securing a technology or a supporting platform. Most benchmarks include at least a Level 1 and Level 2 Profile. Level 2 extends Level 1 recommendations and is not a standalone profile. The Profile Definitions section in the benchmark provides the definitions as they pertain to the recommendations included for the technology. 

### **Description** 

Detailed information pertaining to the setting with which the recommendation is concerned. In some cases, the description will include the recommended value. 

### **Rationale Statement** 

Detailed reasoning for the recommendation to provide the user a clear and concise understanding on the importance of the recommendation. 

Page 11 

Internal Only - General 

### **Impact Statement** 

Any security, functionality, or operational consequences that can result from following the recommendation. 

### **Audit Procedure** 

Systematic instructions for determining if the target system complies with the recommendation. 

### **Remediation Procedure** 

Systematic instructions for applying recommendations to the target system to bring it into compliance according to the recommendation. 

### **Default Value** 

Default value for the given setting in this recommendation, if known. If not known, either not configured or not defined will be applied. 

### **References** 

Additional documentation relative to the recommendation. 

### **CIS Critical Security Controls**<sup>**®**</sup> **(CIS Controls**<sup>**®**</sup> **)** 

The mapping between a recommendation and the CIS Controls is organized by CIS Controls version, Safeguard, and Implementation Group (IG). The Benchmark in its entirety addresses the CIS Controls safeguards of (v7) “5.1 - Establish Secure Configurations” and (v8) '4.1 - Establish and Maintain a Secure Configuration Process” so individual recommendations will not be mapped to these safeguards. 

### **Additional Information** 

Supplementary information that does not correspond to any other field but may be useful to the user. 

Page 12 

Internal Only - General 

### **Profile Definitions** 

The following configuration profiles are defined by this Benchmark: 

- **Level 1 - MySQL RDBMS on Linux** 

Items in this profile apply to MySQL Community Server 8.4 running on Linux and intend to: 

   - be practical and prudent; 

   - provide a clear security benefit; and 

   - not inhibit the utility of the technology beyond acceptable means. 

- **Level 2 - MySQL RDBMS on Linux** 

This profile extends the "Level 1 - MySQL RDBMS on Linux" profile. Items in this profile apply to MySQL Community Server 8.4 running on Linux and exhibit one or more of the following characteristics: 

   - are intended for environments or use cases where security is paramount 

   - acts as defense in depth measure 

   - may negatively inhibit the utility or performance of the technology. 

- **Level 1 - MySQL RDBMS** 

Items in this profile apply to MySQL Community Server 8.4 and intend to: 

- be practical and prudent; 

- provide a clear security benefit; and 

- not inhibit the utility of the technology beyond acceptable means. 

**Note** : the intent of this profile is to include checks that can be assessed by remotely connecting to a MySQL RDBMS. Therefore, file system-related checks are not contained in this profile. 

- **Level 2 - MySQL RDBMS** 

This profile extends the "Level 1 - MySQL RDBMS" profile. Items in this profile apply to MySQL Community Server 8.4 and exhibit one or more of the following characteristics: 

- are intended for environments or use cases where security is paramount 

- acts as defense in depth measure 

- may negatively inhibit the utility or performance of the technology. 

Page 13 

Internal Only - General 

**Note** : the intent of this profile is to include checks that can be assessed by remotely connecting to a MySQL RDBMS. Therefore, file system-related checks are not contained in this profile. 

Page 14 

Internal Only - General 

### **Acknowledgements** 

This Benchmark exemplifies the great things a community of users, vendors, and subject matter experts can accomplish through consensus collaboration. The CIS community thanks the entire consensus team with special recognition to the following individuals who contributed greatly to the creation of this guide: 

**Author** 

Michael Frank 

##### **Contributor** 

Krishna Rayavaram 

**Editor** 

Tim Harrison, Center for Internet Security, New York 

Page 15 

Internal Only - General 

## **Recommendations** 

### **1 Operating System Level Configuration** 

This section contains recommendations related to the Operating System on which the MySQL database server is running. 

Page 16 

Internal Only - General 

- _1.1 Place Databases on Non-System Partitions (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

It is generally accepted that host operating systems should include different filesystem partitions for different purposes. One set of filesystems is typically called system partitions, and these are generally reserved for host system/application operation. The other set of filesystems is typically called "non-system partitions", and such locations are generally reserved for storing data. 

##### **Rationale:** 

Moving the database off the system partition will reduce the probability of denial of service caused by exhaustion of available disk space to the operating system. 

##### **Impact:** 

Moving database files and directories to a non-system partition may be difficult depending on whether there was only a single partition when the operating system was set up and whether there are additional non-system partitions available. 

##### **Audit:** 

Execute the following steps to assess this recommendation: 

- Obtain the location of the `datadir` and other MySQL database files by executing the following SQL statement: 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_variables
WHERE (VARIABLE_NAME LIKE '%dir' or VARIABLE_NAME LIKE '%file') and
(VARIABLE_NAME NOT LIKE '%core%'
      AND VARIABLE_NAME <> 'local_infile' AND VARIABLE_NAME <>
'relay_log_info_file') order by
      VARIABLE_NAME;
```

- Using the value returned for the `datadir` , and other results from the above query, execute the following in a system terminal: 

```
df -h <directory>
```

The output returned from the `df` command above should not include root ( `/` ), `/var` , or `/usr` . 

##### **Remediation:** 

Perform the following steps to remediate this setting for the `datadir` : 

Page 17 

Internal Only - General 

1. Backup the database. 

2. Choose a non-system partition `new location` for MySQL data. 

3. Stop `mysqld` using a command like: `service mysql stop` . 

4. Copy the data using a command like: `cp -rp` _`<datadir Value> <new location>`_ . 

5. Set the `datadir` location to the `new location` in the MySQL configuration file. 

6. Start `mysqld` using a command like: 

```
service mysql start
```

**Note:** On some Linux distributions you may need to additionally modify `apparmor` settings. For example, on a Ubuntu 14.04.1 system edit the file `/etc/apparmor.d/usr.sbin.mysqld` so that the `datadir` access is appropriate. The original might look like this: 

```
# Allow data dir access
/var/lib/mysql/ r,
/var/lib/mysql/** rwk,
```

Alter those two paths to be the new location you chose above. For example, if that new location were `/media/mysql` , then the `/etc/apparmor.d/usr.sbin.mysqld` file should include something like this: 

```
# Allow data dir access
/media/mysql/ r,
/media/mysql/** rwk,
```

##### **Default Value:** 

Not Applicable. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.4/en/securedeployment-permissions.html</u> 

Page 18 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.12Segment Data Processing and Storage Based on<br>Sensitivity<br>Segment data processing and storage based on the sensitivity of the data. Do<br>not process sensitive data on enterprise assets intended for lower sensitivity<br>data.||●|●|
|v7|2.10Physically or Logically Segregate High Risk<br>Applications<br>Physically or logically segregated systems should be used to isolate and run<br>software that is required for business operations but incur higher risk for the<br>organization.|||●|



Page 19 

Internal Only - General 

_1.2 Use Dedicated Least Privileged Account for MySQL Daemon/Service (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

As with any service installed on a host, it can be provided with its own user context. Providing a dedicated user to the service provides the ability to precisely constrain the service within the larger host context. 

##### **Rationale:** 

Utilizing a least privilege account for MySQL to execute as needed may reduce the impact of a MySQL-born vulnerability. A restricted account will be unable to access resources unrelated to MySQL, such as operating system configurations. 

##### **Audit:** 

Execute the following command at a terminal prompt to assess this recommendation: 

```
ps -ef | egrep "^mysql.*$"
```

If no lines are returned, then this is a fail. 

**Note:** It is assumed that the MySQL user is `mysql` . Additionally, you may consider running `sudo -l` as the MySQL user or to check the sudoers file. 

##### **Remediation:** 

Create a user which is only used for running MySQL and directly related processes. This user must not have administrative rights to the system. Additionally, it's best to avoid providing shell access to such an account. 

Shell access can be removed using the following command at a terminal prompt: 

```
/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g mysql -o -r -d /var/lib/mysql -s /bin/false \
    -c "MySQL Server" -u 27 mysql >/dev/null 2>&1 || :
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/changing-mysql-user.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/serveroptions.html#option_mysqld_user</u> 

Page 20 

Internal Only - General 

##### **Additional Information:** 

The root user may be used to start the MySQL service on Linux/UNIX, but then it must be configured to drop privileges by specifying a service specific user in the `my.cnf` or `my.ini` file. 

##### **CIS Controls:** 

|**Controls Version**|<br>**Control**|**IG 1**<br>**IG 2**<br>**IG 3**|
|---|---|---|
|v7|14Controlled Access Based on the Need to Know<br>Controlled Access Based on the Need to Know||



Page 21 

Internal Only - General 

### _1.3 Disable MySQL Command History (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

On Linux/UNIX, the MySQL client and MySQL Shell log statements executed interactively to a history file. The default MySQL Client file is named `.mysql_history` in the user's home directory. The files are split by language and named `history.sql` , `history.js` and `history.py` . Most interactive commands run in the MySQL client application are saved to a history file. The MySQL command history should be disabled. By default, the MySQL Shell does not save history between sessions. 

##### **Rationale:** 

Disabling the MySQL Client and MySQL Shell command history reduces the probability of exposing sensitive information, such as passwords, encryption keys, or other sensitive data or information. 

##### **Audit:** 

Execute the following commands to assess this recommendation: 

```
find /home -name ".mysql_history"
find /root -name ".mysql_history"
```

For MySQL Shell 

```
ls -d .??*/* | egrep history | grep mysql
```

For each file returned determine whether that file is symbolically linked to `/dev/null` . 

##### **Remediation:** 

For MySQL Client perform the following steps to remediate this setting: 

1. Remove `.mysql_history` if it exists. 

2. Use either of the techniques below to prevent it from being created again: 

   - Set the `MYSQL_HISTFILE` environment variable to `/dev/null.` This will need to be placed in the shell's startup script. 

   - Create `$HOME/.mysql_history` as a symbolic to `/dev/null` . 

```
> ln -s /dev/null $HOME/.mysql_history
```

Another way to prevent history from being recorded is to use `--batch` option. 

For MySQL Shell perform the following steps to remediate this setting: 

1. Remove `$HOME/.mysqlsh/history.*` if files exists. 

2. Use either of the techniques below to prevent it from being created again: 

Page 22 

Internal Only - General 

- Start shell and list show options using `\option -l` 

- Set to no history using the command `\option --persist history.autoSave=1` 

##### **Default Value:** 

By default, the MySQL command history file is located in `$HOME/.mysql_history` . 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/mysql-logging.html</u> 

2. <u>https://bugs.mysql.com/bug.php?id=72158</u> 

3. <u>https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-working-withhistory.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.5Securely Dispose of Data<br>Securely dispose of data as outlined in the enterprise’s data management<br>process. Ensure the disposal process and method are commensurate with the data<br>sensitivity.|●|●|●|
|v7|13.2Remove Sensitive Data or Systems Not Regularly<br>Accessed by Organization<br>Remove sensitive data or systems not regularly accessed by the organization<br>from the network. These systems shall only be used as stand alone systems<br>(disconnected from the network) by the business unit needing to occasionally use<br>the system or completely virtualized and powered off until needed.|●|●|●|



Page 23 

Internal Only - General 

_1.4 Verify That the MYSQL_PWD Environment Variable is Not in Use (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

MySQL can read a default database password from an environment variable called `MYSQL_PWD` . Avoiding use of this environment variable can better safeguard the confidentiality of MySQL credentials. 

##### **Rationale:** 

Using the `MYSQL_PWD` environment variable implies MySQL credentials are stored as clear text. 

##### **Audit:** 

To assess this recommendation, use the `/proc` filesystem to determine if `MYSQL_PWD` is currently set for any process: 

```
grep MYSQL_PWD /proc/*/environ
```

This may return one entry for the process which is executing the grep command. 

##### **Remediation:** 

Check which users and/or scripts are setting `MYSQL_PWD` and change them to use a more secure method. 

For unattended logins you should consider 

1. MySQL Configuration Editor 

2. Different authentication methods (e.g., X509 certificate verification) 

3. Use MySQL Enterprise LDAP plugin with Kerberos or SASL tokens. 

##### **Default Value:** 

Not set. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/environment-variables.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/mysql-config-editor.html</u> 

3. <u>https://dev.mysql.com/doc/refman/8.4/en/pluggable-authentication.html</u> 

Page 24 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.11Encrypt Sensitive Data at Rest<br>Encrypt sensitive data at rest on servers, applications, and databases containing<br>sensitive data. Storage-layer encryption, also known as server-side encryption,<br>meets the minimum requirement of this Safeguard. Additional encryption methods<br>may include application-layer encryption, also known as client-side encryption,<br>where access to the data storage device(s) does not permit access to the plain-text<br>data.||●|●|
|v7|16.4Encrypt or Hash all Authentication Credentials<br>Encrypt or hash with a salt all authentication credentials when stored.||●|●|



Page 25 

Internal Only - General 

### _1.5 Ensure Interactive Login is Disabled (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

When created, the MySQL user may have interactive access to the operating system, which means that the MySQL user could login to the host as any other user would. 

##### **Rationale:** 

Preventing the MySQL user from logging in interactively may reduce the impact of a compromised MySQL account. There is also more accountability, as accessing the operating system where the MySQL server lies will require the user's own account. Interactive access by the MySQL user is unnecessary and should be disabled. 

##### **Impact:** 

This setting will prevent the MySQL administrator from interactively logging into the operating system using the MySQL user. Instead, the administrator will need to log in using one's own account. 

##### **Audit:** 

Execute the following command to assess this recommendation: 

```
getent passwd mysql | egrep "^.*[\/bin\/false|\/sbin\/nologin]$"
```

Lack of output implies a fail. 

##### **Remediation:** 

Execute one of the following commands in a terminal: 

```
usermod -s /bin/false mysql
```

Or 

```
usermod -s /sbin/nologin mysql
```

Page 26 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet<br>browsing, email, and productivity suite use, from the user’s primary, non-privileged<br>account.|●|●|●|
|v7|4.3Ensure the Use of Dedicated Administrative Accounts<br>Ensure that all users with administrative account access use a dedicated or<br>secondary account for elevated activities. This account should only be used for<br>administrative activities and not internet browsing, email, or similar activities.|●|●|●|



Page 27 

Internal Only - General 

### _1.6 Verify That 'MYSQL_PWD' is Not Set in Users' Profiles (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

MySQL can read a default database password from an environment variable called `MYSQL_PWD` . 

##### **Rationale:** 

Use of the `MYSQL_PWD` environment variable implies MySQL credentials are stored as clear text. Avoiding use of this environment variable may increase assurance that the confidentiality of MySQL credentials is preserved. 

##### **Audit:** 

To assess this recommendation, check if `MYSQL_PWD` is set in login scripts using the following command: 

```
grep MYSQL_PWD /home/*/.{bashrc,profile,bash_profile}
```

##### **Remediation:** 

Check which users and/or scripts are setting `MYSQL_PWD` and change them to use a more secure method. 

##### **Default Value:** 

Not set. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/environment-variables.html</u> 

Page 28 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.11Encrypt Sensitive Data at Rest<br>Encrypt sensitive data at rest on servers, applications, and databases containing<br>sensitive data. Storage-layer encryption, also known as server-side encryption,<br>meets the minimum requirement of this Safeguard. Additional encryption methods<br>may include application-layer encryption, also known as client-side encryption,<br>where access to the data storage device(s) does not permit access to the plain-text<br>data.||●|●|
|v7|16.4Encrypt or Hash all Authentication Credentials<br>Encrypt or hash with a salt all authentication credentials when stored.||●|●|



Page 29 

Internal Only - General 

- _1.7 Ensure MySQL is Run Under a Sandbox Environment (Manual)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS on Linux 

- Level 2 - MySQL RDBMS 

##### **Description:** 

Use of the chroot() system call at startup, Systemd with settings to achieve isolation, or docker will put MySQL in a Sandbox environment. 

##### **Rationale:** 

Running MySQL in a Sandbox environment may reduce the impact of a MySQL-born vulnerability by making portions of the file system inaccessible to the MySQL instance. 

##### **Impact:** 

Use of the chroot option somewhat limits `LOAD DATA INFILE` and `SELECT ... INTO OUTFILE` . 

##### **Audit:** 

Perform the following steps for each mySQL instance to assess this recommendation: 

1. Execute the following SQL statement to determine the value of 

```
chroot
```

```
cat /etc/mysql | egrep '(?<=^chroot=).+$'
```

The returned value should specify a valid path which differs from the `datadir` . No results implies 'chroot' is not in use. 

2. Perform the following to check systemd: 

```
systemctl status <mysqld>.service
```

If something other than `(root)` is listed beside the `PID` , e.g. `Main PID: <PID> (root)` , this is a pass. No results implies mysql is not managed by systemd. 

3. Perform the following to determine if Docker is installed and a MySQL container is in use: 

   1. To check for docker installation, execute this command: 

```
$ docker -v
```

Page 30 

Internal Only - General 

If a message stating the version of docker which is installed proceed to the next steps, otherwise no further action is needed as docker must be installed for mysql to be run in docker. 

2. To check if a mysql image exists in docker run this command: 

|`$ sudo docker image`|`s`|
|---|---|
|`REPOSITORY`|`TAG       IMAGE ID       CREATED       SIZE`|
|`mysql`|`latest    2fe463762680   1 week ago    514MB`|
|`mysql/mysql-server`|`latest    1504607f1ce7   2 weeks ago   401MB`|



If a mysql image is listed proceed to the next steps, otherwise no further action is needed as a mysql image is required for mysql to be run in docker. 

3. Check if a mysql container is running: 

```
$ sudo docker ps
CONTAINER ID  IMAGE  COMMAND    CREATED     STATUS     PORTS
NAMES
0fc229e3df77  mysql  "docker…"  1 hour ago  Up 1 hour
0.0.0.0:3306->3306/tcp,  mysql-server
                                                       :::3306-
>3306/tcp,
                                                       33060/tcp
```

If a mysql container is listed then mysql is running in docker and this is a pass. 

If MySQL does not use `chroot` , `systemd` , or docker, this is a fail. 

##### **Remediation:** 

Perform one of the following steps to remediate this setting: 

- Configure MySQL to use chroot: 

   1. Choose a non-system partition _`<chroot location>`_ for MySQL 

   2. Add `chroot=` _`<chroot_location>`_ to the `my.cnf` option file 

- Configure MySQL to run under systemd: 

   1. If mysql is managed by systemd and running, stop the service: 

```
$ sudo systemctl stop<mysqld>.service
```

2. If a mysql user and group do not already exist, create them: 

```
$ sudo groupadd mysql
$ sudo useradd -r -g mysql -s /bin/false mysql
```

3. Set the oenwership of the base director: 

Page 31 

Internal Only - General 

```
$ sudo chown -R mysql:mysql /usr/local/mysql/
```

4. Create or modify the _`<mysqld>`_ `.service` file in `/lib/systemd/system` to include the following entries, if not already present: 

```
[Unit]
Description=MySQL Server
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
```

5. If mysql was not already already managed by systemd execute this command: 

```
$ sudo systemctl daemon-reload
```

6. Start the MySQL server: 

```
$ sudo systemctl start <mysqld>.service
```

7. If you would like mysql to automatically run at startup execute this command: 

```
$ sudo systemctl enable <mysqld>.service
```

- Follow documentation in the references for standing up MySQL in a Docker container. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/serveroptions.html#option_mysqld_chroot</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/docker-mysql-getting-started.html</u> 

3. <u>https://hub.docker.com/r/mysql/mysql-server</u> 

Page 32 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.12Segment Data Processing and Storage Based on<br>Sensitivity<br>Segment data processing and storage based on the sensitivity of the data. Do<br>not process sensitive data on enterprise assets intended for lower sensitivity<br>data.||●|●|
|v7|2.10Physically or Logically Segregate High Risk<br>Applications<br>Physically or logically segregated systems should be used to isolate and run<br>software that is required for business operations but incur higher risk for the<br>organization.|||●|



Page 33 

Internal Only - General 

### **2 Installation and Planning** 

This section contains important considerations when deploying MySQL services to your production network and defining the configuration. The recommendations made herein are not scored from a benchmark perspective and generally align with best current practices as conveyed in most control frameworks. 

The first consideration is related to the configuration options via the MySQL configuration file (e.g., `my.cnf` ) and placing options under the proper section of `[mysqld]` . Options placed in the `my.cnf` configuration file should not prefix with a double dash ( `--` ). On Linux systems, `my.cnf` is located in the `/etc/` directory. 

The second consideration is for an administrator to connect to a MySQL instance and change or add to the configuration options using the `SET PERSIST` command. This persists system variables in `mysqld-auto.cnf` which is located in the MySQL `datadir` by default. The file permissions on `mysqld-auto.cnf` are by default more restrictive than `my.cnf` (no world permissions). 

Finally, configuration options can also be placed on the command line by modifying the MySQL startup script. The startup script is system dependent and based on your operating system. 

Page 34 

Internal Only - General 

#### **2.1 Backup and Disaster Recovery** 

This section contains recommendations related to backup and recovery. 

Page 35 

Internal Only - General 

### _2.1.1 Backup Policy in Place (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

- Level 1 - MySQL RDBMS 

##### **Description:** 

A backup policy should be in place. 

##### **Rationale:** 

Backing up MySQL databases, including `mysql` , will help ensure the availability of data in the event of an incident. Without backups, it might be hard to recover from an incident. 

##### **Audit:** 

Check with `crontab -l` if there is a backup schedule. 

##### **Remediation:** 

Create a backup policy and backup schedule. 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|11.2Perform Automated Backups<br>Perform automated backups of in-scope enterprise assets. Run backups<br>weekly, or more frequently, based on the sensitivity of the data.|●|●|●|
|v7|10.1Ensure Regular Automated Back Ups<br>Ensure that all system data is automatically backed up on regular basis.|●|●|●|



Page 36 

Internal Only - General 

### _2.1.2 Verify Backups are Good (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

- Level 1 - MySQL RDBMS 

##### **Description:** 

Backups should be validated on a regular basis. 

##### **Rationale:** 

Verifying that backups are occurring appropriately will help ensure data availability in the event of an incident. Without a well-tested backup, it might be hard to recover from an incident if the backup procedure contains errors or doesn't include all required data. 

##### **Audit:** 

Check reports of backup validation tests. 

##### **Remediation:** 

Implement regular backup checks and document each check. 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|11.5Test Data Recovery<br>Test backup recovery quarterly, or more frequently, for a sampling of in-<br>scope enterprise assets.|●|●|
|v7|10.3Test Data on Backup Media<br>Test data integrity on backup media on a regular basis by performing a data<br>restoration process to ensure that the backup is properly working.|●|●|



Page 37 

Internal Only - General 

### _2.1.3 Secure Backup Credentials (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

- Level 1 - MySQL RDBMS 

##### **Description:** 

A database user with the least amount of privileges required to perform backup is needed. The credentials for this user should be protected. The password, certificate, and any other credentials should be protected. 

##### **Rationale:** 

When the backup credentials are not properly secured, then they might be abused to gain access to the server. The backup user needs an account with many privileges, so an attacker might potentially gain (almost) complete access to the server. 

##### **Audit:** 

Check permissions of files containing passwords and/or SSL keys. 

##### **Remediation:** 

Change file permissions. 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply<br>data access control lists, also known as access permissions, to local and remote<br>file systems, databases, and applications.|●|●|●|
|v8|11.3Protect Recovery Data<br>Protect recovery data with equivalent controls to the original data. Reference<br>encryption or data separation, based on requirements.|●|●|●|
|v7|10.4Ensure Protection of Backups<br>Ensure that backups are properly protected via physical security or encryption<br>when they are stored, as well as when they are moved across the network. This<br>includes remote backups and cloud services.|●|●|●|



Page 38 

Internal Only - General 

### _2.1.4 Point-in-Time Recovery (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS on Linux 

- Level 2 - MySQL RDBMS 

##### **Description:** 

With binlogs it is possible to implement point-in-time recovery. This makes it possible to restore the changes between the last full backup and the point-in-time. 

Enabling binlogs is not sufficient. The binlogs need to be backed up to separate media. The restore procedure should be created and tested. The data in the binlog files may contain sensitive information which needs be stored in the proper location with restrictive permissions and may require encryption. 

##### **Rationale:** 

Using binlogs can reduce the amount of information lost when recovering from a backup. 

##### **Impact:** 

Binlogs can grow quite large and take up a large amount of space so auto remove needs to be put into place. 

##### **Audit:** 

Check if binlogs are enabled and if there is a restore procedure. Check to see if `-binlog-expire-logs-second` is set. 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE, 'BINLOG - Log Expiration' as Note
FROM performance_schema.global_variables where variable_name =
'binlog_expire_logs_seconds';
```

Ensure this value is not set to `0` . 

**Note:** Consider implementing MySQL Enterprise Backup which includes support for at rest encryption of any MySQL Encrypted data files including the binary and relay log files. 

##### **Remediation:** 

Enable binlogs, then create and test a restore procedure. 

##### **Default Value:** 

The default for `binlog-expire-logs-seconds` is `2592000` seconds, or 30 days. 

Page 39 

Internal Only - General 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/replication-options-binarylog.html#sysvar_binlog_expire_logs_seconds</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/point-in-time-recovery-binlog.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|11.2Perform Automated Backups<br>Perform automated backups of in-scope enterprise assets. Run backups<br>weekly, or more frequently, based on the sensitivity of the data.|●|●|●|
|v7|10.2Perform Complete System Backups<br>Ensure that each of the organization's key systems are backed up as a<br>complete system, through processes such as imaging, to enable the quick<br>recovery of an entire system.|●|●|●|



Page 40 

Internal Only - General 

### _2.1.5 Disaster Recovery (DR) Plan (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

- Level 1 - MySQL RDBMS 

##### **Description:** 

A disaster recovery plan should be created. 

MySQL Cluster (group replication), MySQL Replica Sets (asynchronous replication) or both may be used. 

A replica in a different data center and offsite backups may be used. There should be information regarding the Recovery Time Objective (RTO), i.e., how long recovery will take, and if the recovery site has the same capacity. Additionally, delayed replicas can be a valuable part of a DR plan. Network (default) and at rest encryption should be used to protect data. 

##### **Rationale:** 

A disaster recovery strategy should be planned and formalized. Without a well-tested disaster recovery plan, it might not be possible to recover in time. 

##### **Audit:** 

Check if there is a disaster recovery plan. 

##### **Remediation:** 

Create a disaster recovery plan. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/group-replication-security.html</u> 2. <u>https://dev.mysql.com/doc/refman/8.4/en/replication-security.html</u> 

Page 41 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|11.1Establish and Maintain a Data Recovery Process<br>Establish and maintain a data recovery process. In the process, address the<br>scope of data recovery activities, recovery prioritization, and the security of backup<br>data. Review and update documentation annually, or when significant enterprise<br>changes occur that could impact this Safeguard.|●|●|●|
|v7|10Data Recovery Capabilities<br>Data Recovery Capabilities||||



Page 42 

Internal Only - General 

### _2.1.6 Backup of Configuration and Related Files (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

- Level 1 - MySQL RDBMS 

##### **Description:** 

It is important to include configuration, log, key, certificates, and customized files in backups. 

##### **Rationale:** 

Including all configuration, log, key, certificates, and customized files in any backup will ensure the backup can fully restore an instance. 

##### **Audit:** 

Check if these files are in use and are saved in the backup. 

- Edited Configuration files ( `my.cnf` and included files) 

- `SET PERSIST` Configuration file ( `mysqld-auto.cnf` ) 

- Files related to Key Management and Keyring (KMIP, other Key Management Services) 

- Audit Log Files (if not handled by other methods) 

- SSL files (certificates, keys) 

- User Defined Functions (UDFs) 

- Source code for customizations 

##### **Remediation:** 

Add any omitted files to the backup. 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|11.2Perform Automated Backups<br>Perform automated backups of in-scope enterprise assets. Run backups<br>weekly, or more frequently, based on the sensitivity of the data.|●|●|●|
|v7|10.2Perform Complete System Backups<br>Ensure that each of the organization's key systems are backed up as a<br>complete system, through processes such as imaging, to enable the quick<br>recovery of an entire system.|●|●|●|



Page 43 

Internal Only - General 

#### **2.2 Data Encryption** 

This section contains recommendations for securing data at rest and in transit for MySQL. 

Page 44 

Internal Only - General 

### _2.2.1 Ensure Binary and Relay Logs are Encrypted (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS on Linux 

- Level 2 - MySQL RDBMS 

##### **Description:** 

The `binlog_encryption` system variable may be used to configure encryption of the binary and relay logs. This may be configured to `ON` even if binary logging is not enabled in order to encrypt relay log files. 

##### **Rationale:** 

The database, and thus the binary and relay logs, may contain sensitive information. Encrypting the binary and relay logs protects all data stored in these logs from internal and external threats. 

##### **Audit:** 

To audit this setting, run the following command: 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE, 'BINLOG - At Rest Encryption' as Note
FROM performance_schema.global_variables where variable_name =
'binlog_encryption';
```

Ensure it is set to `ON` . 

##### **Remediation:** 

To remediate misconfiguration, run this command: 

```
SET GLOBAL binlog_encryption=ON;
```

If you receive the error message below, you need to install keyring. For instructions see <u>Section 8.4.4, “The MySQL Keyring”</u> in the MySQL documentation. 

```
ERROR 3794 (HY000): Unable to recover binlog encryption master key, please
check if keyring plugin is loaded.
```

##### **Default Value:** 

The default for `binlog_encryption` is `OFF` . 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/replication-binlog-encryption.html</u> 

2. <u>https://dev.mysql.com/doc/mysql-enterprise-backup/8.4/en/advanced.encryptedbinlog-relaylog.html</u> 

3. <u>https://dev.mysql.com/doc/refman/8.4/en/replication-options-binarylog.html#sysvar_binlog_encryption</u> 

Page 45 

Internal Only - General 

##### **Additional Information:** 

It is necessary to install a keyring plugin prior to configuring encryption. 

Consider implementing MySQL Enterprise Backup which includes support for at rest encryption of any MySQL Encrypted data files including the binary and relay log files. 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**<br>**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|3.11Encrypt Sensitive Data at Rest<br>Encrypt sensitive data at rest on servers, applications, and databases containing<br>sensitive data. Storage-layer encryption, also known as server-side encryption,<br>meets the minimum requirement of this Safeguard. Additional encryption methods<br>may include application-layer encryption, also known as client-side encryption,<br>where access to the data storage device(s) does not permit access to the plain-text<br>data.|●|●|
|v7|14.8Encrypt Sensitive Information at Rest<br>Encrypt all sensitive information at rest using a tool that requires a secondary<br>authentication mechanism not integrated into the operating system, in order to<br>access the information.||●|



Page 46 

Internal Only - General 

### _2.3 Dedicate the Machine Running MySQL (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

- Level 1 - MySQL RDBMS 

##### **Description:** 

It is recommended that MySQL Server software be installed on a dedicated server. This architectural consideration affords flexibility in that the database server can be placed on a separate zone allowing access only from particular hosts and over particular protocols. 

##### **Rationale:** 

The attack surface is reduced on a server with only the underlying operating system, MySQL server software, and any security or operational tooling that may be additionally installed. A smaller attack surface reduces the probability of the data within MySQL being compromised. 

##### **Impact:** 

Care must be taken that applications or services that are required for proper operation of the operating system are not removed. 

Custom applications may need to be modified to accommodate database connections over the network rather than on the use (e.g., using TCP/IP connections). 

Additional hardware and operating system licenses may be required to make the architectural change. 

##### **Audit:** 

Verify there are no other roles enabled for the underlying operating system and that no additional applications or services unrelated to the proper operation of the MySQL server software are installed. 

##### **Remediation:** 

Remove excess applications or services and/or remove unnecessary roles from the underlying operating system. 

Page 47 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.12Segment Data Processing and Storage Based on<br>Sensitivity<br>Segment data processing and storage based on the sensitivity of the data. Do<br>not process sensitive data on enterprise assets intended for lower sensitivity<br>data.||●|●|
|v7|2.10Physically or Logically Segregate High Risk<br>Applications<br>Physically or logically segregated systems should be used to isolate and run<br>software that is required for business operations but incur higher risk for the<br>organization.|||●|



Page 48 

Internal Only - General 

### _2.4 Do Not Specify Passwords in the Command Line (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

When a command is executed on the command line, for example `mysql -u admin -p password` or `mysqlsh -u admin -p password` , the password may be visible in the user's shell/command history or in the process list. 

##### **Rationale:** 

If the password is visible in the process list or user's shell/command history, an attacker will be able to access the MySQL database using the stolen credentials. 

##### **Impact:** 

Depending on the remediation chosen, additional steps may need to be undertaken like: 

- Entering a password when prompted. 

- Ensuring the file permissions on `.my.cnf` is restricted yet accessible by the user. 

- • Using `mysql_config_editor` to encrypt the authentication credentials in `.mylogin.cnf` . 

- Use a pluggable secure password store, e.g., a keychain. 

- In the case of shell don't authenticate until `mysqlsh` is started, then use `\connect` 

Additionally, not all scripts/applications may be able to use `.mylogin.cnf` . 

##### **Audit:** 

Check the process or task list if the password is visible. 

Check the shell or command history if the password is visible. 

##### **Remediation:** 

_MySQL Client:_ 

Use `-p` without password and then enter the password when prompted, use a properly secured `.my.cnf` file, or store authentication information in encrypted format in `.mylogin.cnf` . 

Page 49 

Internal Only - General 

#### _MySQL Shell:_ 

Use without password and then enter the password when prompted, store authentication information in encrypted format in `.mylogin.cnf` , enter shell then authenticate using `\connect` command ( **Note:** this also ensures the username is not exposed on the command), or use `mysqlsh` pluggable password store, e.g., a keychain. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/mysql-config-editor.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/password-security-user.html</u> 

3. <u>https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-pluggable-passwordstore.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).|●|●|
|v7|16.4Encrypt or Hash all Authentication Credentials<br>Encrypt or hash with a salt all authentication credentials when stored.|●|●|



Page 50 

Internal Only - General 

### _2.5 Do Not Reuse Usernames (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

- Level 1 - MySQL RDBMS 

##### **Description:** 

Database user accounts should not be reused for multiple applications or users. 

##### **Rationale:** 

Utilizing unique database accounts across applications will reduce the impact of a compromised MySQL account. If a user is reused, then a compromise of this user will compromise multiple parts of the system and/or application. 

##### **Audit:** 

Each user (excluding mysql reserved users) should be linked to one of these: 

- system accounts 

- a person 

- an application 

To list users (and exclude mysql reserved users): 

```
SELECT host, user, plugin,
  IF(plugin = 'mysql_native_password',
 'WEAK SHA1', 'STRONG SHA2') AS HASHTYPE
FROM mysql.user WHERE user NOT IN
  ('mysql.infoschema', 'mysql.session', 'mysql.sys') AND
  plugin NOT LIKE 'auth%' AND plugin <> 'mysql_no_login' AND
  LENGTH(authentication_string) > 0
ORDER BY plugin;
```

##### **Remediation:** 

Add/Remove users so that each user is only used for one specific purpose. 

Page 51 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.1Establish and Maintain an Inventory of Accounts<br>Establish and maintain an inventory of all accounts managed in the enterprise.<br>The inventory must include both user and administrator accounts. The inventory, at<br>a minimum, should contain the person’s name, username, start/stop dates, and<br>department. Validate that all active accounts are authorized, on a recurring<br>schedule at a minimum quarterly, or more frequently.|●|●|●|
|v7|4.3Ensure the Use of Dedicated Administrative Accounts<br>Ensure that all users with administrative account access use a dedicated or<br>secondary account for elevated activities. This account should only be used for<br>administrative activities and not internet browsing, email, or similar activities.|●|●|●|



Page 52 

Internal Only - General 

_2.6 Ensure Non-Default, Unique Cryptographic Material is in Use (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The cryptographic material used by MySQL, such as digital certificates and encryption keys, should be used only for MySQL and only for one instance. Default cryptographic material should not be used since it is not unique to the instance. 

##### **Rationale:** 

If a cryptographic material is used on multiple MySQL instances and/or systems, then a compromise of one may lead to the network traffic of all servers being compromised that use the same cryptographic material. If an attacker gains access to shared cryptographic material, including default material, the attacker can reuse that material to impersonate the MySQL server or otherwise compromise its operations. 

##### **Audit:** 

Review all cryptographic material. If it is default, used for other MySQL instances and/or for purposes other than MySQL then this is a finding. 

Review the server certificate by running: 

```
cd <data_dir and/or ssl_cert>
sudo openssl x509 -in server-cert.pem -subject -noout | grep
Auto_Generated_Server_Certificate
```

The output for the auto generated pem will look something like: 

```
subject= /CN=MySQL_Server_8.0.21_Auto_Generated_Server_Certificate
```

If no rows return, the check is a pass since the certificate is not MySQL auto-generated. 

##### **Remediation:** 

Generate new certificates, keys, and other cryptographic material as needed for each affected MySQL instance. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/using-encrypted-connections.html</u> 

Page 53 

Internal Only - General 

_2.7 Ensure 'password_lifetime' is Less Than or Equal to '365' (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

Password expiration provides users with a unique time bounded password lifetime. 

##### **Rationale:** 

Allows additional security factors pertinent to a specific user to provide further password security; predetermined by varying security needs and usability requirements in a system or organization. 

##### **Audit:** 

The global password lifetime is set using `default_password_lifetime` . If the value of `default_password_lifetime` is greater than `0` , it indicates the permitted password lifetime. 

Execute the following command to check the global password lifetime: 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_variables where VARIABLE_NAME like
'default_password_lifetime';
```

A value greater than `365` implies a fail. 

When the global password lifetime is less than or equal to `365` , or not configured, each user account shall be checked by executing the following command: 

```
SELECT user, host, password_lifetime from mysql.user where password_lifetime
= 0 OR password_lifetime > 365;
```

A lack of results implies compliance. 

**Note:** A value of `0` implies the password never expires. 

##### **Remediation:** 

To configure the global password lifetime to `365` by executing the following command: 

```
set persist default_password_lifetime = 365;
```

Alternatively, configure the password lifetime for each user returned by the audit procedure by executing the following command: 

```
ALTER USER '<username>'@'<localhost>' PASSWORD EXPIRE INTERVAL 365 DAY;
```

Page 54 

Internal Only - General 

##### **Default Value:** 

```
NULL
```

##### **References:** 

1. <u>https://csrc.nist.gov/csrc/media/publications/sp/800-118/archive/2009-0421/documents/draft-sp800-118.pdf</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/validate-password.html</u> 

##### **Additional Information:** 

When a user's `password_lifetime` is set to `NULL` it takes on the value set in global `default_password_lifetime` variable. 

Page 55 

Internal Only - General 

### _2.8 Ensure Password Resets Require Strong Passwords (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

Disabling password reuse, enforcing password strength, and denying reuse can be implemented to prevent successful usage of stolen or previously guessed passwords by malicious users. 

Restricted accounts using passwords on the basis of the number of password changes and length ensure a password cannot be chosen from a specified number of the most recent passwords. 

##### **Rationale:** 

Repeated use of old passwords can increase risk of a compromise. This may lead to access by malicious users who have discovered a user's prior password(s). 

##### **Audit:** 

To assess this recommendation run the following statement: 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_variables where VARIABLE_NAME in
('password_history', 'password_reuse_interval');
```

A value of `0` indicates that NO policy is defined for the associated variable. 

The `password_history` variable indicates the number of subsequent account password changes that must occur before the password can be reused. The `password_history` should be greater than or equal to `5` , thus attempts to use any of the prior five, or more, passwords for this account will be denied. 

The `password_reuse_interval` defines the global policy for controlling reuse of previous passwords based on time elapsed. For an account password used previously, this variable indicates the number of days that must pass before the password can be reused. 

Password should not be reused over the period of a year. The value of `password_reuse_interval` should be greater than or equal to `365` . 

##### **Remediation:** 

Set a global policy that passwords may not be reused for a minimum of five password changes: 

Page 56 

Internal Only - General 

```
SET PERSIST password_history = 5;
```

Set a global policy that passwords have a lifetime to approximately one year (in days) 

```
SET PERSIST password_reuse_interval = 365;
```

##### **Default Value:** 

Both `password_history` and `password_reuse_interval` are `0` (off) by default. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/passwordmanagement.html#password-reuse-policy</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.2Use Unique Passwords<br>Use unique passwords for all enterprise assets. Best practice implementation<br>includes, at a minimum, an 8-character password for accounts using MFA and a<br>14-character password for accounts not using MFA.|●|●|●|



Page 57 

Internal Only - General 

- _2.9 Require Current Password for Password Reset (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

Require the current password for password reset. 

##### **Rationale:** 

Requiring a prior password for password reset enables DBAs to prevent users from changing a password without proving that they know the current password. Such changes could otherwise occur, for example, if one user walks away from a terminal session temporarily without logging out, and a malicious user uses the session to change the original user's MySQL password. This can have unfortunate consequences; the most problematic being the malicious user can access MySQL with the user's changed credentials. 

##### **Audit:** 

Run the following statement: 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_variables where VARIABLE_NAME in
('password_require_current');
```

The return value should be `ON` . 

##### **Remediation:** 

Set the value to `ON` 

```
SET PERSIST password_require_current=ON;
```

##### **Default Value:** 

The `password_require_current` is `OFF` by default. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/server-systemvariables.html#sysvar_password_require_current</u> 

Page 58 

Internal Only - General 

_2.10 Use Dual Passwords to Enable Higher Frequency Password Rotation (Manual)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

Dual passwords act as a tool to encourage password rotations in cases where a synchronized password change is not viable. By having a time delta to have old and new passwords in place, the process of replacing old passwords with new passwords within applications is simplified. 

##### **Rationale:** 

Too often passwords used by applications are not changed regularly because of the difficulty in timing for propagating the new password, keeping the applications connected, and connection failures due to race conditions. If it is difficult to perform a synchronized change you can optionally use dual passwords to simplify the task of password rotation. 

##### **Impact:** 

If the original password isn't removed upon completion of the password rotation process, the potential risk for a compromise is increased. 

##### **Audit:** 

To determine which users currently have dual passwords, run the following command: 

```
SELECT user, host FROM mysql.user WHERE length(user_attributes-
>"$.additional_password")>0;
```

If an account has a dual password and the process of password rotation has completed, this is a fail. 

##### **Remediation:** 

To set dual passwords execute the following `ALTER` command: 

```
ALTER USER '<user>'@'<hostname>'
  IDENTIFIED BY '<new_password>'
  RETAIN CURRENT PASSWORD;
```

Once the new password has been distributed `DISCARD` the old password using `ALTER` : 

```
ALTER USER '<user>'@'<hostname>'
  DISCARD OLD PASSWORD;
```

Page 59 

Internal Only - General 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/password-management.html#dualpasswords</u> 

##### **Additional Information:** 

You may wish to first assess the state of passwords on your MySQL Server. 

Password expiration is based on the policy set by the `default_password_lifetime` or by explicit settings on a per account basis. 

To assess when passwords were last changed on accounts and when, or if, they will expire run the following 

```
select user, host, password_last_changed,
IF(IFNULL(password_lifetime, CAST(@@default_password_lifetime as
signed))<1,'NEVER',
concat(
cast(
IFNULL(password_lifetime, @@default_password_lifetime) as signed)
+ cast(datediff(password_last_changed, now()) as signed), " days")) as
days_till_expires
from mysql.user;
```

Applications will fail to authenticate when `days_till_expires` reaches `0` . 

If `NEVER` returns for an account and the password has not be rotated in a long period of time it is recommended that action be taken to set a new password. 

Page 60 

Internal Only - General 

- _2.11 Lock Out Accounts if Not Currently in Use (Manual)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

If users with accounts will not be using their account for some time, to reduce the risk of attacks or inappropriate account usage or if suspicions exist that an account might be under attack, disabling the account will secure it and once it's ready to resume use it can easily be re-enabled. 

##### **Rationale:** 

Only have active accounts that will be used. 

##### **Audit:** 

Review the locked status of accounts: 

```
select user, host, account_locked from mysql.user;
```

Accounts not in use and MySQL Reserved accounts should show as locked ( `Y` ). 

##### **Remediation:** 

To lock accounts - example: 

```
ALTER USER 'jeffrey'@'localhost' ACCOUNT LOCK;
```

To unlock accounts - example 

```
ALTER USER 'jeffrey'@'localhost' ACCOUNT UNLOCK;
```

Note: Works for `CREATE` as well. It is good practice to `LOCK` an account if created ahead of time. 

##### **Default Value:** 

Accounts are unlocked by default. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/account-locking.html</u> 

##### **Additional Information:** 

When a client attempts to connect to a locked account, the attempt fails. 

```
Access denied for user '<user_name>'@'<host_name>'.
Account is locked.
```

Page 61 

Internal Only - General 

The server increments the `Locked_connects` status variable that indicates the number of attempts to connect to a locked account. To view the `Locked_conects` execute this query: 

```
show global status like 'Locked_connects';
```

The error log will contain the message `ER_ACCOUNT_HAS_BEEN_LOCKED` . 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.3Disable Dormant Accounts<br>Delete or disable any dormant accounts after a period of 45 days of<br>inactivity, where supported.|●|●|●|
|v7|16.9Disable Dormant Accounts<br>Automatically disable dormant accounts after a set period of inactivity.|●|●|●|



Page 62 

Internal Only - General 

### _2.12 Ensure AES Encryption Mode for_ 

_AES_ENCRYPT/AES_DECRYPT is Configured Correctly (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

A block encryption mode with a Cipher Block Chaining (CBC) mode value and key length of 256 is recommended when using the `AES_ENCRYPT()` and `AES_DECRYPT()` functions for encryption. 

##### **Rationale:** 

The default for backward compatibility on upgraded MySQL databases is `aes-128-ecb` . Using 128-bit keys does not provide sufficient security. Regardless of whether breaking the lowest level is beyond existing technology, larger key sizes are needed to better protect data and satisfy regulations. 

##### **Impact:** 

Configuring a key length of 256 may impact backwards compatibility. 

##### **Audit:** 

Run the following statement: 

```
select @@block_encryption_mode;
```

A value other than `aes-256-*` is a fail. 

Where `*` is one of the following - `ECB` , `CBC` , `CFB1` , `CFB8` , `CFB128` , `OFB` 

##### **Remediation:** 

Add the following lines to the MySQL server's `/etc/my.cnf` : 

For example, if Block Encryption Mode for aes-256 CBC 

```
block_encryption_mode=aes-256-cbc
```

Or, run the following command: 

```
set persist block_encryption_mode='aes-256-cbc';
```

Restart the server for this change to take effect. 

Page 63 

Internal Only - General 

##### **Default Value:** 

```
aes-128-ecb
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.4/en/securedeployment-block-encryption-mode.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**<br>**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|16.11Leverage Vetted Modules or Services for Application<br>Security Components<br>Leverage vetted modules or services for application security components, such<br>as identity management, encryption, and auditing and logging. Using platform<br>features in critical security functions will reduce developers’ workload and minimize<br>the likelihood of design or implementation errors. Modern operating systems provide<br>effective mechanisms for identification, authentication, and authorization and make<br>those mechanisms available to applications. Use only standardized, currently<br>accepted, and extensively reviewed encryption algorithms. Operating systems also<br>provide mechanisms to create and maintain secure audit logs.|●|●|
|v7|18.5Use Only Standardized and Extensively Reviewed<br>Encryption Algorithms<br>Use only standardized and extensively reviewed encryption algorithms.|●|●|



Page 64 

Internal Only - General 

- _2.13 Ensure Socket Peer-Credential Authentication is Used Appropriately (Manual)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS on Linux 

- Level 2 - MySQL RDBMS 

##### **Description:** 

The server-side `auth_socket` authentication plugin, authenticates clients that connect to the MySQL server from the local host through the Unix socket file. Users authenticated by the `auth_socket` need not specify a password when connecting to the server. However, users authenticated by the `auth_socket` plugin are restricted from connecting remotely; they can only connect from the local host through the Unix socket file. This method is only suitable in situations where the server administrator OS account access is restricted. 

##### **Rationale:** 

This method may be desirable in specific cases, including: 

- The Linux system where MySQL is running is dedicated to the MySQL server and only the MySQL DBA and OS Admin have access. 

- When control over user authentication is centralized in the operating system. 

- It is desirable that audit trails in the database and operating system can use the same user names. 

- For certain other narrow installation use cases `auth_socket` may be desirable. 

- Only local connections for a user. 

##### **Impact:** 

Things to consider when using the operating system to authenticate users: 

- The user must have an operating system account on the computer which must be accessed. 

- If a user has logged in using this method and steps away from the terminal, another user could easily log in because this user does not need any passwords or credentials. This could pose a serious security problem. 

- When an operating system is used to authenticate database users, managing distributed database environments and database links requires special care. Special care must also be taken not to leave such a terminal unlocked and unattended. Hence, we recommend that you carefully evaluate your requirements before opting for `auth_socket` . 

- This will not work where distributed connections are required. 

Page 65 

Internal Only - General 

##### **Audit:** 

To assess this recommendation run the following: 

```
SELECT PLUGIN_NAME, PLUGIN_STATUS
       FROM INFORMATION_SCHEMA.PLUGINS
       WHERE PLUGIN_NAME LIKE 'auth%';
```

To determine users who can use auth socket: 

```
select user, host, plugin from mysql.user where plugin = 'auth_socket';
```

If this is enabled and the organization does not allow use of this feature, this is a fail. 

If `host` is not the localhost or an unauthorized user is listed, this is a fail. 

##### **Remediation:** 

Add these options under the `[mysqld]` option group in the MySQL `/etc/my.cnf` : 

```
plugin-load-add=auth_socket.so
auth_socket=FORCE_PLUS_PERMANENT
```

**For example:** 

For an OS user which can login to MySQL using `auth_socket` : 

```
CREATE USER '<user>'@'<localhost>' IDENTIFIED WITH auth_socket;
```

The user can then login using: 

```
mysql -u <user>
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.4/en/securedeployment-configure-authentication.html#secure-deployment-auth-socket</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|6.6Establish and Maintain an Inventory of Authentication<br>and Authorization Systems<br>Establish and maintain an inventory of the enterprise’s authentication and<br>authorization systems, including those hosted on-site or at a remote service<br>provider. Review and update the inventory, at a minimum, annually, or more<br>frequently.|●|●|



Page 66 

Internal Only - General 

- _2.14 Ensure MySQL is Bound to an IP Address (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

By default, the MySQL server accepts TCP/IP connections from MySQL user accounts on all server host IPv6 and IPv4 interfaces. You can make this configuration more restrictive by setting the `bind_address` configuration option to a specific IPv4 or IPv6 address so that the server only accepts TCP/IP connections on that address. 

##### **Rationale:** 

Limiting the IP address provides additional controls and restrictions on how client applications can connect to MySQL. If not configured to a specific IP all IPs for this server can be used to connect to MySQL. 

##### **Audit:** 

Run the following statement: 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_variables
WHERE VARIABLE_NAME = 'bind_address';
```

No rows returned implies a fail. 

##### **Remediation:** 

For example, to have the MySQL server only accept connections on a specific IPv4 address, add an entry similar to this under the `[mysqld]` option group in the MySQL `/etc/my.cnf` : 

```
bind_address=192.0.2.24
```

In this case, clients can connect to the server using `--host=192.0.2.24` . Connections on other server host addresses are not permitted. 

##### **Default Value:** 

Not set. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.4/en/securedeployment-secure-connections.html</u> 

Page 67 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|16.10Apply Secure Design Principles in Application<br>Architectures<br>Apply secure design principles in application architectures. Secure design<br>principles include the concept of least privilege and enforcing mediation to validate<br>every operation that the user makes, promoting the concept of "never trust user<br>input." Examples include ensuring that explicit error checking is performed and<br>documented for all input, including for size, data type, and acceptable ranges or<br>formats. Secure design also means minimizing the application infrastructure attack<br>surface, such as turning off unprotected ports and services, removing unnecessary<br>programs and files, and renaming or removing default accounts.||●|●|



Page 68 

Internal Only - General 

_2.15 Limit Accepted Transport Layer Security (TLS) Versions (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

MySQL supports multiple protocols of TLS. The higher the version the stronger the security and/or better the performance. 

##### **Rationale:** 

Requiring clients attempting to connect to MySQL to use higher versions of TLS to better protect data in transit. 

##### **Impact:** 

Connections attempting to use an unsupported version of TLS or Cipher will fail. 

##### **Audit:** 

To list the versions of TLS the server accepts, run the following statement: 

```
select @@tls_version;
```

If the list includes `TLSv1` and/or `TLSv1.1` , this is a fail. 

To view current connections and the version of SSL in use run: 

```
select * from performance_schema.status_by_thread where VARIABLE_NAME like
'ssl_version';
```

If the list includes, `TLSv1` and/or `TLSv1.1` , this is a fail. 

MySQL negotiates to the highest version of TLS, if connections are using older TLS versions, those clients will need to be upgraded to newer MySQL Connectors or community drivers that support newer versions of TLS. 

##### **Remediation:** 

Set the version(s) of TLS you wish to accept in `mysql.conf` specify TLS and Ciphers. 

For example to only accept TLS 1.3 set `tls_version` in `my.conf` : 

```
tls_version=TLSv1.3
```

If TLS 1.3 is not supported on the Operating System then set to TLS 1.2: 

```
tls_version=TLSv1.2
```

Page 69 

Internal Only - General 

**Note:** with this setting, only clients that support the specified TLS version(s) are able to establish an encrypted connection to the server. 

##### **Default Value:** 

All TLS and cipher versions are enabled by default. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.4/en/securedeployment-secure-connections.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/encrypted-connection-protocolsciphers.html#encrypted-connection-protocol-configuration</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**<br>**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).|●|●|
|v8|16.11Leverage Vetted Modules or Services for Application<br>Security Components<br>Leverage vetted modules or services for application security components, such<br>as identity management, encryption, and auditing and logging. Using platform<br>features in critical security functions will reduce developers’ workload and minimize<br>the likelihood of design or implementation errors. Modern operating systems provide<br>effective mechanisms for identification, authentication, and authorization and make<br>those mechanisms available to applications. Use only standardized, currently<br>accepted, and extensively reviewed encryption algorithms. Operating systems also<br>provide mechanisms to create and maintain secure audit logs.|●|●|
|v7|14.4Encrypt All Sensitive Information in Transit<br>Encrypt all sensitive information in transit.|●|●|
|v7|18.5Use Only Standardized and Extensively Reviewed<br>Encryption Algorithms<br>Use only standardized and extensively reviewed encryption algorithms.|●|●|



Page 70 

Internal Only - General 

- _2.16 Require Client-Side Certificates (X.509) (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

Client-side certificates may be used as proof of identity as well as to encrypt data in transit. 

##### **Rationale:** 

Requiring client-side certificates provides additional validation of a user's identity, thus increasing the level of security, while also providing strong encryption. 

##### **Audit:** 

Run the following statement 

```
select user, host, ssl_type from mysql.user where user not in
('mysql.infoschema', 'mysql.session', 'mysql.sys');
```

If `ssl_type` returns `X509` or `SSL` , client-side certificate details must be provided to connect. 

##### **Remediation:** 

Create or Alter users using the `REQUIRE X509` . 

For example: 

```
CREATE USER 'newuser2'@'%' IDENTIFIED BY <password> require x509;
```

For accounts created with a `REQUIRE X509` clause, clients must specify at least `--sslcert` and `--ssl-key` . In addition, `--ssl-ca` (or `--ssl-capath` ) is recommended so that the public certificate provided by the server can be verified. 

For example: 

```
mysql --ssl-ca=ca.pem \
      --ssl-cert=client-cert.pem \
      --ssl-key=client-key.pem
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/using-encrypted-connections.html</u> 

Page 71 

Internal Only - General 

##### **Additional Information:** 

The audit procedure excludes these internal user accounts from evaluation because, by default, they are created with an invalid password and are locked to disallow access. 

- `‘mysql.infoschema’@’localhost’` 

- `‘mysql.session’@’localhost’` 

- `‘mysql.sys’@’localhost’` 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).|●|●|
|v7|14.4Encrypt All Sensitive Information in Transit<br>Encrypt all sensitive information in transit.|●|●|



Page 72 

Internal Only - General 

- _2.17 Ensure Only Approved Ciphers are Used (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS on Linux 

- Level 2 - MySQL RDBMS 

##### **Description:** 

MySQL supports multiple encryption ciphers. Ciphers can vary in strength, speed and overhead. 

##### **Rationale:** 

Requiring clients attempting to connect to MySQL to use strong ciphers protects data in transit. 

##### **Impact:** 

Connections attempting to use an unsupported cipher will fail. 

##### **Audit:** 

Run the following statement: 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_variables
WHERE VARIABLE_NAME IN ('ssl_cipher', 'tls_ciphersuites');
```

If `ssl_cipher` is not set to `ECDHE-ECDSA-AES128-GCM-SHA256` or `tls_ciphersuites` is not set to `TLS_AES_256_GCM_SHA384` , this is a fail. 

##### **Remediation:** 

Set `ssl_cipher` and `tls_ciphersuites` in the `mysql.conf` to an approved cipher suite: 

```
tls_ciphersuites='TLS_AES_256_GCM_SHA384'
ssl_cipher='ECDHE-ECDSA-AES128-GCM-SHA256'
```

Or 

Execute the following commands: 

```
set persist ssl_cipher='ECDHE-ECDSA-AES128-GCM-SHA256';
set persist tls_ciphersuites='TLS_AES_256_GCM_SHA384';
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/encrypted-connection-protocolsciphers.html#encrypted-connection-cipher-configuration</u> 

Page 73 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|16.11Leverage Vetted Modules or Services for Application<br>Security Components<br>Leverage vetted modules or services for application security components, such<br>as identity management, encryption, and auditing and logging. Using platform<br>features in critical security functions will reduce developers’ workload and minimize<br>the likelihood of design or implementation errors. Modern operating systems provide<br>effective mechanisms for identification, authentication, and authorization and make<br>those mechanisms available to applications. Use only standardized, currently<br>accepted, and extensively reviewed encryption algorithms. Operating systems also<br>provide mechanisms to create and maintain secure audit logs.||●|●|
|v7|18.5Use Only Standardized and Extensively Reviewed<br>Encryption Algorithms<br>Use only standardized and extensively reviewed encryption algorithms.||●|●|



Page 74 

Internal Only - General 

_2.18 Implement Connection Delays to Limit Failed Login Attempts (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

MySQL Server can enable administrators to introduce an increasing delay in server response to clients after a certain number of consecutive failed connection attempts. 

##### **Rationale:** 

Delaying connection attempts provides a deterrent that slows down brute force attacks that attempt to access MySQL user accounts. 

##### **Audit:** 

Determine if the plugins for delaying connections are installed. 

```
SELECT PLUGIN_NAME, PLUGIN_STATUS
       FROM INFORMATION_SCHEMA.PLUGINS
       WHERE PLUGIN_NAME LIKE 'connection%';
```

Two rows should be returned showing `ACTIVE` status. 

```
CONNECTION_CONTROL                       | ACTIVE
CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS | ACTIVE
```

If both plugins are not active, this is a fail. 

Next assess the setting for the connection controls by running 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE
       FROM performance_schema.global_variables WHERE VARIABLE_NAME LIKE
'connection_control%';
```

Time doubling throttling (in minutes) between each retry ( `0` , `1` , `2` , `4` , `8` , etc.) with a permanent account lockout (IT reset required) after 12 retries. 

If `connection_control_failed_connections_threshold` is less than `5` (attempts), this is a fail. 

If `connection_control_min_connection_delay` is less than `60000` (ms - 1 minute), this is a fail. 

Max delay `connection_control_max_connection_delay` is `0` or less than `1920000` (ms, 32 minutes) a, this is a fail. 

Finally, assess the failed login attempts. 

Page 75 

Internal Only - General 

```
select host, user, JSON_EXTRACT(user_attributes,
'$.Password_locking.failed_login_attempts') as failed_login_attempts from
mysql.user;
```

If failed login attempts is less than `12` this is a fail. 

##### **Remediation:** 

Add the following lines to `my.cnf` : 

```
[mysqld]
plugin-load-add=connection_control.so
connection-control=FORCE_PLUS_PERMANENT
connection-control-failed-login-attempts=FORCE_PLUS_PERMANENT
connection_control_failed_connections_threshold=5
connection_control_min_connection_delay=60000
connection_control_max_connection_delay=1920000
```

Delays are in milliseconds for server response to failed connection attempt. 

- `60000` (ms - 1 minute) 

- `1920000` (ms, 32 minutes) 

For each user set 

```
ALTER USER <user> FAILED_LOGIN_ATTEMPTS 12;
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/connection-control.html</u> 

##### **CIS Controls:** 

|**Controls Version**|**Control**<br>**IG**|**1**<br>**IG 2**<br>**IG 3**|
|---|---|---|
|v7|16Account Monitoring and Control<br>Account Monitoring and Control||



Page 76 

Internal Only - General 

- _2.19 Ensure FIPS 140-2 OpenSSL Cryptography Is Used (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

Install, configure, and use OpenSSL on a platform that has a NIST certified FIPS 140-2 installation of OpenSSL. This provides MySQL instances the ability to generate and validate cryptographic hashes to protect unclassified information requiring confidentiality and cryptographic protection, in accordance with the data owner's requirements. 

##### **Rationale:** 

Federal Information Processing Standards 140-2 (FIPS 140-2) describes a security standard that can be required by Federal (US Government) agencies for cryptographic modules used to protect sensitive or valuable information. To be considered acceptable for such Federal use, a cryptographic module must be certified for FIPS 140-2. If a system intended to protect sensitive data lacks the proper FIPS 140-2 certificate, Federal agencies cannot purchase it. 

Products such as OpenSSL can be used in FIPS mode, although the OpenSSL library itself is not validated for FIPS. Instead, the OpenSSL library is used with the OpenSSL FIPS Object Module to enable OpenSSL-based applications to operate in FIPS mode. 

For general information about FIPS and its implementation in OpenSSL, these references may be helpful: 

- <u>National Institute of Standards and Technology FIPS PUB 140-2</u> 

- <u>OpenSSL FIPS 140-2 Security Policy</u> 

- <u>fips_module manual page</u> 

##### **Audit:** 

For MySQL to support FIPS mode, these system requirements must be satisfied: 

1. MySQL must be compiled with an OpenSSL version that is certified for use with FIPS. Currently OpenSSL 3.0 is certified, but OpenSSL 1.1.1 is not. Binary distributions for recent versions of MySQL are compiled using OpenSSL 3.0 on some platforms, which means they are not certified for FIPS. This means you have the following options, depending on system and MySQL configuration: 

   - Use a system that has OpenSSL 3.0 and the required FIPS object module. In this case, you can enable FIPS mode for MySQL if you use a binary distribution compiled using OpenSSL 3.0, or compile MySQL from source using OpenSSL 3.0. For general information about upgrading to OpenSSL 3.0, see OpenSSL 3.0 Migration Guide 

Page 77 

Internal Only - General 

   - Use a system that has OpenSSL 1.1.1 or higher. In this case, you can install MySQL using binary packages, and you can use the TLS v1.3 protocol and ciphersuites, in addition to other already supported TLS protocols. However, you cannot enable FIPS mode for MySQL. 

   - Use a system that has OpenSSL 1.0.2 and the required FIPS Object Module. In this case, you can enable FIPS mode for MySQL if you use a binary distribution compiled using OpenSSL 1.0.2, or compile MySQL from source using OpenSSL 1.0.2. In this case, you cannot use the TLS v1.3 protocol or ciphersuites, which require OpenSSL 1.1.1 or 3.0. In addition, you should be aware that OpenSSL 1.0.2 reached end of life status in 2019, and that all operating platforms embedding OpenSSL 1.1.1 reach their end of life in 2024. 

2. At runtime, the OpenSSL library and OpenSSL FIPS Object Module must be available as shared (dynamically linked) objects. 

If FIPS mode is required, it is recommended to use an operating platforms that includes it; if it does, you can (and should) use it. If your platform does not include FIPS, you have two options: 

- Migrate to a platform which has FIPS OpenSSL support. 

- Build the OpenSSL library and FIPS object module from source, using the instructions from the fips_module manpage see <u>FIPS Overview.</u> 

Your version of mysql should be a version linked to the certified Operating Systems OpenSSL. Run - ldd on your mysqld executable. 

If the libssl library is linked to and openssl library listed originates from within MySQL's installed lib directory. That is not a FIPS certified OpenSSL. This can happen on Windows, MacOS and if MySQL is installed via a generic linux tar. 

For Linuxes where MySQL references the Operating systems OpenSSL certified library checking for FIPS depends on OpenSSL version. 

For OpenSSL prior to 3.0 

To determine whether MySQL is running on a system with FIPS mode enabled, check the value of the `ssl_fips_mode` server system variable using an SQL statement such as 

```
SHOW VARIABLES LIKE '%fips%'
```

or 

```
SELECT @@ssl_fips_mode
```

If the value of this variable is `1 (ON)` or `2 (STRICT)` , FIPS mode is enabled for OpenSSL; if it is `0 (OFF)` , FIPS mode is not available. 

For OpenSSL 3.0 and higher Check the Operating system to see that FIPS mode is enabled. For example on Oracle Linux 9 to verify that FIPS mode is enabled, run the following command after Oracle Linux 9 has been installed: 

Page 78 

Internal Only - General 

As the system administrator: 

1. Run the following to see if FIPS is enabled: 

```
fips-mode-setup --check
```

If `FIPS mode is enabled` is not displayed, then the system is not FIPS enabled and this is a fail. 

2. Run the following (your results and version may vary): 

```
# openssl version
OpenSSL 3.0.7 1 Nov 2022 (Library: OpenSSL 3.0.7 1 Nov 2022)
```

OpenSSL should show a 3.0 version. 

3. Check to see if OpenSSL configuration has enabled the FIPS provider. 

```
openssl list –provider
```

If FIPS is not listed as a provider - OpenSSL is not in FIPS mode. 

4. Test - for example 

##### <u>Try a non-FIPS TLS connection</u> 

```
# mysql -u root -p --host=localhost --protocol=TCP --ssl-mode=REQUIRED
--tls-version=TLSv1.3 --tls-ciphersuites=TLS_CHACHA20_POLY1305_SHA256
Enter password:
ERROR 2026 (HY000): SSL connection error: error:0A0000B5:SSL
routines::no ciphers available
```

If this succeeds you are NOT in FIPS mode 

Next connect and run 

```
mysql> select md5(8);show warnings;
```

```
+----------------------------------+
| md5(8)                           |
+----------------------------------+
| 00000000000000000000000000000000 |
+----------------------------------+
1 row in set, 1 warning (0.00 sec)
+---------+------+-----------------------------------------------------
-------------------+
| Level   | Code | Message
|
+---------+------+-----------------------------------------------------
-------------------+
| Warning | 4073 | SSL fips mode error: FIPS mode ON/STRICT: MD5 digest
is not supported. |
+---------+------+-----------------------------------------------------
-------------------+
1 row in set (0.00 sec)
------------
```

Page 79 

Internal Only - General 

The error was expected – demonstrates FIPS compliant 

If you are in FIPS mode - you will see the following error. If not you are not in FIPS mode. 

##### **Remediation:** 

Configure OpenSSL to be FIPS compliant as MySQL uses OpenSSL for cryptographic modules. To configure OpenSSL to be FIPS 140-2 or FIPS 140-3 compliant, see the official documentation for your operating system. 

Below is a general summary of the steps required: To switch the system to FIPS mode in Oracle Linux 9 or RHEL 9: 

```
# fips-mode-setup –enable
You must reboot the system for the setting to take effect.
FIPS mode will be enabled.
Please reboot the system for the setting to take effect.
```

Before you reboot be sure that sshd is configured for FIPS mode and that any SSH keys are FIPS mode compatible and have a password. 

After the reboot, you should re-check the current state of FIPS mode: 

```
# fips-mode-setup --check
FIPS mode is enabled.
```

For MySQL running OpenSSL prior to version 3.0 in the mysql configuration file: add 

```
[mysqld]
ssl_fips_mode=ON  # or STRICT
```

For MySQL running OpenSSL 3.0 and higher: 

In addition to setting the operating system to FIPS mode. 

Configure the openssl configuration for FIPS mode. 

##### **References:** 

1. <u>https://docs.oracle.com/en/operating-systems/oraclelinux/9/security/configuring_fips_mode.html#enabling-and-disabling-fips-mode</u> 

2. <u>https://csrc.nist.gov/CSRC/media/projects/cryptographic-module-validationprogram/documents/security-policies/140sp1758.pdf</u> 

3. <u>https://csrc.nist.gov/publications/fips</u> 

Page 80 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).||●|●|
|v7|14.4Encrypt All Sensitive Information in Transit<br>Encrypt all sensitive information in transit.||●|●|



Page 81 

Internal Only - General 

### **3 File Permissions** 

File Permissions are critical for keeping the data and configuration of the MySQL server secure. 

Page 82 

Internal Only - General 

- _3.1 Ensure 'datadir' Has Appropriate Permissions (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The data directory is the location of the MySQL databases. 

##### **Rationale:** 

Limiting the accessibility of these objects will protect the confidentiality, integrity, and availability of the MySQL database. If someone other than the MySQL user is allowed to read files from the data directory, it may be possible to read data from the `mysql.user` table which contains passwords. Additionally, the ability to create files can lead to denial of service, or might otherwise allow someone to gain access to specific data by manually creating a file with a view definition. 

##### **Audit:** 

Perform the following steps to assess this recommendation: 

- Execute the following SQL statement to determine the `Value` of `datadir` 

<mark>`show variables where variable_name = 'datadir';`</mark> Or 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_variables
WHERE VARIABLE_NAME LIKE 'datadir';
```

- Execute the following command at a terminal prompt 

```
sudo ls -ld <datadir> | grep "drwxr-x---.*mysql.*mysql"
```

Lack of output implies a fail. 

##### **Remediation:** 

Execute the following commands at a terminal prompt: 

```
chmod 750 <datadir>
chown mysql:mysql <datadir>
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.4/en/securedeployment-permissions.html</u> 

Page 83 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 84 

Internal Only - General 

_3.2 Ensure 'log_bin_basename' Files Have Appropriate Permissions (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

MySQL can operate using a variety of log files, each used for different purposes. These are the binary log (which can be encrypted), error log, slow query log, relay log, general log, and in the enterprise edition, the audit log (which can be encrypted). Because these are files on the host operating system, they are subject to the permissions and ownership structure provided by the host and may be accessible by users other than the MySQL user. Additionally, using secure key management and at rest MySQL encryption can further protect data from OS users. 

##### **Rationale:** 

Limiting the accessibility of these objects will protect the confidentiality, integrity, and availability of the MySQL logs. 

##### **Impact:** 

Changing the permissions and ownership of the relay logs and binary log files might have impact on external tools. 

If the permissions on the relay logs and binary log files are accidentally changed to exclude the user account which is used to run the MySQL service, then this might break replication. 

The binary log file can be used for point-in-time recovery so this can also affect backup, restore, and disaster recovery procedures. 

##### **Audit:** 

Perform the following steps to assess this recommendation: 

1. Execute the following SQL statement to determine the Value of `log_bin_basename` : 

```
show variables like 'log_bin_basename';
```

2. Execute the following command at a terminal prompt to list all non-compliant `log_bin_basename.*` file permissions: 

```
ls -l | egrep '^-(?![r|w]{2}-[r|w]{2}----
.*mysql\s*mysql).*<log_bin_basename>.*$'
```

Lack of output implies compliance. 

Page 85 

Internal Only - General 

##### **Remediation:** 

Execute the following command for each log file location requiring corrected permissions and ownership: 

```
chmod 660 <log file>
chown mysql:mysql <log file>
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/password-logging.html</u> 

2. <u>https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.4/en/securedeployment-permissions.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 86 

Internal Only - General 

### _3.3 Ensure 'log_error' Has Appropriate Permissions (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

MySQL can operate using a variety of log files, each used for different purposes. These are the binary log (which can be encrypted), error log, slow query log, relay log, general log, and in the enterprise edition, the audit log (which can be encrypted). Because these are files on the host operating system, they are subject to the permissions and ownership structure provided by the host and may be accessible by users other than the MySQL user. Additionally, using secure key management and at rest MySQL encryption can further protect data from OS users. 

Much of the information about the state of MySQL exists in MySQL, the MySQL `performance_schema` or `informations_schema` . In cases where the information you need is within a running MySQL, use these methods as they are more secure as they do not require OS login and access. 

##### **Rationale:** 

Limiting the accessibility of these objects will protect the confidentiality, integrity, and availability of the MySQL logs. 

##### **Impact:** 

Changing the permissions of the error log files might have impact on monitoring tools which use an error log file adapter. 

##### **Audit:** 

Perform the following steps to assess this recommendation: 

1. Execute the following SQL statement to determine the Value of `log_error` : 

```
show variables like 'log_error';
```

2. Execute the following command at a terminal prompt to list all non-compliant _`<log_error>`_ `.*` file permissions: 

```
ls -l /usr/local/mysql/data/mysqld.local.err | grep '^-rw-------
.*mysql.*mysql.*$'
```

Lack of output implies a fail. 

Page 87 

Internal Only - General 

##### **Remediation:** 

Execute the following command for each log file location requiring corrected permissions and ownership: 

```
chmod 600 <log file>
chown mysql:mysql <log file>
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/error-log.html</u> 

2. <u>https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.4/en/securedeployment-permissions.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).||●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 88 

Internal Only - General 

### _3.4 Ensure 'slow_query_log' Has Appropriate Permissions (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

MySQL can operate using a variety of log files, each used for different purposes. These are the binary log (which can be encrypted), error log, slow query log, relay log, general log, and in the enterprise edition, the audit log (which can be encrypted). Because these are files on the host operating system, they are subject to the permissions and ownership structure provided by the host and may be accessible by users other than the MySQL user. Additionally, using secure key management and at rest MySQL encryption can further protect data from OS users. 

Much of the information about the state of MySQL exists in MySQL, the MySQL `performance_schema` or `informations_schema` . If you can get the information you need from within MySQL that is more secure as it does not require OS access. If you are not going to use log files it is best to first disable (don’t enable) and remove any prior logs. 

##### **Rationale:** 

Limiting the accessibility of these objects will protect the confidentiality, integrity, and availability of the MySQL logs. 

##### **Impact:** 

Changing the permissions of the log files may impact monitoring tools which use a log file adapter. Also, the slow query log can be used for performance analysis by application developers. 

The information about the performance exists in MySQL `performance_schema` or `sys` schema views. In cases where the information you need is within a running MySQL, disable the slow query log and instead use these methods as they are more secure and do not require OS login and access. 

##### **Audit:** 

Perform the following steps to assess this recommendation: 

1. Execute the following SQL statement to determine the Value of `slow_query_log` : 

```
show variables like 'slow_query_log';
```

Best for the slow query log to be disabled indicated by OFF. 

Page 89 

Internal Only - General 

2. Execute the following SQL statement to determine the location of `slow_query_log_file` : 

```
show variables like 'slow_query_log_file';
```

3. Execute the following command at a terminal prompt to list non-compliant _`<slow_query_log_file>.*`_ file permissions: 

```
ls -l | egrep '^-(?![r|w]{2}-[r|w]{2}----
.*mysql\s*mysql).*<slow_query_log_file>.*$'
```

If the slow query log is enabled, lack of output implies compliance. 

If the slow query log is disabled, remove any old slow query log files. 

##### **Remediation:** 

Set slow query log to OFF (instead use `SYS` schema views or query `Performance_Schema` ) 

```
SET PERSIST slow_query_log = OFF;
```

If slow query is enabled, execute the following command to correct permissions and ownership: 

```
chmod 660 <log file>
chown mysql:mysql <log file>
```

##### **Default Value:** 

Slow query log is off by default. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/slow-query-log.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 90 

Internal Only - General 

_3.5 Ensure 'relay_log_basename' Files Have Appropriate Permissions (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

MySQL can operate using a variety of log files, each used for different purposes. These are the binary log (which can be encrypted), error log, slow query log, relay log (which can be encrypted), general log, and in the enterprise edition, the audit log (which can be encrypted). Because these are files on the host operating system, they are subject to the permissions and ownership structure provided by the host and may be accessible by users other than the MySQL user. Additionally, using secure key management and at rest MySQL encryption can further protect data from OS users. 

##### **Rationale:** 

Limiting the accessibility of these objects will protect the confidentiality, integrity, and availability of the MySQL logs. 

##### **Impact:** 

If the permissions on the relay logs and binary log files are accidentally changed to exclude the user account which is used to run the MySQL service, then this might break replication. 

The binary log file can be used for point in time recovery so this can also affect backup, restore and disaster recovery procedures. 

##### **Audit:** 

Perform the following steps to assess this recommendation: 

1. Execute the following SQL statement to determine the Value of `relay_log_basename` : 

```
show variables like 'relay_log_basename';
```

2. Execute the following command at a terminal prompt to list non-compliant _`<relay_log_basename>.*`_ file permissions: 

```
ls -l | egrep '^-(?![r|w]{2}-[r|w]{2}----
.*mysql\s*mysql).*<relay_log_basename>.*$'
```

Lack of output implies compliance. 

Page 91 

Internal Only - General 

##### **Remediation:** 

Execute the following command for each log file location requiring corrected permissions and ownership: 

```
chmod 660 <log file>
chown mysql:mysql <log file>
```

##### **Default Value:** 

_`<datadir>`_ + '/' + _`<hostname>`_ + '-relay-bin' 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 92 

Internal Only - General 

### _3.6 Ensure 'general_log_file' Has Appropriate Permissions (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

MySQL can operate using a variety of log files, each used for different purposes. These are the binary log (which can be encrypted), error log, slow query log, relay log (which can be encrypted), general log, and in the enterprise edition, the audit log (which can be encrypted). Because these are files on the host operating system, they are subject to the permissions and ownership structure provided by the host and may be accessible by users other than the MySQL user. Additionally, using secure key management and at rest MySQL encryption can further protect data from OS users. 

Much of the information about the state of MySQL exists in MySQL, the MySQL `performance_schema` or `informations_schema` . If you can get the information you need from within MySQL that is more secure as it does not require OS access. If you are not going to use log files it is best to first disable (don’t enable) and remove any prior logs. 

##### **Rationale:** 

Limiting the accessibility, or existence, of these log files will protect the confidentiality, integrity, and availability of the MySQL logs. 

##### **Impact:** 

Changing the permissions of the general log files may impact monitoring tools which use a log file adapter. 

##### **Audit:** 

Perform the following steps to assess this recommendation: 

1. Execute the following SQL statement to determine the Values of `general_log` and `general_log_file` : 

```
select @@general_log, @@general_log_file;
```

With a `general_log` value of `0` or `OFF` , indicates the log is disabled. If `1` or `ON` it is enabled. 

2. Whether the value is `0` , `OFF` , `1` or `ON` execute the following command at a terminal prompt to list non-compliant _`<general_log_file>.*`_ file permissions: 

```
ls -l <general_log_file>
```

Page 93 

Internal Only - General 

If `general_log` is `0` or `OFF` (disabled) and the log file exists, remove the old general log file. 

If `general_log` is `1` or `ON` (enabled) review the permissions 

```
ls -l <general_log_file>grep '^-rw-------.*mysql.*mysql'
```

Lack of output implies compliance. 

##### **Remediation:** 

If you can, use MySQL `SYS` , `PERFORMANCE_SCHEMA` , or MySQL Auditing as these are more secure options. 

By default the `general_log` is disabled ( `0` or `OFF` ). It's most secure to disable the `general_log` . 

To disable the `general_log_file` : 

```
SET PERSIST @@GENERAL_LOG=OFF;
```

If you must use `general_log` then assure the permissions are correct. Execute the following command for each log file location requiring corrected permissions and ownership: 

```
chmod 600 <general_log_file>
chown mysql:mysql <general_log_file>
```

##### **Default Value:** 

The variable `general_log` is set to `OFF` by default. The variable `general_log_file` is set to _`<host_name>`_ `.log` by default. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/query-log.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 94 

Internal Only - General 

### _3.7 Ensure SSL Key Files Have Appropriate Permissions (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

When configured to use SSL/TLS, MySQL relies on Secure Sockets Layer (SSL) key files, which are stored on the host's filesystem. These SSL key files are subject to the host's permissions and ownership structure. 

MySQL 8.0 provides ways to create the SSL certificate, SSL key files and RSA key-pair files required to support encrypted connections using SSL and secure password exchange using RSA over unencrypted connections, if those files are missing the server will attempt to autogenerate these files at startup if compiled with OpenSSL. 

##### **Rationale:** 

Limiting the accessibility of these objects will protect the confidentiality, integrity, and availability of the MySQL database and the communication with the client. 

If the contents of the SSL key file are known to an attacker, he or she might impersonate the server. This can be used for a man-in-the-middle attack. 

Depending on the SSL cipher suite, the key might also be used to decipher previously captured network traffic. 

##### **Impact:** 

If the permissions or ownership for the SSL key file are configured incorrectly, this can cause SSL to be disabled when MySQL is restarted or can cause MySQL not to start at all. 

If other applications are using the same key pair, then changing the permissions or ownership of the SSL key file will affect this application. If this were to occur a new key pair must be generated for MySQL. 

##### **Audit:** 

Perform the following steps to assess this recommendation: 

1. Locate the SSL keys and certs in use by executing the following SQL statement. To show all ssl variables: 

```
SELECT * FROM performance_schema.global_variables
WHERE
```

```
REGEXP_LIKE(VARIABLE_NAME,'^.*ssl_(ca|capath|cert|crl|crlpath|key)$')
AND VARIABLE_VALUE <> '';
```

Page 95 

Internal Only - General 

**Note:** Any `mysqlx_%` values that are null default to the classic protocols equivalent value. 

2. Execute the following commands at a terminal prompt to list non-compliant _`<ssl_file>`_ file permissions: 

```
ls -l <ssl_file> | egrep "^-(?!r-{8}.*mysql\s*mysql).*$"
```

Lack of output implies compliance 

##### **Remediation:** 

Execute the following commands at a terminal prompt to remediate these settings using the Value from the audit procedure: 

```
chown mysql:mysql <ssl_file>
chmod 400 <ssl_file>
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/encrypted-connections.html</u> 2. <u>https://dev.mysql.com/doc/refman/8.4/en/creating-ssl-rsa-files-using-mysql.html</u> 

##### **Additional Information:** 

If SSL is not configured this recommendation is not applicable. By default MySQL enables SSL. Using SSL is highly recommended. 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 96 

Internal Only - General 

### _3.8 Ensure Plugin Directory Has Appropriate Permissions (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The plugin directory is the location of the MySQL plugins. Plugins are storage engines or user defined functions (UDFs). 

##### **Rationale:** 

Limiting the accessibility of these objects will protect the confidentiality, integrity, and availability of the MySQL database. If someone can modify plugins then these plugins might be loaded when the server starts and the code will get executed. 

##### **Impact:** 

Users other than the MySQL user will no longer be able to update and add/remove plugins unless they're able to switch to the MySQL user. 

##### **Audit:** 

To assess this recommendation, execute the following SQL statement to discover the Value of `plugin_dir` : 

```
show variables where variable_name = 'plugin_dir';
```

Then, execute the following command at a terminal prompt (using the discovered `plugin_dir Value` ) to determine the permissions and ownership. 

```
ls -ld <plugin_dir Value> | grep "dr-xr-x---\|dr-xr-xr--" | grep "plugin"
```

Lack of output implies a fail. 

**Note:** Permissions are intended to be either `550` or `554` . 

##### **Remediation:** 

To remediate these settings, execute the following commands at a terminal prompt using the `plugin_dir Value` from the audit procedure. MySQL server must not be allowed to write to this location. 

```
chmod 550 <plugin_dir Value> #(or use 554)
chown mysql:mysql <plugin_dir Value>
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/install-plugin.html</u> 

Page 97 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 98 

Internal Only - General 

### **4 General** 

This section contains recommendations related to various parts of the database server. 

Page 99 

Internal Only - General 

- _4.1 Ensure the Latest Security Patches are Applied (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

Periodically, updates to MySQL server are released to resolve bugs, mitigate vulnerabilities, and provide new features. It is recommended that MySQL installations are up to date with the latest security updates. 

##### **Rationale:** 

Maintaining currency with MySQL patches will help reduce risk associated with known vulnerabilities present in the MySQL server. 

Without the latest security patches MySQL might have known vulnerabilities which could be used by an attacker to gain access. 

##### **Impact:** 

To update the MySQL server a restart is required. 

##### **Audit:** 

Execute the following SQL statement to identify the MySQL server version: 

```
SHOW VARIABLES WHERE Variable_name LIKE "version";
```

Now compare the version with the security announcements from Oracle and/or the OS if the OS packages are used. 

##### **Remediation:** 

Install the latest patches for your version or upgrade to the latest version. 

##### **References:** 

1. <u>http://www.oracle.com/technetwork/topics/security/alerts-086861.html</u> 

2. <u>http://dev.mysql.com/doc/relnotes/mysql/8.4/en/</u> 

3. <u>https://nvd.nist.gov/vuln/search/results?form_type=Advanced&results_type=over view&search_type=all&cpe_vendor=cpe%3A%2F%3Aoracle&cpe_product=cpe %3A%2F%3Aoracle%3Amysql&cpe_version=cpe%3A%2F%3Aoracle%3Amysql %3A8.0</u> 

Page 100 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|2.2Ensure Authorized Software is Currently Supported<br>Ensure that only currently supported software is designated as authorized in the<br>software inventory for enterprise assets. If software is unsupported, yet necessary<br>for the fulfillment of the enterprise’s mission, document an exception detailing<br>mitigating controls and residual risk acceptance. For any unsupported software<br>without an exception documentation, designate as unauthorized. Review the<br>software list to verify software support at least monthly, or more frequently.|●|●|●|
|v7|2.2Ensure Software is Supported by Vendor<br>Ensure that only software applications or operating systems currently supported<br>by the software's vendor are added to the organization's authorized software<br>inventory. Unsupported software should be tagged as unsupported in the inventory<br>system.|●|●|●|



Page 101 

Internal Only - General 

- _4.2 Ensure Example or Test Databases are Not Installed on Production Servers (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The default MySQL installation does not contain any example or test databases. However, it is a good idea to review for common example databases and ensure they have been removed from production systems. 

##### **Rationale:** 

Dropping example databases will reduce the attack surface of the MySQL server. 

##### **Audit:** 

Execute the following SQL statement to determine if the test database is present: 

```
SELECT * FROM information_schema.SCHEMATA where SCHEMA_NAME not in
('mysql','information_schema', 'sys', 'performance_schema');
```

If this is a production system, and a database name includes an example database this is a finding. 

Common example database names are: 

- employees 

- world 

- world_x 

- sakila 

- airportdb 

- menagerie 

##### **Remediation:** 

Execute the following SQL statement to drop an example database: 

```
DROP DATABASE <database name>;
```

##### **Default Value:** 

By default, MySQL 8.0 does not contain any example or test databases. 

##### **References:** 

1. <u>http://dev.mysql.com/doc/refman/8.4/en/mysql-secure-installation.html</u> 

Page 102 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|16.10Apply Secure Design Principles in Application<br>Architectures<br>Apply secure design principles in application architectures. Secure design<br>principles include the concept of least privilege and enforcing mediation to validate<br>every operation that the user makes, promoting the concept of "never trust user<br>input." Examples include ensuring that explicit error checking is performed and<br>documented for all input, including for size, data type, and acceptable ranges or<br>formats. Secure design also means minimizing the application infrastructure attack<br>surface, such as turning off unprotected ports and services, removing unnecessary<br>programs and files, and renaming or removing default accounts.||●|●|



Page 103 

Internal Only - General 

- _4.3 Ensure 'allow-suspicious-udfs' is Set to 'OFF' (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

This option prevents attaching arbitrary shared library functions as user-defined functions by checking for at least one corresponding method named `_init` , `_deinit` , `_reset` , `_clear` , or `_add` . 

##### **Rationale:** 

Preventing shared libraries that do not contain user-defined functions from loading will reduce the attack surface of the server. 

##### **Audit:** 

Perform the following to determine if the recommended state is in place: 

- Ensure `--allow-suspicious-udfs` is not specified in the the `mysqld` start up command line. 

- Ensure `allow-suspicious-udfs` is set to `OFF` in the MySQL configuration: 

```
my_print_defaults mysqld | grep allow-suspicious-udfs
```

No results returned is a pass. 

##### **Remediation:** 

Perform the following to establish the recommended state: 

- Remove `--allow-suspicious-udfs` from the `mysqld` start up command line. 

- • Remove `allow-suspicious-udfs` from the MySQL option file. 

##### **Default Value:** 

```
OFF
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/extending-mysql/8.4/en/adding-loadablefunction.html#loadable-function-security</u> 

2. <u>http://dev.mysql.com/doc/refman/8.4/en/serveroptions.html#option_mysqld_allow-suspicious-udfs</u> 

##### **Additional Information:** 

This option has no corresponding state in `SHOW VARIABLES` . 

Page 104 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|16.10Apply Secure Design Principles in Application<br>Architectures<br>Apply secure design principles in application architectures. Secure design<br>principles include the concept of least privilege and enforcing mediation to validate<br>every operation that the user makes, promoting the concept of "never trust user<br>input." Examples include ensuring that explicit error checking is performed and<br>documented for all input, including for size, data type, and acceptable ranges or<br>formats. Secure design also means minimizing the application infrastructure attack<br>surface, such as turning off unprotected ports and services, removing unnecessary<br>programs and files, and renaming or removing default accounts.||●|●|



Page 105 

Internal Only - General 

- _4.4 Harden Usage for 'local_infile' on MySQL Clients (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `local_infile` parameter dictates whether files located on the MySQL client's computer can be loaded or selected via `LOAD DATA INFILE` or `SELECT local_file` . 

##### **Rationale:** 

For MySQL client programs and connectors prior to 8.0.21, disabling `local_infile` reduces an attacker's ability to read sensitive files off the affected server via an SQL injection vulnerability. 

##### **Impact:** 

Disabling `local_infile` will impact the functionality of solutions that rely on it. 

##### **Audit:** 

Check the version of MySQL clients and connectors. For example: 

```
$ mysqlsh --version
$ mysql --version
```

The version should be 8.0.21 or higher. 

For connectors inspect the library in use. 

Most connectors provide functions which return version information. 

For C - `libmysqlclient` has: 

```
const char *mysql_get_client_info(void)
```

If clients have not been upgraded to 8.0.21 check the value of `local_infile` . 

Execute the following SQL statement: 

```
SHOW VARIABLES WHERE Variable_name = 'local_infile';
```

If clients are older than 8.0.21 or if `local_infile` is not in use, ensure the value returned is `0` . 

##### **Remediation:** 

Upgrade all MySQL clients and connectors to 8.0.21 or higher. 

In the case where using `local_infile` is needed, the following changes further harden security: 

Page 106 

Internal Only - General 

On client side, secure by: 

Limiting the location from where data can be read using `--load-data-local-dir` . 

```
mysql --local-infile=0 --load-data-local-dir=/my/local/data
```

Adding TLS connection to assure server identity by requiring verification. 

```
mysql --local-infile=0 --load-data-local-dir=/my/local/data --ssl-
mode=VERIFY_IDENTITY
```

If `local_infile` is not in use or if clients are not upgraded - add the following line to the `[mysqld]` section of the MySQL configuration file and restart the MySQL service: 

```
local-infile=0
```

##### **Default Value:** 

`0` (OFF) 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/string-functions.html#function_load-file</u> 2. <u>https://dev.mysql.com/doc/refman/8.4/en/load-data.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|4.8Uninstall or Disable Unnecessary Services on<br>Enterprise Assets and Software<br>Uninstall or disable unnecessary services on enterprise assets and software,<br>such as an unused file sharing service, web application module, or service<br>function.|●|●|
|v7|4.7Limit Access to Script Tools<br>Limit access to scripting tools (such as Microsoft PowerShell and Python) to<br>only administrative or development users with the need to access those<br>capabilities.|●|●|



Page 107 

Internal Only - General 

- _4.5 Ensure 'mysqld' is Not Started With '--skip-grant-tables' (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

This option causes `mysqld` to start without using the privilege system. 

##### **Rationale:** 

If this option is used, all clients of the affected server will have unrestricted access to all databases. 

##### **Audit:** 

Perform the following to determine if the recommended state is in place: 

- Open the MySQL configuration (e.g., `my.cnf` ) file and search for skip-granttables 

- Ensure `skip-grant-tables` is set to `FALSE` 

##### **Remediation:** 

Perform the following to establish the recommended state: 

- Open the MySQL configuration (e.g., `my.cnf` ) file and set: 

```
skip-grant-tables = FALSE
```

##### **References:** 

1. <u>http://dev.mysql.com/doc/refman/8.4/en/server-options.html#option_mysqld_skipgrant-tables</u> 

##### **Additional Information:** 

This option has no `SHOW VARIABLES` counterpart. 

Page 108 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 109 

Internal Only - General 

- _4.6 Ensure Symbolic Links are Disabled (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `symbolic-links` and `skip-symbolic-links` options for MySQL determine whether symbolic link support is available. When use of symbolic links is enabled, they have different effects depending on the host platform. When symbolic links are disabled, then symbolic links stored in files or entries in tables are not used by the database. 

##### **Rationale:** 

Prevents symbolic links from being used for database files. This is especially important when MySQL is executing as root as arbitrary files may be overwritten. The `symboliclinks` option might allow someone to direct actions by the MySQL server to other files and/or directories. 

##### **Audit:** 

Execute the following SQL statement to assess this recommendation: 

```
SHOW variables LIKE 'have_symlink';
```

Ensure the `Value` returned is `DISABLED` . 

##### **Remediation:** 

Perform the following actions to remediate this setting: 

- Open the MySQL configuration file ( `my.cnf` ) 

- Locate `skip-symbolic-links` in the configuration 

- • Set the `skip-symbolic-links` to `YES` 

**Note:** If `skip-symbolic-links` does not exist, add it to the configuration file in the `mysqld` section. 

##### **References:** 

1. <u>http://dev.mysql.com/doc/refman/8.4/en/symbolic-links.html</u> 

2. <u>http://dev.mysql.com/doc/refman/8.4/en/serveroptions.html#option_mysqld_symbolic-links</u> 

Page 110 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|16.10Apply Secure Design Principles in Application<br>Architectures<br>Apply secure design principles in application architectures. Secure design<br>principles include the concept of least privilege and enforcing mediation to validate<br>every operation that the user makes, promoting the concept of "never trust user<br>input." Examples include ensuring that explicit error checking is performed and<br>documented for all input, including for size, data type, and acceptable ranges or<br>formats. Secure design also means minimizing the application infrastructure attack<br>surface, such as turning off unprotected ports and services, removing unnecessary<br>programs and files, and renaming or removing default accounts.||●|●|
|v7|13Data Protection<br>Data Protection||||



Page 111 

Internal Only - General 

### _4.7 Ensure the 'secure_file_priv' is Configured Correctly (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `secure_file_priv` option restricts to paths used by `LOAD DATA INFILE` or `SELECT local_file` . It is recommended that this option be set to a file system location that contains only resources expected to be loaded by MySQL. Even better, if data import/export using `LOAD DATA INFILE` or `SELECT local_file` is not used, the functionality should be disabled entirely by setting `--secure-file-priv` to `NULL` . 

##### **Rationale:** 

Setting `secure_file_priv` reduces an attacker's ability to read sensitive files off the affected server via a SQL injection vulnerability. 

##### **Impact:** 

Solutions that rely on loading data from various sub-directories may be negatively impacted by this change. Consider consolidating load directories under a common parent directory. 

The server checks the value of `secure_file_priv` at startup and writes a warning to the error log if the value is insecure. A non-NULL value is considered insecure if it is empty, or the value is the data directory or a subdirectory of it, or a directory that is accessible by all users. 

##### **Audit:** 

Execute the following SQL statement and ensure one row is returned: 

```
SHOW GLOBAL VARIABLES WHERE Variable_name = 'secure_file_priv';
```

The Value should either contain `NULL` (thus is disabled entirely) or a valid path. If set to an empty string this is a fail. 

##### **Remediation:** 

If you are not going to use this feature, remove `secure_file_priv` from the `[mysqld]` section of the MySQL configuration file and restart the MySQL service. 

If you need this feature add the following line to the `[mysqld]` section of the MySQL configuration file and restart the MySQL service: 

```
secure_file_priv=<path_to_load_directory>
```

Page 112 

Internal Only - General 

##### **Default Value:** 

No value set. 

##### **References:** 

1. <u>http://dev.mysql.com/doc/refman/8.4/en/server-systemvariables.html#sysvar_secure_file_priv</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply<br>data access control lists, also known as access permissions, to local and remote<br>file systems, databases, and applications.|●|●|●|
|v7|13Data Protection<br>Data Protection||||



Page 113 

Internal Only - General 

### _4.8 Ensure 'sql_mode' Contains 'STRICT_ALL_TABLES' (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

When data changing statements are made (i.e., `INSERT` , `UPDATE` ), MySQL can handle invalid or missing values differently depending on whether strict SQL mode is enabled. When strict SQL mode is enabled, data may not be truncated or otherwise "adjusted" to make the data changing statement work. 

##### **Rationale:** 

Without strict mode the server tries to proceed with the action when an error might have been a more secure choice. For example, by default MySQL will truncate data if it does not fit in a field, which can lead to unknown behavior, or be leveraged by an attacker to circumvent data validation. 

##### **Impact:** 

Applications relying on the MySQL database should be aware that `STRICT_ALL_TABLES` is in use, such that error conditions are handled appropriately. 

##### **Audit:** 

To audit for this recommendation, execute the following query: 

```
SHOW VARIABLES LIKE 'sql_mode';
```

```
+---------------+-----------------------------------------------------------+
| Variable_name | Value                                                     |
+---------------+-----------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,   |
|               | NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,                  |
|               | NO_ENGINE_SUBSTITUTION                                    |
+---------------+-----------------------------------------------------------+
```

If `STRICT_ALL_TABLES` is not in the list returned, this is a fail. 

##### **Remediation:** 

Set `STRICT_ALL_TABLES` to the `sql_mode` in the server's global configuration, for example: 

```
SET GLOBAL sql_mode
='STRICT_ALL_TABLES,ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO
_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
```

Page 114 

Internal Only - General 

##### **Default Value:** 

```
ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ER
ROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
```

##### **References:** 

##### 1. <u>https://dev.mysql.com/doc/refman/8.4/en/sql-mode.html</u> 

##### **Additional Information:** 

The `sql_mode` is a set and might contain more elements than just `STRICT_ALL_TABLES` . 

There is a global `sql_mode` and a per session `sql_mode` . The per session `sql_mode` is based on the global `sql_mode` on initialization and might be changed by the application. 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|16.10Apply Secure Design Principles in Application<br>Architectures<br>Apply secure design principles in application architectures. Secure design<br>principles include the concept of least privilege and enforcing mediation to validate<br>every operation that the user makes, promoting the concept of "never trust user<br>input." Examples include ensuring that explicit error checking is performed and<br>documented for all input, including for size, data type, and acceptable ranges or<br>formats. Secure design also means minimizing the application infrastructure attack<br>surface, such as turning off unprotected ports and services, removing unnecessary<br>programs and files, and renaming or removing default accounts.|●|●|



Page 115 

Internal Only - General 

### _4.9 Use MySQL TDE for At-Rest Data Encryption (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

Transparent Data Encryption (TDE) at-rest encryption protects your critical data by enabling data-at-rest encryption in the database. It protects the privacy of your information, prevents data breaches and helps meet regulatory requirements. 

##### **Rationale:** 

File system based encryption does a good job of protecting against data theft on devices unable to limit physical access. It does not, however, protect against users who have or gain access to the operating system, backups, over the network copies, etc. Encrypting data from mysqld adds an additional layer of data protection. 

##### **Audit:** 

Check for the types of at-rest encryption enabled. 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_variables where
variable_name in ('audit_log_encryption', 'binlog_encryption',
'innodb_redo_log_encrypt', 'innodb_undo_log_encrypt',
'table_encryption_privilege_check');
```

`OFF` or `NONE` indicate at-rest encryption is not enabled. 

To check which tables or tablespaces are not encrypted 

```
SELECT
    INNODB_TABLESPACES.NAME,
    INNODB_TABLESPACES.ENCRYPTION
FROM information_schema.INNODB_TABLESPACES
WHERE NAME NOT IN ('innodb_temporary','sys/sys_config');
```

If any tables or tablespaces show encryption as `N` and are therefore not encrypted, this is a fail. 

Backup data should be encrypted at rest as well. If you are running the MySQL Enterprise Backup verify that the backup uses `--encrypt` . 

For example: 

```
$ mysqlbackup --defaults-file=/home/dbadmin/my.cnf --backup-
image=/home/admin/backups/my.mbi \
  --backup-dir=/home/admin/backup-tmp --encrypt-password backup-to-image
```

If `--encrypt-password` is not included the backup is not encrypted, this is a fail. 

Page 116 

Internal Only - General 

##### **Remediation:** 

Edit `my.cnf` : 

```
# AUDIT LOG
sudo vi /etc/my.cnf
[mysqld]
audit-log=FORCE_PLUS_PERMANENT
audit-log-format=JSON
audit-log-encryption=AES
```

Execute these commands: 

```
#### Table Encryption
>set persist table_encryption_privilege_check=ON;
#### BINLOG
>set persist binlog_encryption=ON;
##### REDO and UNDO
>set persist innodb_redo_log_encrypt=ON;
>set persist innodb_undo_log_encrypt=ON;
# DO NOT USE GENERAL LOG OR SLOW LOGS - USE AUDIT AND PERFORMANCE_SCHEMA.
>SET PERSIST general_log = 'OFF';
```

Run `ALTER` to enable encryption ( **Note:** This will lock the table as table is encrypted). 

```
# TABLESPACES, TABLES
ALTER TABLESPACE <tablespacename> ENCRYPTION = 'Y';
// if innodb file per table (indicated by schemaname/tablename in report)
ALTER TABLE <tablename> ENCRYPTION = 'Y';
#Encrypt the system tablespace
ALTER TABLESPACE mysql ENCRYPTION = 'Y';
```

Run MySQL Enterprise Backup with encryption. 

For example: 

```
$ mysqlbackup --defaults-file=/home/dbadmin/my.cnf --backup-
image=/home/admin/backups/my.mbi \
  --backup-dir=/home/admin/backup-tmp --encrypt-password backup-to-image
```

##### **Default Value:** 

At rest encryption is off by default. 

Administrators can force tables or tablespaces to be encrypted for all schemas by default by setting in `my.cnf` . 

```
default-table-encryption=ON
```

or Per schema by defining `DEFAULT ENCRYPTION` : 

```
CREATE {DATABASE | SCHEMA} ...
  | DEFAULT ENCRYPTION [=] {'Y' | 'N'}
```

Page 117 

Internal Only - General 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/innodb-data-encryption.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/server-systemvariables.html#sysvar_table_encryption_privilege_check</u> 

3. <u>https://dev.mysql.com/doc/refman/8.4/en/create-database.html</u> 

4. <u>https://dev.mysql.com/doc/refman/8.4/en/replication-binlog-encryption.html</u> 

5. <u>https://dev.mysql.com/doc/refman/8.4/en/audit-log-loggingconfiguration.html#audit-log-file-encryption</u> 

6. <u>https://dev.mysql.com/doc/mysql-enterprise-backup/8.4/en/meb-encryptedinnodb.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**<br>**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|3.11Encrypt Sensitive Data at Rest<br>Encrypt sensitive data at rest on servers, applications, and databases containing<br>sensitive data. Storage-layer encryption, also known as server-side encryption,<br>meets the minimum requirement of this Safeguard. Additional encryption methods<br>may include application-layer encryption, also known as client-side encryption,<br>where access to the data storage device(s) does not permit access to the plain-text<br>data.|●|●|
|v7|14.8Encrypt Sensitive Information at Rest<br>Encrypt all sensitive information at rest using a tool that requires a secondary<br>authentication mechanism not integrated into the operating system, in order to<br>access the information.||●|



Page 118 

Internal Only - General 

### **5 MySQL Permissions** 

This section contains recommendations about user privileges. 

Page 119 

Internal Only - General 

- _5.1 Ensure Only Administrative Users Have Full Database Access (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `mysql.user` , `mysql.db` , and other `mysql` tables ending in `_priv` list a variety of privileges that can be granted (or denied) to MySQL users. Some of the privileges of concern include: `Select_priv` , `Insert_priv` , `Update_priv` , `Delete_priv` , `Drop_priv` , and so on. Typically, these privileges should not be available to every MySQL user and often are reserved for administrative use only. The `information_schema.user_privileges` provides a consolidated view of all user privileges. 

##### **Rationale:** 

Limiting the accessibility of the `mysql` database will protect the confidentiality, integrity, and availability of the data housed within MySQL. A user which has direct access to `mysql.*` might view password hashes, change permissions, or alter or destroy information intentionally or unintentionally. 

##### **Audit:** 

Execute the following SQL statement(s) to assess this recommendation: 

```
select * from information_schema.user_privileges
where grantee not like ('\'mysql.%localhost\'');
```

Ensure all users returned are administrative users with minimal privileges required. 

The above query ignores MySQL internal `reserved accounts` . 

##### **Remediation:** 

Perform the following actions to remediate this setting: 

1. Enumerate non-administrative users resulting from the audit procedure. 

2. For each non-administrative user, use the `REVOKE` statement to remove privileges as appropriate. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/information-schema-user-privilegestable.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/reserved-accounts.html</u> 

Page 120 

Internal Only - General 

##### **Additional Information:** 

Consideration should be made for which privileges are required by each user requiring interactive database access. 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet browsing,<br>email, and productivity suite use, from the user’s primary, non-privileged account.|●|●|●|
|v7|4.1Maintain Inventory of Administrative Accounts<br>Use automated tools to inventory all administrative accounts, including domain<br>and local accounts, to ensure that only authorized individuals have elevated<br>privileges.||●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share, claims,<br>application, or database specific access control lists. These controls will enforce the<br>principle that only authorized individuals should have access to the information<br>based on their need to access the information as a part of their responsibilities.|●|●|●|



Page 121 

Internal Only - General 

- _5.2 Ensure 'FILE' is Not Granted to Non-Administrative Users (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `FILE` privilege is used to allow or disallow a user from reading and writing files on the server host. Any user with the `FILE` right granted has the ability to: 

- Read files from the local file system that are readable by the MySQL server (this includes world-readable files). 

- Write files to the local file system where the MySQL server has write access. 

##### **Rationale:** 

The `FILE` right allows MySQL users to read files from disk and to write files to disk. This may be leveraged by an attacker to further compromise MySQL. It should be noted that the MySQL server should not overwrite existing files. 

##### **Audit:** 

Execute the following SQL statement to audit this setting: 

```
SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES
WHERE PRIVILEGE_TYPE = 'FILE';
```

Ensure only administrative users are returned in the result set. 

##### **Remediation:** 

Perform the following steps to remediate this setting: 

1. Enumerate the non-administrative users found in the result set of the audit procedure. 

2. For each user, issue the following SQL statement (replace _`<user>`_ with the nonadministrative user): 

```
REVOKE FILE ON *.* FROM '<user>';
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#priv_file</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#privilegesprovided-summary</u> 

Page 122 

Internal Only - General 

##### **Additional Information:** 

##### See also: `secure_file_priv` system settings. 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet browsing,<br>email, and productivity suite use, from the user’s primary, non-privileged account.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 123 

Internal Only - General 

_5.3 Ensure 'PROCESS' is Not Granted to Non-Administrative Users (Manual)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

The `PROCESS` privilege found in the `mysql.user` table determines whether a given user can see statement execution information for all sessions. 

##### **Rationale:** 

The `PROCESS` privilege allows principals to view currently executing MySQL statements beyond their own, including statements used to manage passwords. This may be leveraged by an attacker to compromise MySQL or to gain access to potentially sensitive data. 

##### **Impact:** 

Users denied the `PROCESS` privilege may also be denied use of `SHOW ENGINE` . 

##### **Audit:** 

Execute the following SQL statement to audit this setting: 

```
SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES
WHERE PRIVILEGE_TYPE = 'PROCESS';
```

Ensure only administrative users are returned in the result set. 

##### **Remediation:** 

Perform the following steps to remediate this setting: 

1. Enumerate the non-administrative users found in the result set of the audit procedure 

2. For each user, issue the following SQL statement (replace _`<user>`_ with the nonadministrative user): 

```
REVOKE PROCESS ON *.* FROM '<user>';
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#priv_process</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#privilegesprovided-summary</u> 

Page 124 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet browsing,<br>email, and productivity suite use, from the user’s primary, non-privileged account.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 125 

Internal Only - General 

_5.4 Ensure 'SUPER' is Not Granted to Non-Administrative Users (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `SUPER` privilege is a powerful and far-reaching privilege and should not be granted lightly. In MySQL 8.0, `SUPER` is deprecated and will be removed in a future version of MySQL. 

The `SUPER` privilege shown in the `INFORMATION_SCHEMA.USER_PRIVILEGES` table governs the use of a variety of MySQL features. These features include, `CHANGE MASTER TO` , `KILL` , `mysqladmin kill` option, `PURGE BINARY LOGS` , `SET GLOBAL` , `mysqladmin debug` option, logging control, and more. 

In MySQL 8.0, `SUPER` is deprecated and will be removed in a future version of MySQL. Migrating Accounts from SUPER to Dynamic Privileges is recommended. 

##### **Rationale:** 

The `SUPER` privilege allows principals to perform many actions, including view and terminate currently executing MySQL statements (including statements used to manage passwords). This privilege also provides the ability to configure MySQL, such as enable/disable logging, alter data, disable/enable features. Limiting the accounts that have the `SUPER` privilege reduces the chances that an attacker can exploit these capabilities. 

It is more secure to migrate administrative users off `SUPER` and instead assign the specific and minimal set of mysql Dynamic Privileges needed to perform their tasks. 

##### **Impact:** 

When the `SUPER` privilege is denied to a given user, that user will be unable to take advantage of certain capabilities, such as certain `mysqladmin` options. 

##### **Audit:** 

Execute the following SQL statement to audit this setting: 

```
SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES
WHERE PRIVILEGE_TYPE = 'SUPER’;
```

Ensure only administrative users are returned in the result set. 

Page 126 

Internal Only - General 

##### **Remediation:** 

Perform the following steps to remediate this setting: 

1. Enumerate the non-administrative users found in the result set of the audit procedure 

2. For each user, issue the following SQL statement (replace _`<user>`_ with the nonadministrative user): 

```
REVOKE SUPER ON *.* FROM '<user>';
```

Next minimize administrator rights 

1. Assess the minimal set of Dynamic Permissions needed by a user to perform their duties. 

2. For each user assign the appropriate Dynamic Permission and then revoke that _`<user>`_ `SUPER` capability. 

For example, if administrator `'u1'@'localhost'` requires `SUPER` for binary log purging and system variable modification, these statements make the required changes to the account thus limiting rights to what is needed: 

```
GRANT BINLOG_ADMIN, SYSTEM_VARIABLES_ADMIN ON *.* TO
'u1'@'localhost';
REVOKE SUPER ON *.* FROM 'u1'@'localhost';
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#priv_super</u> 2. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#privilegesprovided-summary</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet browsing,<br>email, and productivity suite use, from the user’s primary, non-privileged account.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 127 

Internal Only - General 

_5.5 Ensure 'SHUTDOWN' is Not Granted to Non-Administrative Users (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `SHUTDOWN` privilege simply enables use of the `shutdown` option to the `mysqladmin` command, which allows a user with the `SHUTDOWN` privilege the ability to shut down the MySQL server. 

##### **Rationale:** 

The `SHUTDOWN` privilege allows principals to shutdown MySQL. This may be leveraged by an attacker to negatively impact the availability of MySQL. 

##### **Audit:** 

Execute the following SQL statement to audit this setting: 

```
SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES
WHERE PRIVILEGE_TYPE = 'SHUTDOWN';
```

Ensure only administrative users are returned in the result set. 

##### **Remediation:** 

Perform the following steps to remediate this setting: 

1. Enumerate the non-administrative users found in the result set of the audit procedure. 

2. For each user, issue the following SQL statement (replace _`<user>`_ with the nonadministrative user): 

```
REVOKE SHUTDOWN ON *.* FROM '<user>';
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#priv_shutdown</u> 2. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#privilegesprovided-summary</u> 

Page 128 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet browsing,<br>email, and productivity suite use, from the user’s primary, non-privileged account.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 129 

Internal Only - General 

_5.6 Ensure 'CREATE USER' is Not Granted to Non-Administrative Users (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `CREATE USER` privilege governs the right of a given user to add or remove users, change existing users' names, or revoke existing users' privileges. 

##### **Rationale:** 

Reducing the number of users granted the `CREATE USER` right minimizes the number of users able to add/drop users, alter existing users' names, and manipulate existing users' privileges. 

##### **Impact:** 

Users that are denied the `CREATE USER` privilege will not only be unable to create a user, but they may be unable to drop a user, rename a user, or otherwise revoke a given user's privileges. 

##### **Audit:** 

Execute the following SQL statement to audit this setting: 

```
SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES
WHERE PRIVILEGE_TYPE = 'CREATE USER';
```

Ensure only administrative users are returned in the result set. 

##### **Remediation:** 

Perform the following steps to remediate this setting: 

1. Enumerate the non-administrative users found in the result set of the audit procedure 

2. For each user, issue the following SQL statement (replace _`<user>`_ with the nonadministrative user): 

```
REVOKE CREATE USER ON *.* FROM '<user>';
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#priv_createuser</u> 

Page 130 

Internal Only - General 

##### 2. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#privilegesprovided-summary</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet browsing,<br>email, and productivity suite use, from the user’s primary, non-privileged account.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 131 

Internal Only - General 

- _5.7 Ensure 'GRANT OPTION' is Not Granted to NonAdministrative Users (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `GRANT OPTION` privilege exists in different contexts ( `mysql.user` , `mysql.db` ) for the purpose of governing the ability of a privileged user to manipulate the privileges of other users. 

##### **Rationale:** 

The `GRANT OPTION` privilege allows a principal to grant other principals additional privileges. This may be used by an attacker to compromise MySQL. 

##### **Audit:** 

Execute the following SQL statements to audit this setting: 

```
SELECT DISTINCT GRANTEE
FROM INFORMATION_SCHEMA.USER_PRIVILEGES
WHERE IS_GRANTABLE = 'YES';
```

Ensure only administrative users are returned in the result set. 

##### **Remediation:** 

Perform the following steps to remediate this setting: 

1. Enumerate the non-administrative users found in the result sets of the audit procedure 

2. For each user, issue the following SQL statement (replace _`<user>`_ with the nonadministrative user): 

```
REVOKE GRANT OPTION ON *.* FROM '<user>';
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#priv_grantoption</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#privilegesprovided-summary</u> 

Page 132 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet browsing,<br>email, and productivity suite use, from the user’s primary, non-privileged account.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 133 

Internal Only - General 

_5.8 Ensure 'REPLICATION SLAVE' is Not Granted to NonAdministrative Users (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `REPLICATION SLAVE` privilege governs whether a given user (in the context of the source server) can request updates that have been made on the source server. 

##### **Rationale:** 

The `REPLICATION SLAVE` privilege allows a principal to fetch `binlog` files containing all data changing statements and/or changes to table data from the source. This may be used by an attacker to read/fetch sensitive data from MySQL. 

##### **Audit:** 

Execute the following SQL statement to audit this setting: 

```
SELECT GRANTEE
FROM INFORMATION_SCHEMA.USER_PRIVILEGES
WHERE PRIVILEGE_TYPE = 'REPLICATION SLAVE';
```

Ensure only accounts designated for replica users are granted this privilege. 

##### **Remediation:** 

Perform the following steps to remediate this setting: 

1. Enumerate the non-replica users found in the result set of the audit procedure 

2. For each user, issue the following SQL statement (replace _`<user>`_ with the nonreplica user): 

```
REVOKE REPLICATION SLAVE ON *.* FROM '<user>';
```

Use the `REVOKE` statement to remove the `REPLICATION SLAVE` privilege from users who shouldn't have it. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/privilegesprovided.html#priv_replication-slave</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#privilegesprovided-summary</u> 

Page 134 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 135 

Internal Only - General 

_5.9 Ensure DML/DDL Grants are Limited to Specific Databases and Users (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

DML/DDL includes the set of privileges used to modify or create data structures. This includes `INSERT` , `SELECT` , `UPDATE` , `DELETE` , `DROP` , `CREATE` , and `ALTER` privileges. 

##### **Rationale:** 

`INSERT` , `SELECT` , `UPDATE` , `DELETE` , `DROP` , `CREATE` , and `ALTER` are powerful privileges in any database. Such privileges should be limited only to those users requiring such rights. By limiting the users with these rights and ensuring that they are limited to specific databases, the attack surface of the database is reduced. 

##### **Audit:** 

Execute the following SQL statement to audit this setting: 

```
SELECT User,Host,Db
FROM mysql.db
WHERE Select_priv='Y'
  OR Insert_priv='Y'
  OR Update_priv='Y'
  OR Delete_priv='Y'
  OR Create_priv='Y'
  OR Drop_priv='Y'
  OR Alter_priv='Y';
```

Ensure all users returned are permitted to have these privileges on the indicated databases. 

##### **Remediation:** 

Perform the following steps to remediate this setting: 

1. Enumerate the unauthorized users, hosts, and databases returned in the result set of the audit procedure 

2. For each user, issue the following SQL statement (replace _`<user>`_ with the unauthorized user, _`<host>`_ with host name, and _`<database>`_ with the database name): 

```
REVOKE SELECT ON <host>.<database> FROM <user>;
REVOKE INSERT ON <host>.<database> FROM <user>;
REVOKE UPDATE ON <host>.<database> FROM <user>;
```

Page 136 

Internal Only - General 

```
REVOKE DELETE ON <host>.<database> FROM <user>;
REVOKE CREATE ON <host>.<database> FROM <user>;
REVOKE DROP ON <host>.<database> FROM <user>;
REVOKE ALTER ON <host>.<database> FROM <user>;
```

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 137 

Internal Only - General 

- _5.10 Securely Define Stored Procedures and Functions DEFINER and INVOKER (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

Stored procedure and stored function declarations include a definition of permissions which can be used to escalate permissions. It's important to inspect these settings to ensure they do not unnecessarily escalate privileges. 

##### **Rationale:** 

A stored procedure or function that improperly escalates privileges may provide unintended access rights which can be improperly used. 

##### **Audit:** 

Run the following: 

```
SHOW PROCEDURE STATUS;
SHOW FUNCTION STATUS;
```

Inspect Definer and Invoker security types. 

If DEFINER is a powerful user consider that user's permissions. 

If INVOKER then the rights for the stored procedure or function are that of the user executing these. 

Review code using 

```
SHOW CREATE PROCEDURE <name>;
SHOW CREATE FUNCTION <name>;
```

For more details on Procedures and Functions 

```
SELECT * FROM information_schema.routines;
```

For more details on Procedures and Functions input and output parameters. 

```
SELECT * FROM information_schema.parameters;
```

##### **Remediation:** 

Drop and recreate stored procedures and functions using proper DEFINER and INVOKER settings, or other code changes. 

Page 138 

Internal Only - General 

##### **References:** 

##### 1. <u>https://dev.mysql.com/doc/refman/8.4/en/create-procedure.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|16.10Apply Secure Design Principles in Application<br>Architectures<br>Apply secure design principles in application architectures. Secure design<br>principles include the concept of least privilege and enforcing mediation to validate<br>every operation that the user makes, promoting the concept of "never trust user<br>input." Examples include ensuring that explicit error checking is performed and<br>documented for all input, including for size, data type, and acceptable ranges or<br>formats. Secure design also means minimizing the application infrastructure attack<br>surface, such as turning off unprotected ports and services, removing unnecessary<br>programs and files, and renaming or removing default accounts.||●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share, claims,<br>application, or database specific access control lists. These controls will enforce the<br>principle that only authorized individuals should have access to the information<br>based on their need to access the information as a part of their responsibilities.|●|●|●|



Page 139 

Internal Only - General 

- _5.11 Ensure Proper Use Of 'SET_ANY_DEFINER' (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

##### **Description:** 

Its critical to limit users ability to set and effective authorization ID that is used with executing a view or stored program. This grant provides a method to escalate privileges within MySQL views and procedures. A user with this privilege can specify any account as the `DEFINER` attribute for `CREATE PROCEDURE` , `CREATE FUNCTION` , `CREATE TRIGGER` , `CREATE EVENT` , `ALTER EVENT` , `CREATE VIEW` , and `ALTER VIEW` . Without this privilege, only the effective authentication ID can be specified. 

##### **Rationale:** 

Enabling a user to create a view, stored procedure or function that improperly escalates privileges may provide unintended access rights which can be improperly used. 

Side Note: The previous versions of MySQL users required a grant to `SET_USER_ID` privilege to create procedures with `DEFINER` set. 

##### **Audit:** 

Execute the following SQL statements to audit this setting: 

```
SELECT GRANTEE
FROM INFORMATION_SCHEMA.USER_PRIVILEGES
WHERE PRIVILEGE_TYPE = ‘SET_ANY_DEFINER’;
```

Ensure only administrative users are returned in the result set. 

##### **Remediation:** 

Perform the following steps to remediate this setting: 

1. Enumerate the non-administrative users found in the result set of the audit procedure 

2. For each user, issue the following SQL statement (replace with the nonadministrative user): 

```
REVOKE SET_ANY_DEFINER ON *.* FROM '<user>';\
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#priv_set-anydefiner</u> 

Page 140 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|16.10Apply Secure Design Principles in Application<br>Architectures<br>Apply secure design principles in application architectures. Secure design<br>principles include the concept of least privilege and enforcing mediation to validate<br>every operation that the user makes, promoting the concept of "never trust user<br>input." Examples include ensuring that explicit error checking is performed and<br>documented for all input, including for size, data type, and acceptable ranges or<br>formats. Secure design also means minimizing the application infrastructure attack<br>surface, such as turning off unprotected ports and services, removing unnecessary<br>programs and files, and renaming or removing default accounts.||●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share, claims,<br>application, or database specific access control lists. These controls will enforce the<br>principle that only authorized individuals should have access to the information<br>based on their need to access the information as a part of their responsibilities.|●|●|●|



Page 141 

Internal Only - General 

- _5.12 Ensure Proper Use Of ALLOW_NONEXISTENT_DEFINER (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

##### **Description:** 

Its critical to limit users ability to set and effective authorization ID that is used with executing a view or stored program. This grant provides a method to escalate privileges within MySQL views and procedures. A user with this privilege can specify an nonexisting account as the `DEFINER` attribute for `CREATE PROCEDURE` , `CREATE FUNCTION` , `CREATE TRIGGER` , `CREATE EVENT` , `ALTER EVENT` , `CREATE VIEW` , and `ALTER VIEW` . 

Later a user with escalated privileges could be created, providing unintended access rights which can be improperly used. 

This permission is often needed temporarily when performing database migration. Once a migration is complete this permission is typically no longer necessary and should be removed. 

##### **Rationale:** 

Enabling a user to create a view, stored procedure or function and later create a user that improperly escalates privileges may provide unintended access rights which can be improperly used. 

##### **Audit:** 

Execute the following SQL statements to audit this setting: 

```
SELECT GRANTEE
FROM INFORMATION_SCHEMA.USER_PRIVILEGES
WHERE PRIVILEGE_TYPE = ‘ALLOW_NONEXISTENT_DEFINER’;
```

Ensure only administrative users are returned in the result set. 

##### **Remediation:** 

Perform the following steps to remediate this setting: 

1. Enumerate the non-administrative users found in the result set of the audit procedure 

2. For each user, issue the following SQL statement (replace with the nonadministrative user): 

```
REVOKE ALLOW_NONEXISTENT_DEFINER ON *.* FROM '<user>';
```

Page 142 

Internal Only - General 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#priv_allownonexistent-definer</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|16.10Apply Secure Design Principles in Application<br>Architectures<br>Apply secure design principles in application architectures. Secure design<br>principles include the concept of least privilege and enforcing mediation to validate<br>every operation that the user makes, promoting the concept of "never trust user<br>input." Examples include ensuring that explicit error checking is performed and<br>documented for all input, including for size, data type, and acceptable ranges or<br>formats. Secure design also means minimizing the application infrastructure attack<br>surface, such as turning off unprotected ports and services, removing unnecessary<br>programs and files, and renaming or removing default accounts.||●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share, claims,<br>application, or database specific access control lists. These controls will enforce the<br>principle that only authorized individuals should have access to the information<br>based on their need to access the information as a part of their responsibilities.|●|●|●|



Page 143 

Internal Only - General 

### **6 Auditing and Logging** 

This section provides guidance with respect to MySQL's logging behavior. 

Page 144 

Internal Only - General 

### _6.1 Ensure 'log_error' is configured correctly (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The error log contains information about events such as `mysqld` starting and stopping, when a table needs to be checked or repaired, and, depending on the host operating system, stack traces when `mysqld` fails. 

##### **Rationale:** 

Enabling error logging can increase the ability to detect malicious attempts against MySQL, and other critical messages. For example, if the error log is not enabled then a connection error could go unnoticed. 

When configured to `stderr` MySQL will send log data to the console. Logging to the console is useful, but remember it is ephemeral. This is not recommended due to the fact that logging to console does not provide a means to force restricted access via permissions strictly to MySQL and dedicated MySQL audit accounts. This may compromise the confidentiality of the MySQL log data. Furthermore use caution if comingling log data from multiple sources as that can complicate log inspection. Additionally from a security auditing perspective, it’s difficult and error prone to verify logging is correct using `stderr` or redirected `stderr` . 

##### **Audit:** 

Execute the following SQL statement to audit this setting: 

```
SHOW variables LIKE 'log_error';
```

Ensure the `Value` returned is a path to a file and not `./stderr.err` . 

##### **Remediation:** 

Perform the following actions to remediate this setting: 

1. Open the MySQL configuration file ( `my.cnf` or `my.ini` ). 

2. Set the `log-error` option to the path for the error log. 

##### **Default Value:** 

```
./stderr.err
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/error-log.html</u> 

Page 145 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|8.2Collect Audit Logs<br>Collect audit logs. Ensure that logging, per the enterprise’s audit log<br>management process, has been enabled across enterprise assets.|●|●|●|
|v7|6.2Activate audit logging<br>Ensure that local logging has been enabled on all systems and networking<br>devices.|●|●|●|



Page 146 

Internal Only - General 

- _6.2 Ensure Log Files are Stored on a Non-System Partition (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

- Level 1 - MySQL RDBMS 

##### **Description:** 

MySQL log files can be set in the MySQL configuration to exist anywhere on the filesystem. It is common practice to ensure that the system filesystem is left uncluttered by application logs. System filesystems include the root ( `/` ), `/var` , or `/usr` . 

##### **Rationale:** 

Moving the MySQL logs off the system partition will reduce the probability of denial of service via the exhaustion of available disk space to the operating system. 

##### **Audit:** 

Execute the following SQL statement to assess this recommendation: 

```
SELECT @@global.log_bin_basename;
```

Ensure the value returned does not indicate root ( `/` ), `/var` , or `/usr` . 

##### **Remediation:** 

Perform the following actions to remediate this setting: 

1. Open the MySQL configuration file ( `my.cnf` ) 

2. Locate the `log-bin` entry and set it to a file not on root ( `/` ), `/var` , or `/usr` 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/binary-log.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/replication-options-binary-log.html</u> 

Page 147 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|8.3Ensure Adequate Audit Log Storage<br>Ensure that logging destinations maintain adequate storage to comply with<br>the enterprise’s audit log management process.|●|●|●|
|v7|6.4Ensure adequate storage for logs<br>Ensure that all systems that store logs have adequate storage space for the<br>logs generated.||●|●|



Page 148 

Internal Only - General 

- _6.3 Ensure 'log_error_verbosity' is Set to '2' (Automated)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

The `log_error_verbosity` system variable, set to `2` by default, specifies the verbosity of events sent to the MySQL error log. A value of `2` enables logging of error and warning messages, a value of `3` also includes informational logging, a value of `1` logs only errors. 

##### **Rationale:** 

This might help to detect malicious behavior by logging communication errors and aborted connections. 

##### **Audit:** 

Execute the following SQL statement to assess this recommendation: 

```
SHOW GLOBAL VARIABLES LIKE 'log_error_verbosity';
```

Ensure the `Value` returned equals `2` . 

##### **Remediation:** 

Perform the following actions to remediate this setting: 

- Open the MySQL configuration file ( `my.cnf` ) 

- Ensure the following line is found in the `mysqld` section 

```
log_error_verbosity = 2
```

##### **Default Value:** 

The option is enabled ( `2` ) - errors and warning events are logged - by default. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/server-systemvariables.html#sysvar_log_error_verbosity</u> 

Page 149 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|8.5Collect Detailed Audit Logs<br>Configure detailed audit logging for enterprise assets containing sensitive data.<br>Include event source, date, username, timestamp, source addresses, destination<br>addresses, and other useful elements that could assist in a forensic investigation.||●|●|
|v7|6.3Enable Detailed Logging<br>Enable system logging to include detailed information such as an event source,<br>date, user, timestamp, source addresses, destination addresses, and other useful<br>elements.||●|●|



Page 150 

Internal Only - General 

### _6.4 Ensure 'log-raw' is Set to 'OFF' (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `log-raw` MySQL option determines whether passwords are rewritten by the server so as not to appear in log files as plain text. If `log-raw` is enabled, then passwords are written to the various log files ( `general query log` , `slow query log` , and `binary log` ) in plain text. 

##### **Rationale:** 

With raw logging of passwords enabled someone with access to the log files might see plain text passwords. 

##### **Audit:** 

Perform the following actions to assess this recommendation: 

- Open the MySQL configuration file ( `my.cnf` ) 

- Ensure the `log-raw` entry is present 

- Ensure the `log-raw` entry is set to `OFF` 

##### **Remediation:** 

Perform the following actions to remediate this setting: 

- Open the MySQL configuration file ( `my.cnf` ) 

- • Find the `log-raw` entry and set it as follows 

```
log-raw = OFF
```

##### **Default Value:** 

```
OFF
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/password-logging.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/serveroptions.html#option_mysqld_log-raw</u> 

Page 151 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.5Securely Dispose of Data<br>Securely dispose of data as outlined in the enterprise’s data management<br>process. Ensure the disposal process and method are commensurate with the data<br>sensitivity.|●|●|●|
|v7|13.2Remove Sensitive Data or Systems Not Regularly<br>Accessed by Organization<br>Remove sensitive data or systems not regularly accessed by the organization<br>from the network. These systems shall only be used as stand alone systems<br>(disconnected from the network) by the business unit needing to occasionally use<br>the system or completely virtualized and powered off until needed.|●|●|●|



Page 152 

Internal Only - General 

### **7 Authentication** 

This section contains configuration recommendations that pertain to the authentication mechanisms of MySQL. 

Page 153 

Internal Only - General 

### _7.1 Ensure your authentication_policy is Set to a Secure Option (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

Define your authentication policy by setting the mysql system variable authentication_policy. 

The default value of authentication_policy is '*,,'. This means that factor 1 is required in account definitions and can use any authentication plugin (with caching_sha2_password being the default), and that factors 2 and 3 are optional and each can use any authentication plugin. 

Note the The default_authentication_plugin was deprecated in MySQL 8.0.27, and removed from 8.4. 

Use authentication_policy instead. The `–default-authentication-plugin` system variable governs two things: 

- Authentication plugin used by a new user account if a plugin is not specified explicitly through `CREATE USER` statement 

- Initial authentication data payload generated by server in case of a new connection. 

Caching SHA-2 Authentication is the default in MySQL 8.4. 

It provides stronger password protection than the prior Native Authentication and provides better performance than SHA2 Authentication. Alternatively, there are additional methods to securely connect using Lightweight Directory Access Protocol (LDAP) and Active Directory authentication. 

##### **Rationale:** 

MySQL Native Authentication relies on the Secure Hash Algorithm 1 (SHA1) algorithm and the National Institute of Standards and Technology (NIST) has suggested to stop using it. 

The MySQL Native Authentication plugin leverages this weak hashing algorithm that can be quickly brute forced. 

##### **Audit:** 

Execute the following SQL statement to assess this recommendation: 

Page 154 

Internal Only - General 

```
SHOW VARIABLES WHERE Variable_name = 'authentication_policy';
```

Ensure no field is not set to `mysql_native_password` . 

If specific authentication methods are required for accounts define the required authenticaiton plugin name within the string. 

##### **Remediation:** 

Assess the value of the system variable authentication_policy. If it is set to *,, This means the default policy is single factor using mysql caching_sha2 

Determine if any users are using `mysql_native_password` . 

```
select host, user, plugin from mysql.user;
```

Migrate these users from `mysql_native_password` . 

```
ALTER USER user
  IDENTIFIED WITH caching_sha2_password IDENTIFIED BY RANDOM PASSWORD
PASSWORD EXPIRE;
```

Provide users the random password value through a secure mechanism - on next login they will be forced to change the password. 

Set the policy to meet compliance requirements and to enhance security by defining specific authentication methods and the number of authentication factors required. 

<u>https://dev.mysql.com/doc/refman/8.4/en/server-systemvariables.html#sysvar_authentication_policy</u> 

##### **Default Value:** 

New users default to `caching_sha2_password` . Migrated users will initially be `mysql_native` or other authentication method. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/upgrading-from-previousseries.html#upgrade-caching-sha2-password-compatibility-issues</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/authentication-plugins.html</u> 

3. <u>https://dev.mysql.com/doc/refman/8.4/en/server-systemvariables.html#sysvar_authentication_policy</u> 

Page 155 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.11Encrypt Sensitive Data at Rest<br>Encrypt sensitive data at rest on servers, applications, and databases containing<br>sensitive data. Storage-layer encryption, also known as server-side encryption,<br>meets the minimum requirement of this Safeguard. Additional encryption methods<br>may include application-layer encryption, also known as client-side encryption,<br>where access to the data storage device(s) does not permit access to the plain-text<br>data.||●|●|
|v7|16.4Encrypt or Hash all Authentication Credentials<br>Encrypt or hash with a salt all authentication credentials when stored.||●|●|



Page 156 

Internal Only - General 

_7.2 Ensure Passwords are Not Stored in the Global Configuration (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `[client]` section of the MySQL configuration file allows setting a `user` and `password` to be used. Verify the `password` option is not used in the global configuration file ( `my.cnf` ). 

##### **Rationale:** 

Using the `password` parameter may negatively impact the confidentiality of the user's password. 

##### **Impact:** 

The global configuration is by default readable for all users on the system. This is needed for global defaults (prompt, port, socket, etc.). If a password is present in this file then all users on the system may be able to access it. 

##### **Audit:** 

To assess this recommendation, perform the following steps: 

- Open the MySQL configuration file (e.g., `my.cnf` ) 

- Examine the `[client]` section of the MySQL configuration file and ensure `password` is not employed. 

##### **Remediation:** 

Use the `mysql_config_editor` to store authentication credentials in `.mylogin.cnf` in encrypted form. 

If not possible, use the user-specific options file, `.my.cnf.` , and restricting file access permissions to the user identity. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/mysql-config-editor.html</u> 

##### **Additional Information:** 

There must not be a password in any of the sections of the global configuration. 

Page 157 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.11Encrypt Sensitive Data at Rest<br>Encrypt sensitive data at rest on servers, applications, and databases containing<br>sensitive data. Storage-layer encryption, also known as server-side encryption,<br>meets the minimum requirement of this Safeguard. Additional encryption methods<br>may include application-layer encryption, also known as client-side encryption,<br>where access to the data storage device(s) does not permit access to the plain-text<br>data.||●|●|
|v7|16.4Encrypt or Hash all Authentication Credentials<br>Encrypt or hash with a salt all authentication credentials when stored.||●|●|



Page 158 

Internal Only - General 

### _7.3 Ensure Passwords are Set for All MySQL Accounts (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

Blank passwords allow a user to login without using a password. 

##### **Rationale:** 

Without a password only knowing the username and the list of allowed hosts will allow someone to connect to the server and assume the identity of the user. This, in effect, bypasses authentication mechanisms. 

##### **Audit:** 

Execute the following SQL query to determine if any users have a blank password: 

```
SELECT User,host
FROM mysql.user
WHERE
(plugin='sha256_password' OR plugin='caching_sha2_password') AND
LENGTH(authentication_string) = 0;
UNION
SELECT User,host
FROM mysql.user
WHERE
(plugin IN('mysql_native_password', 'mysql_old_password','')
 AND (LENGTH(authentication_string) = 0
 OR authentication_string IS NULL));
```

No rows will be returned if all accounts have a password set. 

##### **Remediation:** 

For each row returned from the audit procedure, reset the password for the given user using the following statement (as an example): 

```
ALTER USER
<user>@<host> IDENTIFIED BY RANDOM PASSWORD PASSWORD EXPIRE;
```

This resets the password temporarily to a RANDOM string and returns that temporary password as a result. The user can then use this temporary password to login and is forced to set the password to one of their choosing upon login. 

**Note:** Replace _`<user>`_ , _`<host>`_ with appropriate values. 

Page 159 

Internal Only - General 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/assigning-passwords.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/validate-password-transitioning.html</u> 

3. <u>https://dev.mysql.com/doc/refman/8.4/en/validate-password.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.2Use Unique Passwords<br>Use unique passwords for all enterprise assets. Best practice implementation<br>includes, at a minimum, an 8-character password for accounts using MFA and a<br>14-character password for accounts not using MFA.|●|●|●|
|v7|4.4Use Unique Passwords<br>Where multi-factor authentication is not supported (such as local administrator,<br>root, or service accounts), accounts will use passwords that are unique to that<br>system.||●|●|



Page 160 

Internal Only - General 

_7.4 Set 'default_password_lifetime' to Require a Yearly Password Change (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

Password expiry provides passwords with a time bounded lifetime. 

##### **Rationale:** 

The `default_password_lifetime` global variable prevents a password being set for an indefinite period. Excessive password expiration requirements do more harm than good, because these requirements make users select predictable passwords, composed of sequential words and numbers that are closely related to each other. More importantly, when events occur that could compromise password security account passwords should be expired immediately. 

##### **Impact:** 

Scripted clients or users dependent on automated login in a controlled environment will need to consider their authentication procedures. The server will accept the user but the user is placed in restricted mode. In restricted mode, operations performed within the session result in an error until the user establishes a new account password. 

##### **Audit:** 

Execute the following SQL statements to assess this recommendation: 

```
SHOW VARIABLES LIKE 'default_password_lifetime';
```

The result should not be `0` and less than or equal to `365` . 

##### **Remediation:** 

To remediate this recommendation, execute the following command: 

```
SET GLOBAL default_password_lifetime=365;
```

##### **Default Value:** 

```
360
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/password-management.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/expired-password-handling.html</u> 

Page 161 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.3Disable Dormant Accounts<br>Delete or disable any dormant accounts after a period of 45 days of<br>inactivity, where supported.|●|●|●|
|v7|16.10Ensure All Accounts Have An Expiration Date<br>Ensure that all accounts have an expiration date that is monitored and<br>enforced.||●|●|



Page 162 

Internal Only - General 

### _7.5 Ensure Password Complexity Policies are in Place (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

- Level 1 - MySQL RDBMS 

##### **Description:** 

Password complexity includes password characteristics such as length, case, numerical, and character sets. 

##### **Rationale:** 

Complex passwords help mitigate dictionary, brute forcing, and other password attacks. This recommendation prevents users from choosing weak passwords which can easily be guessed. 

##### **Audit:** 

Execute the following to see if the password validation component is installed: 

```
select * from mysql.component where component_urn like '%validate_password';
```

If no rows are returned, this check fails. 

Execute the following SQL statements to assess this recommendation: 

```
SHOW VARIABLES LIKE 'validate_password%';
```

The result set from the above statement should show: 

- `validate_password.length` should be `14` or more 

- `validate_password.check_user_name` should be `ON` 

- `validate_password.policy` should be `STRONG` - checks length; numeric, lowercase/uppercase, and special characters; dictionary file 

New passwords should be checked against a dictionary file that contains values known to be commonly-used, expected, or compromised. For example, the list should include, but is not limited to: 

- Passwords obtained from previous breaches 

- Dictionary words 

- Repetitive or sequential characters (e.g., `aaaaaa` , `1234abcd` ) 

- Context-specific words, such as the name of the service, the username, and derivatives thereof 

- `validate_password.dictionary_file` should point to a dictionary file of common words used in passwords. 

Page 163 

Internal Only - General 

The following may make the password complexity too difficult, use sparingly. 

- `validate_password.mixed_case_count` not more than `1` 

- `validate_password.number_count` not more than `1` 

- `validate_password.special_char_count` not more than `1` 

##### **Remediation:** 

Install component_validate_password component: 

```
INSTALL COMPONENT 'file://component_validate_password';
```

Persist following configuration: 

```
SET PERSIST validate_password.length=14;
SET PERSIST validate_password.check_user_name=ON;
SET PERSIST validate_password.dictionary_file=<path to dictionary file>;
SET PERSIST validate_password.policy=STRONG;
```

Optionally set one or more of these - ensuring complexity is not overly onerous 

```
SET PERSIST validate_password.mixed_case_count=1;
SET PERSIST validate_password.number_count=1;
SET PERSIST validate_password.special_char_count=1;
```

And change passwords for users which have passwords which are identical to their username. 

##### **Default Value:** 

By default `component_validate_password` is not installed. 

```
validate_password.length=8
validate_password.mixed_case_count=1
validate_password.number_count=1
validate_password.policy=MEDIUM
validate_password.special_char_count=1
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/validate-password.html</u> 

##### **Additional Information:** 

The 'validate password plugin' can be used instead of the password validation component to enforce password complexity polices; however, it is deprecated and will be removed in a future release. 

Page 164 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.2Use Unique Passwords<br>Use unique passwords for all enterprise assets. Best practice implementation<br>includes, at a minimum, an 8-character password for accounts using MFA and a<br>14-character password for accounts not using MFA.|●|●|●|
|v7|4.4Use Unique Passwords<br>Where multi-factor authentication is not supported (such as local administrator,<br>root, or service accounts), accounts will use passwords that are unique to that<br>system.||●|●|



Page 165 

Internal Only - General 

- _7.6 Ensure No Users Have Wildcard Hostnames (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

MySQL can make use of host wildcards when granting permissions to users on specific databases. For example, you may grant a given privilege to `'` _`<user>`_ `'@'%'` . 

##### **Rationale:** 

Avoiding the use of wildcards within hostnames helps control the specific locations from which a given user may connect to and interact with the database. 

##### **Audit:** 

Execute the following SQL statement to assess this recommendation: 

```
SELECT user, host FROM mysql.user WHERE host = '%';
```

Ensure no rows are returned. 

##### **Remediation:** 

Perform the following actions to remediate this setting: 

1. Enumerate all users returned after running the audit procedure. 

2. Either `ALTER` the user's host to be specific or `DROP` the user. 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply data<br>access control lists, also known as access permissions, to local and remote file<br>systems, databases, and applications.|●|●|●|
|v7|14.6Protect Information through Access Control Lists<br>Protect all information stored on systems with file system, network share,<br>claims, application, or database specific access control lists. These controls will<br>enforce the principle that only authorized individuals should have access to the<br>information based on their need to access the information as a part of their<br>responsibilities.|●|●|●|



Page 166 

Internal Only - General 

- _7.7 Ensure No Anonymous Accounts Exist (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

Anonymous accounts are users with empty usernames (''). Anonymous accounts have no passwords, so anyone can use them to connect to the MySQL server. 

##### **Rationale:** 

Removing anonymous accounts will help ensure that only identified and trusted principals are capable of interacting with MySQL. 

##### **Impact:** 

Any applications relying on anonymous database access will be adversely affected by this change. 

##### **Audit:** 

Execute the following SQL query to identify anonymous accounts: 

```
SELECT user,host FROM mysql.user WHERE user = '';
```

The above query will return zero rows if no anonymous accounts are present. 

##### **Remediation:** 

Perform the following actions to remediate this setting: 

1. Enumerate the anonymous users returned from executing the audit procedure. 

2. For each anonymous user, `DROP` or assign them a name. 

**Note:** As an alternative, you may execute the `mysql_secure_installation` utility. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/mysql-secure-installation.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/default-privileges.html</u> 

3. <u>https://dev.mysql.com/doc/refman/8.4/en/proxy-users.html#proxy-users-conflicts</u> 

Page 167 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.1Establish and Maintain an Inventory of Accounts<br>Establish and maintain an inventory of all accounts managed in the enterprise.<br>The inventory must include both user and administrator accounts. The inventory, at<br>a minimum, should contain the person’s name, username, start/stop dates, and<br>department. Validate that all active accounts are authorized, on a recurring<br>schedule at a minimum quarterly, or more frequently.|●|●|●|
|v7|16.6Maintain an Inventory of Accounts<br>Maintain an inventory of all accounts organized by authentication system.||●|●|



Page 168 

Internal Only - General 

### **8 Network** 

This section contains recommendations related to how the MySQL server uses the network. 

Page 169 

Internal Only - General 

- _8.1 Ensure 'require_secure_transport' is Set to 'ON' (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

All network traffic must use SSL/TLS when traveling over untrusted networks. 

##### **Rationale:** 

Enabling Secure Sockets Layer (SSL) will allow clients to encrypt network traffic and verify the identity of the server. The SSL/TLS-protected MySQL protocol helps to prevent eavesdropping and man-in-the-middle attacks. 

##### **Impact:** 

Enabling SSL could have impact on network traffic inspection. 

##### **Audit:** 

Execute the following SQL statements to assess this recommendation: 

Check the global default. 

```
select @@require_secure_transport;
```

Ensure the returned `Value` is `ON` or `1` 

##### **Remediation:** 

Follow the procedures as documented in the MySQL 8.4 Reference Manual to setup SSL. 

Set global policy to force SSL for all connections: 

```
set persist require_secure_transport=ON;
```

##### **Default Value:** 

```
DISABLED
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/using-encrypted-connections.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/connection-options.html</u> 

3. <u>https://dev.mysql.com/doc/refman/8.4/en/server-systemvariables.html#sysvar_require_secure_transport</u> 

Page 170 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).||●|●|
|v7|14.4Encrypt All Sensitive Information in Transit<br>Encrypt all sensitive information in transit.||●|●|



Page 171 

Internal Only - General 

_8.2 Ensure 'ssl_type' is Set to 'ANY', 'X509', or 'SPECIFIED' for All Remote Users (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

All network traffic must use SSL/TLS when traveling over untrusted networks. 

SSL/TLS should be enforced on a per-user basis for users which enter the system through the network. 

##### **Rationale:** 

The SSL/TLS-protected MySQL protocol helps to prevent eavesdropping and man-inthe-middle attacks. 

##### **Impact:** 

When SSL/TLS is enforced then clients which do not use SSL will not be able to connect. If the server is not configured for SSL/TLS then accounts for which SSL/TLS is mandatory will not be able to connect. 

##### **Audit:** 

Execute the following SQL statements to assess this recommendation: 

```
SELECT user, host, ssl_type FROM mysql.user
WHERE NOT HOST IN ('::1', '127.0.0.1', 'localhost');
```

Ensure the `ssl_type` for each user returned is equal to `X509` , or `SPECIFIED` . 

**Note:** `ANY` means the connection must be using TLS and could optionally provide a client-side certificate. 

##### **Remediation:** 

Use the ALTER USER statement to require the use of SSL: 

```
ALTER USER 'my_user'@'app1.example.com' REQUIRE X509;
```

**Note:** `REQUIRE SSL` only enforces SSL. There are additional options `REQUIRE ISSUER` , `REQUIRE SUBJECT` which can be used to further restrict the connection. 

##### **Default Value:** 

On the server-side SSL is `ON` by default `--ssl` (permits but does not require secure connections) and `require_secure_transport` is `OFF` (turning `ON` allows only secure connections) 

Page 172 

Internal Only - General 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/using-encrypted-connections.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/alter-user.html#alter-user-tls</u> 

3. <u>https://dev.mysql.com/doc/refman/8.4/en/connectionoptions.html#option_general_ssl</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).|●|●|
|v7|14.4Encrypt All Sensitive Information in Transit<br>Encrypt all sensitive information in transit.|●|●|



Page 173 

Internal Only - General 

_8.3 Set Maximum Connection Limits for Server and per User (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

Limiting concurrent connections to a MySQL server can be used to reduce risk of Denial of Service (DoS) attacks performed by exhausting connection resources. 

##### **Rationale:** 

Limiting the number of concurrent sessions at the server and per user level helps to reduce the risk of DoS attacks. MySQL provides mechanisms to limit the number of simultaneous connections that can be made at the server level or by any given account. 

##### **Audit:** 

To check global (default) concurrent-sessions settings in the MySQL database server, to check the per user default run the query: 

```
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_variables
WHERE VARIABLE_NAME LIKE 'max_%connections';
```

If the value of `max_user_connections` is `0` this means there is “no limit”. 

If the value of `max_connections` is not set, there is no limit. 

Also check the values on a per user basis run the following: 

```
select user, host, max_user_connections from mysql.user where user not like
'mysql.%' and user not like 'root';
```

If the value is `0` this means the global value of `max_user_connections` applies. 

If no limits are configured this is a fail. 

##### **Remediation:** 

Connect to the MySQL Database as an administrator. 

For example, to set the global default per user to `50` run the command: 

```
SET PERSIST max_user_connections=50;
```

To control the maximum number of clients the server permits to connect simultaneously, set the `max_connections` system variable: 

```
SET PERSIST max_connections=1000;
```

Page 174 

Internal Only - General 

Additionally, this max user connections can be set per user as well as for a given period of time period using `CREATE` or `ALTER` . 

For example: 

```
ALTER USER 'fred'@'localhost'
WITH MAX_CONNECTIONS_PER_HOUR 5
MAX_USER_CONNECTIONS 2;
```

##### **Default Value:** 

The default value of `max_connections` is `151` , `max_user_connections` is `0` (unlimited, thus limited by `max_connections` ). 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/user-resources.html</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/connection-interfaces.html#connectioninterfaces-volume-management</u> 

Page 175 

Internal Only - General 

### **9 Replication** 

Everything related to replicating data from one server to another. 

Page 176 

Internal Only - General 

- _9.1 Ensure Replication Traffic is Secured (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS on Linux 

- Level 1 - MySQL RDBMS 

##### **Description:** 

The replication traffic between servers should be secured. Security measures should include ensuring the confidentiality and integrity of the traffic, and performing mutual authentication between the servers before performing replication. 

##### **Rationale:** 

The replication traffic should be secured as it gives access to all transferred information and might leak passwords. 

##### **Impact:** 

When the replication traffic is not secured someone might be able to capture passwords and other sensitive information when sent to the replica. 

##### **Audit:** 

Check if the replication traffic is using one or more of the following to provide confidentiality and integrity for the traffic, and mutual authentication for the servers: 

- A private network 

- A VPN 

- SSL/TLS 

- A SSH Tunnel 

##### **Remediation:** 

Secure the network traffic using one or more technologies to provide confidentiality and integrity for the traffic, and mutual authentication for the servers. 

Page 177 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).||●|●|
|v7|14.4Encrypt All Sensitive Information in Transit<br>Encrypt all sensitive information in transit.||●|●|



Page 178 

Internal Only - General 

_9.2 Ensure 'SOURCE_SSL_VERIFY_SERVER_CERT' is Set to 'YES' or '1' (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

In the MySQL `REPLICA` ( `SLAVE` is deprecated as of 8.0.22) context the setting `SOURCE_SSL_VERIFY_SERVER_CERT` ( `MASTER_SSL_VERIFY_SERVER_CERT` is deprecated as of 8.0.22) indicates whether the `REPLICA` should verify the `SOURCE` 's certificate. This configuration item may be set to `Yes` or `No` , and unless SSL has been enabled on the `REPLICA` , the value will be ignored. 

##### **Rationale:** 

When SSL is in use certificate verification is important to authenticate the party to which a connection is being made. In this case, the `REPLICA` (client) should verify the SOURCE's (server's) certificate to authenticate the `SOURCE` prior to continuing the connection. 

##### **Impact:** 

When using `CHANGE REPLICATION SOURCE TO` , ( `CHANGE MASTER` is deprecated as of 8.0.23) be aware of the following: 

- `REPLICA` processes need to be stopped prior to executing `CHANGE SOURCE TO` 

- • Use of `CHANGE REPLICATION SOURCE TO` starts new relay logs without keeping the old ones unless explicitly told to keep them 

- When `CHANGE REPLICATION SOURCE TO` is invoked, some information is dumped to the error log (previous values for `SOURCE_HOST` , `SOURCE_PORT` , `SOURCE_LOG_FILE` , and `SOURCE_LOG_POS` ) 

- Invoking `CHANGE REPLICATION SOURCE TO` will implicitly commit any ongoing transactions in the session where the `CHANGE REPLICATION SOURCE` was run, but not all ongoing transactions on the database. 

##### **Audit:** 

To assess this recommendation, issue the following statement: 

```
select ssl_verify_server_cert from mysql.slave_master_info;
```

Verify the value of `ssl_verify_server_cert` is `1` . 

Page 179 

Internal Only - General 

##### **Remediation:** 

To remediate this setting, you must use the `CHANGE SOURCE TO` command. 

##### From 8.0.23: 

```
STOP REPLICA; -- required if replication was already running
CHANGE REPLICATION SOURCE TO SOURCE_SSL_VERIFY_SERVER_CERT=1;
START REPLICA; -- required if you want to restart replication
```

##### Prior to 8.0.23: 

```
STOP SLAVE; -- required if replication was already running
CHANGE MASTER TO MASTER_SSL_VERIFY_SERVER_CERT=1;
START SLAVE; -- required if you want to restart replication
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/change-replication-source-to.html</u> 2. <u>https://dev.mysql.com/doc/refman/8.4/en/change-master-to.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|13.9Deploy Port-Level Access Control<br>Deploy port-level access control. Port-level access control utilizes 802.1x, or<br>similar network access control protocols, such as certificates, and may<br>incorporate user and/or device authentication.||●|



Page 180 

Internal Only - General 

_9.3 Ensure 'super_priv' is Not Set to 'Y' for Replication Users (Automated)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

The `SUPER` privilege found in the `mysql.user` table governs the use of a variety of MySQL features. These features include, `CHANGE MASTER TO` , `KILL` , `mysqladmin kill` option, `PURGE BINARY LOGS` , `SET GLOBAL` , `mysqladmin debug` option, logging control, and more. 

##### **Rationale:** 

The `SUPER` privilege allows principals to perform many actions, including view and terminate currently executing MySQL statements (including statements used to manage passwords). This privilege also provides the ability to configure MySQL, such as enable/disable logging, alter data, disable/enable features. Limiting the accounts that have the `SUPER` privilege reduces the chances that an attacker can exploit these capabilities. 

##### **Impact:** 

When the `SUPER` privilege is denied to a given user, that user will be unable to take advantage of certain capabilities, such as certain `mysqladmin` options. 

##### **Audit:** 

Execute the following SQL statement to audit this setting: 

```
select user, host from mysql.user where user='repl' and Super_priv = 'Y';
```

No rows should be returned. 

If you wish to validate permissions in more detail: 

|`select * from mysql.user where user='repl'\G`|
|---|



The following columns should return `Y` . 

|`*************************`|`** 1. row ***************************`|
|---|---|
|`Select_priv:`|`Y`|
|`Reload_priv:`|`Y`|
|`Shutdown_priv:`|`Y`|
|`Process_priv:`|`Y`|
|`File_priv:`|`Y`|
|`Grant_priv:`|`Y`|
|`Execute_priv:`|`Y`|
|`Repl_slave_priv:`|`Y`|



Page 181 

Internal Only - General 

```
        Repl_client_priv: Y
        Create_user_priv: Y
1 row in set (0.0007 sec)
```

Check Dynamic Privileges : 

```
select PRIV from mysql.global_grants where user like 'repl'\G
```

Expected results are: 

```
BACKUP_ADMIN
CLONE_ADMIN
PERSIST_RO_VARIABLES_ADMIN
REPLICATION_SLAVE_ADMIN
SYSTEM_VARIABLES_ADMIN
```

**Note:** Substitute your replication user's name for `repl` in the above queries. 

##### **Remediation:** 

Execute the following steps to remediate this setting: 

1. Enumerate the replication users found in the result set of the audit procedure 

2. For each replication user, issue the following SQL statement (replace `repl` with your replication user's name): 

```
REVOKE SUPER ON *.* FROM 'repl';
```

**Note:** Prior to 8.0.21 if MySQL Replica Set was used to create the replications administrator (call to `dba.configureReplicaSetInstance` in MySQL Shell) after performing the above revoke you will need to grant the following dynamic privilege. 

```
GRANT REPLICATION_SLAVE_ADMIN ON *.* TO `repl WITH GRANT OPTION;
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#priv_super</u> 2. <u>https://dev.mysql.com/doc/refman/8.4/en/deploying-innodb-replicasets.html</u> 

Page 182 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|5.4Restrict Administrator Privileges to Dedicated<br>Administrator Accounts<br>Restrict administrator privileges to dedicated administrator accounts on<br>enterprise assets. Conduct general computing activities, such as internet<br>browsing, email, and productivity suite use, from the user’s primary, non-privileged<br>account.|●|●|●|
|v7|4.7Limit Access to Script Tools<br>Limit access to scripting tools (such as Microsoft PowerShell and Python) to<br>only administrative or development users with the need to access those<br>capabilities.||●|●|



Page 183 

Internal Only - General 

### **10 MySQL InnoDB Cluster / Group Replication** 

MySQL InnoDB cluster provides a complete high availability solution for MySQL. MySQL Shell includes AdminAPI which enables you to easily configure and administer a group of at least three MySQL server instances to function as an InnoDB cluster. Each MySQL server instance runs MySQL Group Replication, which provides the mechanism to replicate data within InnoDB clusters, with built-in failover. AdminAPI removes the need to work directly with Group Replication in InnoDB clusters. 

Various things can be configured to enhance the security of MySQL InnoDB Cluster. 

Page 184 

Internal Only - General 

_10.1 Ensure All Group Replication Traffic is Secured (Manual)_ 

##### **Profile Applicability:** 

- Level 1 - MySQL RDBMS 

- Level 1 - MySQL RDBMS on Linux 

##### **Description:** 

MySQL Group communication connections and distributed recovery connections can be secured using SSL. 

##### **Rationale:** 

SSL encryption ensures data cannot be seen over the network for Group Replication. 

##### **Audit:** 

Using MySQL InnoDB Cluster admin api: Run shell 

```
mysql-js> var cluster = dba.getCluster()
mysql-js> cluster.status()
{
    "clusterName": "testCluster",
    "defaultReplicaSet": {
        "name": "default",
        "primary": "localhost:3320",
"ssl": "REQUIRED",
        "status": "OK",
```

`ssl` should **not** be `DISABLED` . 

Run the following statement from mysql client: 

```
select @@group_replication_ssl_mode;
```

If `DISABLED` communication is not secure it is a finding. 

`REQUIRED` , `VERIFY_CA` , or `VERIFY_IDENTITY` - indicate SSL is required. 

##### **Remediation:** 

Edit `my.cnf` and set `group_replication_ssl_mode` , for example: 

```
group_replication_ssl_mode=REQUIRED
```

Acceptable values are: 

- `REQUIRED` - Establish a secure connection if the server supports secure connections. 

- `VERIFY_CA` - Like `REQUIRED` , but additionally verify the server TLS certificate against the configured Certificate Authority (CA) certificates. 

Page 185 

Internal Only - General 

- `VERIFY_IDENTITY` - Like `VERIFY_CA` , but additionally verify that the server certificate matches the host to which the connection is being established. 

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/group-replication-secure-socket-layersupport-ssl.html</u> 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|
|v8|3.10Encrypt Sensitive Data in Transit<br>Encrypt sensitive data in transit. Example implementations can include:<br>Transport Layer Security (TLS) and Open Secure Shell (OpenSSH).|●|●|
|v7|14.4Encrypt All Sensitive Information in Transit<br>Encrypt all sensitive information in transit.|●|●|



Page 186 

Internal Only - General 

_10.2 Allowlist Approved Servers Belonging to a MySQL InnoDB Cluster (Manual)_ 

##### **Profile Applicability:** 

- Level 2 - MySQL RDBMS 

- Level 2 - MySQL RDBMS on Linux 

##### **Description:** 

Optionally, specify an allowlist of approved servers that belong to the MySQL InnoDB Cluster. 

##### **Rationale:** 

When using MySQL InnoDB Cluster by specifying the allowlist explicitly, you can increase the security of your cluster as only servers in the allowlist are allowed to connect to the cluster. 

##### **Audit:** 

Open MySQL Shell and execute the following command to create the allowlist of servers. This list is a comma separated list, surrounded by quotes. For example: 

```
select @@group_replication_ip_allowlist
```

The result set from the above statement should be the IPv4, IPv6, or host names allowed to join the MySQL InnoDB Cluster (Group). 

##### **Remediation:** 

Example - to configure a cluster to only accept connections from servers at addresses `203.0.113.0/24` and `198.51.100.110` . The whitelist can also include host names, which are resolved only when a connection request is made by another server. 

```
mysql-js> cluster.addInstance("icadmin@ic-3:3306", {ipAllowlist:
"203.0.113.0/24, 198.51.100.110"})
```

##### **References:** 

1. <u>https://dev.mysql.com/doc/refman/8.4/en/mysql-innodb-cluster-working-withcluster.html#mysql-innodb-cluster-securing</u> 

2. <u>https://dev.mysql.com/doc/refman/8.4/en/group-replication-ip-addresspermissions.html</u> 

Page 187 

Internal Only - General 

##### **CIS Controls:** 

|**Controls**<br>**Version**|**Control**|**IG 1**|<br>**IG 2**|<br>**IG 3**|
|---|---|---|---|---|
|v8|3.3Configure Data Access Control Lists<br>Configure data access control lists based on a user’s need to know. Apply<br>data access control lists, also known as access permissions, to local and remote<br>file systems, databases, and applications.|●|●|●|



Page 188 

Internal Only - General 

## **Appendix: Summary Table** 

||**CIS Benchmark Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|---|
|||Yes|No|
|**1**|**Operating System Level Configuration**|||
|1.1|Place Databases on Non-System Partitions (Manual)|||
|1.2|Use Dedicated Least Privileged Account for MySQL<br>Daemon/Service (Automated)|||
|1.3|Disable MySQL Command History (Automated)|||
|1.4|Verify That the MYSQL_PWD Environment Variable is<br>Not in Use (Automated)|||
|1.5|Ensure Interactive Login is Disabled (Automated)|||
|1.6|Verify That 'MYSQL_PWD' is Not Set in Users' Profiles<br>(Automated)|||
|1.7|Ensure MySQL is Run Under a Sandbox Environment<br>(Manual)|||
|**2**|**Installation and Planning**|||
|**2.1**|**Backup and Disaster Recovery**|||
|2.1.1|Backup Policy in Place (Manual)|||
|2.1.2|Verify Backups are Good (Manual)|||
|2.1.3|Secure Backup Credentials (Manual)|||
|2.1.4|Point-in-Time Recovery (Automated)|||
|2.1.5|Disaster Recovery (DR) Plan (Manual)|||
|2.1.6|Backup of Configuration and Related Files (Manual)|||
|**2.2**|**Data Encryption**|||



Page 189 

Internal Only - General 

||**CIS Benchmark Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|---|
|||Yes|No|
|2.2.1|Ensure Binary and Relay Logs are Encrypted<br>(Automated)|||
|2.3|Dedicate the Machine Running MySQL (Manual)|||
|2.4|Do Not Specify Passwords in the Command Line<br>(Manual)|||
|2.5|Do Not Reuse Usernames (Manual)|||
|2.6|Ensure Non-Default, Unique Cryptographic Material is in<br>Use (Manual)|||
|2.7|Ensure 'password_lifetime' is Less Than or Equal to '365'<br>(Automated)|||
|2.8|Ensure Password Resets Require Strong Passwords<br>(Automated)|||
|2.9|Require Current Password for Password Reset<br>(Automated)|||
|2.10|Use Dual Passwords to Enable Higher Frequency<br>Password Rotation (Manual)|||
|2.11|Lock Out Accounts if Not Currently in Use (Manual)|||
|2.12|Ensure AES Encryption Mode for<br>AES_ENCRYPT/AES_DECRYPT is Configured<br>Correctly (Automated)|||
|2.13|Ensure Socket Peer-Credential Authentication is Used<br>Appropriately (Manual)|||
|2.14|Ensure MySQL is Bound to an IP Address (Automated)|||
|2.15|Limit Accepted Transport Layer Security (TLS) Versions<br>(Automated)|||
|2.16|Require Client-Side Certificates (X.509) (Automated)|||
|2.17|Ensure Only Approved Ciphers are Used (Automated)|||



Page 190 

Internal Only - General 

||**CIS Benchmark Recommendation**|**S**<br>**Corr**<br>|**et**<br>**ectly**<br>|
|---|---|---|---|
|||Yes|No|
|2.18|Implement Connection Delays to Limit Failed Login<br>Attempts (Automated)|||
|2.19|Ensure FIPS 140-2 OpenSSL Cryptography Is Used<br>(Manual)|||
|**3**|**File Permissions**|||
|3.1|Ensure 'datadir' Has Appropriate Permissions<br>(Automated)|||
|3.2|Ensure 'log_bin_basename' Files Have Appropriate<br>Permissions (Automated)|||
|3.3|Ensure 'log_error' Has Appropriate Permissions<br>(Automated)|||
|3.4|Ensure 'slow_query_log' Has Appropriate Permissions<br>(Automated)|||
|3.5|Ensure 'relay_log_basename' Files Have Appropriate<br>Permissions (Automated)|||
|3.6|Ensure 'general_log_file' Has Appropriate Permissions<br>(Automated)|||
|3.7|Ensure SSL Key Files Have Appropriate Permissions<br>(Automated)|||
|3.8|Ensure Plugin Directory Has Appropriate Permissions<br>(Automated)|||
|**4**|**General**|||
|4.1|Ensure the Latest Security Patches are Applied (Manual)|||
|4.2|Ensure Example or Test Databases are Not Installed on<br>Production Servers (Automated)|||
|4.3|Ensure 'allow-suspicious-udfs' is Set to 'OFF'<br>(Automated)|||



Page 191 

Internal Only - General 

||**CIS Benchmark Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|---|
|||Yes|No|
|4.4|Harden Usage for 'local_infile' on MySQL Clients<br>(Automated)|||
|4.5|Ensure 'mysqld' is Not Started With '--skip-grant-tables'<br>(Automated)|||
|4.6|Ensure Symbolic Links are Disabled (Automated)|||
|4.7|Ensure the 'secure_file_priv' is Configured Correctly<br>(Automated)|||
|4.8|Ensure 'sql_mode' Contains 'STRICT_ALL_TABLES'<br>(Automated)|||
|4.9|Use MySQL TDE for At-Rest Data Encryption<br>(Automated)|||
|**5**|**MySQL Permissions**|||
|5.1|Ensure Only Administrative Users Have Full Database<br>Access (Manual)|||
|5.2|Ensure 'FILE' is Not Granted to Non-Administrative<br>Users (Manual)|||
|5.3|Ensure 'PROCESS' is Not Granted to Non-<br>Administrative Users (Manual)|||
|5.4|Ensure 'SUPER' is Not Granted to Non-Administrative<br>Users (Manual)|||
|5.5|Ensure 'SHUTDOWN' is Not Granted to Non-<br>Administrative Users (Manual)|||
|5.6|Ensure 'CREATE USER' is Not Granted to Non-<br>Administrative Users (Manual)|||
|5.7|Ensure 'GRANT OPTION' is Not Granted to Non-<br>Administrative Users (Manual)|||
|5.8|Ensure 'REPLICATION SLAVE' is Not Granted to Non-<br>Administrative Users (Manual)|||



Page 192 

Internal Only - General 

||**CIS Benchmark Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|---|
|||Yes|No|
|5.9|Ensure DML/DDL Grants are Limited to Specific<br>Databases and Users (Manual)|||
|5.10|Securely Define Stored Procedures and Functions<br>DEFINER and INVOKER (Manual)|||
|5.11|Ensure Proper Use Of 'SET_ANY_DEFINER' (Manual)|||
|5.12|Ensure Proper Use Of<br>ALLOW_NONEXISTENT_DEFINER (Manual)|||
|**6**|**Auditing and Logging**|||
|6.1|Ensure 'log_error' is configured correctly (Automated)|||
|6.2|Ensure Log Files are Stored on a Non-System Partition<br>(Automated)|||
|6.3|Ensure 'log_error_verbosity' is Set to '2' (Automated)|||
|6.4|Ensure 'log-raw' is Set to 'OFF' (Automated)|||
|**7**|**Authentication**|||
|7.1|Ensure your authentication_policy is Set to a Secure<br>Option (Automated)|||
|7.2|Ensure Passwords are Not Stored in the Global<br>Configuration (Automated)|||
|7.3|Ensure Passwords are Set for All MySQL Accounts<br>(Automated)|||
|7.4|Set 'default_password_lifetime' to Require a Yearly<br>Password Change (Automated)|||
|7.5|Ensure Password Complexity Policies are in Place<br>(Automated)|||
|7.6|Ensure No Users Have Wildcard Hostnames<br>(Automated)|||



Page 193 

Internal Only - General 

||**CIS Benchmark Recommendation**|**S**<br>**Corr**|**et**<br>**ectly**|
|---|---|---|---|
|||Yes|No|
|7.7|Ensure No Anonymous Accounts Exist (Automated)|||
|**8**|**Network**|||
|8.1|Ensure 'require_secure_transport' is Set to 'ON'<br>(Automated)|||
|8.2|Ensure 'ssl_type' is Set to 'ANY', 'X509', or 'SPECIFIED'<br>for All Remote Users (Automated)|||
|8.3|Set Maximum Connection Limits for Server and per User<br>(Manual)|||
|**9**|**Replication**|||
|9.1|Ensure Replication Traffic is Secured (Manual)|||
|9.2|Ensure 'SOURCE_SSL_VERIFY_SERVER_CERT' is<br>Set to 'YES' or '1' (Automated)|||
|9.3|Ensure 'super_priv' is Not Set to 'Y' for Replication Users<br>(Automated)|||
|**10**|**MySQL InnoDB Cluster / Group Replication**|||
|10.1|Ensure All Group Replication Traffic is Secured (Manual)|||
|10.2|Allowlist Approved Servers Belonging to a MySQL<br>InnoDB Cluster (Manual)|||



Page 194 

Internal Only - General 

## **Appendix: Change History** 

|**Date**|**Version**|**Changes for this version**|
|---|---|---|
|Apr 14, 2021|1.0.0|Least Priv MySQL Account should not<br>have shell access (Ticket 10283)|
|Apr 14, 2021|1.0.0|Fix links (Ticket 10284)|
|Apr 14, 2021|1.0.0|Typo in Description (Ticket 9912)|
|Apr 14, 2021|1.0.0|Why don't you use<br>'validate_password_check_user_name'?<br>(Ticket 9896)|
|Apr 14, 2021|1.0.0|Set to null if import/export not used.<br>(Ticket 10319)|
|Apr 14, 2021|1.0.0|Add detailed permissions guide to<br>reference (Ticket 10311)|
|Apr 14, 2021|1.0.0|permissions intended should be more<br>restrictive (Ticket 10315)|
|Apr 14, 2021|1.0.0|Add Section - Securely define Store<br>Procedures and Functions DEFINER<br>and SQL SECURITY clauses (Ticket<br>10385)|
|Apr 14, 2021|1.0.0|Binlog Strategy additional guidance<br>(Ticket 10289)|
|Apr 14, 2021|1.0.0|Enhance description - refer to new<br>versus old technology and product<br>names (Ticket 10291)|
|Apr 14, 2021|1.0.0|Add mysql-auto.cnf (.. where SET<br>PERSIST values go) (Ticket 10292)|
|Apr 14, 2021|1.0.0|Add MySQL Shell (Ticket 10285)|
|Apr 14, 2021|1.0.0|Add Section - Require current password<br>for password replacement (Ticket<br>10357)|



Page 195 

Internal Only - General 

|**Date**|**Version**|**Changes for this version**|
|---|---|---|
|Apr 14, 2021|1.0.0|Add section - Use dual password to<br>increase frequency of application<br>password rotation. (Ticket 10358)|
|Apr 14, 2021|1.0.0|If connection delays are enable monitor<br>(Ticket 10362)|
|Apr 14, 2021|1.0.0|Add section - limit host IP using bind<br>(Ticket 10363)|
|Apr 14, 2021|1.0.0|Require specific TLS versions (Ticket<br>10364)|
|Apr 14, 2021|1.0.0|Add Section on -  Enabling TDE<br>encryption (Ticket 10365)|
|Apr 14, 2021|1.0.0|Add to dual password audit the following<br>SQL (Ticket 10373)|
|Apr 14, 2021|1.0.0|Add section - Set Password Reuse<br>Policy (Ticket 10356)|
|Apr 14, 2021|1.0.0|Add section - Lock accounts if not in<br>current use. (Ticket 10359)|
|Apr 14, 2021|1.0.0|Add section - Implement Connection<br>Delays to defend against brute<br>authentication attacks (Ticket 10361)|
|Apr 14, 2021|1.0.0|Create Section - Timeout authentication<br>for interactive and non-interactive<br>sessions (Ticket 10383)|
|Apr 14, 2021|1.0.0|Add Section - Set Account Resource<br>Limits (Ticket 10384)|
|Apr 14, 2021|1.0.0|Add section - Ensure MySQL Cluster<br>requires SSL Mode (Ticket 10386)|
|Apr 14, 2021|1.0.0|Add Section - Optionally specify a<br>whitelist of approved servers that belong<br>to the MySQL InnoDB Cluster (Ticket<br>10393)|



Page 196 

Internal Only - General 

|**Date**|**Version**|**Changes for this version**|
|---|---|---|
|Apr 14, 2021|1.0.0|Change title and update content (Ticket<br>10323)|
|Apr 14, 2021|1.0.0|Should mention reserved users (new to<br>8.0) (Ticket 10294)|
|Apr 14, 2021|1.0.0|Shouldn't this be level 1? (Ticket 10295)|
|Apr 14, 2021|1.0.0|Not sufficient to just check location of<br>the data directory (Ticket 10282)|
|Apr 14, 2021|1.0.0|Update References (Ticket 10286)|
|Apr 14, 2021|1.0.0|Update Env Ref (Ticket 10287)|
|Apr 14, 2021|1.0.0|check require_secure_transport (Ticket<br>10327)|
|Apr 14, 2021|1.0.0|Need to rewrite this entirely.  Old and<br>dated. (Ticket 10312)|
|Apr 14, 2021|1.0.0|general_log_file should be off. (Ticket<br>10313)|
|Apr 14, 2021|1.0.0|Should show all files for ssl (Ticket<br>10314)|
|Apr 14, 2021|1.0.0|Add encryption to this (Ticket 10316)|
|Apr 14, 2021|1.0.0|keyring_file_data is not a best practice<br>(Ticket 10317)|
|Apr 14, 2021|1.0.0|Remove section - there is no test<br>database in 5.7 nor 8 (Ticket 10318)|
|Apr 14, 2021|1.0.0|In 8 super replaced by dynamic privy<br>(Ticket 10321)|
|Apr 14, 2021|1.0.0|No longer in 8.0 - remove section<br>Ensure 'secure_auth' is set to 'ON'<br>(Ticket 10324)|
|Apr 14, 2021|1.0.0|need to rewrite 6.5-6.7 - this is legacy<br>modes - too course grained etc. (Ticket<br>10322)|



Page 197 

Internal Only - General 

|**Date**|**Version**|**Changes for this version**|
|---|---|---|
|Apr 14, 2021|1.0.0|Remove section 'sql_mode' contains ...<br>not in 8 (Ticket 10325)|
|Apr 14, 2021|1.0.0|Consider a more comprehsive SQL<br>statement to audit admin privy (Ticket<br>10320)|
|Apr 14, 2021|1.0.0|Should Group Replication be added to<br>this section? (Ticket 10328)|
|Apr 14, 2021|1.0.0|Better to set global policy than per user.<br>(Ticket 10296)|
|Apr 14, 2021|1.0.0|MySQL Shell needs to be added (Ticket<br>10293)|
|Apr 14, 2021|1.0.0|MySQL Enterprise Backup (Ticket<br>10288)|
|Apr 14, 2021|1.0.0|First reference link is not existing (Ticket<br>12331)|
|Apr 14, 2021|1.0.0|MySQL 8.0 Benchmark Final Version<br>(Ticket 10405)|
|Jun 10, 2021|1.0.0|Typo in Default Value (Ticket 13100)|
|Jun 28, 2021|1.0.0|Rows returned by the regular<br>expression in the query will include<br>'ssl_cipher' (Ticket 12784)|
|Jul 1, 2021|1.0.0|validate password plugin is deprecated<br>(Ticket 12774)|
|Jul 1, 2021|1.0.0|There is no 'source_info_repository' in<br>8.0.23 (Ticket 13011)|
|Jul 2, 2021|1.0.0|Error in the remediation procedures<br>(Ticket 12997)|
|Jul 13, 2021|1.0.0|log_error can't be empty (Ticket 13288)|
|Jul 13, 2021|1.0.0|Internal users which are locked by<br>default should be excluded (Ticket<br>13289)|



Page 198 

Internal Only - General 

|**Date**|**Version**|**Changes for this version**|
|---|---|---|
|Jul 14, 2021|1.0.0|Map to Controls v8 (Ticket 13307)|
|Nov 3, 2021|1.0.0|Update artifact to include example<br>databases along with test (Ticket<br>14089)|
|Apr 28, 2022|1.0.0|Change 'FALSE' in the audit procedure<br>to 'OFF' (Ticket 14274)|
|May 4, 2022|1.0.0|Add recommendation to ensure MySQL<br>is run in Jail or Chroot. (Ticket 14254)|
|May 4, 2022|1.0.0|Delete duplicate recommendation for<br>password complexity (Ticket 13400)|
|May 4, 2022|1.0.0|Revise MySQL Permissions<br>recommendations to be similar to the<br>recommendation to limit the use of<br>'SUPER' (Ticket 14622)|
|May 6, 2022|1.0.0|Alter duplicate query suggestion 7.6<br>Ensure No Users Have Wildcard<br>Hostnames and 9.5 Ensure No<br>Replication Users Have Wildcard<br>Hostnames (Ticket 15104)|
|May 12, 2022|1.0.0|Closing quote in second Audit<br>procedure missing (Ticket 13699)|
|May 12, 2022|1.0.0|Typo in Description section (Ticket<br>13701)|
|Mar 29, 2023|1.0.0|Republished as v1.2.1 to address an<br>AAC bug.|
|Nov 25, 2024|1.0.0|ADD - Ensure Proper Use Of<br>'SET_ANY_DEFINER' (Ticket 23149)|
|Nov 25, 2024|1.0.0|Add - Ensure Proper Use Of<br>ALLOW_NONEXISTENT_DEFINER<br>(Ticket 23151)|
|Nov 25, 2024|1.0.0|Auditing plugin not available for<br>community edition (Ticket 23161)|



Page 199 

Internal Only - General 

|**Date**|**Version**|**Changes for this version**|
|---|---|---|
|Nov 25, 2024|1.0.0|Missing remediation for<br>table_encryption_privilege_check<br>(Ticket 23159)|
|Dec 6, 2024|1.0.0|ADD - Ensure FIPS 140-2 OpenSSL<br>Cryptography Is Used (Ticket 23304)|
|Oct 31, 2025|1.1.0|--default-authentication-plugin is no<br>longer available (Ticket 24065)|
|Oct 31, 2025|1.1.0|DELETE - 4.7 Ensure the<br>'daemon_memcached' Plugin is<br>Disabled (Ticket 25173)|
|Oct 31, 2025|1.1.0|'have_ssl' and 'have_openssl' no longer<br>used (Ticket 24082)|
|Oct 31, 2025|1.1.0|UPDATE - 2.19 Ensure FIPS 140-2<br>OpenSSL Cryptography Is Used (Ticket<br>25176)|
|Oct 31, 2025|1.1.0|Potential false negative in audit<br>procedure (Ticket 24064)|
|Oct 31, 2025|1.1.0|"master_info_repository" is now<br>removed from MySQL v8.4 and<br>hardening it is useless "9.3 Ensure<br>'master_info_repository' is Set to<br>'TABLE'" (Ticket 24007)|
|Oct 31, 2025|1.1.0|Artifact 3.7.2 - does not appear to be<br>prepending datadir string to relative<br>filepath (Ticket 21812)|



Page 200 

Internal Only - General 

