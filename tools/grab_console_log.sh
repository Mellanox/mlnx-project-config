#!/bin/bash -xe

RETRY_LIMIT=300
log_dir=/tmp/$$
mkdir -p $log_dir
log_file=${log_dir}/console.html

# Keep fetching until this uuid appears in the logs before uploading

[ -f $log_file ] && sudo rm -rf $log_file
touch $log_file
sync

# Since we are appending to fetched logs, remove any possibly old runs

# Grab the HTML version of the log (includes timestamps)
TRIES=0
console_log_path='logText/progressiveHtml'
while ! egrep -q "Finished: " $log_file; do
    TRIES=$((TRIES+1))
    if [ $TRIES -gt $RETRY_LIMIT ]; then
        break
    fi
    # -X POST because Jenkins doesn't do partial gets properly when
    #         job is running.
    # --data start=X instructs Jenkins to mimic a partial get using
    #                POST. We determine how much data we need based on
    #                how much we already have.
    # --fail will cause curl to not output data if the request
    #        fails. This allows us to retry when we have Jenkins proxy
    #        errors without polluting the output document.
    # --insecure because our Jenkins masters use self signed SSL certs.
    curl -X POST --data "start=$(stat -c %s $log_file || echo 0)" --fail --insecure $BUILD_URL$console_log_path >> $log_file || true
done

sleep 10
curl -X POST --data "start=$(stat -c %s $log_file || echo 0)" --fail --insecure $BUILD_URL$console_log_path >> $log_file
# We need to add <pre> tags around the output for log-osanalyze to not escape
# the content

sed -i '1s/^/<pre>\n/' $log_file
echo "</pre>" >> $log_file
sync

arch=${log_file}.gz
sudo rm -rf $arch
gzip -9 -r $log_file 2>&1|tee >/dev/null
scp $arch $LOGSERVER://var/www/html/${LOG_PATH:-${JOB_NAME}_${BUILD_NUMBER}}
rm -rf $arch $log_dir
