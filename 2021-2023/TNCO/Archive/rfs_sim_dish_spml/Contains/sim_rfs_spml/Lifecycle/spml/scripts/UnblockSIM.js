logger.debug('Generating Modification requst message for sim rfss');
load('classpath:scripts/lib.js');
// Create the message object to be returned
var message = { modifications: []};
    message.modifications = [
        {
            "operation": "remove",
            "path": "hlr/imsiActive"
        },
        {
            "path": "hss",
            "operation": "addorset",
            "valueObject": {
                "adminBlocked": "false"
            }
        },
        {
            "operation": "remove",
            "path": "udm5gData/servingPlmnId/provisionedData/accessAndMobilitySubscriptionData/accessRestr"
        }
    ];
message["requestId"] = executionRequest.properties.extOrderId;
message["supi"] = executionRequest.properties.SUPI;
message["objectClass"] = executionRequest.properties.objectClass;
message["targetVersion"] = executionRequest.properties.targetVersion;
message["loopbackMode"] = "false";
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