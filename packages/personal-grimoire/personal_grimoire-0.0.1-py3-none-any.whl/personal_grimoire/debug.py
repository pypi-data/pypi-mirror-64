
def save_to_file(msg):
    with open("jean.txt", "a") as f:
        final = str(datetime.now()) + f" {os.getenv('USER')} " + msg + " \n"
        print(final)
        print(final, file=sys.stdout)
        f.write(final)

