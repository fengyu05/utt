import subprocess


def pipeRun(cmd):
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            shell=True)
  output, error = p.communicate()
  print output
  print error
  return result
