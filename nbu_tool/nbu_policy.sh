#!/bash/bin

TABLE_NAME=nbu_policy

#请空原有数据
mysql -u appuser -ppassw0rd  -D appdb -h x.x.x.x -e "delete from $TABLE_NAME;alter table $TABLE_NAME auto_increment=1"


#查询所有策略
bppllist | while read _name
do
	_BACKUP_WINDOWS (){
	bppllist $_name  -U |awk '/Schedule:/,/^$/' |grep Type: |grep -v Application |awk -F ":" '{print $NF}' |while read i
	do
		echo $i:
		bppllist $_name  -U |awk '/Schedule:/,/^$/' | awk '/'"$i"'/,/^$/' | awk '/Daily Windows/,/^$/'|sed '/^$/d' |awk '/Daily Windows/,/^$/'|sed '/Daily Windows:/d' |awk '{printf("%-11s%-10s%-4s%-10s\n",$1,$2,"--",$NF)}'
		echo
	done
	}
	
	#查询策略基本信息
	_POLICY_NAME=$(bppllist $_name -U|awk '/Policy Name/{print $NF}')	
	_POLICY_TYPE=$(bppllist $_name -U |awk '/Policy Type/{print $NF }')
	_POLICY_STATUS=$(bppllist $_name -U |awk '/Active/{print $NF }')
	_CLIENT_HARDWARE=$(bppllist $_name -U |awk '/HW\/OS\/Client:/{print $2}')
	_CLIENT_OS=$(bppllist $_name -U |awk '/HW\/OS\/Client:/{print $3}')
	_CLIENT_NAME=$(bppllist $_name -U |awk '/HW\/OS\/Client:/{print $4}')
	_CLIENT_IP=$(awk -v CLIENT_NAME=$_CLIENT_NAME '$2==CLIENT_NAME || $3==CLIENT_NAME{print $1}' /etc/hosts)
	_VOLUME_POOL=$(bppllist $_name -U |awk '/Policy Name:/,/Include/'|awk '/Residence:/{print $NF}')
	_POLICY_CONTENT=$(bppllist $_name -U |awk '/Include:/,/^$/'|awk NF|awk '{print $NF}' |sed 's/\\/\\\\/g')
	_BACKUP_TYPE=$(bppllist $_name -U|awk -F "Type:                " '/    Type:/{print $NF}' |grep -v "Application Backup")
	_POLICY_RETENTION_LEVEL=$(bppllist $_name -U |awk '/Schedule:/,/^$/{print A}{A=$0}' |sed -e '/Default-Application-Backup/,/^$/{//!d}' -e '/Default-Application-Backup/d' -e '/^$/d' |awk -F "(" '/Retention Level:/{print substr($2,0,length($2)-1)}')
	_POLICY_FREQUENCY=$(bppllist $_name -U |awk '/Schedule:/,/^$/{print A}{A=$0}' |sed -e '/Default-Application-Backup/,/^$/{//!d}' -e '/Default-Application-Backup/d' -e '/^$/d' |awk -F "Frequency:           " '/Frequency:/{print $NF}')
	_POLICY_WINDOWS=$(_BACKUP_WINDOWS)
	
	
	#SQL语句
	STATEMENT_SQL=$(echo "insert into $TABLE_NAME (Policy_Name,Policy_Type,Policy_Status,Volume_Pool,Client_Name,Client_IP,Hardware,OS,Backup_Type,Retention_Level,Frequency,Backup_Windows,Content) values(\"$_POLICY_NAME\",\"$_POLICY_TYPE\",\"$_POLICY_STATUS\",\"$_VOLUME_POOL\",\"$_CLIENT_NAME\",\"$_CLIENT_IP\",\"$_CLIENT_HARDWARE\",\"$_CLIENT_OS\",\"$_BACKUP_TYPE\",\"$_POLICY_RETENTION_LEVEL\",\"$_POLICY_FREQUENCY\",\"$_POLICY_WINDOWS\",\"$_POLICY_CONTENT\")")
	
	#插入数据库
	mysql -u appuser ppassw0rd -D appdb -h x.x.x.x -e "$STATEMENT_SQL"

done
