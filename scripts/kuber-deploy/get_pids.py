import subprocess

keywords=["frontend", "geo", "profile", "rate", "recommendation", "reservation", "search", "user"]
for keyword in keywords:
    cmd = "crictl inspect --output go-template --template \'{{.info.pid}}\' $(crictl ps --name \"" + keyword + "*\" -q)"
    output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(output.stdout)