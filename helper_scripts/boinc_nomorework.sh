boinccmd --get_project_status | grep master URL | awk '{print()}' | xargs -I{} boinccmd --project {} nomorework
