# -*- coding:utf-8 -*-
"""
文件上传下载接口
"""

from __future__ import absolute_import, unicode_literals, division, print_function
from future.utils import raise_
import json
import os
import requests


def upload(url, file, headers=None, timeout=30):
    """
    文件上传
    :param url: 文件上传请求路径
    :param file: 本地文件路径
    :param headers: 请求头参数
    :param timeout: 超时时间
    :return: http状态码 和 response body
    """
    try:
        if not headers or not headers.get('X-File-Path') and not headers.get('X-Type'):
            raise_(ValueError, "参数缺失")
        if not os.path.isfile(file):
            raise_(ValueError, "文件类型错误")
        file_like_obj = open(file, 'rb')
        param = {'picData': file_like_obj}
        resp = requests.post(url=url, files=param, headers=headers, verify=False, timeout=timeout)
        http_code = resp.status_code
        if http_code == 200:
            response = resp.content.decode('utf-8')
            try:
                body = json.loads(response)
            except Exception as exc:
                body = response
        else:
            body = {}
        return http_code, body
    except Exception as exc:
        raise_(Exception, exc)


def download(url, remote_path, local_path=None, return_file=True, headers=None, timeout=30):
    """
    文件下载
    :param url: 下载请求地址
    :param remote_path: 远程文件存储路径
    :param local_path: 下载的文件本地存储路径，如不传或者本地文件已存在则返回saved为False
    :param return_file: 是否需要将文件流返回
    :param headers: 请求头
    :param timeout: 超时时间
    :return: 字典，包含http code, 是否存储，文件流
    """
    try:
        saved = False
        if not remote_path:
            raise_(ValueError, "参数缺失")
        param = {'locateFile': remote_path}
        if headers:
            resp = requests.post(url=url, json=param, headers=headers, verify=False, timeout=timeout)
        else:
            resp = requests.post(url=url, json=param, verify=False, timeout=timeout)
        http_code = resp.status_code
        if http_code == 200:
            file = resp.content
            if local_path:
                if not os.path.exists(local_path):
                    with open(local_path, "wb") as f:
                        f.write(file)
                    saved = True
        else:
            file = ""
            saved = False
        if return_file:
            return {"code": http_code, "saved": saved, "file": file}
        return {"code": http_code, "saved": saved}
    except Exception as exc:
        raise_(Exception, exc)
