# resetService.sh
#!/bin/bash

systemctl stop pointeuse.service
cp -ru /home/axel/actions-runner/_work/pointeuse/pointeuse/* /home/axel/pointeuse
systemctl start pointeuse.service
