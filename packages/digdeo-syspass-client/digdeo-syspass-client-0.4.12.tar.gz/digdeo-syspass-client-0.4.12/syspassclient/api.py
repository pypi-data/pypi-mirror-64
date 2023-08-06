#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# This file is part of SysPass Client
#
# Copyright (C) 2020  DigDeo SAS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
from colorama import init, Fore, Style
import syspassclient

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
init(autoreset=True)


class SyspassApi(syspassclient.Object):
    def __init__(self):
        syspassclient.Object.__init__(self)
        self.__api_directory = None
        self.__api_filename = None
        self.__api_filename_ext = None
        self.__api_file = None
        self.__api_version = None
        self.__api_data = None

        self.api_directory = None
        self.api_filename_ext = None

    @property
    def api_data(self):
        """
        Return the config file as Python dictionary structure

        :return: Config as a big dictionary
        :rtype: dict
        """
        return self.__api_data

    @api_data.setter
    def api_data(self, parameters):
        """
        set en data and raise in case of error

        :param parameters: something it like a dictionary key
        :type parameters: dict
        :raise TypeError: 'parameters' is not a dict type
        """
        if self.api_data != parameters:
            self.__api_data = parameters

    @property
    def api_3_0(self):
        return {
            "account/search": {
                # Search for accounts
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                # categoryId 	int 	no 	        Category’s Id for filtering
                # clientId 	    int 	no 	        Client’s Id for filtering
                # tagsId 	    array 	no 	        Tags’ Id for filtering
                # op 	        string 	no 	        Operator used for filtering. It can be either ‘or’ or ‘and’
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": False},
                    "count": {"type": "int", "required": False},
                    "categoryId": {"type": "int", "required": False},
                    "clientId": {"type": "int", "required": False},
                    "tagsId": {"type": "array", "required": False},
                    "op": {"type": "str", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/search",
                    "params": {
                        "authToken": None,
                        "text": None,
                        "count": None,
                        "categoryId": None,
                        "clientId": None,
                        "tagsid": None,
                        "op": None,
                    },
                    "id": None,
                },
            },
            "account/view": {
                # Get account’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tokenPass 	string 	yes 	    API token’s pass
                # id 	        int 	yes 	    Account’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "account_id": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/view",
                    "params": {"authToken": None, "account_id": None, "tokenPass": None},
                    "id": None,
                },
            },
            "account/viewPass": {
                # Get account’s password
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tokenPass 	string 	yes 	    API token’s pass
                # id 	        int 	yes 	    Account’s Id
                # details 	    int 	no 	        Whether to return account’s details within response account/editPass
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "account_id": {"type": "int", "required": True},
                    "details": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/viewPass",
                    "params": {"authToken": None, "account_id": None, "tokenPass": None, "details": None},
                    "id": None,
                },
            },
            "account/editPass": {
                # Edit account’s password
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	User’s API token
                # tokenPass 	string 	yes 	API token’s pass
                # id 	int 	yes 	Account’s Id
                # pass 	string 	yes 	Account’s password
                # expireDate 	int 	no 	Expire date in UNIX timestamp format
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "account_id": {"type": "int", "required": True},
                    "password": {"type": "str", "required": True},
                    "expireDate": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/editPass",
                    "params": {"authToken": None, "tokenPass": None, "account_id": None, "password": None,
                               "expireDate": None},
                    "id": None,
                },
            },
            "account/create": {
                # Create account
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	User’s API token
                # tokenPass 	string 	yes 	API token’s pass
                # name 	        string 	yes 	Account’s name
                # categoryId 	int 	yes 	Account’s category Id
                # clientId 	    int 	yes 	Account’s client Id
                # pass 	        string 	yes 	Account’s password
                # tagsId 	    array 	no 	    Account’s tags Id
                # userGroupId 	int 	no 	    Account’s user group Id
                # parentId 	    int 	no 	    Account’s parent Id
                # login 	    string 	no 	    Account’s login
                # url 	        string 	no 	    Account’s access URL or IP
                # notes 	    string 	no 	    Account’s notes
                # private 	    int 	no 	    Set account as private. It can be either 0 or 1
                # privateGroup 	int 	no 	    Set account as private for group. It can be either 0 or 1
                # expireDate 	int 	no 	    Expire date in UNIX timestamp format
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                    "categoryId": {"type": "int", "required": True},
                    "clientId": {"type": "int", "required": True},
                    "password": {"type": "str", "required": True},
                    "tagsId": {"type": "array", "required": False},
                    "userGroupId": {"type": "int", "required": False},
                    "parentId": {"type": "int", "required": False},
                    "login": {"type": "str", "required": False},
                    "url": {"type": "str", "required": False},
                    "notes": {"type": "str", "required": False},
                    "private": {"type": "int", "required": False},
                    "privateGroup": {"type": "int", "required": False},
                    "expireDate": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/create",
                    "params": {
                        "authToken": None,
                        "tokenPass": None,
                        "name": None,
                        "categoryId": None,
                        "clientId": None,
                        "password": None,
                        "tagsId": None,
                        "userGroupId": None,
                        "parentId": None,
                        "login": None,
                        "url": None,
                        "notes": None,
                        "private": None,
                        "privateGroup": None,
                        "expireDate": None,
                    },
                    "id": None,
                },
            },
            "account/edit": {
                # Create account
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	User’s API token
                # tokenPass 	string 	yes 	API token’s pass
                # id 	        int 	yes 	Account’s Id
                # name 	        string 	no 	    Account’s name
                # categoryId 	int 	no 	    Account’s category Id
                # clientId 	    int 	no 	    Account’s client Id
                # tagsId 	    array 	no 	    Account’s tags Id
                # userGroupId 	int 	no 	    Account’s user group Id
                # parentId 	    int 	no 	    Account’s parent Id
                # login 	    string 	no 	    Account’s login
                # url 	        string 	no 	    Account’s access URL or IP
                # notes 	    string 	no 	    Account’s notes
                # private 	    int 	no 	    Set account as private. It can be either 0 or 1
                # privateGroup 	int 	no 	    Set account as private for group. It can be either 0 or 1
                # expireDate 	int 	no 	    Expire date in UNIX timestamp format
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "account_id": {"type": "int", "required": True},
                    "name": {"type": "str", "required": False},
                    "categoryId": {"type": "int", "required": False},
                    "clientId": {"type": "int", "required": False},
                    "tagsId": {"type": "array", "required": False},
                    "userGroupId": {"type": "int", "required": False},
                    "parentId": {"type": "int", "required": False},
                    "login": {"type": "str", "required": False},
                    "url": {"type": "str", "required": False},
                    "notes": {"type": "str", "required": False},
                    "private": {"type": "int", "required": False},
                    "privateGroup": {"type": "int", "required": False},
                    "expireDate": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/edit",
                    "params": {
                        "authToken": None,
                        "tokenPass": None,
                        "account_id": None,
                        "name": None,
                        "categoryId": None,
                        "clientId": None,
                        "tagsId": None,
                        "userGroupId": None,
                        "parentId": None,
                        "login": None,
                        "url": None,
                        "notes": None,
                        "private": None,
                        "privateGroup": None,
                        "expireDate": None,
                    },
                    "id": None,
                },
            },
            "account/delete": {
                # Delete an account
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	User’s API token
                # id 	        int 	yes 	Account’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "account_id": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/delete",
                    "params": {"authToken": None, "account_id": None},
                    "id": None,
                },
            },
            "category/search": {
                # Search for categories
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": False},
                    "count": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "category/search",
                    "params": {"authToken": None, "text": None, "count": None},
                    "id": None,
                },
            },
            "category/view": {
                # Get category’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": True},
                    "count": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "category/view",
                    "params": {"authToken": None, "text": None, "count": None},
                    "id": None,
                },
            },
            "category/create": {
                # Create category
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # name 	        string 	yes 	    Category’s name
                # description 	string 	no 	        Category’s description
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                    "description": {"type": "str", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "category/create",
                    "params": {"authToken": None, "name": None, "description": None},
                    "id": None,
                },
            },
            "category/edit": {
                # Edit category
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    Category’s Id
                # name 	        string 	yes 	    Category’s name
                # description 	string 	no 	        Category’s description
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "cid": {"type": "int", "required": True},
                    "name": {"type": "str", "required": True},
                    "description": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "category/edit",
                    "params": {"authToken": None, "cid": None, "name": None, "description": None},
                    "id": None,
                },
            },
            "category/delete": {
                # Delete category
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    Category’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "cid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "category/delete",
                    "params": {"authToken": None, "cid": None},
                    "cid": None,
                },
            },
            "client/search": {
                # Search for clients
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": False},
                    "count": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "client/search",
                    "params": {"authToken": None, "text": None, "count": None},
                    "id": None,
                },
            },
            "client/view": {
                # Get client’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tokenPass 	string 	yes 	    API token’s pass
                # id 	        int 	yes 	    Client’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "cid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "client/view",
                    "params": {"authToken": None, "tokenPass": None, "cid": None},
                    "id": None,
                },
            },
            "client/create": {
                # Get client’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	User’s API token
                # name 	        string 	yes 	Client’s name
                # description 	string 	no 	    Client’s description
                # Global 	    int 	no 	    Set client as Global. It can be either 0 or 1
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                    "description": {"type": "str", "required": False},
                    "Global": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "client/create",
                    "params": {"authToken": None, "name": None, "description": None, "Global": None},
                    "id": None,
                },
            },
            "client/edit": {
                # Edit client
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    Client’s Id
                # name 	        string 	yes 	    Client’s name
                # description 	string 	no 	        Client’s description
                # Global 	    int 	no 	        Set client as Global. It can be either 0 or 1
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "cid": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                    "description": {"type": "int", "required": False},
                    "Global": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "client/edit",
                    "params": {"authToken": None, "cid": None, "name": None, "description": None, "Global": None},
                    "id": None,
                },
            },
            "client/delete": {
                # Delete client
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    Client’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "cid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "client/delete",
                    "params": {"authToken": None, "cid": None},
                    "id": None,
                },
            },
            "tag/search": {
                # Search for tags
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": False},
                    "count": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "tag/search",
                    "params": {"authToken": None, "text": None, "count": None},
                    "id": None,
                },
            },
            "tag/view": {
                # Get tag’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tokenPass 	string 	yes 	    API token’s pass
                # id 	        int 	yes 	    Tag’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "tagid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "tag/view",
                    "params": {"authToken": None, "tokenPass": None, "tagid": None},
                    "id": None,
                },
            },
            "tag/create": {
                # Create tag
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # name 	        string 	yes 	    API token’s pass
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "tag/create",
                    "params": {"authToken": None, "name": None},
                    "id": None,
                },
            },
            "tag/edit": {
                # Create tag
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    Tag’s Id
                # name 	        string 	yes 	    Tag’s name
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "id": {"type": "int", "required": True},
                    "name": {"type": "str", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "tag/edit",
                    "params": {"authToken": None, "id": None, "name": None},
                    "id": None,
                },
            },
            "tag/delete": {
                # Delete tag
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    Tag’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tagid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "tag/delete",
                    "params": {"authToken": None, "tagid": None},
                    "id": None,
                },
            },
            "usergroup/search": {
                # Search for user groups
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": False},
                    "count": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "usergroup/search",
                    "params": {"authToken": None, "text": None, "count": None},
                    "id": None,
                },
            },
            "usergroup/view": {
                # Get user group’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tokenPass 	string 	yes 	    API token’s pass
                # id 	        int 	yes 	    User group’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "ugid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "usergroup/view",
                    "params": {"authToken": None, "tokenPass": None, "ugid": None},
                    "id": None,
                },
            },
            "usergroup/create": {
                # Create user group
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # name 	        string 	yes 	    User group’s name
                # description 	string 	no 	        User group’s description
                # usersId 	    array 	no 	        User group’s users Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                    "description": {"type": "str", "required": False},
                    "usersId": {"type": "array", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "usergroup/create",
                    "params": {"authToken": None, "name": None, "description": None, "usersId": None},
                    "id": None,
                },
            },
            "usergroup/edit": {
                # Edit user group
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    User group’s Id
                # name 	        string 	yes 	    User group’s name
                # description 	string 	no 	        User group’s description
                # usersId 	    array 	no 	        User group’s users Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "ugid": {"type": "int", "required": True},
                    "name": {"type": "string", "required": True},
                    "description": {"type": "string", "required": False},
                    "usersId": {"type": "array", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "usergroup/edit",
                    "params": {"authToken": None, "ugid": None, "name": None, "description": None, "usersId": None},
                    "id": None,
                },
            },
            "usergroup/delete": {
                # Delete user group
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    User group’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "ugid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "usergroup/delete",
                    "params": {"authToken": None, "ugid": None},
                    "ugid": None,
                },
            },
            "config/backup": {
                # Perform an application and database backup
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # path 	        string 	no 	        Server path to store the application and database backup
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "path": {"type": "str", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "config/backup",
                    "params": {"authToken": None, "path": None},
                    "id": None,
                },
            },
            "config/export": {
                # Export application data in XML format
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # path 	        string 	no 	        Server path to store the XML file
                # password 	    string 	no 	        Password used to encrypt the exported data
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "path": {"type": "str", "required": False},
                    "password": {"type": "str", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "config/export",
                    "params": {"authToken": None, "path": None, "password": None},
                    "id": None,
                },
            },
        }

    @property
    def api_3_1(self):
        return {
            "account/search": {
                # Search for accounts
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                # categoryId 	int 	no 	        Category’s Id for filtering
                # clientId 	    int 	no 	        Client’s Id for filtering
                # tagsId 	    array 	no 	        Tags’ Id for filtering
                # op 	        string 	no 	        Operator used for filtering. It can be either ‘or’ or ‘and’
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": False},
                    "count": {"type": "int", "required": False},
                    "categoryId": {"type": "int", "required": False},
                    "clientId": {"type": "int", "required": False},
                    "tagsId": {"type": "array", "required": False},
                    "op": {"type": "str", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/search",
                    "params": {
                        "authToken": None,
                        "text": None,
                        "count": None,
                        "categoryId": None,
                        "clientId": None,
                        "tagsid": None,
                        "op": None,
                    },
                    "id": None,
                },
            },
            "account/view": {
                # Get account’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tokenPass 	string 	yes 	    API token’s pass
                # id 	        int 	yes 	    Account’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "account_id": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/view",
                    "params": {"authToken": None, "account_id": None, "tokenPass": None},
                    "id": None,
                },
            },
            "account/viewPass": {
                # Get account’s password
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tokenPass 	string 	yes 	    API token’s pass
                # id 	        int 	yes 	    Account’s Id
                # details 	    int 	no 	        Whether to return account’s details within response account/editPass
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "account_id": {"type": "int", "required": True},
                    "details": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/viewPass",
                    "params": {"authToken": None, "account_id": None, "tokenPass": None, "details": None},
                    "id": None,
                },
            },
            "account/editPass": {
                # Edit account’s password
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	User’s API token
                # tokenPass 	string 	yes 	API token’s pass
                # id 	int 	yes 	Account’s Id
                # pass 	string 	yes 	Account’s password
                # expireDate 	int 	no 	Expire date in UNIX timestamp format
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "account_id": {"type": "int", "required": True},
                    "password": {"type": "str", "required": True},
                    "expireDate": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/editPass",
                    "params": {"authToken": None,
                               "tokenPass": None,
                               "account_id": None,
                               "password": None,
                               "expireDate": None
                               },
                    "id": None,
                },
            },
            "account/create": {
                # Create account
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	User’s API token
                # tokenPass 	string 	yes 	API token’s pass
                # name 	        string 	yes 	Account’s name
                # categoryId 	int 	yes 	Account’s category Id
                # clientId 	    int 	yes 	Account’s client Id
                # pass 	        string 	yes 	Account’s password
                # tagsId 	    array 	no 	    Account’s tags Id
                # userGroupId 	int 	no 	    Account’s user group Id
                # parentId 	    int 	no 	    Account’s parent Id
                # login 	    string 	no 	    Account’s login
                # url 	        string 	no 	    Account’s access URL or IP
                # notes 	    string 	no 	    Account’s notes
                # private 	    int 	no 	    Set account as private. It can be either 0 or 1
                # privateGroup 	int 	no 	    Set account as private for group. It can be either 0 or 1
                # expireDate 	int 	no 	    Expire date in UNIX timestamp format
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                    "categoryId": {"type": "int", "required": True},
                    "clientId": {"type": "int", "required": True},
                    "password": {"type": "str", "required": True},
                    "tagsId": {"type": "array", "required": False},
                    "userGroupId": {"type": "int", "required": False},
                    "parentId": {"type": "int", "required": False},
                    "login": {"type": "str", "required": False},
                    "url": {"type": "str", "required": False},
                    "notes": {"type": "str", "required": False},
                    "private": {"type": "int", "required": False},
                    "privateGroup": {"type": "int", "required": False},
                    "expireDate": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/create",
                    "params": {
                        "authToken": None,
                        "tokenPass": None,
                        "name": None,
                        "categoryId": None,
                        "clientId": None,
                        "password": None,
                        "tagsId": None,
                        "userGroupId": None,
                        "parentId": None,
                        "login": None,
                        "url": None,
                        "notes": None,
                        "private": None,
                        "privateGroup": None,
                        "expireDate": None,
                    },
                    "id": None,
                },
            },
            "account/edit": {
                # Create account
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	User’s API token
                # tokenPass 	string 	yes 	API token’s pass
                # id 	        int 	yes 	Account’s Id
                # name 	        string 	no 	    Account’s name
                # categoryId 	int 	no 	    Account’s category Id
                # clientId 	    int 	no 	    Account’s client Id
                # tagsId 	    array 	no 	    Account’s tags Id
                # userGroupId 	int 	no 	    Account’s user group Id
                # parentId 	    int 	no 	    Account’s parent Id
                # login 	    string 	no 	    Account’s login
                # url 	        string 	no 	    Account’s access URL or IP
                # notes 	    string 	no 	    Account’s notes
                # private 	    int 	no 	    Set account as private. It can be either 0 or 1
                # privateGroup 	int 	no 	    Set account as private for group. It can be either 0 or 1
                # expireDate 	int 	no 	    Expire date in UNIX timestamp format
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "account_id": {"type": "int", "required": True},
                    "name": {"type": "str", "required": False},
                    "categoryId": {"type": "int", "required": False},
                    "clientId": {"type": "int", "required": False},
                    "tagsId": {"type": "array", "required": False},
                    "userGroupId": {"type": "int", "required": False},
                    "parentId": {"type": "int", "required": False},
                    "login": {"type": "str", "required": False},
                    "url": {"type": "str", "required": False},
                    "notes": {"type": "str", "required": False},
                    "private": {"type": "int", "required": False},
                    "privateGroup": {"type": "int", "required": False},
                    "expireDate": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/edit",
                    "params": {
                        "authToken": None,
                        "tokenPass": None,
                        "account_id": None,
                        "name": None,
                        "categoryId": None,
                        "clientId": None,
                        "tagsId": None,
                        "userGroupId": None,
                        "parentId": None,
                        "login": None,
                        "url": None,
                        "notes": None,
                        "private": None,
                        "privateGroup": None,
                        "expireDate": None,
                    },
                    "id": None,
                },
            },
            "account/delete": {
                # Delete an account
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	User’s API token
                # id 	        int 	yes 	Account’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "account_id": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "account/delete",
                    "params": {"authToken": None, "account_id": None},
                    "id": None,
                },
            },
            "category/search": {
                # Search for categories
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": False},
                    "count": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "category/search",
                    "params": {"authToken": None, "text": None, "count": None},
                    "id": None,
                },
            },
            "category/view": {
                # Get category’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": True},
                    "count": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "category/view",
                    "params": {"authToken": None, "text": None, "count": None},
                    "id": None,
                },
            },
            "category/create": {
                # Create category
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # name 	        string 	yes 	    Category’s name
                # description 	string 	no 	        Category’s description
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                    "description": {"type": "str", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "category/create",
                    "params": {"authToken": None, "name": None, "description": None},
                    "id": None,
                },
            },
            "category/edit": {
                # Edit category
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    Category’s Id
                # name 	        string 	yes 	    Category’s name
                # description 	string 	no 	        Category’s description
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "cid": {"type": "int", "required": True},
                    "name": {"type": "str", "required": True},
                    "description": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "category/edit",
                    "params": {"authToken": None, "cid": None, "name": None, "description": None},
                    "id": None,
                },
            },
            "category/delete": {
                # Delete category
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    Category’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "cid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "category/delete",
                    "params": {"authToken": None, "id": None},
                    "cid": None,
                },
            },
            "client/search": {
                # Search for clients
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": False},
                    "count": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "client/search",
                    "params": {"authToken": None, "text": None, "count": None},
                    "id": None,
                },
            },
            "client/view": {
                # Get client’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tokenPass 	string 	yes 	    API token’s pass
                # id 	        int 	yes 	    Client’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "cid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "client/view",
                    "params": {"authToken": None, "tokenPass": None, "cid": None},
                    "id": None,
                },
            },
            "client/create": {
                # Get client’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	User’s API token
                # name 	        string 	yes 	Client’s name
                # description 	string 	no 	    Client’s description
                # Global 	    int 	no 	    Set client as Global. It can be either 0 or 1
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                    "description": {"type": "str", "required": False},
                    "Global": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "client/create",
                    "params": {"authToken": None, "name": None, "description": None, "Global": None},
                    "id": None,
                },
            },
            "client/edit": {
                # Edit client
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    Client’s Id
                # name 	        string 	yes 	    Client’s name
                # description 	string 	no 	        Client’s description
                # Global 	    int 	no 	        Set client as Global. It can be either 0 or 1
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "cid": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                    "description": {"type": "int", "required": False},
                    "Global": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "client/edit",
                    "params": {"authToken": None, "cid": None, "name": None, "description": None, "Global": None},
                    "id": None,
                },
            },
            "client/delete": {
                # Delete client
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # cid 	        int 	yes 	    Client’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "cid": {"type": "int", "required": True}
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "client/delete",
                    "params": {"authToken": None, "cid": None},
                    "id": None,
                },
            },
            "tag/search": {
                # Search for tags
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": False},
                    "count": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "tag/search",
                    "params": {"authToken": None, "text": None, "count": None},
                    "id": None,
                },
            },
            "tag/view": {
                # Get tag’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tokenPass 	string 	yes 	    API token’s pass
                # tagid 	    int 	yes 	    Tag’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "tagid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "tag/view",
                    "params": {"authToken": None, "tokenPass": None, "tagid": None},
                    "id": None,
                },
            },
            "tag/create": {
                # Create tag
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # name 	        string 	yes 	    API token’s pass
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "tag/create",
                    "params": {"authToken": None, "name": None},
                    "id": None,
                },
            },
            "tag/edit": {
                # Create tag
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tagid 	    int 	yes 	    Tag’s Id
                # name 	        string 	yes 	    Tag’s name
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tagid": {"type": "int", "required": True},
                    "name": {"type": "str", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "tag/edit",
                    "params": {"authToken": None, "id": None, "name": None},
                    "id": None,
                },
            },
            "tag/delete": {
                # Delete tag
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tagid 	    int 	yes 	    Tag’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tagid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "tag/delete",
                    "params": {"authToken": None, "tagid": None},
                    "id": None,
                },
            },
            "userGroup/search": {
                # Search for user groups
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # text 	        string 	no 	        Text to search for
                # count 	    int 	no 	        Number of results to display
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "text": {"type": "str", "required": False},
                    "count": {"type": "int", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "userGroup/search",
                    "params": {"authToken": None, "text": None, "count": None},
                    "id": None,
                },
            },
            "userGroup/view": {
                # Get user group’s details
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # tokenPass 	string 	yes 	    API token’s pass
                # id 	        int 	yes 	    User group’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "tokenPass": {"type": "str", "required": True},
                    "ugid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "usergroup/view",
                    "params": {"authToken": None, "tokenPass": None, "ugid": None},
                    "id": None,
                },
            },
            "userGroup/create": {
                # Create user group
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # name 	        string 	yes 	    User group’s name
                # description 	string 	no 	        User group’s description
                # usersId 	    array 	no 	        User group’s users Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "name": {"type": "str", "required": True},
                    "description": {"type": "str", "required": False},
                    "usersId": {"type": "array", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "usergroup/create",
                    "params": {"authToken": None, "name": None, "description": None, "usersId": None},
                    "id": None,
                },
            },
            "userGroup/edit": {
                # Edit user group
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    User group’s Id
                # name 	        string 	yes 	    User group’s name
                # description 	string 	no 	        User group’s description
                # usersId 	    array 	no 	        User group’s users Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "ugid": {"type": "int", "required": True},
                    "name": {"type": "string", "required": True},
                    "description": {"type": "string", "required": False},
                    "usersId": {"type": "array", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "usergroup/edit",
                    "params": {"authToken": None, "ugid": None, "name": None, "description": None, "usersId": None},
                    "id": None,
                },
            },
            "userGroup/delete": {
                # Delete user group
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # id 	        int 	yes 	    User group’s Id
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "ugid": {"type": "int", "required": True},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "usergroup/delete",
                    "params": {"authToken": None, "ugid": None},
                    "ugid": None,
                },
            },
            "config/backup": {
                # Perform an application and database backup
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # path 	        string 	no 	        Server path to store the application and database backup
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "path": {"type": "str", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "config/backup",
                    "params": {"authToken": None, "path": None},
                    "id": None,
                },
            },
            "config/export": {
                # Export application data in XML format
                # Parameter 	Type 	Required 	Description
                # authToken 	string 	yes 	    User’s API token
                # path 	        string 	no 	        Server path to store the XML file
                # password 	    string 	no 	        Password used to encrypt the exported data
                "params_details": {
                    "authToken": {"type": "str", "required": True},
                    "path": {"type": "str", "required": False},
                    "password": {"type": "str", "required": False},
                },
                "json_body": {
                    "jsonrpc": "2.0",
                    "method": "config/export",
                    "params": {"authToken": None, "path": None, "password": None},
                    "id": None,
                },
            },
        }

    @property
    def api_version(self):
        if 'DD_SYSPASS_CLIENT_API_VERSION' in os.environ:
            print(
                Fore.WHITE + Style.BRIGHT + "DD_SYSPASS_CLIENT_API_VERSION: {0}".format(
                    os.environ['DD_SYSPASS_CLIENT_API_VERSION'])
            )
            return os.environ['DD_SYSPASS_CLIENT_API_VERSION']
        if self.__api_version is None:
            return syspassclient.dd.syspass["api"]["version"]
        return self.__api_version

    @api_version.setter
    def api_version(self, version=None):
        if version is None:
            if self.__api_version is not None:
                self.__api_version = None
            return

        if type(version) != str:
            raise TypeError('"version" must be a str type or None')

        if self.__api_version != version:
            self.__api_version = version

    @property
    def api_filename_ext(self):
        """
        Return the api_filename_extension property

        :return: the filename extension like '.yaml'
        :rtype: str
        """
        return self.__api_filename_ext

    @api_filename_ext.setter
    def api_filename_ext(self, extension=None):
        """
        Set the api_filename_ext property

        :param extension: a extension like '.yaml' or None for restore default one ('.yaml')
        :type extension: str or None
        :raise TypeError: When 'extension' is not a str type
        """
        if extension is None:
            extension = ".yaml"

        if not isinstance(extension, str):
            raise TypeError("'extension' must be a str type")

        if self.__api_filename_ext != extension:
            self.__api_filename_ext = extension

    @property
    def api_directory(self):
        return self.__api_directory

    @api_directory.setter
    def api_directory(self, directory=None):
        """
        Return the directory path where is store API yaml file(s)

        :param directory: in case you want force a special directory
        :type directory: str
        :return: the absolute path of the api_directory
        :rtype: str
        """
        if directory is None:
            if self.__api_directory != os.path.join(os.path.dirname(os.path.abspath(__file__)), "api"):
                self.__api_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api")

        else:
            if type(directory) != str:
                raise TypeError('"directory" must be a str type or None')
            if self.__api_directory != directory:
                self.__api_directory = directory

    @property
    def api_filename(self):
        """
        Return the api_filename)

        :return: the filename to load
        :rtype: str
        """
        return self.api_version + self.api_filename_ext

    @property
    def api_file(self):
        """
        Return the absolute path of the API yaml file to load

        :return: path of the API yaml file to load
        :rtype: str
        """
        return os.path.join(self.api_directory, self.api_filename)

    def read_api(self):
        """
        Read the API file
        """

        # if api_file is None:
        #     api_file = self.api_file

        with open(self.api_file) as f:
            self.api_data = load(f, Loader=Loader)
            f.close()
            if self.debug and self.debug_level > 1:
                print(Fore.YELLOW + Style.BRIGHT + "{0}: ".format(self.__class__.__name__.upper()), end='')
                print(Fore.WHITE + Style.BRIGHT + "{0} ".format("Load API File"))

                print(Fore.WHITE + Style.BRIGHT + "File: ", end='')
                print(self.api_file)

                if self.debug and self.debug_level > 2:
                    for line in dump(self.api_data).split("\n"):
                        if self.verbose:
                            print(Fore.CYAN + Style.BRIGHT + "< " + Fore.RESET + Style.RESET_ALL + str(line))
