#!/bin/ksh
#NIM MasterԶ������ִ�й���--nim_tool.sh
_SCRIPT_RESOURCE=/nimdata/script/nim.sh
while true
do      
	clear echo                                                         
	echo "�X=========================================================�[" 
	echo "�U                                                         �U"
	echo "�U               NIM MasterԶ������ִ�й���                �U" 
	echo "�U                                                         �U"
	echo "�^=========================================================�a" 
	_MACHINE=$(lsnim -t standalone |cut -d" " -f1)
	echo
	echo "----------NIM�ͻ���"----------
	lsnim -t standalone |cut -d" " -f1 | awk '{printf("%-5s%-15s\n","("NR")",$0)}'
	echo
	echo "���棺���ڱ����߶Կͻ��˾���rootȨ�ޣ������ִ�����"
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
		>  ${_SCRIPT_RESOURCE}
		clear echo                                                     
		echo "�X=========================================================�[" 
		echo "�U                                                         �U"
		echo "�U               NIM MasterԶ������ִ�й���                �U" 
		echo "�U                                                         �U"
		echo "�^=========================================================�a" 
		echo "----------NIM�ͻ���----------"
		echo ${CHOICE}
		echo
		echo "��������Ҫִ�е����\c"
		read _CMD
		echo "$_CMD" >  ${_SCRIPT_RESOURCE}
		/usr/lpp/bos.sysmgt/nim/methods/m_cust -a script=script_nim ${CHOICE}
		echo
		echo
		echo "���أ���q��    ��������Enter��\c"
		read _CHOICE_2
		if [ "${_CHOICE_2}" == "q" -o "${_CHOICE_2}" == "Q" ]
        then
                 break
		fi
	done
done
	

