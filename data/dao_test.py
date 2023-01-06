import dao

def main():
    saves = dao.get_saves(4)
    for save in saves:
        print(save['id_ep'])

if __name__ == '__main__':
    main()