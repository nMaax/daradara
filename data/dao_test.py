import dao

def main():
    comments = dao.get_comments(id_user=1)
    for comment in comments:
        print(comment['text'])

if __name__ == '__main__':
    main()