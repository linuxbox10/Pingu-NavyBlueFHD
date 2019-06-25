#/usr/bin/bash
timePeriod=1

sleep 5

currSkin=`cat /etc/enigma2/settings|grep 'config.skin.primary_skin='|cut -d '=' -f2|cut -d '/' -f1`
SkinModsPath="/usr/share/enigma2/$currSkin/mySkin"

currEPOC=`date +%s`
echo curr EPOC=$currEPOC
lastGScount=0
GScont=0
for filename in `ls /hdd/dvbapp2_crash*.log`
do
    fileEPOC=`date -r $filename +%s`
    diffEPOC=$((currEPOC - fileEPOC))
    diffEPOC=$((diffEPOC / 60))
    GScont=$((GScont+1))
    if [ $diffEPOC -lt $timePeriod ];then
        lastGScount=$((lastGScount+1))
    fi
    #echo $filename created $diffEPOC minutes ago, skipping
    cat $filename|grep 'File*UserSkin'
    #if [ `cat $filename|grep -c 'File*UserSkin'` -gt 0 ];then
    #    echo aqq
    #fi
done
if [ $lastGScount -gt 1 ];then
    echo "Analyzed $GScont GS logs." >> /tmp/safeMode.log
    echo "Multiple GS's ($lastGScount) in short time detected !!!"
    echo "removing skin parts configuration"
    [ -e $SkinModsPath ] && rm -f $SkinModsPath/*.xml
    echo "Multiple GS's in short time detected, skin parts configuration has been removed!!!" >> /tmp/safeMode.log
else
    echo "Analyzed $GScont GS logs. No issues found. :)"
    echo "Analyzed $GScont GS logs. No issues found. :)" >> /tmp/safeMode.log
fi

