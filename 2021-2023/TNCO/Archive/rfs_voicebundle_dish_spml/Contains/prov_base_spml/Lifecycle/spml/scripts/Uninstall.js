logger.debug('Generating Modification requst message for prov gateway');
load('classpath:scripts/lib.js');
var extOrderId;
var imports = new JavaImporter(java.lang.Runtime,java.lang.ProcessBuilder,java.io.BufferedReader,java.io.InputStreamReader,java.lang.StringBuffer);
with(imports){
function read(inputStream){
    var inReader = new BufferedReader(new InputStreamReader(inputStream));
    var inputLine;
    var response = new StringBuffer();
    while ((inputLine = inReader.readLine()) != null) {
           response.append(inputLine);
    }
    inReader.close();
    return response.toString();
}
print("URL"+dishTmfUrl);
token_url = dishTmfUrl+ "KamiCore/oauth/token?grant_type=client_credentials";
print(token_url);
var process = new ProcessBuilder("curl","--location","--request","POST",token_url,"-H","Authorization: Basic ZGlzaDpkaXNoMTIzNA==","-k","-H","Content-Type: application/json").start();
result=read(process.getInputStream());
print(result);
result = JSON.parse(result).access_token;
//command = JSON.parse(command);
command = "Authorization: Bearer " + result ;
data_send = "{ \"almInstanceName\": \""+executionRequest.properties.instance_name+"\"}"
ext_url =  dishTmfUrl+ "KamiCore/getExtOrderId";
var process = new ProcessBuilder("curl","--location","--request","GET",ext_url,"-H",command,"-k","-H","Content-Type: application/json","--data",data_send).start();
//process.waitFor();
inputStream = process.getInputStream();
//result = new BufferedReader(new InputStreamReader(inputStream)).lines().collect(Collectors.joining("\n"));
results = read(process.getInputStream());

print(results);
extOrderId = JSON.parse(results).extOrderId;
print("external order id " + extOrderId);
}
// Create the message object to be returned
var message = { modifications: []};
message.modifications = 
[
        {
            "path": executionRequest.properties.hlr_path1,
            "operation": executionRequest.properties.operation2
        },
        {
            "path": executionRequest.properties.hlr_path2,
            "operation": executionRequest.properties.operation2
        },
        {
            "path": executionRequest.properties.hlr_path3,
            "operation": executionRequest.properties.operation2
        },
        {
            "path": executionRequest.properties.hss_path1,
            "operation": executionRequest.properties.operation2
        },
        {
            "operation": executionRequest.properties.operation2,
            "path": "udm5gData/servingPlmnId/provisionedData/smfSelectionSubscriptionData/sNssaiInfo/dnnInfo[@dnnId="+executionRequest.properties.dnn1+"]"
        },
        {
            "operation": executionRequest.properties.operation2,
            "path": "udm5gData/servingPlmnId/provisionedData/smfSelectionSubscriptionData/sNssaiInfo/dnnInfo[@dnnId="+executionRequest.properties.dnn2+"]"
        },
        {
            "operation": executionRequest.properties.operation2,
            "path": "udm5gData/servingPlmnId/provisionedData/smfSelectionSubscriptionData/sNssaiInfo/dnnInfo[@dnnId="+executionRequest.properties.dnn3+"]"
        },
        {
            "operation": executionRequest.properties.operation2,
            "path": "udm5gData/servingPlmnId/provisionedData/sessionManagementSubscriptionData/dnnConfiguration[@dnnId="+executionRequest.properties.dnn1+"]"
        },
        {
            "operation": executionRequest.properties.operation2,
            "path": "udm5gData/servingPlmnId/provisionedData/sessionManagementSubscriptionData/dnnConfiguration[@dnnId="+executionRequest.properties.dnn2+"]"
        },
        {
            "operation": executionRequest.properties.operation2,
            "path": "udm5gData/servingPlmnId/provisionedData/sessionManagementSubscriptionData/dnnConfiguration[@dnnId="+executionRequest.properties.dnn3+"]"
        },
        {
            "operation": executionRequest.properties.operation2,
            "path": "pcf/smPolicyData/smPolicySnssaiData/smPolicyDnnData[@dnn="+executionRequest.properties.dnn1+"]"
        },
        {
            "operation": executionRequest.properties.operation2,
            "path": "pcf/smPolicyData/smPolicySnssaiData/smPolicyDnnData[@dnn="+executionRequest.properties.dnn2+"]"
        },
        {
            "operation": executionRequest.properties.operation2,
            "path": "pcf/smPolicyData/smPolicySnssaiData/smPolicyDnnData[@dnn="+executionRequest.properties.dnn3+"]"
        }
    ];
message["loopbackMode"] = "false";
message["requestId"] = extOrderId;
message["supi"] = executionRequest.properties.SUPI;
message["objectClass"] = "Subscriber";
message["targetVersion"] = "SDL_MULTIAPPSUBSCRIBER_v10";
for (var key in executionRequest.getProperties()) {
    if (key.startsWith('additionalParams.') || key.startsWith('extVirtualLinks.') || key.startsWith('extManagedVirtualLinks.') || key.startsWith('modifications.') ) {
         print('Got property [' + key + '], value = [' + executionRequest.properties[key] + ']');
        addProperty(message, key, executionRequest.properties[key]);
    }
}
logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);
