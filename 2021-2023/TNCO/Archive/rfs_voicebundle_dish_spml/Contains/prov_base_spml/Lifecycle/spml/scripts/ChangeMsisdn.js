logger.debug('Generating Modification requst message for prov gateway');
load('classpath:scripts/lib.js');
var message = {};
// Set the standard message properties
// The VNFD id is required, the other fields are optional
message["loopbackMode"] = "false";
message["requestId"] = executionRequest.properties.extOrderId;
message["supi"] = executionRequest.properties.SUPI;
message["objectClass"] = executionRequest.properties.objectClass;
message["targetVersion"] = executionRequest.properties.targetVersion;
message["oldId"] = executionRequest.properties.Old_GPSI;
message["newId"] = executionRequest.properties.GPSI;
message["aliasType"] = "msisdn";
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