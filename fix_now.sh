#!/bin/bash
echo "============================================"
echo "FIXING DATABASE - RECREATING TABLE"
echo "============================================"
echo
mysql -u root -p purchase_slips_db < recreate_table.sql
if [ $? -eq 0 ]; then
    echo
    echo "SUCCESS! Table recreated with correct schema."
    echo "Now restart your backend: python backend/app.py"
else
    echo
    echo "ERROR! Check MySQL credentials."
fi
