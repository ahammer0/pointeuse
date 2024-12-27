# resetService.sh
#!/bin/bash

systemctl stop pointeuse.service
cp -ru ~/actions-runner/_work/pointeuse/pointeuse/* ~/pointeuse
systemctl start pointeuse.service
