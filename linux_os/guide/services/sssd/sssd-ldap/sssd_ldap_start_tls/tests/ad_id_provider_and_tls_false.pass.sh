#!/bin/bash
# profiles = xccdf_org.ssgproject.content_profile_stig

. $SHARED/setup_config_files.sh
setup_correct_sssd_config
sed -i 's/ldap_id_use_start_tls = True/ldap_id_use_start_tls = False/' /etc/sssd/sssd.conf
sed -i 's/id_provider = ldap/id_provider = ad/' /etc/sssd/sssd.conf
