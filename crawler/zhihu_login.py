# coding=utf-8

from __future__ import unicode_literals, print_function

import os

from zhihu_oauth import ZhihuClient

TOKEN_FILE = 'token.pkl'


client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)

me = client.me()


print('name', me.name)
print('headline', me.headline)
print('description', me.description)

print('following topic count', me.following_topic_count)
print('following people count', me.following_topic_count)
print('followers count', me.follower_count)

print('voteup count', me.voteup_count)
print('get thanks count', me.thanked_count)

print('answered question', me.answer_count)
print('question asked', me.question_count)
print('collection count', me.collection_count)
print('article count', me.articles_count)
print('following column count', me.following_column_count)



answer = client.answer(94150403)

print(answer.question.title)
print(answer.author.name)
print(answer.voteup_count)
print(answer.thanks_count)
print(answer.created_time)
print(answer.updated_time)

for voter in answer.voters:
    print(voter.name, voter.headline)