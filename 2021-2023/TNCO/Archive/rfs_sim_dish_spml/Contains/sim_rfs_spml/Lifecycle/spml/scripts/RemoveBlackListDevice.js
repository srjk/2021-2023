 
logger.debug('Generating RemoveBlackListDevice request message for prov gateway');
load('classpath:scripts/lib.js');
var message = {};

message["requestId"] = executionRequest.properties.extOrderId;
message["targetVersion"] = executionRequest.properties.targetVersion;
message["objectClass"] = executionRequest.properties.objectClass;
message["identifier"] = executionRequest.properties.identifier;
message["loopbackMode"] = "true";
// Whilst not specifically present in the 2.4.1 version of the specification, we will add an
// additionalParams block here since all other request messages feature this.
 


logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);