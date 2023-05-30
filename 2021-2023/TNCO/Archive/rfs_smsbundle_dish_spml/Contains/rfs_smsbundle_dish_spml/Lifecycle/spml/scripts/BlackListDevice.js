 
logger.debug('Generating BlackListDevice request message for prov gateway');
load('classpath:scripts/lib.js');
var message = {};

var message = {valueObject: {}};
message.valueObject={
        "device": {
            "identifier": "12345678901341",
            "colour": {
                "colour": "black",
                "reason": "0011",
                "organization": "313/PLMN/034000",
                "clarifyReason": "Lost"
            }
        }
    };
message["loopbackMode"] = "true";
message["requestId"] = executionRequest.properties.extOrderId;
message["targetVersion"] = executionRequest.properties.targetVersion;
// Whilst not specifically present in the 2.4.1 version of the specification, we will add an
// additionalParams block here since all other request messages feature this.
 


logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);