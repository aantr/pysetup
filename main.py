from pysetup import main

main: callable
try:
    log = []
    main(log)
except Exception as e:
    open('err.txt', 'w').write(str(e))

# exe = EXE(pyz,
#           a.scripts,
#           a.binaries,
#           Tree('data', prefix='data\\'),
# ....

message = '\n'.join(log)
open('log.txt', 'w').write(message)
