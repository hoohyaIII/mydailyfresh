#!/usr/bin/env python
# -*-encoding:UTF-8-*-

from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client

from django.conf import settings


class FDFSStorage(Storage):
    '''fast dfs 文件存储类'''

    def __init__(self, client_conf=None, base_url=None):
        """构造函数初始化"""
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        '''打开文件时使用'''
        pass

    def _save(self, name, content, client_conf=None, base_url=None):
        '''保存文件时使用'''
        # name:你选择上传文件的名字
        # content:包含你上传文件内容的File对象

        # 创建一个Fdfs_client对象
        client = Fdfs_client(self.client_conf)

        # 上传文件到fast dfs系统中
        res = client.upload_appender_by_buffer(content.read())

        # res 返回 dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': local_file_name,
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }
        if res.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到fast dfs失败!')

        # 获取返回的文件id
        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):
        '''Django判断文件名是否可用'''
        return False

    def url(self,name):
        '''返回访问文件的url路径,网站的文件存储路径的返回'''
        return self.base_url + name
