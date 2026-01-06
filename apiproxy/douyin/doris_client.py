#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Doris 数据库客户端
用于从 Doris 数据库读取用户链接
"""

import pymysql
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class DorisConnection:
    """Doris 数据库连接类"""
    
    def __init__(self, host: str, port: int, database: str, 
                 user: str = 'root', password: str = ''):
        """
        初始化 Doris 连接
        
        Args:
            host: Doris 主机地址
            port: Doris 端口
            database: 数据库名
            user: 用户名
            password: 密码
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
    
    def connect(self) -> bool:
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info(f"成功连接到 Doris 数据库: {self.host}:{self.port}/{self.database}")
            return True
        except Exception as e:
            logger.error(f"连接 Doris 数据库失败: {e}")
            return False
    
    def fetch_user_links(self, table_name: str, 
                        url_column: str = 'url',
                        where_clause: str = '',
                        limit: int = 0) -> List[str]:
        """
        从数据库获取用户链接列表
        
        Args:
            table_name: 表名
            url_column: URL 列名
            where_clause: WHERE 条件（可选）
            limit: 限制返回数量（0=不限制）
        
        Returns:
            URL 列表
        """
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            with self.connection.cursor() as cursor:
                # 构建 SQL 语句
                sql = f"SELECT {url_column} FROM {table_name}"
                if where_clause:
                    sql += f" WHERE {where_clause}"
                if limit > 0:
                    sql += f" LIMIT {limit}"
                
                logger.info(f"执行 SQL: {sql}")
                cursor.execute(sql)
                
                # 提取 URL 列表
                results = cursor.fetchall()
                urls = [row[url_column] for row in results if url_column in row and row[url_column]]
                
                logger.info(f"从数据库获取到 {len(urls)} 个 URL")
                return urls
                
        except Exception as e:
            logger.error(f"从数据库获取链接失败: {e}")
            return []
    
    def fetch_user_links_custom_sql(self, sql: str, url_column: str = 'url') -> List[str]:
        """
        使用自定义 SQL 查询获取链接列表
        
        Args:
            sql: 自定义 SQL 语句
            url_column: URL 列名
        
        Returns:
            URL 列表
        """
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            with self.connection.cursor() as cursor:
                logger.info(f"执行自定义 SQL: {sql}")
                cursor.execute(sql)
                
                results = cursor.fetchall()
                urls = [row[url_column] for row in results if url_column in row and row[url_column]]
                
                logger.info(f"从数据库获取到 {len(urls)} 个 URL")
                return urls
                
        except Exception as e:
            logger.error(f"执行自定义 SQL 失败: {e}")
            return []
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("Doris 数据库连接已关闭")
    
    def __enter__(self):
        """支持 with 语句"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持 with 语句"""
        self.close()


if __name__ == '__main__':
    # 测试代码
    with DorisConnection(
        host='',
        port=9030,
        database='',
        user='',
        password=''
    ) as doris:
        urls = doris.fetch_user_links(
            table_name='ods_cnt_dyuser_mainurl',
            url_column='sec_url',
            limit=5
        )
        print(f"获取到的 URLs: {urls}")
