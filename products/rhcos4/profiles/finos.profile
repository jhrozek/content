documentation_complete: true

title: 'finos benchmark - for testing only'

metadata:
    SMEs:
        - jhrozek

reference: https://github.com/finos/compliant-financial-infrastructure/blob/dev/accelerators/kubernetes/ocp/sat_rh_ocp.adoc

title: 'OpenShift Security Configuration (Service Accelerator)'

description: |-
    OpenShift Security Configuration (Service Accelerator)

selections:
  ### Audit
  - service_auditd_enabled
  - var_auditd_flush=incremental_async
  - auditd_data_retention_flush
  - auditd_local_events
  - auditd_write_logs
  - auditd_log_format
  - auditd_freq
  - auditd_name_format
  - audit_rules_login_events_tallylog
  - audit_rules_login_events_faillock
  - audit_rules_login_events_lastlog
  - audit_rules_login_events
  - audit_rules_time_adjtimex
  - audit_rules_time_clock_settime
  - audit_rules_time_watch_localtime
  - audit_rules_time_settimeofday
  - audit_rules_time_stime
  - audit_rules_execution_restorecon
  - audit_rules_execution_chcon
  - audit_rules_execution_semanage
  - audit_rules_execution_setsebool
  - audit_rules_execution_setfiles
  - audit_rules_execution_seunshare
  - audit_rules_sysadmin_actions
  - audit_rules_networkconfig_modification
  - audit_rules_usergroup_modification
  - audit_rules_dac_modification_chmod
  - audit_rules_dac_modification_chown
  - audit_rules_kernel_module_loading_delete
  - audit_rules_kernel_module_loading_finit
  - audit_rules_kernel_module_loading_init


