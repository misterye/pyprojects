from app import app

if __name__ == "__main__":
    #app.run('0.0.0.0', 443, ssl_context=('fullchain1.pem', 'privkey1.pem'))
    app.run('0.0.0.0', 80)
