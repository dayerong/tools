#!/bin/ksh
#NIM MasterԶ�̱���ִ�й���--nim_backup.sh
_MKSYSB_LOCATION=/nimdata/os_backup
_DATE=$(date +%Y%m%d)
_MKSYSB_LOG=${_MKSYSB_LOCATION}/mksysb.history

while true
do      
	clear echo                                                         
	echo "�X=========================================================�[" 
	echo "�U                                                         �U"
	echo "�U               NIM MasterԶ�̱���ִ�й���                �U" 
	echo "�U                                                         �U"
	echo "�^=========================================================�a" 
	_MACHINE=$(lsnim -t standalone |cut -d" " -f1)
	echo
	echo "----------NIM�ͻ���"----------
	lsnim -t standalone |cut -d" " -f1 | awk '{printf("%-5s%-15s\n","("NR")",$0)}'
	echo
	echo "���棺���������ڿͻ��˵�ϵͳ���ݡ�"
	echo "�˳�����q��"
	echo
	echo "��ѡ��\c"
	read _CHOICE
	if [ "${_CHOICE}" == "q" -o "${_CHOICE}" == "Q" ]
        then
                exit
        else
                CHOICE=$(lsnim -t standalone |cut -d" " -f1 | awk '{printf("%-5s%-15s\n","("NR")",$0)}' | awk -v CHOICE=$_CHOICE 'NR==CHOICE{print $2}')
        fi
	echo
	
	while true
	do
		clear echo                                                     
		echo "�X=========================================================�[" 
		echo "�U                                                         �U"
		echo "�U               NIM MasterԶ�̱���ִ�й���                �U" 
		echo "�U                                                         �U"
		echo "�^=========================================================�a" 
		echo "----------NIM�ͻ���----------"
		echo ${CHOICE}
		echo
		echo "�������${CHOICE}�ı������ȷ�ϣ�y/n��? \c"
		read YN
		if [ "$YN" = Y -o "$YN" = y -o "$YN" = "Yes" -o "$YN" = "yes" -o "$YN" = "YES" ]
		then
			echo
			echo "${CHOICE}���ݿ�ʼ..."
			_BEGIN_DATE=$(date +%Y/%m/%d-%H:%M:%S)
			nim -o define -t mksysb -a server=master -a source=${CHOICE} -a mk_image=yes -a mksysb_flags="X e" -a location=${_MKSYSB_LOCATION}/${CHOICE}_mksysb_${_DATE} ${CHOICE}_mksysb_${_DATE}
			if [ $? -eq 0 ]
			then
				echo
				echo "${CHOICE}���ݳɹ���"
				_END_DATE=$(date +%Y/%m/%d-%H:%M:%S)
				_CHOICE_IP=`host ${CHOICE} |awk '{print $3}'`
				echo "${_CHOICE_IP}\t\t${CHOICE}\t\t${_BEGIN_DATE}\t\t${_END_DATE}" >> ${_MKSYSB_LOG}
			else
				echo
				echo "${CHOICE}����ʧ�ܡ�"
				exit 1
			fi
		else
			break
		fi

		echo
		echo
		echo "���أ���q��\c"
		read _CHOICE_2
		if [ "${_CHOICE_2}" == "q" -o "${_CHOICE_2}" == "Q" ]
        then
                 break
		fi
	done
done
	

##########
#20151105#
##########

