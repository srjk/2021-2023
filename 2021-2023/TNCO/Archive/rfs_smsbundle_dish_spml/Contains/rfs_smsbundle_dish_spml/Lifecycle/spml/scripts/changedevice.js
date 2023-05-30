logger.debug('Generating Modification requst message for Device mgt rfss');
load('classpath:scripts/lib.js');
// Create the message object to be returned
var message = { modifications: []};
    message.modifications = [
        {
            "path": "hss/repositoryData[@serviceIndId='vowifi_e911_flags']",
            "operation": "setoradd",
            "valueObject": {
				"serviceIndId": "vowifi_e911_flags",
                "publicUserId": "sip:311480222333000@ims.mnc340.mcc313.3gppnetwork.org",
                "asData": "<![CDATA[<DM-VoWiFi-Data xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:nokia=\"http://nokia.com\" xmlns=\"http://nokia.com\" xsi:schemaLocation=\"http://nokia.com DM-VoWiFi-Data.xsd\"><addr_status>true</addr_status><tc_status>true</tc_status><prov_status>true</prov_status>true</DM-VoWiFi-Data>]]>"
            }
        }
    ],
message["loopbackMode"] = "true";
message["requestId"] = executionRequest.properties.extOrderId;
message["supi"] = executionRequest.properties.SUPI;
message["objectClass"] = executionRequest.properties.objectClass;
message["targetVersion"] = executionRequest.properties.targetVersion;
// Whilst not specifically present in the 2.4.1 version of the specification, we will add an
// additionalParams block here since all other request messages feature this.
 


logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);