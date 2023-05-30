logger.debug('Generating ChangeNumber requst message for prov gateway');
load('classpath:scripts/lib.js');
var message = { modifications: []};
message.modifications=[
        {
                "path": "privateUserId",
                "operation": "add",
                "valueObject": {
                    "privateUserId": "+"+executionRequest.properties.GPSI+"@ims.mnc340.mcc313.3gppnetwork.org",
                    "provisionedImsi": [
                        {
                            "provisionedImsi": executionRequest.properties.SUPI,
                        }
                    ],
                    "msisdn": executionRequest.properties.GPSI,
                    "preferredAuthenticationScheme": "tlsDigestAkaV2",
                    "preferredDomain": "ims",
                    "refGussDataId": "1",
                    "looseRoutingIndicationRequired": "false",
                    "digestRealm": "ims.mnc340.mcc313.3gppnetwork.org"
                }
            },
			 {
                "path": "hss/privateUserId[@privateUserId='+"+executionRequest.properties.Old_GPSI+"@ims.mnc340.mcc313.3gppnetwork.org']",
                "operation": "remove"
            },
            {
                "path": "upiListItem",
                "operation": "set",
                "valueObject": {
                    "upi": "sip:+"+executionRequest.properties.GPSI+"@ims.mnc340.mcc313.3gppnetwork.org"
                }
            }
    ];
message["loopbackMode"] = "false";
message["requestId"] = executionRequest.properties.extOrderId;
message["supi"] = executionRequest.properties.SUPI;
message["objectClass"] = executionRequest.properties.objectClass;
message["targetVersion"] = executionRequest.properties.targetVersion;
// Whilst not specifically present in the 2.4.1 version of the specification, we will add an
// additionalParams block here since all other request messages feature this.
for (var key in executionRequest.getProperties()) {
    if (key.startsWith('additionalParams.') || key.startsWith('extVirtualLinks.') || key.startsWith('extManagedVirtualLinks.') || key.startsWith('modifications.') ) {
         print('Got property [' + key + '], value = [' + executionRequest.properties[key] + ']');
        addProperty(message, key, executionRequest.properties[key]);
    }
}
logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);