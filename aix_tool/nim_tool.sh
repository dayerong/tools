#!/bin/ksh
#NIM Master远程命令执行工具--nim_tool.sh
_SCRIPT_RESOURCE=/nimdata/script/nim.sh
while true
do      
	clear echo                                                         
	echo "╔=========================================================╗" 
	echo "║                                                         ║"
	echo "║               NIM Master远程命令执行工具                ║" 
	echo "║                                                         ║"
	echo "╚=========================================================╝" 
	_MACHINE=$(lsnim -t standalone |cut -d" " -f1)
	echo
	echo "----------NIM客户端"----------
	lsnim -t standalone |cut -d" " -f1 | awk '{printf("%-5s%-15s\n","("NR")",$0)}'
	echo
	echo "警告：由于本工具对客户端具有root权限，请谨慎执行命令！"
	echo "退出：（q）"
	echo
	echo "请选择：\c"
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
		echo "╔=========================================================╗" 
		echo "║                                                         ║"
		echo "║               NIM Master远程命令执行工具                ║" 
		echo "║                                                         ║"
		echo "╚=========================================================╝" 
		echo "----------NIM客户端----------"
		echo ${CHOICE}
		echo
		echo "请输入需要执行的命令：\c"
		read _CMD
		echo "$_CMD" >  ${_SCRIPT_RESOURCE}
		/usr/lpp/bos.sysmgt/nim/methods/m_cust -a script=script_nim ${CHOICE}
		echo
		echo
		echo "返回：（q）    继续：（Enter）\c"
		read _CHOICE_2
		if [ "${_CHOICE_2}" == "q" -o "${_CHOICE_2}" == "Q" ]
        then
                 break
		fi
	done
done
	

