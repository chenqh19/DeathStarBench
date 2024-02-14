pids=("2332642" "2333181" "2332756" "2333507" "2333362" "2333126" "2333570" "2333455")
for pid in "${pids[@]}"; do
    ../profile.sh "searchaway-$pid" "sudo perf record -e cycles -F 999 -p" "-- sleep 30" $pid
done