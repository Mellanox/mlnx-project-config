#!/usr/bin/python

import commands
import tempfile
import smtplib
from email.mime.text import MIMEText
import sys
import os

known_issues = { 'loop_device': { 'file': 'stack.sh.log',
                        'pattern': "Unable to add physical volume '/dev/loop0' to volume group 'stack-volumes-lvmdriver-1'",
                        'msg': "PLease reset the server or try to debug it"
                      },
                 '855578': { 'file' : 'n-cpu.log',
                        'pattern': "libvirtError: Failed to connect socket to",
                        'msg': "PLease restart libvirtd-bin service"
                      },
                 'networking_issue': { 'file': 'stack.sh.log',
                        'pattern': "Unable to look up git.openstack.org",
                        'msg': "PLease rerun the job again"
                      },
                 'git_clone_failed': { 'file': 'stack.sh.log',
                        'pattern': "git call failed",
                        'msg': "PLease rerun the job again"
                      },
                 '861642': { 'file': 'n-cpu.log',
                        'pattern': "libvirtError: Domain not found: no domain with matching uuid",
                        'msg': "Open Issue need to debug"
                      },
                 'stack_failed': { 'file': 'stack.sh.log',
                        'pattern': "exit",
                        'msg': "stack.sh failed. please check"
                      },
                 'tempest_install': { 'file': 'stack.sh.log',
                        'pattern': "tempest does not match installed location of tempest",
                        'msg': "stack.sh failed with tempest install. please check"
                      }

               }

report = { "mail": "lennyb@mellanox.com,moshele@mellanox.com" }

def send_email(rm):
    fp = tempfile.NamedTemporaryFile(delete=True)
    fp.write('RM %s is back again\n' % rm)

    #http://13.69.151.247/05/357105/5/check-nova/Nova-ML2-Sriov/46b5418/env/environment.txt.gz
    fp.write('More details in http://%s/%s\n' % (os.environ.get('EXT_SERVER','') ,os.environ.get('LOG_PATH','')))
    fp.write("\n%s\n\n" % known_issues[rm]['msg'])
    #fp.write("\n\n\n %s\n" % os.environ)
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

    # Check stack.sh status
    rm = 'stack_failed'
    log = "%s/%s/logs/stack.sh.log.gz" % ( log_dir, known_issues[rm]['file'])
    last_line = commands.getoutput('tail -n1 %s ' % log)
    if last_line.find(known_issues[rm]['pattern']) >= 0:
        send_email(rm)
    del known_issues[rm]


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











