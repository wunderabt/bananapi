boinccmd --get_tasks | grep "fraction done"
echo "----"
boinccmd --get_tasks | grep remaining | awk '{print $5}' | xargs -I{} date -u +%H:%M:%S -d@{}

