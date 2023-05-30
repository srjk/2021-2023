#!/bin/sh

if [ "$#" -ne 1 ]; then
	echo "Error: Expected arguments not provided"
	echo "Usage: noi_consumer_request.sh <Managed Object Instance ID>"
	echo "Example: noi_consumer_request.sh MW463105"
	exit
else

	curl -k --location --request POST 'http://noi-nci-0.noi:9080/jaxws/impact/ImpactWebServiceListenerDLIfc' \
--header 'Content-Type: text/xml' -u impactadmin:impact@dmin \
--data-raw "<soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/' xmlns:typ='http://response.micromuse.com/types'>
   <soapenv:Header/>
   <soapenv:Body>
      <typ:runPolicy>
         <arg0>WSListenerPolicy</arg0>
         <arg1>
            <desc>input_parameter</desc>
            <format>String</format>
            <label>MOID</label>
            <name>MOID</name>
            <value>${1}</value>
         </arg1>
         <arg2>true</arg2>
      </typ:runPolicy>
   </soapenv:Body>
</soapenv:Envelope>" > /tmp/noi_consumerResponse.txt 2> /dev/null

	cat /tmp/noi_consumerResponse.txt | sed 's/.*NE/NE/g' | sed 's/Available.*/Available/g' > /tmp/noi_consumerResponse_tmp.txt

	cat /tmp/noi_consumerResponse_tmp.txt
	rm /tmp/noi_consumerResponse.txt /tmp/noi_consumerResponse_tmp.txt
fi