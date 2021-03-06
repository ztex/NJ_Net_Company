#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pathlib

from github import Github
from github.Repository import Repository
import json
import pandas as pd
import telegram

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


def to_tg():
    bot = telegram.Bot("5284719273:AAF9DFMuDQhr1h0lp6Yj4Smj3u_eXtYrtNE")
    bot.send_message(chat_id='-789012721',
                     text="南京互联网公司最新消息:" + "https://raw.githubusercontent.com/ztex/NJ_Net_Company/main/%E5%8D%97%E4%BA%AC%E4%BA%92%E8%81%94%E7%BD%91%E5%85%AC%E5%8F%B8%E7%BB%9F%E8%AE%A1%E6%B1%87%E6%80%BB.xlsx")


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
    company_obj.to_markdown("南京互联网公司统计汇总.md")
    to_tg()


if __name__ == '__main__':
    login()
    execute()
