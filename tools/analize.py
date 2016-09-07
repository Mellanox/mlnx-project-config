#!/usr/bin/python

import commands
import tempfile
import smtplib
from email.mime.text import MIMEText
import sys
import os

known_issues = { '1': { 'file': 'stack.sh.log',
                        'pattern': "Unable to add physical volume '/dev/loop0' to volume group 'stack-volumes-lvmdriver-1'",
                        'msg': "PLease reset the server or try to debug it"
                      },
                 '2': { 'file' : 'n-cpu.log',
                        'pattern': "libvirtError: Failed to connect socket to",
                        'msg': "PLease restart libvirtd-bin service"
                      },
                 '3': { 'file': 'stack.sh.log',
                        'pattern': "Unable to look up git.openstack.org",
                        'msg': "PLease rerun the job again"
                      },
                 '4': { 'file': 'stack.sh.log',
                        'pattern': "git call failed",
                        'msg': "PLease rerun the job again"
                      }
               }

report = { "mail": "lennyb@mellanox.com" }


def send_email(rm):
    fp = tempfile.NamedTemporaryFile(delete=True)
    fp.write('RM %s is back again\n' % rm)
    fp.write("%s\n" % known_issues[rm]['msg'])
    fp.write("1 %s\n" % os.environ)
    fp.write("cloudx-16-01:/home/CI/scripts/rerun_jobs.py -p %s -j %s\n" % (os.environ.get('JOB_NAME',""), os.environ.get('BUILD_NUMBER',"")))
    fp.seek(0)
    msg = MIMEText(fp.read())
    fp.close()

    msg['Subject'] = "CI Failure, %s issue back" % rm
    msg['From'] = 'lennyb@mellanox.com'
    msg['To'] = report['mail']
    print "Sending email to %s" % report["mail"]
    print msg
    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], [msg['From']], msg.as_string())
    s.quit()


def main(log_dir='.'):
    for rm, details in known_issues.iteritems():
        try:
            log = "%s/%s" % ( log_dir, details['file'])
            print ("Checking %s for %s" % (log, details['pattern']))
            if details['pattern'] in open(log).read():
                print "RM#%s happened again in %s" % (rm, log_dir)
                send_email(rm)
        except Exception as e:
            print "Exception %s" % ( e )
            pass


if __name__ == "__main__":
   main(sys.argv[1:][0])











