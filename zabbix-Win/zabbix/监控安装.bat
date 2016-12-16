@ECHO OFF&PUSHD %~DP0 &TITLE zabbix 安装向导
mode con cols=80 lines=30
:menu
cls
echo.
echo zabbix 客户端安装菜单
echo ===============================================
echo.
echo 输入1，安装zabbix客户端
echo.
echo 输入2，启动zabbix客户端
echo.
echo 输入3，检测zabbix客户端
echo.
echo 输入4，关闭zabbix客户端
echo.
echo 输入5，删除zabbix客户端
echo.
echo ===============================================
echo.
echo.
set /p user_input=请输入数字：
if %user_input% equ 1 c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win -i
if %user_input% equ 2 c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win -s
if %user_input% equ 3 netstat -an |find "10050"
if %user_input% equ 4 c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win -x
if %user_input% equ 5 c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win -d
pause
goto menu