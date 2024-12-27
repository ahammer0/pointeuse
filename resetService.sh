# resetService.sh
#!/bin/bash

systemctl stop pointeuse.service
rm -rf /home/axel/pointeuse
mkdir /home/axel/pointeuse
cp -ru /home/axel/actions-runner/_work/pointeuse/pointeuse/* /home/axel/pointeuse
cp /home/axel/env.pointeuse /home/axel/pointeuse/.env
systemctl start pointeuse.service
