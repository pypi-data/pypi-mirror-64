import pygrading.general_test as gg

ret = gg.utils.exec("python3 ./test/input_test.py", "Charles Zhang!")

print("======= Stdout =======")
print(ret.stdout)
print("======= Stderr =======")
print(ret.stderr)
print("======== Cmd =========")
print(ret.cmd)
print("======== Time ========")
print(ret.exec_time)
print("===== ReturnCode =====")
print(ret.returncode)