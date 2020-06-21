#!/bin/sh
#
# To run it: 
# 	nohup ./download_un_data.sh < country_id_list.csv &
#
# Check the progress:
# 	tail -f ./nohup.out
#
# UN data API:
# 	https://comtrade.un.org/data/doc/api/#DataAvailabilityRequests
#
# NOTE:
#   - The API has QPS control and is very fragile:
#     https://comtrade.un.org/data/doc/api/bulk/
#   - We will need to sleep some seconds between the downloads to
#     avoid overloading the site.
#   - It takes super long (>24 hours) to pull down all data, and for
#     safty, it's better to check the logs and retry the failed ones.

#set -x

while read line; do
  # As of 06/2020, the API provides data between 1998 and 2019.
  for y in $(seq 1988 2019); do
	echo "Country code: ${line}  Year: ${y}"

	# Download data for each <reporting-country, year> pair, this covers all partner countries and products.
	wget --tries=1 \
		 --output-document="tmp_un.csv" \
	 'https://comtrade.un.org/api/get?r='${line}'&freq=A&ps='${y}'&px=HS&p=all&rg=all&cc=AG2&fmt=csv&max=100000&type=C&head=M'

    # Merge data for same country
	cat ./tmp_un.csv >> "./un_country_id_${line}_all_prod.csv"

 	sleep 20
  done
  sleep 100
done

#set +x
