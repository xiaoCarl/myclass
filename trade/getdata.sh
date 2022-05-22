#!/bin/bash
RESULT=$(curl http://quotes.money.163.com/service/chddata.html?code=$1&start=19991110&end=20180418&fields=CHG;TCAP)
echo $RESULT > $1.csv
