import subprocess
import re


from script_logger import script_log


def run_command(com):
    command = subprocess.run(com.split(), capture_output=True)
    if command.stderr:
        script_log("Something goes wrong with update at running \"" + com + "\" command:")
        script_log(command.stderr.decode("utf-8"))
    return str(command.stdout.decode("utf-8"))


def check_if_was_updated(log):
    is_not_updated = bool(re.search(r"Already up to date.", log))
    if not is_not_updated:
        script_log("Repository updated!")


def git_update():
    run_command("git stash")
    check_if_was_updated(run_command("git pull --rebase"))
    run_command("git stash pop")

