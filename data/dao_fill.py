import dao

def main():

    # GENERATE BY CHAT GPT https://chat.openai.com/chat/

    dao.new_user('JohnDoe', 'john.doe@email.com', 'john', 'John', 'Doe', 'I am John Doe', 'johnDoe.jpeg')
    dao.new_user('JaneSmith', 'jane.smith@email.com', 'jane', 'Jane', 'Smith', 'I am Jane Smith', 'janeSmith.jpeg')
    dao.new_user('RobertJohnson', 'robert.johnson@email.com', 'robert', 'Robert', 'Johnson', 'I am Robert Johnson', 'robertJohnson.jpeg')
    dao.new_user('EmilyWilliams', 'emily.williams@email.com', 'emily', 'Emily', 'Williams', 'I am Emily Williams', 'emilyWilliams.jpeg')
    dao.new_user('MichaelBrown', 'michael.brown@email.com', 'michael', 'Michael', 'Brown', 'I am Michael Brown', 'michaelBrown.jpeg')

    dao.new_podcast('Soccer', 'For those who love soccer!', 'soccer.jpeg', 1, ('sport', 'soccer', 'CL'))
    dao.new_podcast('Basketball', 'For those who love basketball!', 'basketball.jpeg', 2, ('sport', 'basketball', 'hoop'))
    dao.new_podcast('Baseball', 'For those who love baseball!', 'baseball.jpeg', 1, ('sport', 'baseball', 'MLB'))
    dao.new_podcast('Football', 'For those who love football!', 'football.jpeg', 3, ('sport', 'football', 'NFL'))
    dao.new_podcast('Tennis', 'For those who love tennis!', 'tennis.jpeg', 5, ('sport', 'tennis', 'ATP'))
    dao.new_podcast('Golf', 'For those who love golf!', 'golf.jpeg', 1, ('sport', 'golf', 'PGA'))

    dao.new_episode('In a few words: soccer', 'Today we are going to dive into soccer and how it\'s played!', 'ep1_soccer.mp4', '2023-06-01-21:49:00', 1)
    dao.new_episode('Soccer 101: The basics', 'In this episode, we will cover the basic rules and terminology of soccer.', 'ep2_soccer.mp4', '2023-06-01-22:00:00', 1)
    dao.new_episode('Soccer legends: Pelé', 'In this episode, we will discuss the career and achievements of soccer legend Pelé.', 'ep3_soccer.mp4', '2023-06-01-23:00:00', 1)
    dao.new_episode('Soccer tactics: Formations and strategies', 'In this episode, we will explore different formations and strategies used in soccer.', 'ep4_soccer.mp4', '2023-06-02-00:00:00', 1)
    dao.new_episode('Soccer rivalries: El Clásico', 'In this episode, we will delve into the historic rivalry between Barcelona and Real Madrid.', 'ep5_soccer.mp4', '2023-06-02-01:00:00', 1)
    dao.new_episode('Soccer around the world: Regional differences', 'In this episode, we will compare and contrast the styles of soccer played in different regions of the world.', 'ep6_soccer.mp4', '2023-06-02-02:00:00', 1)

    dao.new_episode('Basketball fundamentals: Dribbling, passing, and shooting', 'In this episode, we will focus on the fundamental skills of dribbling, passing, and shooting in basketball.', 'ep1_basketball.mp4', '2023-06-01-21:00:00', 1)
    dao.new_episode('Basketball 101: The basics', 'In this episode, we will cover the basic rules and terminology of basketball.', 'ep2_basketball.mp4', '2023-06-01-22:00:00', 1)
    dao.new_episode('Basketball legends: Michael Jordan', 'In this episode, we will discuss the career and achievements of basketball legend Michael Jordan.', 'ep3_basketball.mp4', '2023-06-01-23:00:00', 1)
    dao.new_episode('Basketball tactics: Offense and defense', 'In this episode, we will explore different offensive and defensive strategies used in basketball.', 'ep4_basketball.mp4', '2023-06-02-00:00:00', 1)
    dao.new_episode('Basketball rivalries: Lakers vs. Celtics', 'In this episode, we will delve into the historic rivalry between the Los Angeles Lakers and the Boston Celtics.', 'ep5_basketball.mp4', '2023-06-02-01:00:00', 1)
    dao.new_episode('Basketball around the world: International play', 'In this episode, we will compare and contrast the styles of basketball played in different countries around the world.', 'ep6_basketball.mp4', '2023-06-02-02:00:00', 1)

    dao.new_follow(1, 1)
    dao.new_follow(2, 1)
    dao.new_follow(3, 1)
    dao.new_follow(1, 5)
    dao.new_follow(2, 3)

    dao.new_save(1, 1)
    dao.new_save(1, 8)
    dao.new_save(2, 2)
    dao.new_save(3, 6)

    dao.new_comment(4, 1, 'I realy like the final part!', '2023-01-06-22:00:00')
    dao.new_comment(1, 2, 'I really enjoyed the discussion on basketball tactics!', '2023-01-06-22:10:00')
    dao.new_comment(2, 3, 'The analysis of Michael Jordan\'s career was really insightful.', '2023-01-06-22:20:00')
    dao.new_comment(3, 4, 'I loved hearing about the international styles of basketball play.', '2023-01-06-22:30:00')
    dao.new_comment(4, 5, 'The episode on the Lakers vs. Celtics rivalry was really entertaining.', '2023-01-06-22:40:00')
    dao.new_comment(5, 1, 'I appreciated the focus on the fundamental skills of dribbling, passing, and shooting.', '2023-01-06-22:50:00')
    dao.new_comment(1, 3, 'The discussion on offensive and defensive strategies was very useful.', '2023-01-06-23:00:00')
    dao.new_comment(2, 4, 'I enjoyed learning about the basic rules and terminology of basketball.', '2023-01-06-23:10:00')
    dao.new_comment(3, 5, 'The episode on the rivalry between the Lakers and Celtics was very informative.', '2023-01-06-23:20:00')
    dao.new_comment(4, 1, 'The discussion on the different styles of basketball played around the world was very interesting.', '2023-01-06-23:30:00')
    dao.new_comment(5, 2, 'The analysis of Michael Jordan\'s career was really well done.', '2023-01-06-23:40:00')

if __name__ == '__main__':
    main()