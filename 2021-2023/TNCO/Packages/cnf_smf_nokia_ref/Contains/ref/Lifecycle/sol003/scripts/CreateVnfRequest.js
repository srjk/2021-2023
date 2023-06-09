/*
 This is the generic message creation logic for CreateVnfRequest messages based on the 2.4.1 version of the ETSI SOL003 specification
 */
logger.info('Generating CreateVnfRequest message for Ericsson VNFM');
load('classpath:scripts/lib.js');

// Create the message object to be returned
var message = {additionalParams: {}}; {vnfConfigurableProperties: {}}; 

// Set the standard message properties
// The VNFD id is required, the other fields are optional
setPropertyIfNotNull(executionRequest.properties, message, 'vnfdId');
setPropertyIfNotNull(executionRequest.properties, message, 'vnfInstanceName');
setPropertyIfNotNull(executionRequest.properties, message, 'vnfInstanceDescription');
setPropertyIfNotNull(executionRequest.properties, message.additionalParams, 'vnfPkgId');

logger.info('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);
