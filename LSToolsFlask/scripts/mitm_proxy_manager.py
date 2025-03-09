import subprocess


class MitmProxyManager:
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def start(self):
        try:
            self.process = subprocess.Popen(self.cmd)
            print("mitmdump started successfully.")
        except Exception as e:
            print("Error starting mitmdump:", e)

    def stop(self):
        if self.process:
            self.process.terminate()
            print("mitmdump stopped.")
        else:
            print("mitmdump is not running.")

    def __del__(self):
        self.stop()
