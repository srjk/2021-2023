
logger.info('Generating InstantiateVnfRequest message for ETSI SOL003 v2.4.1');
load('classpath:scripts/lib.js');

var chassis_key = executionRequest.properties.vnfInstanceName;
var message = {};

message.vimConnectionInfo = [
  {
        id: executionRequest.properties.vim_id,
        extra: {
            name: ""
        },
        vimType: executionRequest.properties.vimType,
        vimId: executionRequest.properties.vim_id,
        interfaceInfo: {
          endpoint: executionRequest.properties.baseUrl
        },
        accessInfo: {
            username: executionRequest.properties.accessInfo_username,
            password: executionRequest.properties.accessInfo_password,
            vim_project: executionRequest.properties.accessInfo_vim_project
        },
		extra: {
            region: executionRequest.properties.region,
            availability_zone: executionRequest.properties.availability_zone
         },
        interfaceInfo: {
            baseUrl: executionRequest.properties.baseUrl
         }
    }
];

message["flavourId"] = executionRequest.properties.flavourId;
message.additionalParams = {};
message.additionalParams['VIM_NETWORK_ORCH_SEC_GRP_1'] = executionRequest.properties.VIM_NETWORK_ORCH_SEC_GRP_1;
message.additionalParams['CF_BOOT0_VOL_ID'] = executionRequest.properties.CF_BOOT0_VOL_ID;
message.additionalParams['CF_VIP_PREFIX'] = executionRequest.properties.CF_VIP_PREFIX;
message.additionalParams['CF1_SLOT_CARD_NUMBER'] =  executionRequest.properties.CF1_SLOT_CARD_NUMBER;
message.additionalParams['CF_IP_TYPE'] =  executionRequest.properties.CF_IP_TYPE;
message.additionalParams['SF_FLAVOR'] = executionRequest.properties.SF_FLAVOR;
message.additionalParams['CF_NAME_SERVER'] = executionRequest.properties.CF_NAME_SERVER;
message.additionalParams['EM_CONFD_USER'] = executionRequest.properties.EM_CONFD_USER;
//vnfConfigurableProperties
// message.vnfConfigurableProperties = {};
// message.vnfConfigurableProperties['slice_config_param1'] = executionRequest.properties.slice_config_param1';
// message.vnfConfigurableProperties['slice_config_param2'] = executionRequest.properties.slice_config_param2';
// message.vnfConfigurableProperties['slice_config_param3'] = executionRequest.properties.slice_config_param3';

// setPropertyIfNotNull(executionRequest.properties, message, 'vnfdId');
// setPropertyIfNotNull(executionRequest.properties, message, 'vnfInstanceName');
// setPropertyIfNotNull(executionRequest.properties, message, 'instantiation_level');



logger.info('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);
