#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from github import Github
from github.Repository import Repository
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from gspread import SpreadsheetNotFound, WorksheetNotFound

user: Github
username: str
repo: Repository


def login():
    global user, username, repo
    github_repo_env = os.environ.get('GITHUB_REPOSITORY')
    username = github_repo_env[0:github_repo_env.index('/')]
    password = os.environ.get('GITHUB_TOKEN')
    user = Github(username, password)
    repo = user.get_repo("ztex/NJ_Net_Company")


def to_google_doc(company_obj):
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(
        'premium-odyssey-281313-d3ff47a72c46.json',
        scopes=scopes
    )

    gc = gspread.authorize(credentials)
    try:
        sh = gc.open('互联网公司统计')
    except SpreadsheetNotFound:
        sh = gc.create("互联网公司统计")
    try:
        worksheet = sh.get_worksheet(0)
    except WorksheetNotFound:
        worksheet = sh.add_worksheet(title="南京互联网", rows="100000", cols="30")
    worksheet.update([company_obj.columns.values.tolist()] + company_obj.values.tolist())


def execute():
    issues = repo.get_issues()
    company_list = []
    for issue in issues:
        issue_json = json.loads(issue.body)
        comments = '/'.join(map(lambda x: x.body, issue.get_comments()))
        issue_json['评论'] = comments
        issue_json['更新时间'] = issue.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        company_list.append(issue_json)
    company_obj = pd.DataFrame(company_list)
    company_obj.sort_values(by="公司名称", ascending=True)
    company_obj.to_excel('南京互联网公司统计汇总.xlsx')
    company_obj.to_markdown("Readme.md")
    to_google_doc(company_obj)


if __name__ == '__main__':
    login()
    execute()
