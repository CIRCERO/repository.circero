#!/bin/bash
#Setup vsftpd.conf
#You may use default configuration if you choose.
echo 'Setting up vsftpd'
cp /etc/vsftpd.conf /etc/vsftpd.conf-backup; rm -f /etc/vsftpd.conf; touch /etc/vsftpd.conf
echo 'listen=YES' >> /etc/vsftpd.conf
echo 'pasv_min_port=49152' >> /etc/vsftpd.conf
echo 'pasv_max_port=65535' >> /etc/vsftpd.conf
echo 'pasv_promiscuous=YES' >> /etc/vsftpd.conf
echo 'local_max_rate=0' >> /etc/vsftpd.conf
echo 'local_enable=YES' >> /etc/vsftpd.conf
echo 'write_enable=YES' >> /etc/vsftpd.conf
echo 'local_umask=077' >> /etc/vsftpd.conf
echo 'dirmessage_enable=YES' >> /etc/vsftpd.conf
echo 'use_localtime=YES' >> /etc/vsftpd.conf
echo 'xferlog_enable=YES' >> /etc/vsftpd.conf
echo 'connect_from_port_20=YES' >> /etc/vsftpd.conf
echo 'port_enable=NO' >> /etc/vsftpd.conf
echo 'chown_uploads=YES' >> /etc/vsftpd.conf
echo 'chown_username=xbmc' >> /etc/vsftpd.conf
echo 'ftpd_banner=Welcome to Kodi FTP Server' >> /etc/vsftpd.conf
echo 'chroot_local_user=NO' >> /etc/vsftpd.conf
echo 'secure_chroot_dir=/var/run/vsftpd/empty' >> /etc/vsftpd.conf
echo 'pam_service_name=vsftpd' >> /etc/vsftpd.conf
echo 'rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem' >> /etc/vsftpd.conf
echo 'async_abor_enable=YES' >> /etc/vsftpd.conf
echo 'anon_mkdir_write_enable=NO' >> /etc/vsftpd.conf
echo 'anon_other_write_enable=NO' >> /etc/vsftpd.conf
echo 'force_dot_files=YES' >> /etc/vsftpd.conf
echo 'tcp_wrappers=YES' >> /etc/vsftpd.conf
mkdir /home/vsftpd
touch /home/vsftpd/xferlog.log
touch /home/vsftpd/vsftpd.log
echo 'xferlog_file=/home/vsftpd/xferlog.log' >> /etc/vsftpd.conf
echo 'vsftpd_log_file=/home/vsftpd/vsftpd.log' >> /etc/vsftpd.conf
echo 'Setting up vsftpd, complete!'
restart vsftpd