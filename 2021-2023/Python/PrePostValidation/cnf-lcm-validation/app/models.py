#base models for incoming requests and response
from pydantic import BaseModel, Field, root_validator
from typing import Optional, Dict, List


class podinfo(BaseModel):
   request_id: int
   cnf_namespace :str
   eks_cluster_kube_config: str
   eks_cluster_name: str
   target_cluster_role: str
   creds: str
   interface: str



class oaminfo(BaseModel):
    pod_name_active:str
    oam_ip: str
    oam_port: str
    cmd_prompt: str
    


class s3_info(BaseModel):
    s3_role: str
    s3_bucket: str
    s3_input_dir: str


 
class kubectl_cmds(BaseModel):
    kubectl_commands: List[str]
    nf_commands: List[str]

    
  
class commandsinfo(BaseModel):
   request_id: int 
   cnf_namespace :str
   eks_cluster_kube_config: str
   eks_cluster_name: str
   #site_bucket_tar: str
   #site_bucket: str
   target_cluster_role: str
   deploy_env: str
   operation: str
   commands: List[kubectl_cmds]
   creds: str
   pod_info: oaminfo
   s3_data: s3_info
class commandsinfos(BaseModel):
   request_id: int 
   cnf_namespace :str
   eks_cluster_kube_config: str
   eks_cluster_name: str
   site_bucket_tar: str
   site_bucket: str
   target_cluster_role: str
   deploy_env: str
   operation: str
   commands: List[kubectl_cmds]
   creds: str
   pod_info: oaminfo
   s3_data: s3_info
