#! /usr/bin/env python

import unittest

import responses

from obsversioncheck import get_operating_systems, get_link_to_project_repository, parse_repository, split_name_and_version


class ParseRepoInformationTestCase(unittest.TestCase):
    def test_getting_link_to_repo(self):
        self.assertEquals('http://download.opensuse.org/repositories/home:/uibmz:/opsi:/opsi40/',
                          get_link_to_project_repository('home:uibmz:opsi:opsi40'))

    @responses.activate
    def test_parsing_for_os(self):
        responses.add(responses.GET,
                      'http://download.opensuse.org/repositories/home:/uibmz:/opsi:/opsi40/',
                      body='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n <head>\n  <title>Index of /repositories/home:/uibmz:/opsi:/opsi40</title>\n  <link rel="stylesheet" href="http://static.opensuse.org/css/mirrorbrain.css" type="text/css" />\n </head>\n <body>\n<h1>Index of /repositories/home:/uibmz:/opsi:/opsi40</h1>\n<pre><img src="/icons/blank.gif" alt="Icon " /> <a href="?C=N;O=D">Name</a>                              <a href="?C=M;O=A">Last modified</a>      <a href="?C=S;O=A">Size</a>  <hr /><img src="/icons/up.png" alt="[DIR]" /> <a href="/repositories/home:/uibmz:/opsi:/">Parent Directory</a>                                       -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="CentOS_7/">CentOS_7/</a>                         11-Dec-2014 14:35    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="CentOS_CentOS-6/">CentOS_CentOS-6/</a>                  11-Dec-2014 14:33    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="Debian_6.0/">Debian_6.0/</a>                       11-Dec-2014 14:32    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="Debian_7.0/">Debian_7.0/</a>                       11-Dec-2014 14:32    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="RHEL_7/">RHEL_7/</a>                           11-Dec-2014 14:35    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="RedHat_RHEL-6/">RedHat_RHEL-6/</a>                    11-Dec-2014 14:35    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="SLE_11_SP3/">SLE_11_SP3/</a>                       23-Dec-2014 15:00    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="Univention_3.2/">Univention_3.2/</a>                   11-Dec-2014 14:36    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="openSUSE_12.3/">openSUSE_12.3/</a>                    11-Dec-2014 14:30    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="openSUSE_13.1/">openSUSE_13.1/</a>                    11-Dec-2014 14:35    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="ucs3.0/">ucs3.0/</a>                           11-Dec-2014 14:35    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="xUbuntu_10.04/">xUbuntu_10.04/</a>                    11-Dec-2014 14:33    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="xUbuntu_12.04/">xUbuntu_12.04/</a>                    11-Dec-2014 14:32    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="xUbuntu_14.04/">xUbuntu_14.04/</a>                    11-Dec-2014 14:33    -   \n<hr /></pre>\n<address>Apache/2.2.12 (Linux/SUSE) Server at download.opensuse.org Port 80</address>\n<br/><address><a href="http://mirrorbrain.org/">MirrorBrain</a> powered by <a href="http://httpd.apache.org/">Apache</a></address>\n</body></html>\n'
        )

        operating_systems = [os for os in get_operating_systems('home:uibmz:opsi:opsi40')]

        self.assertEquals(sorted(operating_systems),
                          ['CentOS_7', 'CentOS_CentOS-6', 'Debian_6.0',
                           'Debian_7.0', 'RHEL_7', 'RedHat_RHEL-6',
                            'SLE_11_SP3', 'Univention_3.2',
                            'openSUSE_12.3', 'openSUSE_13.1', 'ucs3.0',
                            'xUbuntu_10.04', 'xUbuntu_12.04', 'xUbuntu_14.04'])

    @responses.activate
    def test_parsing_repo(self):
        responses.add(responses.GET,
                      'http://download.opensuse.org/repositories/home:/uibmz:/opsi:/opsi40/CentOS_7',
                      body='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n <head>\n  <title>Index of /repositories/home:/uibmz:/opsi:/opsi40/CentOS_7</title>\n  <link rel="stylesheet" href="http://static.opensuse.org/css/mirrorbrain.css" type="text/css" />\n </head>\n <body>\n<h1>Index of /repositories/home:/uibmz:/opsi:/opsi40/CentOS_7</h1>\n<pre><img src="/icons/blank.gif" alt="Icon " /> <a href="?C=N;O=D">Name</a>                                     <a href="?C=M;O=A">Last modified</a>      <a href="?C=S;O=A">Size</a>  <hr /><img src="/icons/up.png" alt="[DIR]" /> <a href="/repositories/home:/uibmz:/opsi:/opsi40/">Parent Directory</a>                                              -   \n<img src="/icons/folder_red.png" alt="[   ]" /> <a href="./home:uibmz:opsi:opsi40.repo">home:uibmz:opsi:opsi40.repo</a>              11-Dec-2014 14:35  277    <a href="./home:uibmz:opsi:opsi40.repo.mirrorlist">Details</a>\n<img src="/icons/folder.png" alt="[DIR]" /> <a href="noarch/">noarch/</a>                                  11-Dec-2014 14:35    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="repodata/">repodata/</a>                                11-Dec-2014 14:35    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="src/">src/</a>                                     11-Dec-2014 14:35    -   \n<img src="/icons/folder.png" alt="[DIR]" /> <a href="x86_64/">x86_64/</a>                                  11-Dec-2014 00:29    -   \n<hr /></pre>\n<address>Apache/2.2.12 (Linux/SUSE) Server at download.opensuse.org Port 80</address>\n<br/><address><a href="http://mirrorbrain.org/">MirrorBrain</a> powered by <a href="http://httpd.apache.org/">Apache</a></address>\n</body></html>\n')
        responses.add(responses.GET,
                      'http://download.opensuse.org/repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/noarch/',
                      body='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n <head>\n  <title>Index of /repositories/home:/uibmz:/opsi:/opsi40/CentOS_7//noarch</title>\n  <link rel="stylesheet" href="http://static.opensuse.org/css/mirrorbrain.css" type="text/css" />\n </head>\n <body>\n<h1>Index of /repositories/home:/uibmz:/opsi:/opsi40/CentOS_7//noarch</h1>\n<pre><img src="/icons/blank.gif" alt="Icon " /> <a href="?C=N;O=D">Name</a>                                               <a href="?C=M;O=A">Last modified</a>      <a href="?C=S;O=A">Size</a>  <hr /><img src="/icons/up.png" alt="[DIR]" /> <a href="/repositories/home:/uibmz:/opsi:/opsi40/CentOS_7//">Parent Directory</a>                                                        -   \n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-configed-4.0.5.1.8-1.1.noarch.rpm">opsi-configed-4.0.5.1.8-1.1.noarch.rpm</a>             11-Dec-2014 14:31  2.7M   <a href="opsi-configed-4.0.5.1.8-1.1.noarch.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-depotserver-4.0.5.11-1.2.noarch.rpm">opsi-depotserver-4.0.5.11-1.2.noarch.rpm</a>           14-Nov-2014 18:27   27K   <a href="opsi-depotserver-4.0.5.11-1.2.noarch.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-linux-bootimage-20140919-2.2.noarch.rpm">opsi-linux-bootimage-20140919-2.2.noarch.rpm</a>       14-Nov-2014 18:35  181M   <a href="opsi-linux-bootimage-20140919-2.2.noarch.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-nagios-plugins-4.0.2.1-3.2.noarch.rpm">opsi-nagios-plugins-4.0.2.1-3.2.noarch.rpm</a>         14-Nov-2014 18:41  6.0K   <a href="opsi-nagios-plugins-4.0.2.1-3.2.noarch.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-utils-4.0.5.6-2.2.noarch.rpm">opsi-utils-4.0.5.6-2.2.noarch.rpm</a>                  14-Nov-2014 18:52   66K   <a href="opsi-utils-4.0.5.6-2.2.noarch.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsiconfd-4.0.5.2-1.2.noarch.rpm">opsiconfd-4.0.5.2-1.2.noarch.rpm</a>                   14-Nov-2014 18:46   91K   <a href="opsiconfd-4.0.5.2-1.2.noarch.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsipxeconfd-4.0.5.3-6.2.noarch.rpm">opsipxeconfd-4.0.5.3-6.2.noarch.rpm</a>                14-Nov-2014 18:56   16K   <a href="opsipxeconfd-4.0.5.3-6.2.noarch.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-opsi-4.0.5.15-1.2.noarch.rpm">python-opsi-4.0.5.15-1.2.noarch.rpm</a>                14-Nov-2014 19:17  1.4M   <a href="python-opsi-4.0.5.15-1.2.noarch.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-pexpect-3.1-11.2.noarch.rpm">python-pexpect-3.1-11.2.noarch.rpm</a>                 14-Nov-2014 17:45  113K   <a href="python-pexpect-3.1-11.2.noarch.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-serial-2.4-11.2.noarch.rpm">python-serial-2.4-11.2.noarch.rpm</a>                  14-Nov-2014 19:30   61K   <a href="python-serial-2.4-11.2.noarch.rpm.mirrorlist">Details</a>\n<hr /></pre>\n<address>Apache/2.2.12 (Linux/SUSE) Server at download.opensuse.org Port 80</address>\n<br/><address><a href="http://mirrorbrain.org/">MirrorBrain</a> powered by <a href="http://httpd.apache.org/">Apache</a></address>\n</body></html>\n')
        responses.add(responses.GET,
                      'http://download.opensuse.org/repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/repodata/',
                      body='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n <head>\n  <title>Index of /repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/repodata</title>\n  <link rel="stylesheet" href="http://static.opensuse.org/css/mirrorbrain.css" type="text/css" />\n </head>\n <body>\n<h1>Index of /repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/repodata</h1>\n<pre><img src="/icons/blank.gif" alt="Icon " /> <a href="?C=N;O=D">Name</a>                                              <a href="?C=M;O=A">Last modified</a>      <a href="?C=S;O=A">Size</a>  <hr /><img src="/icons/up.png" alt="[DIR]" /> <a href="/repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/">Parent Directory</a>                                                       -   \n<img src="/icons/tgz.png" alt="[   ]" /> <a href="filelists.xml.gz">filelists.xml.gz</a>                                  11-Dec-2014 14:35   34K   <a href="filelists.xml.gz.mirrorlist">Details</a>\n<img src="/icons/tgz.png" alt="[   ]" /> <a href="other.xml.gz">other.xml.gz</a>                                      11-Dec-2014 14:35   18K   <a href="other.xml.gz.mirrorlist">Details</a>\n<img src="/icons/tgz.png" alt="[   ]" /> <a href="primary.xml.gz">primary.xml.gz</a>                                    11-Dec-2014 14:35   13K   <a href="primary.xml.gz.mirrorlist">Details</a>\n<img src="/icons/document.png" alt="[TXT]" /> <a href="repomd.xml">repomd.xml</a>                                        11-Dec-2014 14:35  1.2K   <a href="repomd.xml.mirrorlist">Details</a>\n<img src="/icons/encrypted.png" alt="[   ]" /> <a href="repomd.xml.asc">repomd.xml.asc</a>                                    11-Dec-2014 14:35  189    <a href="repomd.xml.asc.mirrorlist">Details</a>\n<img src="/icons/unknown.png" alt="[   ]" /> <a href="repomd.xml.key">repomd.xml.key</a>                                    11-Dec-2014 14:35  1.0K   <a href="repomd.xml.key.mirrorlist">Details</a>\n<hr /></pre>\n<address>Apache/2.2.12 (Linux/SUSE) Server at download.opensuse.org Port 80</address>\n<br/><address><a href="http://mirrorbrain.org/">MirrorBrain</a> powered by <a href="http://httpd.apache.org/">Apache</a></address>\n</body></html>\n')
        responses.add(responses.GET,
                      'http://download.opensuse.org/repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/src/',
                      body='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n <head>\n  <title>Index of /repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/src</title>\n  <link rel="stylesheet" href="http://static.opensuse.org/css/mirrorbrain.css" type="text/css" />\n </head>\n <body>\n<h1>Index of /repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/src</h1>\n<pre><img src="/icons/blank.gif" alt="Icon " /> <a href="?C=N;O=D">Name</a>                                              <a href="?C=M;O=A">Last modified</a>      <a href="?C=S;O=A">Size</a>  <hr /><img src="/icons/up.png" alt="[DIR]" /> <a href="/repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/">Parent Directory</a>                                                       -   \n<img src="/icons/rpm.png" alt="[   ]" /> <a href="duplicity-0.6.08b-11.2.src.rpm">duplicity-0.6.08b-11.2.src.rpm</a>                    14-Nov-2014 19:32  223K   <a href="duplicity-0.6.08b-11.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="fdupes-1.50-14.1.src.rpm">fdupes-1.50-14.1.src.rpm</a>                          11-Dec-2014 00:00   37K   <a href="fdupes-1.50-14.1.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="librsync-0.9.7-175.2.src.rpm">librsync-0.9.7-175.2.src.rpm</a>                      14-Nov-2014 17:46  339K   <a href="librsync-0.9.7-175.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="lshw-B.02.17-1.2.src.rpm">lshw-B.02.17-1.2.src.rpm</a>                          14-Nov-2014 17:46  1.9M   <a href="lshw-B.02.17-1.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-atftp-0.7.dfsg-11.2.src.rpm">opsi-atftp-0.7.dfsg-11.2.src.rpm</a>                  14-Nov-2014 17:53  875K   <a href="opsi-atftp-0.7.dfsg-11.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-configed-4.0.5.1.8-1.1.src.rpm">opsi-configed-4.0.5.1.8-1.1.src.rpm</a>               11-Dec-2014 14:31  4.9M   <a href="opsi-configed-4.0.5.1.8-1.1.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-depotserver-4.0.5.11-1.2.src.rpm">opsi-depotserver-4.0.5.11-1.2.src.rpm</a>             14-Nov-2014 18:27   34K   <a href="opsi-depotserver-4.0.5.11-1.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-linux-bootimage-20140919-2.2.src.rpm">opsi-linux-bootimage-20140919-2.2.src.rpm</a>         14-Nov-2014 18:35  181M   <a href="opsi-linux-bootimage-20140919-2.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-nagios-plugins-4.0.2.1-3.2.src.rpm">opsi-nagios-plugins-4.0.2.1-3.2.src.rpm</a>           14-Nov-2014 18:41  7.3K   <a href="opsi-nagios-plugins-4.0.2.1-3.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-utils-4.0.5.6-2.2.src.rpm">opsi-utils-4.0.5.6-2.2.src.rpm</a>                    14-Nov-2014 18:52   84K   <a href="opsi-utils-4.0.5.6-2.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsiconfd-4.0.5.2-1.2.src.rpm">opsiconfd-4.0.5.2-1.2.src.rpm</a>                     14-Nov-2014 18:46   58K   <a href="opsiconfd-4.0.5.2-1.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsipxeconfd-4.0.5.3-6.2.src.rpm">opsipxeconfd-4.0.5.3-6.2.src.rpm</a>                  14-Nov-2014 18:56   19K   <a href="opsipxeconfd-4.0.5.3-6.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="p7zip-9.20.1-4.2.src.rpm">p7zip-9.20.1-4.2.src.rpm</a>                          14-Nov-2014 19:01  3.7M   <a href="p7zip-9.20.1-4.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-GnuPG-Interface-0.3.2-4.2.src.rpm">python-GnuPG-Interface-0.3.2-4.2.src.rpm</a>          14-Nov-2014 19:10   22K   <a href="python-GnuPG-Interface-0.3.2-4.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-SQLAlchemy-0.7.7-32.1.src.rpm">python-SQLAlchemy-0.7.7-32.1.src.rpm</a>              17-Nov-2014 10:15  2.5M   <a href="python-SQLAlchemy-0.7.7-32.1.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-Twisted-12.0.0-24.2.src.rpm">python-Twisted-12.0.0-24.2.src.rpm</a>                14-Nov-2014 19:37  2.7M   <a href="python-Twisted-12.0.0-24.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-ldaptor-0.0.43-16.1.src.rpm">python-ldaptor-0.0.43-16.1.src.rpm</a>                17-Nov-2014 10:08  384K   <a href="python-ldaptor-0.0.43-16.1.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-mysql-1.2.2-98.2.src.rpm">python-mysql-1.2.2-98.2.src.rpm</a>                   14-Nov-2014 19:05   81K   <a href="python-mysql-1.2.2-98.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-opsi-4.0.5.15-1.2.src.rpm">python-opsi-4.0.5.15-1.2.src.rpm</a>                  14-Nov-2014 19:17  701K   <a href="python-opsi-4.0.5.15-1.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-pam-0.5.0-4.2.src.rpm">python-pam-0.5.0-4.2.src.rpm</a>                      14-Nov-2014 17:46   23K   <a href="python-pam-0.5.0-4.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-pexpect-3.1-11.2.src.rpm">python-pexpect-3.1-11.2.src.rpm</a>                   14-Nov-2014 17:45  132K   <a href="python-pexpect-3.1-11.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-pysqlite-2.6.3-24.2.src.rpm">python-pysqlite-2.6.3-24.2.src.rpm</a>                14-Nov-2014 19:22   78K   <a href="python-pysqlite-2.6.3-24.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-serial-2.4-11.2.src.rpm">python-serial-2.4-11.2.src.rpm</a>                    14-Nov-2014 19:30   42K   <a href="python-serial-2.4-11.2.src.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="zsync-0.6.2-4.2.src.rpm">zsync-0.6.2-4.2.src.rpm</a>                           14-Nov-2014 19:27  245K   <a href="zsync-0.6.2-4.2.src.rpm.mirrorlist">Details</a>\n<hr /></pre>\n<address>Apache/2.2.12 (Linux/SUSE) Server at download.opensuse.org Port 80</address>\n<br/><address><a href="http://mirrorbrain.org/">MirrorBrain</a> powered by <a href="http://httpd.apache.org/">Apache</a></address>\n</body></html>\n')
        responses.add(responses.GET,
                      'http://download.opensuse.org/repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/x86_64/',
                      body='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n <head>\n  <title>Index of /repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/x86_64</title>\n  <link rel="stylesheet" href="http://static.opensuse.org/css/mirrorbrain.css" type="text/css" />\n </head>\n <body>\n<h1>Index of /repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/x86_64</h1>\n<pre><img src="/icons/blank.gif" alt="Icon " /> <a href="?C=N;O=D">Name</a>                                                  <a href="?C=M;O=A">Last modified</a>      <a href="?C=S;O=A">Size</a>  <hr /><img src="/icons/up.png" alt="[DIR]" /> <a href="/repositories/home:/uibmz:/opsi:/opsi40/CentOS_7/">Parent Directory</a>                                                           -   \n<img src="/icons/rpm.png" alt="[   ]" /> <a href="duplicity-0.6.08b-11.2.x86_64.rpm">duplicity-0.6.08b-11.2.x86_64.rpm</a>                     14-Nov-2014 19:32  354K   <a href="duplicity-0.6.08b-11.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="duplicity-debuginfo-0.6.08b-11.2.x86_64.rpm">duplicity-debuginfo-0.6.08b-11.2.x86_64.rpm</a>           14-Nov-2014 19:32   24K   <a href="duplicity-debuginfo-0.6.08b-11.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="fdupes-1.50-14.1.x86_64.rpm">fdupes-1.50-14.1.x86_64.rpm</a>                           11-Dec-2014 00:00   21K   <a href="fdupes-1.50-14.1.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="fdupes-debuginfo-1.50-14.1.x86_64.rpm">fdupes-debuginfo-1.50-14.1.x86_64.rpm</a>                 11-Dec-2014 00:00   33K   <a href="fdupes-debuginfo-1.50-14.1.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="librsync-0.9.7-175.2.x86_64.rpm">librsync-0.9.7-175.2.x86_64.rpm</a>                       14-Nov-2014 17:46   57K   <a href="librsync-0.9.7-175.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="librsync-debuginfo-0.9.7-175.2.x86_64.rpm">librsync-debuginfo-0.9.7-175.2.x86_64.rpm</a>             14-Nov-2014 17:46   92K   <a href="librsync-debuginfo-0.9.7-175.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="lshw-B.02.17-1.2.x86_64.rpm">lshw-B.02.17-1.2.x86_64.rpm</a>                           14-Nov-2014 17:46  1.5M   <a href="lshw-B.02.17-1.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="lshw-debuginfo-B.02.17-1.2.x86_64.rpm">lshw-debuginfo-B.02.17-1.2.x86_64.rpm</a>                 14-Nov-2014 17:46  1.2M   <a href="lshw-debuginfo-B.02.17-1.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-atftp-0.7.dfsg-11.2.x86_64.rpm">opsi-atftp-0.7.dfsg-11.2.x86_64.rpm</a>                   14-Nov-2014 17:53   32K   <a href="opsi-atftp-0.7.dfsg-11.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-atftp-client-0.7.dfsg-11.2.x86_64.rpm">opsi-atftp-client-0.7.dfsg-11.2.x86_64.rpm</a>            14-Nov-2014 17:53   24K   <a href="opsi-atftp-client-0.7.dfsg-11.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="opsi-atftp-debuginfo-0.7.dfsg-11.2.x86_64.rpm">opsi-atftp-debuginfo-0.7.dfsg-11.2.x86_64.rpm</a>         14-Nov-2014 17:53  111K   <a href="opsi-atftp-debuginfo-0.7.dfsg-11.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="p7zip-9.20.1-4.2.x86_64.rpm">p7zip-9.20.1-4.2.x86_64.rpm</a>                           14-Nov-2014 19:01  1.3M   <a href="p7zip-9.20.1-4.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="p7zip-debuginfo-9.20.1-4.2.x86_64.rpm">p7zip-debuginfo-9.20.1-4.2.x86_64.rpm</a>                 14-Nov-2014 19:01  3.1M   <a href="p7zip-debuginfo-9.20.1-4.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-GnuPG-Interface-0.3.2-4.2.x86_64.rpm">python-GnuPG-Interface-0.3.2-4.2.x86_64.rpm</a>           14-Nov-2014 19:10   25K   <a href="python-GnuPG-Interface-0.3.2-4.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-GnuPG-Interface-debuginfo-0.3.2-4.2.x86_64.rpm">python-GnuPG-Interface-debuginfo-0.3.2-4.2.x86_64.rpm</a> 14-Nov-2014 19:10  2.3K   <a href="python-GnuPG-Interface-debuginfo-0.3.2-4.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-SQLAlchemy-0.7.7-32.1.x86_64.rpm">python-SQLAlchemy-0.7.7-32.1.x86_64.rpm</a>               17-Nov-2014 10:15  1.3M   <a href="python-SQLAlchemy-0.7.7-32.1.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-SQLAlchemy-debuginfo-0.7.7-32.1.x86_64.rpm">python-SQLAlchemy-debuginfo-0.7.7-32.1.x86_64.rpm</a>     17-Nov-2014 10:15   26K   <a href="python-SQLAlchemy-debuginfo-0.7.7-32.1.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-SQLAlchemy-doc-0.7.7-32.1.x86_64.rpm">python-SQLAlchemy-doc-0.7.7-32.1.x86_64.rpm</a>           17-Nov-2014 10:15  796K   <a href="python-SQLAlchemy-doc-0.7.7-32.1.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-Twisted-12.0.0-24.2.x86_64.rpm">python-Twisted-12.0.0-24.2.x86_64.rpm</a>                 14-Nov-2014 19:37  4.7M   <a href="python-Twisted-12.0.0-24.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-Twisted-debuginfo-12.0.0-24.2.x86_64.rpm">python-Twisted-debuginfo-12.0.0-24.2.x86_64.rpm</a>       14-Nov-2014 19:37   63K   <a href="python-Twisted-debuginfo-12.0.0-24.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-Twisted-doc-12.0.0-24.2.x86_64.rpm">python-Twisted-doc-12.0.0-24.2.x86_64.rpm</a>             14-Nov-2014 19:37  1.0M   <a href="python-Twisted-doc-12.0.0-24.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-ldaptor-0.0.43-16.1.x86_64.rpm">python-ldaptor-0.0.43-16.1.x86_64.rpm</a>                 17-Nov-2014 10:08  151K   <a href="python-ldaptor-0.0.43-16.1.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-ldaptor-debuginfo-0.0.43-16.1.x86_64.rpm">python-ldaptor-debuginfo-0.0.43-16.1.x86_64.rpm</a>       17-Nov-2014 10:08  2.1K   <a href="python-ldaptor-debuginfo-0.0.43-16.1.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-mysql-1.2.2-98.2.x86_64.rpm">python-mysql-1.2.2-98.2.x86_64.rpm</a>                    14-Nov-2014 19:05   85K   <a href="python-mysql-1.2.2-98.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-mysql-debuginfo-1.2.2-98.2.x86_64.rpm">python-mysql-debuginfo-1.2.2-98.2.x86_64.rpm</a>          14-Nov-2014 19:05   53K   <a href="python-mysql-debuginfo-1.2.2-98.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-pam-0.5.0-4.2.x86_64.rpm">python-pam-0.5.0-4.2.x86_64.rpm</a>                       14-Nov-2014 17:46   24K   <a href="python-pam-0.5.0-4.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-pam-debuginfo-0.5.0-4.2.x86_64.rpm">python-pam-debuginfo-0.5.0-4.2.x86_64.rpm</a>             14-Nov-2014 17:46   16K   <a href="python-pam-debuginfo-0.5.0-4.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-pysqlite-2.6.3-24.2.x86_64.rpm">python-pysqlite-2.6.3-24.2.x86_64.rpm</a>                 14-Nov-2014 19:22  157K   <a href="python-pysqlite-2.6.3-24.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="python-pysqlite-debuginfo-2.6.3-24.2.x86_64.rpm">python-pysqlite-debuginfo-2.6.3-24.2.x86_64.rpm</a>       14-Nov-2014 19:22   75K   <a href="python-pysqlite-debuginfo-2.6.3-24.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="zsync-0.6.2-4.2.x86_64.rpm">zsync-0.6.2-4.2.x86_64.rpm</a>                            14-Nov-2014 19:27   79K   <a href="zsync-0.6.2-4.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="zsync-debuginfo-0.6.2-4.2.x86_64.rpm">zsync-debuginfo-0.6.2-4.2.x86_64.rpm</a>                  14-Nov-2014 19:27  244K   <a href="zsync-debuginfo-0.6.2-4.2.x86_64.rpm.mirrorlist">Details</a>\n<img src="/icons/rpm.png" alt="[   ]" /> <a href="zsync-devel-0.6.2-4.2.x86_64.rpm">zsync-devel-0.6.2-4.2.x86_64.rpm</a>                      14-Nov-2014 19:27   18K   <a href="zsync-devel-0.6.2-4.2.x86_64.rpm.mirrorlist">Details</a>\n<hr /></pre>\n<address>Apache/2.2.12 (Linux/SUSE) Server at download.opensuse.org Port 80</address>\n<br/><address><a href="http://mirrorbrain.org/">MirrorBrain</a> powered by <a href="http://httpd.apache.org/">Apache</a></address>\n</body></html>\n')

        software = parse_repository('http://download.opensuse.org/repositories/home:/uibmz:/opsi:/opsi40/CentOS_7')

        expected = {'python-pam': '0.5.0-4.2', 'lshw-debuginfo': 'B.02.17-1.2', 'python-pexpect': '3.1-11.2', 'opsi-linux-bootimage-20140919': '2.2', 'lshw': 'B.02.17-1.2', 'librsync-debuginfo': '0.9.7-175.2', 'opsiconfd': '4.0.5.2-1.2', 'python-serial': '2.4-11.2', 'p7zip-debuginfo': '9.20.1-4.2', 'python-GnuPG-Interface-debuginfo': '0.3.2-4.2', 'opsi-configed': '4.0.5.1.8-1.1', 'opsi-atftp': '0.7.dfsg-11.2', 'python-ldaptor': '0.0.43-16.1', 'python-mysql-debuginfo': '1.2.2-98.2', 'opsi-utils': '4.0.5.6-2.2', 'zsync-debuginfo': '0.6.2-4.2', 'python-SQLAlchemy': '0.7.7-32.1', 'zsync': '0.6.2-4.2', 'opsipxeconfd': '4.0.5.3-6.2', 'fdupes-debuginfo': '1.50-14.1', 'opsi-atftp-client': '0.7.dfsg-11.2', 'python-pysqlite': '2.6.3-24.2', 'opsi-nagios-plugins': '4.0.2.1-3.2', 'python-Twisted-doc': '12.0.0-24.2', 'python-Twisted-debuginfo': '12.0.0-24.2', 'python-opsi': '4.0.5.15-1.2', 'python-ldaptor-debuginfo': '0.0.43-16.1', 'python-SQLAlchemy-debuginfo': '0.7.7-32.1', 'python-Twisted': '12.0.0-24.2', 'p7zip': '9.20.1-4.2', 'librsync': '0.9.7-175.2', 'python-GnuPG-Interface': '0.3.2-4.2', 'python-pam-debuginfo': '0.5.0-4.2', 'python-SQLAlchemy-doc': '0.7.7-32.1', 'duplicity-debuginfo': '0.6.08b-11.2', 'python-pysqlite-debuginfo': '2.6.3-24.2', 'opsi-atftp-debuginfo': '0.7.dfsg-11.2', 'duplicity': '0.6.08b-11.2', 'fdupes': '1.50-14.1', 'opsi-depotserver': '4.0.5.11-1.2', 'zsync-devel': '0.6.2-4.2', 'python-mysql': '1.2.2-98.2'}

        self.assertEquals(expected, software)

    def test_splitting_name_and_version(self):
        self.assertEquals(('cabextract', '1.2-5.2'), split_name_and_version('cabextract-1.2-5.2.i586.rpm'))
        self.assertEquals(('opsi-configed', '4.0.5.1.8-1'), split_name_and_version('opsi-configed_4.0.5.1.8-1_all.deb'))
        self.assertEquals(('opsi-atftp', '0.7.dfsg-4'), split_name_and_version('opsi-atftp_0.7.dfsg-4_amd64.deb'))
        self.assertEquals(('python-crypto', '2.1.0-5.2'), split_name_and_version('python-crypto-2.1.0-5.2.i386.rpm'))
        self.assertEquals(('libmagic1-x86', '5.21-5.1'), split_name_and_version('libmagic1-x86-5.21-5.1.ia64.rpm'))
        self.assertEquals(('cabextract', '1.2-5.5'), split_name_and_version('cabextract-1.2-5.5.i686.rpm'))
