/*
 This is the generic message creation logic for CreateVnfRequest messages based on the 2.4.1 version of the ETSI SOL003 specification
 */
logger.debug('Generating CreateVnfRequest message for ETSI SOL003 v2.4.1');
load('classpath:scripts/lib.js');
// Create the message object to be returned
var message = {additionalParams: {}};
message.vnfInstanceName = executionRequest.properties.vendor +"-"+ executionRequest.properties.function
						+ executionRequest.properties.nfAppearance + executionRequest.properties.nfunType+"-"
						+ executionRequest.properties.region + executionRequest.properties.azId
						+ executionRequest.properties.dataCenterType + executionRequest.properties.logicalDCNo
						+ executionRequest.properties.env + executionRequest.properties.envId;
// Set the standard message properties
// The VNFD id is required, the other fields are optional
setPropertyIfNotNull(executionRequest.properties, message, 'vnfdId');
//setPropertyIfNotNull(executionRequest.properties, message, 'vnfInstanceName');
setPropertyIfNotNull(executionRequest.properties, message, 'vnfInstanceDescription');
// Whilst not specifically present in the 2.4.1 version of the specification, we will add an
// additionalParams block here since all other request messages feature this.
for (var key in executionRequest.getProperties()) {
    if (key.startsWith('additionalParams.')) {
        // print('Got property [' + key + '], value = [' + executionRequest.properties[key] + ']');
        addProperty(message, key, executionRequest.properties[key]);
    }
}
logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);
