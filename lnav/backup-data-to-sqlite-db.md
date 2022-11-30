# Backup lnav data to SQLite database

Open a log with `lnav`, preferably one that matches a [format](https://docs.lnav.org/en/latest/formats.html) (`syslog_log` in the example) so that some values have been parsed.

Then use the built-in SQLite interface (invoked using the `;` prefix) to attach to a database (which will be created if it doesn't exist), copy data into it, and detach.

```
;ATTACH '/tmp/lnav-backup.db' AS bkp;
;CREATE TABLE bkp.syslog_log AS SELECT * FROM syslog_log;
;DETACH DATABASE bkp;
```

In the example above, this will result in the following schema:

```sh
$ sqlite3 /tmp/lnav-backup.db .schema
CREATE TABLE syslog_log(
  log_line INT,
  log_part TEXT,
  log_time NUM,
  log_idle_msecs INT,
  log_level TEXT,
  log_mark NUM,
  log_comment TEXT,
  log_tags TEXT,
  log_filters TEXT,
  log_hostname TEXT,
  log_pid TEXT,
  log_procname TEXT,
  log_syslog_tag TEXT,
  log_msgid TEXT,
  log_pri INT,
  log_struct TEXT,
  syslog_version INT
);
```
