# main.py

from typing import Optional, Dict, List
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
import time
from datetime import datetime
from datetime import date
import sys
import json
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from fastapi.encoders import jsonable_encoder
import logging
from fastapi.exceptions import RequestValidationError
from app.cluster_login_upfd import get_pod_info_upfd
from app.cluster_login_amf import get_pod_info_amf
from app.cluster_login_smf import get_pod_info_smf
from app.showCommands_upfd import execute_commands_upfd
from app.showCommands_amf import execute_commands_amf
from app.showCommands_smf import execute_commands_smf
from app.showCommands_post_upfd import execute_commands_post_upfd
from app.showCommands_amf_post import execute_commands_amf_post
from app.showCommands_smf_post import execute_commands_smf_post
from app.nexus import download_file
from app.difference import grenreate_diff
from app.extract_file import extract_file
from app.download_s3 import download_s3


from app.models import *
import os
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
