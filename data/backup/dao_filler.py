import sys
sys.path.append('../')

import data.dao as dao
from datetime import datetime
from werkzeug.security import generate_password_hash

def main():

    #now = datetime.now()
    #now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    now_str = '2023-01-10 10:30:50'

    # GENERATED BY CHAT GPT https://chat.openai.com/chat/

    dao.new_user('john.doe@email.com', generate_password_hash('john', method='sha256'), 'John', 'Doe', '.jpg')
    dao.new_user('jane.smith@email.com', generate_password_hash('jane', method='sha256'), 'Jane', 'Smith', '.jpg')
    dao.new_user('robert.johnson@email.com', generate_password_hash('robert', method='sha256'), 'Robert', 'Johnson', '.jpg')
    dao.new_user('emily.williams@email.com', generate_password_hash('emily', method='sha256'), 'Emily', 'Williams', '.jpg')
    dao.new_user('michael.brown@email.com', generate_password_hash('michael', method='sha256'), 'Michael', 'Brown', '.jpg')
    dao.new_user('admin@daradara.it', generate_password_hash('admin', method='sha256'), 'Massimiliano', 'Carli', '.jpg')

    dao.new_podcast('Soccer', 'For those who love soccer!', '.jpg', 1, 'sport')
    dao.new_podcast('Basketball', 'For those who love basketball!', '.jpg', 2, 'sport')
    dao.new_podcast('Baseball', 'For those who love baseball!', '.jpg', 1, 'sport')
    dao.new_podcast('Football', 'For those who love football!', '.jpg', 3, 'sport')
    dao.new_podcast('Tennis', 'For those who love tennis!', '.jpg', 5, 'sport')
    dao.new_podcast('Golf', 'For those who love golf!', '.jpg', 1, 'sport')

    dao.new_episode('In a few words: soccer', 'Today we are going to dive into soccer and how it\'s played!', '.mp3', now_str, 1)
    dao.new_episode('Soccer 101: The basics', 'In this episode, we will cover the basic rules and terminology of soccer.', '.mp3', now_str, 1)
    dao.new_episode('Soccer legends: Pelé', 'In this episode, we will discuss the career and achievements of soccer legend Pelé.', '.mp3', now_str, 1)
    dao.new_episode('Soccer tactics: Formations and strategies', 'In this episode, we will explore different formations and strategies used in soccer.', '.mp3', now_str, 1)
    dao.new_episode('Soccer rivalries: El Clásico', 'In this episode, we will delve into the historic rivalry between Barcelona and Real Madrid.', '.mp3', now_str, 1)
    dao.new_episode('Soccer around the world: Regional differences', 'In this episode, we will compare and contrast the styles of soccer played in different regions of the world.', '.mp3', now_str, 1)

    dao.new_episode('Basketball fundamentals: Dribbling, passing, and shooting', 'In this episode, we will focus on the fundamental skills of dribbling, passing, and shooting in basketball.', '.mp3', now_str, 2)
    dao.new_episode('Basketball 101: The basics', 'In this episode, we will cover the basic rules and terminology of basketball.', '.mp3', now_str, 2)
    dao.new_episode('Basketball legends: Michael Jordan', 'In this episode, we will discuss the career and achievements of basketball legend Michael Jordan.', '.mp3', now_str, 2)
    dao.new_episode('Basketball tactics: Offense and defense', 'In this episode, we will explore different offensive and defensive strategies used in basketball.', '.mp3', now_str, 2)
    dao.new_episode('Basketball rivalries: Lakers vs. Celtics', 'In this episode, we will delve into the historic rivalry between the Los Angeles Lakers and the Boston Celtics.', '.mp3', now_str, 2)
    dao.new_episode('Basketball around the world: International play', 'In this episode, we will compare and contrast the styles of basketball played in different countries around the world.', '.mp3', now_str, 2)

    dao.new_follow(1, 1, now_str)
    dao.new_follow(2, 1, now_str)
    dao.new_follow(3, 1, now_str)
    dao.new_follow(1, 5, now_str)
    dao.new_follow(2, 3, now_str)

    dao.new_save(1, 1, now_str)
    dao.new_save(1, 8, now_str)
    dao.new_save(2, 2, now_str)
    dao.new_save(3, 6, now_str)

    dao.new_comment(4, 1, 'I realy like the final part!', now_str)
    dao.new_comment(1, 10, 'I really enjoyed the discussion on basketball tactics!', now_str)
    dao.new_comment(2, 9, 'The analysis of Michael Jordan\'s career was really insightful.', now_str)
    dao.new_comment(3, 12, 'I loved hearing about the international styles of basketball play.', now_str)
    dao.new_comment(4, 11, 'The episode on the Lakers vs. Celtics rivalry was really entertaining.', now_str)
    dao.new_comment(5, 1, 'I appreciated the focus on the fundamental skills of dribbling, passing, and shooting.', now_str)
    dao.new_comment(2, 10, 'The discussion on offensive and defensive strategies was very useful.', now_str)
    dao.new_comment(2, 7, 'I enjoyed learning about the basic rules and terminology of basketball.', now_str)
    dao.new_comment(3, 11, 'The episode on the rivalry between the Lakers and Celtics was very informative.', now_str)
    dao.new_comment(4, 12, 'The discussion on the different styles of basketball played around the world was very interesting.', now_str)
    dao.new_comment(5, 9, 'The analysis of Michael Jordan\'s career was really well done.', now_str)

if __name__ == '__main__':
    main()