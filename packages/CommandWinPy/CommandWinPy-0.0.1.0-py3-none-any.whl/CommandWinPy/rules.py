NotRun = "is not recognized as an internal or external command"
import os
def commands(shells):
    kc = os.popen(shells)
    return kc.read()
