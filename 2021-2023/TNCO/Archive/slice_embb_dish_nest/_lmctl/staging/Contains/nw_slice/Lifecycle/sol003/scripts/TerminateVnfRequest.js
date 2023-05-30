/*
 This is the generic message creation logic for TerminateVnfRequest messages based on the 2.4.1 version of the ETSI SOL003 specification
 */
logger.info('Generating TerminateVnfRequest message for Ericsson VNFM');
load('classpath:scripts/lib.js');

// Create the message object to be returned
var message = {additionalParams: {}};

// Should set terminationType and gracefulTerminationTimeout (if required)
message.terminationType = 'FORCEFUL';

logger.info('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);
