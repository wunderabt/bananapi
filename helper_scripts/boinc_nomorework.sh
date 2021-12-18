boinccmd --get_project_status | grep "master URL" | awk '{print($3)}' | xargs -I{} boinccmd --project {} nomorework
