pids=("1042484" "1042823" "1042573" "1042943" "1042777" "1043118" "1043365" "1043411" "1043450")
for pid in "${pids[@]}"; do
    ../profile.sh "2allremote-$pid" "sudo perf record -e cycles -F 999 -p" "-- sleep 30" $pid
done